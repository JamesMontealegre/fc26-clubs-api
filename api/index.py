"""
FC 26 Pro Clubs API — FastAPI application.

Exposes the existing fc26_api_class and national_teams modules as REST endpoints.
Designed for deployment on Vercel as a serverless function.
"""

import sys
from pathlib import Path

# Ensure project root is on the import path so fc26_api_class and national_teams
# are importable regardless of working directory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

import pandas as pd

from fc26_api_class import FC26_API
import national_teams

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="FC 26 Pro Clubs API",
    description="REST API for EA Sports FC 26 Pro Clubs data and national teams database.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Shared API client reused across requests.
_api_client = FC26_API()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _df_to_response(df: Optional[pd.DataFrame]):
    """Convert a DataFrame to a JSON-serialisable list of dicts."""
    if df is None:
        return None
    if df.empty:
        return []
    records = df.to_dict(orient="records")
    # Ensure Timestamp objects become ISO-8601 strings.
    for row in records:
        for key, value in row.items():
            if isinstance(value, pd.Timestamp):
                row[key] = value.isoformat()
    return records


def _series_to_response(s: Optional[pd.Series]):
    """Convert a Series to a JSON-serialisable dict."""
    if s is None:
        return None
    return s.to_dict()


def _club_details_to_response(df: Optional[pd.DataFrame]):
    """Convert the transposed club-details DataFrame to a dict keyed by club ID."""
    if df is None:
        return None
    if df.empty:
        return {}
    return {col: df[col].to_dict() for col in df.columns}


# ---------------------------------------------------------------------------
# Routes — Health
# ---------------------------------------------------------------------------


@app.get("/")
def root():
    return {"status": "ok", "service": "FC 26 Pro Clubs API", "docs": "/docs"}


# ---------------------------------------------------------------------------
# Routes — Clubs (proxy to EA Sports API)
# ---------------------------------------------------------------------------


@app.get("/api/clubs/search")
def search_club(name: str = Query(..., min_length=1, description="Club name to search")):
    result = _api_client.search_club_by_name(name)
    if result is None:
        raise HTTPException(status_code=502, detail="Upstream EA API request failed")
    return {"data": _df_to_response(result)}


@app.get("/api/clubs/{club_id}")
def get_club_details(club_id: str):
    result = _api_client.get_club_details(club_id)
    if result is None:
        raise HTTPException(status_code=502, detail="Upstream EA API request failed")
    return {"data": _club_details_to_response(result)}


@app.get("/api/clubs/{club_id}/matches")
def get_club_matches(
    club_id: str,
    match_type: str = Query(
        "friendlyMatch",
        pattern="^(friendlyMatch|leagueMatch|playoffMatch)$",
        description="Type of match",
    ),
):
    result = _api_client.get_club_matches(club_id, match_type=match_type)
    if result is None:
        raise HTTPException(status_code=502, detail="Upstream EA API request failed")
    return {"data": _df_to_response(result)}


@app.get("/api/clubs/{club_id}/matches/normalized")
def get_club_matches_normalized(
    club_id: str,
    match_type: str = Query(
        "friendlyMatch",
        pattern="^(friendlyMatch|leagueMatch|playoffMatch)$",
        description="Type of match",
    ),
    gmt: int = Query(2, ge=-12, le=14, description="GMT offset for timestamps"),
):
    result = _api_client.get_club_matches_normalized(
        club_id, match_type=match_type, gmt=gmt
    )
    if result is None:
        raise HTTPException(status_code=502, detail="Upstream EA API request failed")
    return {"data": _df_to_response(result)}


# ---------------------------------------------------------------------------
# Routes — National Teams (static data)
# ---------------------------------------------------------------------------


@app.get("/api/teams")
def get_all_teams():
    return {"data": _df_to_response(national_teams.get_national_teams())}


@app.get("/api/teams/summary")
def get_teams_summary():
    df = national_teams.summary().reset_index()
    return {"data": _df_to_response(df)}


@app.get("/api/teams/by-stars")
def get_teams_by_stars(
    stars: float = Query(..., ge=1.0, le=5.0, description="Exact star rating"),
):
    return {"data": _df_to_response(national_teams.get_teams_by_stars(stars))}


@app.get("/api/teams/by-min-stars")
def get_teams_by_min_stars(
    min_stars: float = Query(..., ge=1.0, le=5.0, description="Minimum star rating"),
):
    return {"data": _df_to_response(national_teams.get_teams_by_min_stars(min_stars))}


@app.get("/api/teams/{name}")
def get_team_by_name(name: str):
    result = national_teams.get_team(name)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No team found matching '{name}'")
    return {"data": _series_to_response(result)}
