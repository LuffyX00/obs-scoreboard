import asyncio
import json
from contextlib import asynccontextmanager
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from teams import get_team, list_teams, team_to_state

DEFAULT_STATE: dict[str, Any] = {
    "match_type": "international",
    "tournament": "FIFA WORLD CUP 2026",
    "home_team": team_to_state(get_team("arg") or {}),
    "away_team": team_to_state(get_team("esp") or {}),
    "minutes": 0,
    "seconds": 0,
    "period": "1ST HALF",
    "added_time": 0,
    "is_live": True,
    "timer_running": False,
}

MATCH_TYPE_TITLES = {
    "international": "FIFA WORLD CUP 2028",
    "club": "UEFA CHAMPIONS LEAGUE",
}


class TeamUpdate(BaseModel):
    id: str | None = None
    type: Literal["country", "club"] | None = None
    code: str | None = None
    name: str | None = None
    score: int | None = Field(default=None, ge=0)
    flag_url: str | None = None
    primary_color: str | None = None
    secondary_color: str | None = None


class ScoreboardUpdate(BaseModel):
    match_type: Literal["international", "club"] | None = None
    tournament: str | None = None
    home_team: TeamUpdate | None = None
    away_team: TeamUpdate | None = None
    minutes: int | None = Field(default=None, ge=0, le=120)
    seconds: int | None = Field(default=None, ge=0, le=59)
    period: str | None = None
    added_time: int | None = Field(default=None, ge=0, le=20)
    is_live: bool | None = None
    timer_running: bool | None = None


class CustomTeamRequest(BaseModel):
    side: Literal["home", "away"]
    type: Literal["country", "club"]
    name: str = Field(min_length=1, max_length=40)
    code: str = Field(min_length=2, max_length=4)
    flag_url: str | None = None
    primary_color: str | None = "#1a1a2e"
    secondary_color: str | None = "#c9a227"


class TeamSelectRequest(BaseModel):
    side: Literal["home", "away"]
    team_id: str


class MatchTypeRequest(BaseModel):
    match_type: Literal["international", "club"]


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict[str, Any]) -> None:
        payload = json.dumps(message)
        stale: list[WebSocket] = []
        for connection in self.active_connections:
            try:
                await connection.send_text(payload)
            except Exception:
                stale.append(connection)
        for connection in stale:
            self.disconnect(connection)


manager = ConnectionManager()
state = {
    **DEFAULT_STATE,
    "home_team": DEFAULT_STATE["home_team"].copy(),
    "away_team": DEFAULT_STATE["away_team"].copy(),
}
timer_task: asyncio.Task | None = None


def get_state() -> dict[str, Any]:
    return {
        **state,
        "home_team": state["home_team"].copy(),
        "away_team": state["away_team"].copy(),
    }


async def broadcast_state() -> None:
    await manager.broadcast({"type": "state", "data": get_state()})


async def timer_loop() -> None:
    while True:
        await asyncio.sleep(1)
        if state["timer_running"]:
            state["seconds"] += 1
            if state["seconds"] >= 60:
                state["seconds"] = 0
                state["minutes"] += 1
            await broadcast_state()


@asynccontextmanager
async def lifespan(_: FastAPI):
    global timer_task
    timer_task = asyncio.create_task(timer_loop())
    yield
    if timer_task:
        timer_task.cancel()
        try:
            await timer_task
        except asyncio.CancelledError:
            pass


app = FastAPI(title="OBS Scoreboard API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/teams")
async def read_teams(
    type: Literal["country", "club"] | None = Query(default=None, alias="type"),
) -> list[dict[str, Any]]:
    return list_teams(type)


@app.get("/api/teams/{team_id}")
async def read_team(team_id: str) -> dict[str, Any]:
    team = get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team_to_state(team)


@app.get("/api/state")
async def read_state() -> dict[str, Any]:
    return get_state()


@app.post("/api/state")
async def update_state(update: ScoreboardUpdate) -> dict[str, Any]:
    payload = update.model_dump(exclude_none=True)

    for key, value in payload.items():
        if key in {"home_team", "away_team"}:
            state[key].update(value)
        else:
            state[key] = value

    await broadcast_state()
    return get_state()


@app.post("/api/teams/custom")
async def set_custom_team(request: CustomTeamRequest) -> dict[str, Any]:
    side_key = "home_team" if request.side == "home" else "away_team"
    current_score = state[side_key]["score"]

    team: dict[str, Any] = {
        "id": "custom",
        "type": request.type,
        "name": request.name.strip(),
        "code": request.code.strip().upper(),
        "score": current_score,
    }

    if request.type == "country":
        team["flag_url"] = request.flag_url.strip() if request.flag_url else None
    else:
        team["primary_color"] = request.primary_color or "#1a1a2e"
        team["secondary_color"] = request.secondary_color or "#c9a227"

    state[side_key] = team
    await broadcast_state()
    return get_state()


@app.post("/api/teams/select")
async def select_team(request: TeamSelectRequest) -> dict[str, Any]:
    team = get_team(request.team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    side_key = "home_team" if request.side == "home" else "away_team"
    current_score = state[side_key]["score"]
    state[side_key] = team_to_state(team, score=current_score)
    await broadcast_state()
    return get_state()


@app.post("/api/match-type")
async def set_match_type(request: MatchTypeRequest) -> dict[str, Any]:
    match_type = request.match_type
    state["match_type"] = match_type
    state["tournament"] = MATCH_TYPE_TITLES[match_type]

    default_home = "arg" if match_type == "international" else "bar"
    default_away = "esp" if match_type == "international" else "rma"

    state["home_team"] = team_to_state(get_team(default_home) or {}, score=0)
    state["away_team"] = team_to_state(get_team(default_away) or {}, score=0)
    state["minutes"] = 0
    state["seconds"] = 0
    state["period"] = "1ST HALF"
    state["timer_running"] = False

    await broadcast_state()
    return get_state()


@app.post("/api/reset")
async def reset_state() -> dict[str, Any]:
    global state
    state = {
        **DEFAULT_STATE,
        "home_team": DEFAULT_STATE["home_team"].copy(),
        "away_team": DEFAULT_STATE["away_team"].copy(),
    }
    await broadcast_state()
    return get_state()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    await websocket.send_text(json.dumps({"type": "state", "data": get_state()}))
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
