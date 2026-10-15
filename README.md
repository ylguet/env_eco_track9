# Track 9 — Insurance and the protection gap: analysis package

## Data

| | |
|---|---|
| Producer | European Insurance and Occupational Pensions Authority (EIOPA) |
| Dataset | Dashboard on insurance protection gap for natural catastrophes, *input data* (`EIOPA-BoS-24-474_PowerBI input dashboard on insurance protectiongap.xlsx`) |
| Version | Dashboard last updated 5 Dec 2025; file dated 4 Dec 2025; DB versions 2022–2025 inside the file |
| Methodology | EIOPA, *Technical description – Dashboard on insurance protection gap for natural catastrophes*, EIOPA-BoS-25/565, 6 Oct 2025 |
| Accessed | 12 October 2026, https://www.eiopa.europa.eu/tools-and-data/dashboard-insurance-protection-gap-natural-catastrophes_en |

**What the file contains**

- **Sheet *Historical and estimated pg*.** One row per country × peril × DB version.
  - **Countries:** 30 EEA countries, plus an "EEA" aggregate that we do not use.
  - **Perils:** river and pluvial flood ("Flood\*"), windstorm (which includes convective storms and hail), earthquake, wildfire and coastal flood. There is no drought peril, although the project brief lists one.
  - **Losses:** economic and insured, in million EUR and CPI-adjusted. They come from two sources: CATDAT (RiskLayer, received via the EEA) and EM-DAT (UCLouvain). Spain's insured losses come from the CCS and Norway's from the Norwegian natural perils pool. National supervisors added data and corrections.
  - **Period:** losses are **cumulative from 1980 to (version − 1)**. The 2025 version, which we use, covers 1980–2024.
- **Sheet *Country insurance scheme*.** Qualitative description of each national insurance regime: premium type, mandatory cover, public or private primary insurance and reinsurance, penetration band.

**Important:** the file is **not a yearly time series**. Each figure is a 45-year total. The 2022–2025 vintages are four cumulative windows, and differences between them are dominated by revisions (see Fig. 5).

## Method

- **Protection gap** = 1 − insured losses / economic losses (EIOPA's "uninsured losses %").
- **Main source:** CATDAT, which has wider coverage (98 country × peril cells with losses, against 65 in EM-DAT). EM-DAT is used as a robustness check.
- **Aggregation:** aggregates are **loss-weighted**: 1 − Σinsured / Σeconomic.
- **No losses:** cells with no recorded economic loss have an **undefined** gap. EIOPA codes them as 100% uninsured; we set them to missing.
- **Insured above economic:** where recorded insured losses exceed economic losses (Sweden flood, France coastal flood), the gap is floored at 0 and flagged.
- **Exposure** = average annual economic losses / GDP, in per mille, computed by EIOPA from CATDAT.

**Regression (optional section 5)**

- **Sample:** a cross-section of 98 country × peril cells.
- **Estimator:** OLS with peril fixed effects and standard errors clustered by country.
- **Equation:**

  gap(pp) = α_peril + β·log10(loss intensity) + γ·PublicInvolvement + ε

  PublicInvolvement = 1 if primary insurance or reinsurance for that peril is public, public-private or state-guaranteed (residential, 2025 scheme sheet).

## Key results (2025 version, 1980–2024)

**Totals.** Economic losses are **€802bn** and insured losses **€222bn**, so the gap is **72%** and **€580bn** is uninsured.

**By peril (Fig. 1, Table 1)**

| Peril | Gap, CATDAT | Gap, EM-DAT | Economic losses | Share of all uninsured losses |
|---|---|---|---|---|
| River and pluvial flood | 79% | 84% | €391bn | ≈53% |
| Earthquake | 96% | 97% | €130bn | ≈22% |
| Wildfire | 90% | 99% | €27bn | — |
| Windstorm | **48%** | 59% | — | ≈21% |
| Coastal flood | 31% | not covered | tiny losses | — |

- Windstorm is the best-covered major peril.
- Flood carries most of the uninsured losses.

**By country (Fig. 2, Table 2)**

- **Largest gaps:** Romania 98%, Bulgaria 98%, Croatia 97%, Italy 96%, Slovenia 96%, Greece 96%, Portugal 95%.
- **Smallest gaps:** France 22%, Denmark 31%, Iceland 38%, Liechtenstein 40%.

**Who carries the uninsured losses (Fig. 3).** Italy (€216bn, 37%), Germany (€110bn, 19%) and Spain (€63bn, 11%) together hold **67%** of all uninsured losses. The dataset says *where* the uninsured losses fall. It does not split them between households, firms and the state; that part has to be argued (see the course links below).

**Exposure and regime (Fig. 4, `regression.txt`)**

- **Loss intensity** (average annual losses / GDP, the outcome of hazard × exposure × vulnerability, not IPCC "exposure"): a tenfold higher loss intensity is associated with a gap **4.8 pp higher** (SE 3.2). That is not significant, so countries that lose more are *not* better insured.
- **Public involvement:** cells with public involvement have a gap **37 pp lower** (SE 11.4, p = 0.001). This rests on only 20 cells in 7 countries: Belgium, Denmark, France, Iceland, Malta, Norway and Spain.
- **Fit:** R² = 0.42.

**Over time (Fig. 5).** The vintages do not show a trend, only revisions:

- In the 2025 version, France's insured windstorm losses were revised up by €45.6bn (€24.2bn → €69.8bn).
- France's insured flood losses rose by €16.4bn and Spain's by €8.2bn (CCS data).
- As a result, the windstorm gap fell from 65% to 48%, and France's low gap depends heavily on that revision.

**Averaging matters.** Across all perils, the loss-weighted gap is 72%, but the median cell is 91.5% uninsured. Most country-peril cells are almost entirely uninsured; a few large, well-insured cells (French and German windstorm) pull the aggregate down.


**Added in the audit (14 Oct 2026)**

- **Re-pricing between versions.** Each version re-expresses all past losses at a newer price level (×1.080, ×1.041, ×1.030; 44–65% of cells change by exactly that factor). Of the €185bn rise in cumulative economic losses from the 2022 to the 2025 version, €99bn is re-pricing (`table8_repricing_between_versions.csv`).
- **Burden relative to GDP.** Uninsured losses per year: Slovenia 5.2‰ of GDP, Greece 2.6‰, Italy 2.2‰, against 0.57‰ in Germany and 0.22‰ in France (`table2_by_country.csv`, Fig. 3b).
- **Concentration.** Five country–peril cells hold 59% of the €580bn uninsured.
- **Insurance-system features** (`table5_gap_by_scheme_feature.csv`):

  | Feature | Gap with the feature | Gap without |
  |---|---|---|
  | Mandatory cover | 28% | 82% |
  | Flat premium | 46% | 83% (risk-based) |
  | Systematic state relief | 47% | 89% (ad-hoc relief) |

  Romania has a 98% gap despite compulsory cover.
- **Validation.** EIOPA's modelled penetration score agrees with the historical gap (Spearman 0.57; from 49% to 97% across penetration bands).
- **Hidden gap.** Six cells have at least a medium modelled risk but no recorded loss, for example Dutch coastal flood (`table7_...`).
- **Limits on insured cover.** Insurers' payouts are capped low in a few places: Austrian residential flood and earthquake policies pay at most 2–3% of the sum insured (`table6b_low_insurer_limits.csv`).
- **Robustness.** The public-involvement coefficient ranges from −18 to −45 pp across 11 alternative specifications, all significant at 5%. It is −31 pp with the 2024 data, from before the French correction. A permutation test gives p = 0.0005 (`regression_robustness.csv`, `regression.txt`).
- **Corrections to the first draft.** The windstorm gap drops 16.5 points, not 16. Spain's high historical gap coexists with a 75–100% modelled penetration, so it is not evidence that public schemes fail. One course citation was reworded to match the slide.

## Data issues to report in the data description

1. The data are cumulative totals, not annual. Single events dominate: cells marked † in Fig. 2 have under €100m of losses in total.
2. CATDAT and EM-DAT disagree strongly. For example, Croatian earthquake losses are €1.3bn in CATDAT against €13.8bn in EM-DAT. See `table3_catdat_vs_emdat.csv`.
3. Insured losses exceed economic losses in two cells (Sweden flood, France coastal flood).
4. EIOPA's own "EEA" row does not equal the sum of countries for insured flood losses (€74.2bn against €82.8bn) or for earthquake (€4.79bn against €4.82bn). See `check_eea_row_vs_country_sum.csv`.
5. Coding a no-loss cell as 100% uninsured would bias gaps upward. The technical description itself notes that the historical gap misses risks that did not materialise.
6. Historical losses reflect past exposure and coverage. The modelled "current" gap in the same file is a different concept, and EIOPA warns the two are not comparable.

## What we can and cannot conclude

- **Peril and country results:** these are **descriptions** of realised losses.
- **Regression:** it is a **correlation**. Countries that chose public schemes differ in many other ways (income, risk culture, history of disasters). The scheme may itself respond to past losses, which is reverse causality.
- **What a causal claim would need:** annual data and a policy change to exploit, such as a country introducing mandatory or public-private cover, compared before and after against similar countries (difference-in-differences).

## Files

| File | Content |
|---|---|
| `analysis.py` | Reproduces everything: `python analysis.py` (about 40 s) |
| `raw/EIOPA-BoS-24-474_PowerBI input dashboard on insurance protectiongap.xlsx` | The raw file, byte-identical to the download; `raw/SHA256.txt` holds its checksum, verified by the script |
| `requirements.txt` | Exact package versions used |
| `output/paper_numbers.csv` | Every number quoted in the paper, with the output file it comes from |
| `output/regime_feature_correlations.csv` | Overlap between public involvement, compulsion and flat premiums |
| `build_pdf.sh`, `paper/` | Paper source and the command that rebuilds the PDF |
| `output/clean_data_2025.csv`, `clean_data_all_versions.csv` | Cleaned panel |
| `output/table1_summary_by_peril.csv` | Summary statistics (paper section 3) |
| `output/table2_by_country.csv` | Country results |
| `output/table3_catdat_vs_emdat.csv` | Source comparison |
| `output/table4_vintages.csv` | Vintage comparison |
| `output/regression.txt`, `regression_coefficients.csv` | Optional econometrics |
| `output/table5…table8*.csv`, `regression_robustness.csv` | Audit additions: scheme features, policy limits, hidden gap, re-pricing, robustness |
| `output/fig1…fig5*.png` | Figures (220 dpi, self-contained captions and sources) |
| `paper/paper.md` → `Track9_Protection_Gap_Paper.pdf` | Paper source and PDF (pandoc + XeLaTeX) |

Requirements: see `requirements.txt` (Python 3.13, pandas, numpy, matplotlib, statsmodels, scipy, openpyxl).

## Final self-review (14 Oct 2026)

Graded against the guidelines' assessment criteria. Changes made after that review:

- **Terminology.** "Exposure" was renamed **loss intensity**. The variable is losses relative to GDP, the outcome of hazard × exposure × vulnerability, not exposure in the IPCC sense.
- **Regression robustness.** Two checks were added:
  - A **fractional logit** (average marginal effect −35.0 pp, bootstrap SE 11.1), because the gap is a bounded share and 30% of cells sit at 100%.
  - A **joint model** with all three regime features. Public involvement (−32.7) and compulsion (−25.3) survive; flat premiums (+2.9, SE 6.4) do not. The paper's earlier claim about flat premiums is now qualified.
- **Division bias.** Recorded economic losses enter both the gap and loss intensity, so measurement error moves both together. The modelled-risk specification avoids this.
- **EEA cross-check.** The EEA, using the same CATDAT data, reports less than 20% privately insured, with the same country ranking. The paper explains why its figure is lower.
- **Economic argument.**
  - The remedies are mapped to the course's policy-instrument families: mandate, public support, price-based instruments.
  - The paper states the incentive trade-off: flat premiums create moral hazard and, without compulsion, adverse selection.
  - It gives a design position: compulsory cover, public reinsurance and risk-differentiated premiums.
- **Figures.** Fig. 2 now has a colour scale. Fig. 4 has plain tick labels and the loss-intensity wording.
- **Table 1.** The cell statistics columns are labelled correctly.
- **Reproducibility.**
  - The raw file keeps its original name and is checked by SHA-256.
  - `requirements.txt` pins the package versions.
  - `paper_numbers.csv` traces every quoted number.
  - `build_pdf.sh` rebuilds the PDF.
- **Still open, outside our control.** No annual series is available in the EIOPA file, so a trend cannot be measured. Downloading the EEA country-year data would allow it.
