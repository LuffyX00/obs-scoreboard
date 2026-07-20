from typing import Any, Literal

TeamType = Literal["country", "club"]

COUNTRIES: list[dict[str, Any]] = [
    {"id": "arg", "type": "country", "name": "Argentina", "code": "ARG", "flag_code": "ar"},
    {"id": "esp", "type": "country", "name": "Spain", "code": "SPA", "flag_code": "es"},
    {"id": "bra", "type": "country", "name": "Brazil", "code": "BRA", "flag_code": "br"},
    {"id": "fra", "type": "country", "name": "France", "code": "FRA", "flag_code": "fr"},
    {"id": "ger", "type": "country", "name": "Germany", "code": "GER", "flag_code": "de"},
    {"id": "eng", "type": "country", "name": "England", "code": "ENG", "flag_code": "gb-eng"},
    {"id": "por", "type": "country", "name": "Portugal", "code": "POR", "flag_code": "pt"},
    {"id": "ita", "type": "country", "name": "Italy", "code": "ITA", "flag_code": "it"},
    {"id": "ned", "type": "country", "name": "Netherlands", "code": "NED", "flag_code": "nl"},
    {"id": "bel", "type": "country", "name": "Belgium", "code": "BEL", "flag_code": "be"},
    {"id": "cro", "type": "country", "name": "Croatia", "code": "CRO", "flag_code": "hr"},
    {"id": "mex", "type": "country", "name": "Mexico", "code": "MEX", "flag_code": "mx"},
    {"id": "usa", "type": "country", "name": "United States", "code": "USA", "flag_code": "us"},
    {"id": "jpn", "type": "country", "name": "Japan", "code": "JPN", "flag_code": "jp"},
    {"id": "mar", "type": "country", "name": "Morocco", "code": "MAR", "flag_code": "ma"},
    {"id": "uru", "type": "country", "name": "Uruguay", "code": "URU", "flag_code": "uy"},
    {"id": "col", "type": "country", "name": "Colombia", "code": "COL", "flag_code": "co"},
    {"id": "sui", "type": "country", "name": "Switzerland", "code": "SUI", "flag_code": "ch"},
]

CLUBS: list[dict[str, Any]] = [
    {"id": "bar", "type": "club", "name": "FC Barcelona", "code": "BAR", "primary_color": "#004D98", "secondary_color": "#A50044"},
    {"id": "rma", "type": "club", "name": "Real Madrid", "code": "RMA", "primary_color": "#FEBE10", "secondary_color": "#FFFFFF"},
    {"id": "mci", "type": "club", "name": "Manchester City", "code": "MCI", "primary_color": "#6CABDD", "secondary_color": "#FFFFFF"},
    {"id": "liv", "type": "club", "name": "Liverpool", "code": "LIV", "primary_color": "#C8102E", "secondary_color": "#FFFFFF"},
    {"id": "bay", "type": "club", "name": "Bayern Munich", "code": "BAY", "primary_color": "#DC052D", "secondary_color": "#FFFFFF"},
    {"id": "psg", "type": "club", "name": "Paris Saint-Germain", "code": "PSG", "primary_color": "#004170", "secondary_color": "#DA291C"},
    {"id": "juv", "type": "club", "name": "Juventus", "code": "JUV", "primary_color": "#FFFFFF", "secondary_color": "#000000"},
    {"id": "mil", "type": "club", "name": "AC Milan", "code": "MIL", "primary_color": "#FB090B", "secondary_color": "#000000"},
    {"id": "che", "type": "club", "name": "Chelsea", "code": "CHE", "primary_color": "#034694", "secondary_color": "#FFFFFF"},
    {"id": "ars", "type": "club", "name": "Arsenal", "code": "ARS", "primary_color": "#EF0107", "secondary_color": "#FFFFFF"},
    {"id": "int", "type": "club", "name": "Inter Milan", "code": "INT", "primary_color": "#010E80", "secondary_color": "#000000"},
    {"id": "bvb", "type": "club", "name": "Borussia Dortmund", "code": "BVB", "primary_color": "#FDE100", "secondary_color": "#000000"},
    {"id": "atm", "type": "club", "name": "Atletico Madrid", "code": "ATM", "primary_color": "#CB3524", "secondary_color": "#FFFFFF"},
    {"id": "mun", "type": "club", "name": "Manchester United", "code": "MUN", "primary_color": "#DA291C", "secondary_color": "#FBE122"},
    {"id": "tot", "type": "club", "name": "Tottenham Hotspur", "code": "TOT", "primary_color": "#132257", "secondary_color": "#FFFFFF"},
    {"id": "nap", "type": "club", "name": "Napoli", "code": "NAP", "primary_color": "#12A0D7", "secondary_color": "#FFFFFF"},
]

ALL_TEAMS: dict[str, dict[str, Any]] = {
    team["id"]: team for team in [*COUNTRIES, *CLUBS]
}


def flag_url(flag_code: str, width: int = 80) -> str:
    return f"https://flagcdn.com/w{width}/{flag_code}.png"


def team_to_state(team: dict[str, Any], score: int = 0) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "id": team["id"],
        "type": team["type"],
        "name": team["name"],
        "code": team["code"],
        "score": score,
    }
    if team["type"] == "country":
        payload["flag_url"] = flag_url(team["flag_code"])
    else:
        payload["primary_color"] = team["primary_color"]
        payload["secondary_color"] = team["secondary_color"]
    return payload


def get_team(team_id: str) -> dict[str, Any] | None:
    return ALL_TEAMS.get(team_id)


def list_teams(team_type: TeamType | None = None) -> list[dict[str, Any]]:
    teams = COUNTRIES if team_type == "country" else CLUBS if team_type == "club" else [*COUNTRIES, *CLUBS]
    return [
        {
            "id": team["id"],
            "type": team["type"],
            "name": team["name"],
            "code": team["code"],
            **({"flag_url": flag_url(team["flag_code"])} if team["type"] == "country" else {
                "primary_color": team["primary_color"],
                "secondary_color": team["secondary_color"],
            }),
        }
        for team in teams
    ]


