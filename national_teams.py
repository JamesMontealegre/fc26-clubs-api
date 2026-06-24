"""
FC 26 National Teams Database.

Data sourced from fifaindex.com — FC 26 Kick Off mode ratings.

Columns:
    GRL: Overall rating (Global)
    ATA: Attack rating
    MED: Midfield rating
    DEF: Defense rating
    Stars: Star classification (1-5) derived from GRL
"""

import pandas as pd
from typing import Optional

NATIONAL_TEAMS_DATA = [
    {"team": "Francia", "flag": "\U0001f1eb\U0001f1f7", "league": "International", "GRL": 86, "ATA": 87, "MED": 85, "DEF": 85},
    {"team": "España", "flag": "\U0001f1ea\U0001f1f8", "league": "International", "GRL": 85, "ATA": 85, "MED": 86, "DEF": 83},
    {"team": "Inglaterra", "flag": "\U0001f3f4\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f", "league": "International", "GRL": 84, "ATA": 86, "MED": 85, "DEF": 83},
    {"team": "Brasil", "flag": "\U0001f1e7\U0001f1f7", "league": "International", "GRL": 84, "ATA": 85, "MED": 83, "DEF": 84},
    {"team": "Alemania", "flag": "\U0001f1e9\U0001f1ea", "league": "International", "GRL": 84, "ATA": 82, "MED": 84, "DEF": 84},
    {"team": "Portugal", "flag": "\U0001f1f5\U0001f1f9", "league": "International", "GRL": 84, "ATA": 84, "MED": 86, "DEF": 84},
    {"team": "Italia", "flag": "\U0001f1ee\U0001f1f9", "league": "International", "GRL": 83, "ATA": 82, "MED": 83, "DEF": 83},
    {"team": "Argentina", "flag": "\U0001f1e6\U0001f1f7", "league": "International", "GRL": 83, "ATA": 84, "MED": 83, "DEF": 79},
    {"team": "Países Bajos", "flag": "\U0001f1f3\U0001f1f1", "league": "International", "GRL": 82, "ATA": 80, "MED": 83, "DEF": 83},
    {"team": "Bélgica", "flag": "\U0001f1e7\U0001f1ea", "league": "International", "GRL": 81, "ATA": 82, "MED": 82, "DEF": 78},
    {"team": "Turquía", "flag": "\U0001f1f9\U0001f1f7", "league": "International", "GRL": 79, "ATA": 79, "MED": 80, "DEF": 78},
    {"team": "Croacia", "flag": "\U0001f1ed\U0001f1f7", "league": "International", "GRL": 79, "ATA": 78, "MED": 81, "DEF": 77},
    {"team": "Uruguay", "flag": "\U0001f1fa\U0001f1fe", "league": "International", "GRL": 79, "ATA": 78, "MED": 79, "DEF": 79},
    {"team": "Noruega", "flag": "\U0001f1f3\U0001f1f4", "league": "International", "GRL": 79, "ATA": 80, "MED": 81, "DEF": 75},
    {"team": "Marruecos", "flag": "\U0001f1f2\U0001f1e6", "league": "International", "GRL": 79, "ATA": 80, "MED": 78, "DEF": 78},
    {"team": "Senegal", "flag": "\U0001f1f8\U0001f1f3", "league": "International", "GRL": 79, "ATA": 79, "MED": 80, "DEF": 77},
    {"team": "Austria", "flag": "\U0001f1e6\U0001f1f9", "league": "International", "GRL": 78, "ATA": 77, "MED": 78, "DEF": 79},
    {"team": "Dinamarca", "flag": "\U0001f1e9\U0001f1f0", "league": "International", "GRL": 78, "ATA": 78, "MED": 79, "DEF": 78},
    {"team": "Costa de Marfil", "flag": "\U0001f1e8\U0001f1ee", "league": "International", "GRL": 78, "ATA": 80, "MED": 78, "DEF": 78},
    {"team": "Colombia", "flag": "\U0001f1e8\U0001f1f4", "league": "International", "GRL": 78, "ATA": 79, "MED": 79, "DEF": 78},
    {"team": "Suiza", "flag": "\U0001f1e8\U0001f1ed", "league": "International", "GRL": 78, "ATA": 77, "MED": 79, "DEF": 76},
    {"team": "Estados Unidos", "flag": "\U0001f1fa\U0001f1f8", "league": "International", "GRL": 77, "ATA": 77, "MED": 79, "DEF": 77},
    {"team": "Ucrania", "flag": "\U0001f1fa\U0001f1e6", "league": "International", "GRL": 77, "ATA": 79, "MED": 76, "DEF": 76},
    {"team": "Suecia", "flag": "\U0001f1f8\U0001f1ea", "league": "International", "GRL": 77, "ATA": 86, "MED": 77, "DEF": 75},
    {"team": "Polonia", "flag": "\U0001f1f5\U0001f1f1", "league": "International", "GRL": 77, "ATA": 82, "MED": 75, "DEF": 78},
    {"team": "Japón", "flag": "\U0001f1ef\U0001f1f5", "league": "International", "GRL": 77, "ATA": 78, "MED": 78, "DEF": 76},
    {"team": "República Checa", "flag": "\U0001f1e8\U0001f1ff", "league": "International", "GRL": 77, "ATA": 78, "MED": 75, "DEF": 75},
    {"team": "Argelia", "flag": "\U0001f1e9\U0001f1ff", "league": "International", "GRL": 76, "ATA": 75, "MED": 76, "DEF": 76},
    {"team": "Ecuador", "flag": "\U0001f1ea\U0001f1e8", "league": "International", "GRL": 76, "ATA": 73, "MED": 76, "DEF": 78},
    {"team": "Escocia", "flag": "\U0001f3f4\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f", "league": "International", "GRL": 76, "ATA": 77, "MED": 78, "DEF": 74},
    {"team": "México", "flag": "\U0001f1f2\U0001f1fd", "league": "International", "GRL": 76, "ATA": 78, "MED": 75, "DEF": 75},
    {"team": "Gales", "flag": "\U0001f3f4\U000e0067\U000e0062\U000e0077\U000e006c\U000e0073\U000e007f", "league": "International", "GRL": 75, "ATA": 74, "MED": 76, "DEF": 74},
    {"team": "Canadá", "flag": "\U0001f1e8\U0001f1e6", "league": "International", "GRL": 75, "ATA": 77, "MED": 74, "DEF": 74},
    {"team": "Puerto Rico", "flag": "\U0001f1f5\U0001f1f7", "league": "International", "GRL": 75, "ATA": 79, "MED": 74, "DEF": 74},
    {"team": "Ghana", "flag": "\U0001f1ec\U0001f1ed", "league": "International", "GRL": 75, "ATA": 78, "MED": 75, "DEF": 73},
    {"team": "Paraguay", "flag": "\U0001f1f5\U0001f1fe", "league": "International", "GRL": 75, "ATA": 74, "MED": 75, "DEF": 76},
    {"team": "Congo DR", "flag": "\U0001f1e8\U0001f1e9", "league": "International", "GRL": 74, "ATA": 78, "MED": 71, "DEF": 75},
    {"team": "Hungría", "flag": "\U0001f1ed\U0001f1fa", "league": "International", "GRL": 74, "ATA": 77, "MED": 74, "DEF": 74},
    {"team": "República de Irlanda", "flag": "\U0001f1ee\U0001f1ea", "league": "International", "GRL": 74, "ATA": 75, "MED": 71, "DEF": 74},
    {"team": "Egipto", "flag": "\U0001f1ea\U0001f1ec", "league": "International", "GRL": 74, "ATA": 78, "MED": 73, "DEF": 70},
    {"team": "Bosnia y Herzegovina", "flag": "\U0001f1e7\U0001f1e6", "league": "International", "GRL": 73, "ATA": 78, "MED": 70, "DEF": 73},
    {"team": "Rumanía", "flag": "\U0001f1f7\U0001f1f4", "league": "International", "GRL": 73, "ATA": 72, "MED": 72, "DEF": 72},
    {"team": "Arabia Saudí", "flag": "\U0001f1f8\U0001f1e6", "league": "International", "GRL": 72, "ATA": 74, "MED": 74, "DEF": 71},
    {"team": "Irán", "flag": "\U0001f1ee\U0001f1f7", "league": "International", "GRL": 72, "ATA": 73, "MED": 72, "DEF": 72},
    {"team": "Australia", "flag": "\U0001f1e6\U0001f1fa", "league": "International", "GRL": 71, "ATA": 69, "MED": 68, "DEF": 71},
    {"team": "Túnez", "flag": "\U0001f1f9\U0001f1f3", "league": "International", "GRL": 71, "ATA": 70, "MED": 72, "DEF": 72},
    {"team": "Irlanda del Norte", "flag": "\U0001f1ec\U0001f1e7", "league": "International", "GRL": 71, "ATA": 66, "MED": 70, "DEF": 70},
    {"team": "Islandia", "flag": "\U0001f1ee\U0001f1f8", "league": "International", "GRL": 71, "ATA": 68, "MED": 73, "DEF": 69},
    {"team": "Nueva Zelanda", "flag": "\U0001f1f3\U0001f1ff", "league": "International", "GRL": 70, "ATA": 74, "MED": 69, "DEF": 69},
    {"team": "Panamá", "flag": "\U0001f1f5\U0001f1e6", "league": "International", "GRL": 70, "ATA": 70, "MED": 70, "DEF": 69},
    {"team": "Finlandia", "flag": "\U0001f1eb\U0001f1ee", "league": "International", "GRL": 70, "ATA": 75, "MED": 69, "DEF": 64},
    {"team": "Indonesia", "flag": "\U0001f1ee\U0001f1e9", "league": "International", "GRL": 69, "ATA": 64, "MED": 66, "DEF": 71},
    {"team": "Catar", "flag": "\U0001f1f6\U0001f1e6", "league": "International", "GRL": 69, "ATA": 71, "MED": 68, "DEF": 66},
    {"team": "Haití", "flag": "\U0001f1ed\U0001f1f9", "league": "International", "GRL": 69, "ATA": 70, "MED": 69, "DEF": 69},
    {"team": "Uzbekistán", "flag": "\U0001f1fa\U0001f1ff", "league": "International", "GRL": 68, "ATA": 70, "MED": 67, "DEF": 71},
    {"team": "Curazao", "flag": "\U0001f1e8\U0001f1fc", "league": "International", "GRL": 68, "ATA": 66, "MED": 69, "DEF": 69},
    {"team": "Jordania", "flag": "\U0001f1ef\U0001f1f4", "league": "International", "GRL": 66, "ATA": 66, "MED": 67, "DEF": 66},
    {"team": "Irak", "flag": "\U0001f1ee\U0001f1f6", "league": "International", "GRL": 65, "ATA": 63, "MED": 66, "DEF": 64},
]


def _assign_stars(grl: int) -> float:
    """Map an overall rating (GRL) to a 1–5 star classification."""
    if grl >= 85:
        return 5.0
    if grl >= 82:
        return 4.5
    if grl >= 79:
        return 4.0
    if grl >= 76:
        return 3.5
    if grl >= 73:
        return 3.0
    if grl >= 70:
        return 2.5
    if grl >= 67:
        return 2.0
    if grl >= 64:
        return 1.5
    return 1.0


def get_national_teams() -> pd.DataFrame:
    """Return all national teams as a DataFrame with star ratings."""
    df = pd.DataFrame(NATIONAL_TEAMS_DATA)
    df["stars"] = df["GRL"].apply(_assign_stars)
    return df.sort_values("GRL", ascending=False).reset_index(drop=True)


def get_teams_by_stars(stars: float) -> pd.DataFrame:
    """Return national teams filtered by exact star rating."""
    df = get_national_teams()
    return df[df["stars"] == stars].reset_index(drop=True)


def get_teams_by_min_stars(min_stars: float) -> pd.DataFrame:
    """Return national teams with at least *min_stars* stars."""
    df = get_national_teams()
    return df[df["stars"] >= min_stars].reset_index(drop=True)


def get_team(name: str) -> Optional[pd.Series]:
    """Look up a single team by name (case-insensitive partial match)."""
    df = get_national_teams()
    mask = df["team"].str.lower().str.contains(name.lower())
    matches = df[mask]
    if matches.empty:
        return None
    return matches.iloc[0]


def summary() -> pd.DataFrame:
    """Return a count of teams grouped by star rating."""
    df = get_national_teams()
    return (
        df.groupby("stars")
        .agg(teams=("team", "count"), avg_GRL=("GRL", "mean"))
        .sort_index(ascending=False)
    )


if __name__ == "__main__":
    print("=== FC 26 National Teams by Stars ===\n")

    df = get_national_teams()
    for stars in sorted(df["stars"].unique(), reverse=True):
        group = df[df["stars"] == stars]
        print(f"{'★' * int(stars)}{'½' if stars % 1 else ''} ({stars} stars) — {len(group)} teams")
        for _, row in group.iterrows():
            print(f"  {row['flag']} {row['team']:<25} GRL:{row['GRL']}  ATA:{row['ATA']}  MED:{row['MED']}  DEF:{row['DEF']}")
        print()

    print("=== Summary ===")
    print(summary())
