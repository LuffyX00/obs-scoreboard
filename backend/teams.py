import os
from dotenv import load_dotenv

load_dotenv()  # reads .env and loads LOGO_DEV_TOKEN into os.environ

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
    # --- Premier League (England) ---
    {"id": "mci", "type": "club", "league": "Premier League", "name": "Manchester City", "code": "MCI", "primary_color": "#6CABDD", "secondary_color": "#FFFFFF", "domain": "mancity.com"},
    {"id": "liv", "type": "club", "league": "Premier League", "name": "Liverpool", "code": "LIV", "primary_color": "#C8102E", "secondary_color": "#FFFFFF", "domain": "liverpoolfc.com"},
    {"id": "che", "type": "club", "league": "Premier League", "name": "Chelsea", "code": "CHE", "primary_color": "#034694", "secondary_color": "#FFFFFF", "domain": "chelseafc.com"},
    {"id": "ars", "type": "club", "league": "Premier League", "name": "Arsenal", "code": "ARS", "primary_color": "#EF0107", "secondary_color": "#FFFFFF", "domain": "arsenal.com"},
    {"id": "mun", "type": "club", "league": "Premier League", "name": "Manchester United", "code": "MUN", "primary_color": "#DA291C", "secondary_color": "#FBE122", "domain": "manutd.com"},
    {"id": "tot", "type": "club", "league": "Premier League", "name": "Tottenham Hotspur", "code": "TOT", "primary_color": "#132257", "secondary_color": "#FFFFFF", "domain": "tottenhamhotspur.com"},
    {"id": "new", "type": "club", "league": "Premier League", "name": "Newcastle United", "code": "NEW", "primary_color": "#241F20", "secondary_color": "#FFFFFF", "domain": "nufc.co.uk"},
    {"id": "avl", "type": "club", "league": "Premier League", "name": "Aston Villa", "code": "AVL", "primary_color": "#95BFE5", "secondary_color": "#670E36", "domain": "avfc.co.uk"},
    {"id": "whu", "type": "club", "league": "Premier League", "name": "West Ham United", "code": "WHU", "primary_color": "#7A263A", "secondary_color": "#1BB1E7", "domain": "whufc.com"},
    {"id": "eve", "type": "club", "league": "Premier League", "name": "Everton", "code": "EVE", "primary_color": "#003399", "secondary_color": "#FFFFFF", "domain": "evertonfc.com"},
    {"id": "bha", "type": "club", "league": "Premier League", "name": "Brighton & Hove Albion", "code": "BHA", "primary_color": "#0057B8", "secondary_color": "#FFCD00", "domain": "brightonandhovealbion.com"},
    {"id": "wol", "type": "club", "league": "Premier League", "name": "Wolverhampton Wanderers", "code": "WOL", "primary_color": "#FDB913", "secondary_color": "#231F20", "domain": "wolves.co.uk"},

    # --- La Liga (Spain) ---
    {"id": "bar", "type": "club", "league": "La Liga", "name": "FC Barcelona", "code": "FCB", "primary_color": "#004D98", "secondary_color": "#A50044", "domain": "fcbarcelona.com"},
    {"id": "rma", "type": "club", "league": "La Liga", "name": "Real Madrid", "code": "RMA", "primary_color": "#FEBE10", "secondary_color": "#FFFFFF", "domain": "realmadrid.com"},
    {"id": "atm", "type": "club", "league": "La Liga", "name": "Atletico Madrid", "code": "ATM", "primary_color": "#CB3524", "secondary_color": "#FFFFFF", "domain": "atleticodemadrid.com"},
    {"id": "sev", "type": "club", "league": "La Liga", "name": "Sevilla FC", "code": "SEV", "primary_color": "#D8232A", "secondary_color": "#FFFFFF", "domain": "sevillafc.es"},
    {"id": "rso", "type": "club", "league": "La Liga", "name": "Real Sociedad", "code": "RSO", "primary_color": "#0067B1", "secondary_color": "#FFFFFF", "domain": "realsociedad.eus"},
    {"id": "vil", "type": "club", "league": "La Liga", "name": "Villarreal CF", "code": "VIL", "primary_color": "#FFE667", "secondary_color": "#005187", "domain": "villarrealcf.es"},
    {"id": "bet", "type": "club", "league": "La Liga", "name": "Real Betis", "code": "BET", "primary_color": "#00954C", "secondary_color": "#FFFFFF", "domain": "realbetisbalompie.es"},
    {"id": "ath", "type": "club", "league": "La Liga", "name": "Athletic Bilbao", "code": "ATH", "primary_color": "#EE2523", "secondary_color": "#FFFFFF", "domain": "athletic-club.eus"},

    # --- Ligue 1 (France) ---
    {"id": "psg", "type": "club", "league": "Ligue 1", "name": "Paris Saint-Germain", "code": "PSG", "primary_color": "#004170", "secondary_color": "#DA291C", "domain": "psg.fr"},
    {"id": "mar1", "type": "club", "league": "Ligue 1", "name": "Olympique de Marseille", "code": "OM", "primary_color": "#2FAEE0", "secondary_color": "#FFFFFF", "domain": "om.fr"},
    {"id": "lyo", "type": "club", "league": "Ligue 1", "name": "Olympique Lyonnais", "code": "OL", "primary_color": "#DA0025", "secondary_color": "#0F1C3F", "domain": "ol.fr"},
    {"id": "mon", "type": "club", "league": "Ligue 1", "name": "AS Monaco", "code": "MON", "primary_color": "#E31B23", "secondary_color": "#FFFFFF", "domain": "asmonaco.com"},
    {"id": "lil", "type": "club", "league": "Ligue 1", "name": "LOSC Lille", "code": "LIL", "primary_color": "#E01E13", "secondary_color": "#001A4B", "domain": "losc.fr"},
    {"id": "ren", "type": "club", "league": "Ligue 1", "name": "Stade Rennais", "code": "REN", "primary_color": "#E4032E", "secondary_color": "#000000", "domain": "staderennais.com"},

    # --- Serie A (Italy) ---
    {"id": "juv", "type": "club", "league": "Serie A", "name": "Juventus", "code": "JUV", "primary_color": "#FFFFFF", "secondary_color": "#000000", "domain": "juventus.com"},
    {"id": "mil", "type": "club", "league": "Serie A", "name": "AC Milan", "code": "MIL", "primary_color": "#FB090B", "secondary_color": "#000000", "domain": "acmilan.com"},
    {"id": "int", "type": "club", "league": "Serie A", "name": "Inter Milan", "code": "INT", "primary_color": "#010E80", "secondary_color": "#000000", "domain": "inter.it"},
    {"id": "nap", "type": "club", "league": "Serie A", "name": "Napoli", "code": "NAP", "primary_color": "#12A0D7", "secondary_color": "#FFFFFF", "domain": "sscnapoli.it"},
    {"id": "rom", "type": "club", "league": "Serie A", "name": "AS Roma", "code": "ROM", "primary_color": "#8E1F2F", "secondary_color": "#F0BC42", "domain": "asroma.com"},
    {"id": "laz", "type": "club", "league": "Serie A", "name": "Lazio", "code": "LAZ", "primary_color": "#87D8F7", "secondary_color": "#FFFFFF", "domain": "sslazio.it"},
    {"id": "ata", "type": "club", "league": "Serie A", "name": "Atalanta", "code": "ATA", "primary_color": "#1C1CFF", "secondary_color": "#000000", "domain": "atalanta.it"},

    # --- Bundesliga (Germany) ---
    {"id": "bay", "type": "club", "league": "Bundesliga", "name": "Bayern Munich", "code": "BAY", "primary_color": "#DC052D", "secondary_color": "#FFFFFF", "domain": "fcbayern.com"},
    {"id": "bvb", "type": "club", "league": "Bundesliga", "name": "Borussia Dortmund", "code": "BVB", "primary_color": "#FDE100", "secondary_color": "#000000", "domain": "bvb.de"},
    {"id": "rbl", "type": "club", "league": "Bundesliga", "name": "RB Leipzig", "code": "RBL", "primary_color": "#DD0741", "secondary_color": "#FFFFFF", "domain": "dieroten-rb.de"},
    {"id": "b04", "type": "club", "league": "Bundesliga", "name": "Bayer Leverkusen", "code": "B04", "primary_color": "#E32221", "secondary_color": "#000000", "domain": "bayer04.de"},

    # --- Others (Portugal / Netherlands) ---
    {"id": "ben", "type": "club", "league": "Primeira Liga", "name": "SL Benfica", "code": "BEN", "primary_color": "#E32119", "secondary_color": "#FFFFFF", "domain": "slbenfica.pt"},
    {"id": "por1", "type": "club", "league": "Primeira Liga", "name": "FC Porto", "code": "POR", "primary_color": "#0B3D91", "secondary_color": "#FFFFFF", "domain": "fcporto.pt"},
    {"id": "ajx", "type": "club", "league": "Eredivisie", "name": "AFC Ajax", "code": "AJX", "primary_color": "#D2122E", "secondary_color": "#FFFFFF", "domain": "ajax.nl"},
]

ALL_TEAMS: dict[str, dict[str, Any]] = {
    team["id"]: team for team in [*COUNTRIES, *CLUBS]
}


def flag_url(flag_code: str, width: int = 80) -> str:
    return f"https://flagcdn.com/w{width}/{flag_code}.png"


def logo_url(domain: str, size: int = 128) -> str:
    """

    Get a free token at https://www.logo.dev and set it as the
    LOGO_DEV_TOKEN environment variable. Without a token, this falls back
    to Google's favicon service, which needs no signup or key at all but
    returns lower-resolution images.
    """
    token = os.environ.get("LOGO_DEV_TOKEN")
    print("------------token------------: ",token)
    
    return f"https://img.logo.dev/{domain}?token={token}&size={size}&format=png"


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
        payload["logo_url"] = logo_url(team["domain"])
        # payload["primary_color"] = team["primary_color"]
        # payload["secondary_color"] = team["secondary_color"]
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
                "logo_url": logo_url(team["domain"]),
                # "primary_color": team["primary_color"],
                # "secondary_color": team["secondary_color"],
            }),
        }
        for team in teams
    ]