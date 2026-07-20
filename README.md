# OBS Scoreboard

Real-time FIFA-style scoreboard for OBS, built with **React**, **FastAPI**, and **WebSockets**.

Argentina vs Spain · FIFA World Cup 2026 layout · Live score & timer updates.

## Quick Start

```bash
cd obs-scoreboard
chmod +x start.sh
./start.sh
```

Then open:

| Page | URL | Purpose |
|------|-----|---------|
| **Scoreboard overlay** | http://localhost:5173/ | Add this URL in OBS Browser Source |
| **Control panel** | http://localhost:5173/control | Update scores, timer, period |

## OBS Setup

1. In OBS, click **+** under Sources → **Browser**.
2. Set **URL** to `http://localhost:5173/`
3. Set **Width** `1920` and **Height** `1080`
4. Check **Refresh browser when scene becomes active** (optional)
5. The black background works well as a chroma key if needed

Use the control panel in a regular browser tab to update the overlay in real time.

## Project Structure

```
obs-scoreboard/
├── backend/          # FastAPI + WebSocket server
│   ├── main.py
│   └── requirements.txt
├── frontend/         # React (Vite) scoreboard UI
│   └── src/
├── start.sh          # One-command launcher
└── README.md
```

## Manual Run (optional)

**Backend:**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Features

- Live WebSocket sync between control panel and OBS overlay
- **International mode** — pick from 18 countries with real flag images
- **Club mode** — pick from 16 clubs with color-coded badges
- Searchable team picker for home & away sides
- Score +/- buttons, timer start/pause/reset
- Period presets (1st half, 2nd half, full time)
- LIVE badge toggle
- Tournament title editing

## API

- `GET /api/state` — current scoreboard state
- `POST /api/state` — update any field
- `POST /api/reset` — reset to defaults
- `WS /ws` — real-time state broadcast

Example update:
```bash
curl -X POST http://localhost:8000/api/state \
  -H "Content-Type: application/json" \
  -d '{"home_team":{"score":1},"timer_running":true}'
```
