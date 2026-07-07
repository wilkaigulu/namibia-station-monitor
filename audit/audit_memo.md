# Namibian Station Audit — NOAA GHCND Data Quality Assessment

**Author:** Wilka Igulu  
**Date:** 29 June 2026  
**Repository:** https://github.com/wilkaigulu/namibia-station-monitor  
**DOI:** https://doi.org/10.5281/zenodo.21229782

---

## 1. Purpose

This memo documents the findings of a systematic audit of Namibian weather
station records available in the NOAA Global Historical Climatology Network
Daily (GHCND) archive. The audit was conducted to establish what climate data
is actually available for Namibia in the global archive not what the
station registers say should be there, but what the data says is there.

The findings directly inform the prior specification and Data Quality Score
(DQS) assignments used in the SACRF Bayesian climate risk framework
(Igulu, 2025). They are also relevant to any analyst, modeller, or DFI
technical reviewer who relies on global reanalysis products or hazard
estimates for Namibian infrastructure.

---

## 2. Archive and methodology

**Archive:** NOAA Global Historical Climatology Network Daily (GHCND)  
**Reference:** Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G.
Houston, 2012: An Overview of the Global Historical Climatology Network-Daily
Database. J. Atmos. Oceanic Technol., 29, 897-910.  
**Retrieval date:** 29 June 2026  
**Variables retrieved:** PRCP (precipitation), TMAX, TMIN, AWND (wind speed)  
**Retrieval period:** 1970–2026 in decade-length chunks  

Station IDs were confirmed directly from the NOAA master stations list at:  
https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt

Ten stations were resolvable. One station Lüderitz was confirmed absent
from the archive entirely. The full reproducible retrieval and cleaning code
is in `audit/01_station_audit.ipynb`.

---

## 3. Data Quality Score (DQS v1.0)

The DQS is a continuous scalar in [0, 1] computed from three components:

**L — Record length**  
Years of available data relative to a 56-year reference horizon (1970–2026).  
`L = min(record_years / 56, 1.0)`

**C — Completeness**  
Fraction of non-missing daily observations within the record span.  
`C = actual_days / expected_days`

**G — Normal period coverage**  
Coverage of the 1981–2010 climatological normal period, measured as the
fraction of years in that window with at least one observation.  
`G = years_present_in_normal_period / 30`

**Final score:**  
`DQS = 0.4 × L + 0.4 × C + 0.2 × G`

**Usability threshold:** DQS ≥ 0.70

Stations below this threshold receive substantially higher prior weight in
the SACRF Bayesian inference engine. The DQS scales prior influence
continuously it does not gate stations in or out but reflects genuine
data scarcity in the posterior. A station at DQS 0.98 produces a near-MLE
posterior; a station at DQS 0.35 leans heavily on regional priors.

---

## 4. Station-level findings

### 4.1 Windhoek GSN — DQS 0.9870 — USABLE
**GHCND ID:** WA007401540  
**Records:** 19,793 daily observations  
**Completeness:** 98.5%  
**Record span:** 1970–2024  

The primary long-record station for Namibia. Near-complete record from 1970
to present. This is the anchor station for extreme-value analysis in the
SACRF framework. The high DQS reflects both length and completeness.

---

### 4.2 Rundu — DQS 0.9338 — USABLE
**GHCND ID:** WA012084750  
**Records:** 17,121 daily observations  
**Completeness:** 85.2%  
**Record span:** 1970–2024  

Strong long-record station for the Kavango region in the north. Some gaps
in completeness but sufficient for extreme-value work. The Rundu record is
particularly important given the absence of usable stations in the northeast
of the country.

---

### 4.3 Gobabis — DQS 0.8099 — USABLE
**GHCND ID:** WA007878380  
**Records:** 12,242 daily observations  
**Completeness:** 60.9%  
**Record span:** 1970–2024  

Usable but with meaningful gaps. Completeness of 60.9% is below ideal.
The record length from 1970 carries the DQS above the threshold. Credible
intervals from this station will be wider than Windhoek or Rundu.

---

### 4.4 Ondangwa — DQS 0.5849 — NOT USABLE
**GHCND ID:** WAM00068006  
**Records:** 6,642 daily observations  
**Completeness:** 35.0%  

Ondangwa is the gateway station for Namibia's most densely populated region the Cuvelai Basin, home to the Oshana, Omusati, Oshikoto, and Ohangwena
regions. Its GHCND record covers only 35.0% of expected observation days.
The entire 1990s decade is absent from the archive.

This is not a peripheral station. Any infrastructure risk assessment for
northern Namibia that relies on global reanalysis without acknowledging this
gap is working from a materially incomplete evidential base.

---

### 4.5 Walvis Bay — DQS 0.5566 — NOT USABLE
**GHCND ID:** WAM00068098  
**Records:** 7,429 daily observations  
**Completeness:** 58.3% overall  
**Precipitation completeness since 1990:** 6.6%  

Overall completeness of 58.3% is misleading. Precipitation records
specifically the variable most critical for infrastructure risk cover
only 6.6% of days since 1990. Walvis Bay is the national port, the terminus
of the Trans-Kalahari and Trans-Caprivi corridors, and the site of
significant energy and industrial infrastructure. Its precipitation record
in the global archive is effectively absent for the past 35 years.

---

### 4.6 Mariental — DQS 0.5484 — NOT USABLE
**GHCND ID:** WA005688170  
**Records:** 5,769 daily observations  
**Completeness:** 96.7%  

High completeness but a short record. The record length is insufficient
for reliable extreme-value analysis over return periods beyond 20 years.
The DQS reflects this completeness is strong but length pulls the score
below the usability threshold.

---

### 4.7 Windhoek alt A, B, C — DQS 0.53–0.55 — NOT USABLE
**GHCND IDs:** WA007400630, WA007401240, WA007401850  

Three secondary Windhoek stations with short records beginning around 1980.
High completeness (96–98%) but insufficient length. These records may be
useful as secondary validation against the primary Windhoek GSN record but
are not independently usable for extreme-value analysis.

---

### 4.8 Keetmanshoop — DQS 0.5263 — NOT USABLE
**GHCND ID:** WA004192150  
**Records:** 5,236 daily observations  
**Completeness:** 93.0%  

Similar profile to Mariental good completeness, short record. The
ǁKaras region in the south is underrepresented in the usable archive.

---

### 4.9 Lüderitz — DQS 0.0000 — ABSENT FROM GHCND
**GHCND ID:** NOT IN GHCND  

Lüderitz does not appear in the GHCND archive. It is listed as an active
station in WMO OSCAR/Surface. Its ISD identifier (68096099999) is present
in the NOAA ISD master list but yields no records in GHCND.

This is an archiving gap, not an operational gap. The station exists. The
data is not in the global archive.

Lüderitz has over a century of settlement history. It is the site of the
Kudu Gas Field development, a functioning commercial harbour, and the
proposed terminus of the Tsau ǁKhaeb green hydrogen corridor. Any global
climate risk model that produces a hazard estimate for the southern Namibian
coast is doing so without a single observation from this location. The
model will not disclose this.

**This finding is the headline result of this audit.**

---

## 5. Summary table

| Station | GHCND ID | Records | Completeness | DQS | Usable |
|---|---|---:|:---:|:---:|:---:|
| Windhoek (GSN) | WA007401540 | 19,793 | 98.5% | 0.9870 | ✓ |
| Rundu | WA012084750 | 17,121 | 85.2% | 0.9338 | ✓ |
| Gobabis | WA007878380 | 12,242 | 60.9% | 0.8099 | ✓ |
| Ondangwa | WAM00068006 | 6,642 | 35.0% | 0.5849 | ✗ |
| Walvis Bay | WAM00068098 | 7,429 | 58.3% | 0.5566 | ✗ |
| Mariental | WA005688170 | 5,769 | 96.7% | 0.5484 | ✗ |
| Windhoek (alt B) | WA007401240 | 5,539 | 98.4% | 0.5478 | ✗ |
| Windhoek (alt C) | WA007401850 | 5,175 | 98.3% | 0.5403 | ✗ |
| Windhoek (alt A) | WA007400630 | 5,084 | 96.6% | 0.5334 | ✗ |
| Keetmanshoop | WA004192150 | 5,236 | 93.0% | 0.5263 | ✗ |
| **Lüderitz** | **NOT IN GHCND** | **—** | **—** | **0.0000** | **✗** |

**Usable stations (DQS ≥ 0.70):** 3 of 11  
**Absent from archive:** 1 (Lüderitz)  
**Audit date:** 29 June 2026  

---

## 6. Implications for climate risk modelling

The three usable stations: Windhoek, Rundu, Gobabis cover the central
highlands and the Kavango region. They leave the following areas without
a usable long record in the global archive:

- The entire northern population corridor (Ondangwa gap)
- The Atlantic coast and industrial zone (Walvis Bay, Lüderitz gap)
- The southern Karas region (Keetmanshoop, Mariental)

Global reanalysis products (ERA5, CHIRPS, MSWEP) interpolate across these
gaps using model physics and distant stations. The interpolated output
carries no explicit uncertainty flag for data-sparse regions. A DFI
technical reviewer reading a hazard assessment for a Walvis Bay port
expansion or a Lüderitz hydrogen facility will see a number. They will
not see a footnote saying that number was produced without a single
local observation.

This is the gap the SACRF framework is designed to make explicit and
quantify using the DQS to scale prior influence, widen credible
intervals appropriately, and produce uncertainty estimates that are honest
about what the archive actually contains.

---

## 7. References

Igulu, W. (2025). *A Bayesian Framework for Climate Risk Assessment in
Data-Sparse African Infrastructure Markets* (SACRF Working Paper v0.2).
wilkaigulu.com.

Igulu, W. (2026). *Namibia Station Monitor: GHCND audit and Data Quality
Scoring for Namibian climate stations* (v1.0-audit-2026-06). Zenodo.
https://doi.org/10.5281/zenodo.21229782

Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston (2012).
An Overview of the Global Historical Climatology Network-Daily Database.
*Journal of Atmospheric and Oceanic Technology*, 29, 897–910.

Strohbach, B. (2014). *The SASSCAL/MAWF Weather Stations Network in
Namibia: Overview of equipment and data transfer*. School of Natural
Resources and Spatial Sciences, Polytechnic of Namibia. October 2014.