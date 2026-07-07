# ── monitor/fetch_stations.py ──────────────────────────────────────────
# Pulls the NOAA ISD station history file and extracts Namibian stations.
# No authentication required — ISD history is a public file.
# Called by the GitHub Actions monthly workflow.
# ──────────────────────────────────────────────────────────────────────

import pandas as pd
import requests
from pathlib import Path
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────
ISD_URL     = "https://www1.ncdc.noaa.gov/pub/data/noaa/isd-history.csv"
OUTPUT_DIR  = Path("monitor/data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TODAY       = datetime.utcnow().strftime("%Y-%m-%d")
OUTPUT_FILE = OUTPUT_DIR / "namibia_stations_latest.csv"

# Known Namibian station USAF IDs for targeted filtering
NAMIBIA_USAF = {
    "68110": "Windhoek",
    "68066": "Walvis Bay",
    "68108": "Gobabis",
    "68104": "Keetmanshoop",
    "68006": "Ondangwa",
    "68004": "Rundu",
    "68106": "Mariental",
    "683000": "Lüderitz (Diaz Point)",
    "683005": "Lüderitz",
}

def fetch_isd_history():
    print(f"Fetching ISD history from NOAA...")
    r = requests.get(ISD_URL, timeout=60)
    r.raise_for_status()

    from io import StringIO
    df = pd.read_csv(StringIO(r.text), dtype=str)
    df.columns = [c.strip().upper().replace(" ", "_") for c in df.columns]
    print(f"  Total stations in ISD: {len(df):,}")
    return df

def extract_namibia(df):
    # Filter by country code NA (Namibia in FIPS)
    # and cross-check against known USAF prefixes
    namibia = df[df["CTRY"] == "WA"].copy()

    if len(namibia) == 0:
        # Fallback: filter by known USAF prefixes
        namibia = df[df["USAF"].str[:5].isin(NAMIBIA_USAF.keys())].copy()

    print(f"  Namibian stations found: {len(namibia)}")
    return namibia

def parse_dates(df):
    for col in ["BEGIN", "END"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="%Y%m%d", errors="coerce")
    return df

def flag_luderitz(df):
    luderitz_mask = df["USAF"].isin(["683000", "683005"])
    if luderitz_mask.sum() == 0:
        print("  ✗ Lüderitz (68096): NOT FOUND in ISD history")
        absent = pd.DataFrame([{
            "USAF"       : "68096",
            "WBAN"       : "99999",
            "STATION_NAME": "LUDERITZ",
            "CTRY"       : "WI",
            "ST"         : "",
            "ICAO"       : "",
            "LAT"        : "-26.65",
            "LON"        : "15.16",
            "ELEV(M)"    : "20",
            "BEGIN"      : pd.NaT,
            "END"        : pd.NaT,
            "ABSENT"     : True,
        }])
        df = pd.concat([df, absent], ignore_index=True)
    else:
        df.loc[luderitz_mask, "ABSENT"] = False
        print(f"  Lüderitz found in ISD: {luderitz_mask.sum()} record(s)")
    return df

def main():
    print(f"\n{'='*60}")
    print(f"NAMIBIA STATION MONITOR — fetch_stations.py")
    print(f"Run date: {TODAY}")
    print(f"{'='*60}\n")

    df_isd      = fetch_isd_history()
    df_namibia  = extract_namibia(df_isd)
    df_namibia  = parse_dates(df_namibia)
    df_namibia  = flag_luderitz(df_namibia)

    df_namibia["FETCH_DATE"] = TODAY
    df_namibia.to_csv(OUTPUT_FILE, index=False)

    print(f"\n  Saved {len(df_namibia)} stations to {OUTPUT_FILE}")
    print(f"  Done.\n")

if __name__ == "__main__":
    main()