# Namibia Station Monitor

**What the global climate archive actually contains for Namibia — and what it is missing.**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21229782.svg)](https://doi.org/10.5281/zenodo.21229782)
[![License: Apache 2.0](https://img.shields.io/badge/Code-Apache%202.0-blue.svg)](LICENSE-CODE)
[![License: CC BY 4.0](https://img.shields.io/badge/Data%20%26%20Docs-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA)

---

## What this repository is

This repository has two layers that belong together.

**The audit** (June 2026) is a one-time, reproducible examination of every
Namibian station record available in NOAA's Global Historical Climatology
Network Daily archive (GHCND). It answers the question a DFI analyst or
climate modeller should ask before trusting a regional hazard estimate:
*what is actually in the archive, and how much of it is usable?*

**The monitor** is the audit made operational. A GitHub Actions workflow runs
on the first of every month, re-pulls station availability and completeness
metrics from NOAA ISD, recomputes a Data Quality Score (DQS) for each
station, and commits an updated status table to this repository.

The two layers share the same station list, the same DQS definition, and the
same retrieval logic. They are one project at two points in time.

---

## The June 2026 audit: key findings

Ten Namibian stations were resolvable in GHCND as of 29 June 2026.

| Station | GHCND ID | Records | DQS | Usable |
|---|---|---:|:---:|:---:|
| Windhoek (GSN) | WA007401540 | 19,793 | 0.9870 | ✓ |
| Rundu | WA012084750 | 17,121 | 0.9338 | ✓ |
| Gobabis | WA007878380 | 12,242 | 0.8099 | ✓ |
| Ondangwa | WAM00068006 | 6,642 | 0.5849 | ✗ |
| Walvis Bay | WAM00068098 | 7,429 | 0.5566 | ✗ |
| Mariental | WA005688170 | 5,769 | 0.5484 | ✗ |
| Windhoek (alt B) | WA007401240 | 5,539 | 0.5478 | ✗ |
| Windhoek (alt C) | WA007401850 | 5,175 | 0.5403 | ✗ |
| Windhoek (alt A) | WA007400630 | 5,084 | 0.5334 | ✗ |
| Keetmanshoop | WA004192150 | 5,236 | 0.5263 | ✗ |
| **Lüderitz** | — | — | 0.0000 | **Absent** |

**Four findings warrant explicit statement:**

**1. Three of eleven stations carry usable long records.**
Windhoek GSN, Rundu, and Gobabis meet the DQS ≥ 0.70 threshold for
extreme-value analysis. The remaining seven have records too short,
too incomplete, or too discontinuous to be usable.

**2. Ondangwa has 35% completeness and is missing the entire 1990s.**
Ondangwa is the gateway station for Namibia's most densely populated
region. Its GHCND record covers 35.0% of expected observation days.

**3. Walvis Bay has 6.6% precipitation coverage since 1990.**
The national port and primary industrial corridor has precipitation
records for 6.6% of days since 1990.

**4. Lüderitz is absent from GHCND entirely.**
Lüderitz is listed as an active station in WMO OSCAR/Surface. It does
not appear in GHCND. Not sparse. Not gappy. Absent. Any hazard estimate
a global model produces for the southern Namibian coast is derived from
stations hundreds of kilometres away and from model physics and the
deliverable will not say so.

---

## Repository structure

```
namibia-station-monitor/
│
├── audit/                              # June 2026 founding audit
│   ├── 01_station_audit.ipynb          # Reproducible audit notebook
│   ├── audit_memo.md                   # Plain-language findings memo
│   └── data/
│       ├── clean/                      # Per-station clean daily CSVs
│       └── station_audit_results_2026-06.csv   # Frozen citable output
│
├── monitor/                            # Monthly live monitor (coming July 2026)
│   ├── compute_dqs.py
│   └── fetch_stations.py
│
├── .github/
│   └── workflows/
│       └── monthly_monitor.yml
│
├── docs/                               # Public status page
│   └── index.html
│
├── .env.example                        # NOAA_TOKEN= (no value — template only)
├── .gitignore
├── environment.yml
├── LICENSE-CODE                        # Apache 2.0
├── LICENSE-DATA                        # CC BY 4.0
└── README.md
```

---

## Data Quality Score (DQS v1.0)

The DQS is a continuous scalar in [0, 1] computed per station from
three components weighted as follows:

| Component | Weight | Description |
|---|:---:|---|
| Record length (L) | 0.4 | Years of data relative to a 56-year reference horizon |
| Completeness (C) | 0.4 | Fraction of non-missing daily observations within the record span |
| Normal period coverage (G) | 0.2 | Coverage of the 1981–2010 climatological normal period |

**DQS = 0.4 × L + 0.4 × C + 0.2 × G**

A station with DQS ≥ 0.70 is considered usable for extreme-value
analysis. Stations below this threshold receive substantially higher
prior weight in the SACRF Bayesian framework, reflecting genuine data
scarcity rather than treating sparse records as equivalent to long ones.

The full DQS specification is in `audit/audit_memo.md`.

---

## Reproducing the audit

```bash
# Clone
git clone https://github.com/wilkaigulu/namibia-station-monitor.git
cd namibia-station-monitor

# Create environment
conda env create -f environment.yml
conda activate namibia-monitor

# Open the notebook
cd audit
jupyter notebook 01_station_audit.ipynb
```

The frozen output (`audit/data/station_audit_results_2026-06.csv`) is
included in the repository so the findings are citable without
re-running any retrieval.

---

## How to cite

**For the audit and dataset:**

> Igulu, W. (2026). *Namibia Station Monitor: GHCND audit and Data Quality
> Scoring for Namibian climate stations* (audit-2026-06) [Data and code].
> Zenodo. https://doi.org/10.5281/zenodo.21229782

**BibTeX:**
```bibtex
@software{igulu_namibia_station_monitor_2026,
  author    = {Igulu, Wilka},
  title     = {Namibia Station Monitor: {GHCND} audit and Data Quality
               Scoring for Namibian climate stations},
  year      = {2026},
  version   = {audit-2026-06},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.21229782},
  url       = {https://doi.org/10.5281/zenodo.21229782}
}
```

**For the SACRF methodology this work supports:**

> Igulu, W. (2025). *A Bayesian Framework for Climate Risk Assessment in
> Data-Sparse African Infrastructure Markets* (SACRF Working Paper v0.2).
> wilkaigulu.com.

---

## Licences

- **Code** (`monitor/`, `audit/*.ipynb`): [Apache License 2.0](LICENSE-CODE)
- **Data and documentation** (`audit/data/`, `audit/audit_memo.md`):
  [Creative Commons Attribution 4.0 International](LICENSE-DATA)

---

## Author

**Wilka Igulu**  
Quantitative Analyst 
Windhoek, Namibia  
[wilkaigulu.com](https://wilkaigulu.com) · [github.com/wilkaigulu](https://github.com/wilkaigulu)

---

*Data as retrieved from NOAA GHCND, 29 June 2026. GHCND is a living archive;
findings reflect archive contents at the retrieval date. The monitor workflow
tracks subsequent changes.*