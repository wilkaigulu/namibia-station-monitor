# ── monitor/compute_dqs.py ─────────────────────────────────────────────
# Reads the latest Namibia station file produced by fetch_stations.py,
# computes DQS v1.0 for each station, appends to the history CSV,
# and prints a summary table.
# Called by the GitHub Actions monthly workflow.
# ──────────────────────────────────────────────────────────────────────

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────
MONITOR_DIR   = Path("monitor/data")
HISTORY_FILE  = MONITOR_DIR / "dqs_history.csv"
LATEST_FILE   = MONITOR_DIR / "namibia_stations_latest.csv"
SUMMARY_FILE  = MONITOR_DIR / "dqs_latest.csv"

TODAY         = datetime.utcnow().strftime("%Y-%m-%d")
REFERENCE_YEAR = 1970
CURRENT_YEAR   = datetime.utcnow().year
REFERENCE_YEARS = CURRENT_YEAR - REFERENCE_YEAR
NORMAL_START   = 1981
NORMAL_END     = 2010

# Stations confirmed absent from GHCND despite ISD registration
GHCND_ABSENT = ["683000", "683005"]

# ── DQS v1.0 ──────────────────────────────────────────────────────────
def compute_dqs(row):
    """
    DQS = 0.4*L + 0.4*C + 0.2*G
    L = record length relative to reference horizon
    C = completeness proxy from ISD metadata
    G = normal period coverage
    """
    usaf = str(row.get("USAF", ""))

    # Stations confirmed absent from GHCND get DQS 0.0
    if usaf in GHCND_ABSENT:
        return {
            "dqs"            : 0.0,
            "length_score"   : 0.0,
            "completeness"   : 0.0,
            "normal_coverage": 0.0,
            "record_years"   : 0,
            "usable"         : False,
            "ghcnd_status"   : "ABSENT — ISD registered, GHCND 404",
        }

    # Parse begin and end dates
    try:
        begin = pd.to_datetime(str(row["BEGIN"]), errors="coerce")
        end   = pd.to_datetime(str(row["END"]),   errors="coerce")
    except Exception:
        begin = pd.NaT
        end   = pd.NaT

    if pd.isna(begin) or pd.isna(end):
        return {
            "dqs"            : 0.0,
            "length_score"   : 0.0,
            "completeness"   : 0.0,
            "normal_coverage": 0.0,
            "record_years"   : 0,
            "usable"         : False,
            "ghcnd_status"   : "unknown",
        }

    # L — record length
    record_years = max((end.year - max(begin.year, REFERENCE_YEAR)), 0)
    L = min(record_years / REFERENCE_YEARS, 1.0)

    # C — completeness proxy
    # ISD metadata does not give us day-level completeness directly.
    # We use span completeness: (end - begin).days / expected_days
    # This is a conservative proxy — true completeness from the audit
    # notebook is more precise but requires the full data pull.
    span_days     = (end - begin).days + 1
    expected_days = record_years * 365.25
    C = min(span_days / expected_days, 1.0) if expected_days > 0 else 0.0

    # G — normal period coverage
    normal_begin = max(begin.year, NORMAL_START)
    normal_end   = min(end.year,   NORMAL_END)
    years_in_normal = max(normal_end - normal_begin + 1, 0)
    G = years_in_normal / (NORMAL_END - NORMAL_START + 1)

    dqs = round(0.4*L + 0.4*C + 0.2*G, 4)

    return {
        "dqs"            : dqs,
        "length_score"   : round(L, 4),
        "completeness"   : round(C, 4),
        "normal_coverage": round(G, 4),
        "record_years"   : int(record_years),
        "usable"         : dqs >= 0.70,
        "ghcnd_status"   : "present",
    }

# ── Main ──────────────────────────────────────────────────────────────
def main():
    print(f"\n{'='*60}")
    print(f"NAMIBIA STATION MONITOR — compute_dqs.py")
    print(f"Run date: {TODAY}")
    print(f"{'='*60}\n")

    if not LATEST_FILE.exists():
        raise FileNotFoundError(
            f"Station file not found: {LATEST_FILE}\n"
            f"Run fetch_stations.py first."
        )

    df = pd.read_csv(LATEST_FILE, dtype=str)
    print(f"Stations loaded: {len(df)}")

    # Compute DQS for each station
    records = []
    for _, row in df.iterrows():
        scores = compute_dqs(row)
        record = {
            "run_date"       : TODAY,
            "usaf"           : row.get("USAF", ""),
            "station_name"   : row.get("STATION_NAME", ""),
            "begin"          : row.get("BEGIN", ""),
            "end"            : row.get("END", ""),
            **scores,
        }
        records.append(record)

    df_scores = pd.DataFrame(records)

    # ── Print summary table ───────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"DQS SUMMARY — {TODAY}")
    print(f"{'='*60}")
    print(f"\n{'Station':<30} {'DQS':>6}  {'Usable':>6}  {'Status'}")
    print("-" * 60)

    for _, row in df_scores.sort_values("dqs", ascending=False).iterrows():
        usable_str = "YES" if row["usable"] else "NO"
        print(
            f"  {str(row['station_name']):<28} "
            f"{row['dqs']:>6.4f}  "
            f"{usable_str:>6}  "
            f"{row['ghcnd_status']}"
        )

    print("-" * 60)
    usable_count = df_scores["usable"].sum()
    print(f"\nUsable (DQS ≥ 0.70): {usable_count} of {len(df_scores)}")
    print(f"\nNOTE: Monitor DQS uses ISD metadata as a completeness proxy.")
    print(f"For verified scores from actual daily records see audit/data/station_audit_results_2026-06.csv")
    print(f"GHCND absent: {(df_scores['ghcnd_status'].str.startswith('ABSENT')).sum()}")

    # ── Save latest scores ────────────────────────────────────────────
    df_scores.to_csv(SUMMARY_FILE, index=False)
    print(f"\nLatest scores saved to: {SUMMARY_FILE}")

    # ── Append to history ─────────────────────────────────────────────
    if HISTORY_FILE.exists():
        df_history = pd.read_csv(HISTORY_FILE, dtype=str)
        df_history = pd.concat(
            [df_history, df_scores.astype(str)],
            ignore_index=True
        )
    else:
        df_history = df_scores.astype(str)

    df_history.to_csv(HISTORY_FILE, index=False)
    print(f"History updated: {HISTORY_FILE} ({len(df_history)} total rows)")
    print(f"\nDone.\n")

if __name__ == "__main__":
    main()