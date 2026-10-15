---
title: "Who Pays When Nature Strikes? The Insurance Protection Gap for Natural Catastrophes in Europe, 1980–2024"
subtitle: "Environmental Economics — BSc AIDAMS, ESSEC · Track 9 · Group [X]"
date: "12 October 2026"
---

## Abstract

Between 1980 and 2024, natural catastrophes in the 30 countries of the European Economic Area caused €802bn of economic losses, of which only €222bn was insured: 72% of the damage was left to households, firms and governments. We measure this insurance protection gap with the input data of the EIOPA protection-gap dashboard (2025 version), by peril and by country. Earthquake (96% uninsured), wildfire (90%) and river and pluvial flood (79%) are the least covered perils; windstorm is the best covered (48%). Flood alone accounts for 53% of the €580bn of uninsured losses. Italy, Germany and Spain carry 67% of it in euros, but relative to their economies Slovenia, Greece and Italy bear the most: up to 0.5% of GDP uninsured every year. Countries that lose more relative to GDP are not better insured. Cells with public involvement in insurance or reinsurance show a gap 37 percentage points lower, a result that survives thirteen robustness checks, a fractional logit and a permutation test; compulsory cover also goes with lower gaps, but Romania's 98% gap despite compulsory insurance shows that law alone does not close it. These results are descriptive and correlational: the data are 45-year cumulative totals, re-priced and revised in each release, not an annual panel, so they cannot show a trend or identify why coverage differs.

## 1. The question

**Which natural catastrophe losses in Europe were insured, which were not, and where does the uninsured part fall?** We ask three precise questions, each with a measurable answer:

1. How large is the gap between economic and insured losses in the EEA, and how does it differ by peril?
2. How does it differ across countries, and which country–peril combinations are least covered?
3. Who carries the uninsured share, and is the gap related to how much a country loses to disasters and to how its insurance system is organised?

We define the **protection gap** of a country *c* and a peril *p* as the share of economic losses that was not insured:

$$\text{Gap}_{c,p} = 1 - \frac{\text{Insured losses}_{c,p}}{\text{Economic losses}_{c,p}}$$

This is the measure EIOPA uses in its historical view (EIOPA, 2025a). An answer is a number between 0 and 100% for each country, peril and group, and a ranking of who bears the uninsured euros.

**Why it matters.** In the course framework, the damage of a disaster depends on the *hazard*, the *exposure* of people and assets, and their *vulnerability* (IPCC, 2014; Seghini, 2026, section 3.2). Insurance does not change the damage itself. It changes **who pays for it**. An insured loss is pooled across policyholders and reinsurers. An uninsured loss stays with the household or firm that suffered it, or is shifted to the government budget through ad-hoc relief.

The question matters for four groups. **Households and firms** absorb the uninsured part in their wealth. For **governments** it becomes a fiscal liability: the course's stylized model makes GDP depend on climate damages and adaptive capacity and tracks the primary surplus, and lists spending on disaster management among the forces raising public debt (Seghini, 2026, sections 4.2 and 5.4). **Banks** hold real estate collateral whose value depends on the price and availability of insurance (Seghini, 2026, section 5.1). **Supervisors** watch the trend: the ACPR found that French insurers' natural-catastrophe claims could roughly double between 2022 and 2050 in an adverse scenario, with premiums not keeping pace with extreme losses (ACPR, 2024). If coverage retreats, risk moves back to households and to the banks that lend to them.

The stakes are rising: extreme events are becoming more frequent and severe with every increment of warming (IPCC, 2023), so a constant gap means a growing uninsured amount, and the ECB and EIOPA have proposed EU-level schemes to close it (ECB and EIOPA, 2023; EIOPA and ECB, 2024).

## 2. Description of the data

**Source.** We use the input file of EIOPA's *Dashboard on insurance protection gap for natural catastrophes* (EIOPA, 2025b; file EIOPA-BoS-24-474, dated 4 December 2025, accessed 12 October 2026). EIOPA is the EU supervisor of insurers and pension funds. Its *Technical description* documents how every variable is built (EIOPA, 2025a). The file has two sheets:

- **Historical and estimated protection gap**: one row per country, peril and dashboard version, with economic and insured losses.
- **Country insurance scheme**: a qualitative description of each national insurance system, filled in by national supervisors.

**Underlying loss data.** EIOPA does not record losses itself. It takes them from two disaster databases: **CATDAT**, compiled by the private firm RiskLayer and received through the European Environment Agency, and **EM-DAT**, the open database of CRED, UCLouvain. For Spain, insured losses come from the public insurer Consorcio de Compensación de Seguros (CCS), because the two databases miss its payouts. For Norway, they come from the Norwegian natural perils pool. More than 13 national supervisors supplied extra data or corrections (EIOPA, 2025a).

**Coverage.** The 30 EEA countries (the 27 EU members plus Iceland, Liechtenstein and Norway) and five perils: river and pluvial flood (EIOPA's "Flood\*"), coastal flood, windstorm (extra-tropical cyclones and convective storms, including hail), wildfire and earthquake. There is **no drought peril**, although the project brief lists one. Earthquake is the only peril EIOPA does not regard as climate-related; we keep it because it is a large part of the gap.

**Time, frequency and units.** This is the most important feature of the data. Losses are **cumulative totals from 1980 to the year before the dashboard version**, not annual values (EIOPA, 2025a). The file holds four versions, 2022 to 2025, covering 1980–2021 up to 1980–2024; each has 155 rows, 31 "countries" (30 plus an EEA aggregate) × 5 perils. Losses are in **million euros, adjusted to current prices with the consumer price index**, following EM-DAT practice. We found that each version **re-prices all past losses**: between consecutive versions, 44–65% of cells change by exactly the same factor (×1.080, ×1.041, ×1.030). Our main results use the 2025 version alone, so all values share one price level. The file also gives average annual economic losses as a share of GDP, in per mille, which we call **loss intensity**. It is the realised outcome of hazard, exposure and vulnerability together, not exposure in the IPCC sense, and is our measure of how much a country is hit. The file also gives EIOPA's *modelled* scores of current risk (0–4, from catastrophe models of the 200-year loss relative to GDP) and insurance penetration (1 = 75–100% insured to 4 = 0–25%), which we use only as cross-checks.

**Our cleaning choices.** All are coded in `analysis.py` and change no raw value.

1. **Main version and source.** We use the 2025 version and CATDAT as the main source. CATDAT records losses in 98 country–peril cells, against 61 in EM-DAT. EM-DAT is used as a robustness check.
2. **Undefined gaps.** A cell with no recorded economic loss has an undefined gap. EIOPA codes it as 100% uninsured; we set it to missing. Treating "no event" as "no insurance" would inflate the gap.
3. **Insured above economic.** In two cells, recorded insured losses exceed economic losses: Swedish flood (€326m against €241m) and French coastal flood (€21.0m against €20.8m). We floor the gap at 0 and flag them.
4. **Loss-weighted aggregates.** Group gaps are computed as 1 − Σ insured / Σ economic, so they describe the euros. We also report the median of cell gaps, which describes the typical cell.
5. **Our own totals.** We drop EIOPA's "EEA" row and sum the countries ourselves. The EEA row does not equal the sum of its countries for insured flood losses (€74.2bn against €82.8bn) or for earthquake (€4.79bn against €4.82bn).
6. **Insurance regime.** We code a country–peril cell as having **public involvement** if residential primary insurance or reinsurance for that peril is public, public-private or state-guaranteed (2025 scheme sheet). This flags France (state reinsurer CCR), Spain (CCS), Belgium, Denmark, Iceland and Norway for some perils, and Malta for windstorm.

**Known limitations.**

- **No annual series.** The data cannot show how the gap evolved year by year. Differences between versions mix new losses, revisions of past ones and re-pricing (section 4.5).
- **Rare events dominate.** One storm or earthquake can make up most of a 45-year total. 26 of the 98 cells hold less than €100m of losses in total.
- **Sources disagree.** For earthquakes in Croatia, CATDAT records €1.3bn of economic losses and EM-DAT €13.8bn. EIOPA itself warns that the collection methods of the sources are not aligned and that insured losses are the weakest series (EIOPA, 2025a).
- **Losses reflect the past.** They depend on past exposure and cover (the 1999 storm Lothar is valued with 1999 coverage). EIOPA's modelled "current" gap is a different concept, not comparable (EIOPA, 2025a); we do not mix them.
- **Only materialised risk.** In the course's terms, the data record disasters, not hazards (Seghini, 2026, section 3). Six cells have at least a "medium" modelled risk but no recorded loss, among them Dutch and German coastal flood, where EIOPA rates penetration at 0–25%. The historical gap is silent on them.
- **Two consistency checks.** EIOPA's penetration score is built from supervisor surveys and sum-insured data, not from loss records, yet it ranks cells as our gap does (Spearman correlation 0.57; Table 4). The EEA, using the same CATDAT source, reports that "less than 20% of total losses were privately insured" in 1980–2024, with the same countries at the bottom (Bulgaria, Croatia, Romania) and top (Belgium, Denmark, France) (EEA, 2025). Its share is lower than our 28%, plausibly for two reasons. It also counts climatological events such as heatwaves and droughts, of which "slightly over 10%" were insured. And it counts private insurance only, whereas EIOPA adds public schemes such as Spain's CCS.

## 3. Summary statistics

**Of €802bn of economic losses in 1980–2024, €222bn (28%) was insured; the gap is 72%, or €580bn.** For comparison, Swiss Re estimates that 57% of global natural catastrophe losses in 2024 were uninsured (Swiss Re Institute, 2025); periods and coverage differ, so this is context, not a like-for-like test. Table 1 breaks the European figure down by peril. The **loss-weighted gap** says what share of the euros lost was uninsured; the **cell statistics** (mean, standard deviation, range, median) say how the typical country fared.

**Table 1. Economic losses, insured losses and the protection gap by peril, EEA-30, 1980–2024**

\begingroup\small

| Peril | Countries with losses | Economic losses (€bn) | Insured losses (€bn) | Gap, loss-weighted (%) | Gap, EM-DAT check (%) | Cell gap: mean (%) | Cell gap: s.d. (pp) | Cell gap: min–max (%) | Cell gap: median (%) |
|:----------------|----:|----:|----:|----:|----:|----:|----:|----:|----:|
| River & pluvial flood | 29 | 391.0 | 82.8 | 78.8 | 83.9 | 78.5 | 28.3 | 0–100 | 93.0 |
| Windstorm | 30 | 252.5 | 130.4 | 48.3 | 58.9 | 70.2 | 29.6 | 0–100 | 81.5 |
| Earthquake | 20 | 130.1 | 4.8 | 96.3 | 97.3 | 81.7 | 32.3 | 0–100 | 99.1 |
| Wildfire | 13 | 26.7 | 2.7 | 90.0 | 98.7 | 95.6 | 9.6 | 68–100 | 100.0 |
| Coastal flood | 6 | 1.7 | 1.2 | 30.6 | — | 30.3 | 40.0 | 0–100 | 15.8 |
| **All perils** | **30** | **801.9** | **221.8** | **72.3** | **80.6** | **75.9** | **31.5** | **0–100** | **91.5** |
| Climate-related (excl. earthquake) | 30 | 671.9 | 217.0 | 67.7 | 75.3 | 74.5 | 31.3 | 0–100 | 86.2 |

\endgroup

*Source: EIOPA (2025b), 2025 version, CATDAT, CPI-adjusted million euros. Own calculations. A cell is one country–peril pair; cell statistics are computed over the 98 cells with recorded losses (one per country within each peril). EM-DAT records no coastal-flood losses.*

Four facts stand out:

- **The typical cell is almost fully uninsured.** The median cell gap is 91.5%, far above the 72% aggregate. The aggregate is pulled down by a few very large, well-insured cells, mainly French and German windstorm.
- **The ranking of perils is robust to the source.** EM-DAT gives higher gaps for every peril, by 1 to 11 points, but the same order: windstorm is the best insured major peril, earthquake the worst.
- **Countries differ more than perils.** For flood and windstorm, country gaps range from 0 to 100%, with standard deviations near 30 points.
- **Uninsured losses are concentrated.** Five cells (Italian earthquake and flood, German flood and windstorm, Spanish flood) hold 59% of the €580bn.

\needspace{7cm}

**Table 2. Selected countries: largest and smallest gaps, largest amounts and heaviest burdens, 1980–2024**

| Country | Economic losses (€bn) | Insured losses (€bn) | Gap (%) | Share of EEA uninsured losses (%) | Uninsured losses per year (‰ of GDP) |
|:--|--:|--:|--:|--:|--:|
| Romania | 10.3 | 0.2 | 98.3 | 1.8 | 0.64 |
| Bulgaria | 4.0 | 0.1 | 98.2 | 0.7 | 0.84 |
| Croatia | 4.0 | 0.1 | 97.2 | 0.7 | 1.01 |
| Italy | 223.5 | 8.0 | 96.4 | 37.2 | 2.18 |
| Slovenia | 16.3 | 0.6 | 96.1 | 2.7 | 5.19 |
| Greece | 29.0 | 1.3 | 95.7 | 4.8 | 2.59 |
| Spain | 81.1 | 18.5 | 77.2 | 10.8 | 0.87 |
| Germany | 169.7 | 59.7 | 64.8 | 19.0 | 0.57 |
| Iceland | 0.2 | 0.2 | 37.7 | 0.0 | 0.07 |
| Denmark | 9.0 | 6.2 | 31.0 | 0.5 | 0.16 |
| France | 129.8 | 101.0 | 22.2 | 5.0 | 0.22 |

*Source: as Table 1. Last column: EIOPA's average annual economic losses per mille of GDP, summed over perils after multiplying each by its gap. The full table for the 30 countries is in `output/table2_by_country.csv`.*

## 4. Results

### 4.1 Which perils are least covered?

\begin{figure}[tbp]\centering
\includegraphics[width=0.72\linewidth]{../output/fig1_gap_by_peril.png}\par\smallskip
\begin{minipage}{0.96\linewidth}\small\textit{\textbf{Figure 1.} Share of economic losses not insured, by peril, 30 EEA countries, 1980–2024 (loss-weighted). Filled dots: CATDAT (main source); open dots: EM-DAT. Earthquake, wildfire and flood losses were 79–96\% uninsured; windstorm, at 48\%, is the only major peril where most losses were insured.}\end{minipage}
\end{figure}

The ranking follows the insurability of each peril:

- **Windstorm** is commonly included in standard property policies, so many buildings are covered without a separate decision.
- **Flood and earthquake** are often optional extensions. Losses are concentrated in identifiable high-risk zones, which makes risk-based premiums expensive exactly where cover is most needed.
- **Coastal flood** has a low gap (31%) on tiny losses (€1.7bn in 45 years, mostly Danish); we do not interpret it.

In absolute terms, **river and pluvial flood is Europe's main protection-gap problem**: €308bn uninsured, 53% of the total. Earthquake (€125bn, 22%) and windstorm (€122bn, 21%) follow.

### 4.2 Which countries and combinations are least covered?

\begin{figure}[tbp]\centering
\includegraphics[width=0.53\linewidth]{../output/fig2_heatmap_country_peril.png}\par\smallskip
\begin{minipage}{0.96\linewidth}\small\textit{\textbf{Figure 2.} Uninsured share of economic losses (\%) by country and peril, 1980–2024; countries sorted by their all-peril gap. Grey cells: no recorded loss. † marks cells with under €100m of total losses, ‡ the Swedish flood cell where insured exceeds economic losses. Southern and Eastern Europe left 93–98\% of losses uninsured across almost every peril; only France and Denmark kept the all-peril gap below a third.}\end{minipage}
\end{figure}

The gap has a clear geography:

- **Near-total gaps in the South and East.** Romania, Bulgaria, Croatia, Italy, Slovenia, Greece and Portugal all exceed 95%, and the pattern holds across perils, not just one. Italy is the starkest case: it lost €223bn and recovered 3.6% from insurers, for flood (97% uninsured) as well as earthquake (98%).
- **Low gaps in the North-West.** The smallest all-peril gaps are in France (22%), Denmark (31%) and Iceland (38%).
- **Within-country contrasts.** Germany insured 44% of its windstorm losses but only 26% of its flood losses, so even a wealthy, well-insured market can have a large flood gap.
- **Small cells need caution.** Cells marked † rest on one or a few events.

### 4.3 Who carries the uninsured losses?

\begin{figure}[tbp]\centering
\includegraphics[width=0.86\linewidth]{../output/fig3_uninsured_by_country.png}\par\smallskip
\begin{minipage}{0.96\linewidth}\small\textit{\textbf{Figure 3.} Uninsured economic losses by country and peril, 1980–2024: (a) in € billion, CPI-adjusted, with the share of the EEA total; (b) per year, in per mille of GDP. Italy, Germany and Spain carry 67\% of the €580bn in euros, but relative to the size of their economies Slovenia, Greece and Italy bear the heaviest burden.}\end{minipage}
\end{figure}

The countries with the highest *rates* are not those with the largest *amounts*. Romania, Bulgaria and Croatia have the worst gaps but together hold only 3% of uninsured euros. Italy alone holds 37% (€216bn, half of it from earthquakes), Germany 19% (€110bn, more than half from flood) and Spain 11% (€63bn).

Relative to GDP the ranking changes again (panel b). Slovenia has lost on average 5.2‰ of its GDP a year to uninsured catastrophes, mostly floods: over 0.5% of GDP, nine times Germany's 0.57‰. Greece (2.6‰) and Italy (2.2‰) follow. For a small economy, uninsured losses are a macroeconomic and fiscal shock, not a sectoral one.

The data say *where* uninsured losses fall, not *which agent* inside a country bears them, but the scheme sheet gives two clues:

- **The state as insurer of last resort.** In 16 of the 30 countries, post-disaster public relief is ad hoc, decided after each event; 8 have a systematic mechanism and 6 none.
- **Insured is not fully covered.** Residential policies usually pay up to the full sum insured (median 98–100% by peril), but not everywhere. In Austria a flood or earthquake policy pays at most 2–3% of the sum insured; in Croatia 29% and in Italy 36% for flood. There, even insured households keep most of a large loss.

### 4.4 Is the gap related to loss intensity and to the insurance regime?

\begin{figure}[tbp]\centering
\includegraphics[width=0.7\linewidth]{../output/fig4_loss_intensity_vs_gap.png}\par\smallskip
\begin{minipage}{0.96\linewidth}\small\textit{\textbf{Figure 4.} All-peril protection gap (\%) against loss intensity, average annual economic losses in per mille of GDP (log scale), one dot per country, 1980–2024. Orange: countries with public or public-private flood insurance or reinsurance. Countries that lose more are not better insured, and the three lowest gaps (France, Denmark, Iceland) all have public involvement.}\end{minipage}
\end{figure}

If insurance markets responded to risk, the countries hit hardest would buy the most cover. Figure 4 shows no such pattern. Slovenia, Greece and Italy, the three highest loss intensities (2.3 to 5.4 per mille of GDP lost every year), all leave more than 95% of losses uninsured.

The design of the insurance system separates countries better than loss intensity does (Table 4).

\needspace{12cm}

**Table 4. Protection gap by feature of the national insurance system, country–peril cells with losses, 1980–2024**

\begingroup\small

| Feature (residential cover, 2025) | Value | Cells | Countries | Gap, loss-weighted (%) | Gap, median cell (%) |
|:---------------------|:-----------------|-----:|-----:|--------:|--------:|
| EIOPA modelled penetration | 1: 75–100% insured | 33 | 15 | 49.1 | 55.8 |
| | 2: 50–75% | 27 | 14 | 78.2 | 84.2 |
| | 3: 25–50% | 18 | 13 | 92.7 | 99.9 |
| | 4: 0–25% | 20 | 11 | 97.3 | 98.0 |
| Cover mandatory by law | Yes | 11 | 4 | 27.8 | 40.4 |
| | No | 87 | 28 | 81.8 | 92.4 |
| Premium | Flat | 28 | 11 | 45.8 | 70.2 |
| | Risk-based | 61 | 23 | 82.6 | 93.2 |
| Post-disaster state relief | Systematic mechanism | 23 | 8 | 46.9 | 78.2 |
| | Ad hoc | 52 | 17 | 89.1 | 94.0 |
| | None | 18 | 8 | 65.1 | 88.2 |

\endgroup

*Source: EIOPA (2025b), country insurance scheme sheet (residential) merged with the loss data. A country can appear under several values when its rules differ by peril. Cells with unreported features are left out.*

- **Mandatory cover goes with low gaps, but law alone is not enough.** Cover is compulsory in France, Iceland, Liechtenstein and Romania. Romania is the exception that matters: despite compulsory insurance, EIOPA rates its penetration at 0–25% and 98% of its flood losses were uninsured.
- **Flat premiums go with low gaps, but only through the company they keep.** Eleven countries price nat-cat cover for at least one peril as a flat charge rather than by individual risk, such as France's flat 12% surcharge on property insurance (EIOPA, 2025a). Flat premiums almost always come with public involvement or compulsion; holding those fixed, their own association vanishes (section 5).
- **Ad-hoc relief goes with the highest gaps.** This fits a *charity hazard*: households that expect the state to pay buy less insurance. It fits reverse causality equally well: the state steps in because nobody is insured.
- **Spain is an outlier the other way.** EIOPA rates its current penetration at 75–100% for every peril, yet its historical gap is 77%. Coverage may have improved since the large losses, or insured CCS losses may still be under-recorded; it is not evidence that public schemes fail.

Section 5 tests whether these associations survive once peril and loss intensity are held fixed.

### 4.5 Has the gap changed over time?

\begin{figure}[tbp]\centering
\includegraphics[width=0.68\linewidth]{../output/fig5_vintages.png}\par\smallskip
\begin{minipage}{0.96\linewidth}\small\textit{\textbf{Figure 5.} Protection gap (\%) by peril in the four dashboard versions; each point is a cumulative window starting in 1980. The windstorm gap falls 16.5 points between the 2024 and 2025 versions, but almost all of the change comes from corrections to past insured losses, not from 2024 events.}\end{minipage}
\end{figure}

This file cannot answer the time question well, for two reasons. First, each version re-prices the past: of the €185bn rise in cumulative economic losses between the 2022 and 2025 versions, €99bn is re-pricing and only €86bn is new or revised losses. Second, the corrections are large. Between the 2024 and 2025 versions:

- France's insured windstorm losses were revised from €24.2bn to €69.8bn (+€45.6bn).
- France's insured flood losses rose by €16.4bn and Spain's by €8.2bn, after CCS data were added.

These revisions cut the windstorm gap from 65% to 48% and the flood gap from 85% to 79%. The 2022–2024 versions, before the corrections, are almost flat. Only one step is free of large corrections: the €37bn of new or revised losses added between the 2023 and 2024 versions were 84% uninsured, close to the long-run average. So the honest conclusion is that **we cannot detect a trend**. France's low gap also rests on the 2025 correction: its all-peril gap was 69% in the 2024 version and is 22% in the 2025 version. An annual series, such as the EEA's country-year losses built on the same CATDAT data, would be needed to measure a trend.

## 5. Econometrics

**Holding the peril fixed, loss intensity has no detectable link with the gap, while public involvement in insurance is associated with a gap 37 points lower.** We estimate by ordinary least squares (OLS), on the cross-section of the 98 country–peril cells with recorded losses:

$$\text{Gap}_{c,p} = \alpha_p + \beta \,\log_{10}\!\left(\text{LossIntensity}_{c,p}\right) + \gamma \,\text{Public}_{c,p} + \varepsilon_{c,p}$$

The variables are:

- **Gap** of country *c* and peril *p*: in percentage points, from 0 to 100 (CATDAT, 1980–2024).
- $\alpha_p$: peril fixed effects, which compare countries within the same peril. Without them, the regression would mostly pick up the difference between, say, earthquake and windstorm.
- **LossIntensity**: average annual economic losses for that peril, in per mille of GDP (as computed by EIOPA).
- **Public**: a dummy equal to 1 if residential primary insurance or reinsurance for that peril is public, public-private or state-guaranteed. It equals 1 in 20 cells, spread over 7 countries.

Standard errors are clustered by country (30 clusters), because cells of the same country share one insurance market and are not independent.

\needspace{7cm}

**Table 3. OLS estimates; dependent variable: protection gap (pp)**

| | Model 1 | Model 2 |
|:--|--:|--:|
| log10(loss intensity, ‰ of GDP) | 4.97 (3.91) | 4.81 (3.22) |
| Public involvement (0/1) | — | **−37.08 (11.38)** |
| Peril fixed effects | yes | yes |
| Observations | 98 | 98 |
| Countries (clusters) | 30 | 30 |
| R² | 0.22 | 0.42 |

*Standard errors clustered by country in parentheses. Peril effects relative to coastal flood are in `output/regression.txt`.*

**Interpretation in the units of the problem.**

- **Loss intensity.** A country–peril cell with **ten times** higher annual losses relative to GDP has a gap about **5 points higher**, not lower. The standard error is 3.2 to 3.9 points, so the coefficient is not statistically different from zero (p = 0.14 in Model 2). We cannot reject that loss intensity and coverage are unrelated, but we can reject a strong negative link: a coefficient of −10 lies 4.6 standard errors away.
- **Public involvement.** Comparing cells of the same peril and similar loss intensity, those with public involvement have a gap **37 points lower** (95% confidence interval: −59 to −15 points, p = 0.001). This is large: close to the distance between Germany (65%) and France (22%).

\needspace{6\baselineskip}
**Robustness and caveats.**

The estimate rests on seven countries, France's gap depends on the 2025 correction, the gap is a bounded share (30% of cells sit at 100%), and the regime features overlap (correlations 0.3–0.5). We therefore re-estimate it in thirteen alternative ways (Table 5).

\needspace{8cm}

**Table 5. Robustness of the regime coefficient (pp); each row re-estimates Model 2**

\begingroup\small\setlength{\tabcolsep}{3pt}

| Specification | Coefficient (SE) | Cells | Countries |
|:--------------------------------|:-----------------------|----:|----:|
| Baseline: 2025 version, CATDAT | −37.1 (11.4) | 98 | 30 |
| 2024 version, before the corrections | −31.2 (8.6) | 97 | 30 |
| 2022 version | −34.5 (10.5) | 96 | 30 |
| EM-DAT losses instead of CATDAT | −17.9 (8.4) | 61 | 26 |
| Without France / without France and Spain | −29.8 (10.5) / −33.3 (13.0) | 93 / 88 | 29 / 28 |
| Only cells with losses of €100m or more | −32.1 (11.8) | 72 | 27 |
| Cells weighted by economic losses | −32.6 (16.2) | 98 | 30 |
| Loss intensity replaced by EIOPA modelled risk | −36.8 (11.6) | 98 | 30 |
| Regime = cover mandatory by law | −34.8 (12.1) | 98 | 30 |
| Regime = mandatory, without Romania | −44.8 (7.8) | 95 | 29 |
| Regime = flat premium | −20.2 (10.0) | 98 | 30 |
| Fractional logit, average marginal effect | −35.0 (11.1) | 98 | 30 |
| All three in one model: public / mandatory / flat | −32.7 (10.4) / −25.3 (7.7) / +2.9 (6.4) | 98 | 30 |

\endgroup

*Standard errors clustered by country (fractional logit: country-cluster bootstrap, 500 draws). All coefficients are significant at the 5% level except the flat-premium term in the last row. Full output in `output/regression.txt`.*

- **The French correction does not drive the result.** With the 2024 data, when France's gap was 69%, the coefficient is still −31 points.
- **Clustered errors with few treated countries can be too optimistic.** We therefore run a permutation test: we reassign the seven countries' regime patterns at random across the 30 countries 2,000 times. A coefficient as large as −37 in absolute value appears in 1 of 2,000 draws (p = 0.0005).
- **The size depends on the source, not on the model.** With EM-DAT the effect halves to −18 points, on 61 cells; a fractional logit, built for shares bounded by 0 and 1, gives −35.
- **Public involvement and compulsion each matter; flat premiums do not on their own.** In one model, public involvement keeps −33 points and compulsion −25, while flat premiums fall to +3.
- **Loss intensity never predicts better coverage.** Because economic losses enter both the gap and loss intensity, an error in recorded losses moves both together. EIOPA's forward-looking risk score is free of that problem, and it gives +1.4 points per risk step (SE 2.9).

## 6. What we can and cannot conclude

**Method and nature of each result.**

\begingroup\small

| Result | Method | Nature of the claim |
|:----------------------------------------|:-------------------|:-----------------|
| 72% of 1980–2024 losses were uninsured; flood, earthquake and wildfire gaps of 79–96% | Ratios of summed losses | **Description** of realised losses |
| Southern and Eastern Europe 93–98%; Italy, Germany and Spain carry 67% of uninsured euros; Slovenia, Greece and Italy the heaviest burden relative to GDP | Ratios and sums by country | **Description** |
| No trend can be detected from 2022 to 2025 | Comparison of cumulative windows | **Description**, dominated by revisions |
| Loss intensity unrelated to the gap; public involvement and compulsory cover associated with lower gaps | OLS with peril fixed effects, fractional logit, permutation test | **Correlation**, not a causal effect |

\endgroup

We can state with confidence that **most natural catastrophe losses in Europe since 1980 were not insured**, and that this is not an artefact of one database. EM-DAT gives an even higher gap (81%). We can also state that the gap is concentrated in flood and earthquake and in Southern and Eastern Europe.

**Why the regression is not causal.** The permutation test shows that the association is unlikely to be chance; it does not show that schemes cause coverage. Countries did not choose public schemes at random:

- **Selection.** France, Spain, Belgium and Denmark differ from Italy or Romania in income, history and risk culture. Any of these can raise insurance demand and also make a public scheme more likely.
- **Reverse causality.** Large uninsured disasters can push governments to create schemes, and a scheme in turn changes measured insured losses. Spain's CCS losses only enter the data through a specific correction (section 2).
- **Measurement.** The regime variable is a 2025 snapshot applied to losses since 1980. Several schemes, or their current design, may postdate many of the losses.

A causal claim would need annual data and a policy change: for example, a country's flood gap before and after it introduced compulsory or public-private cover, against similar countries that did not (difference-in-differences), using the EEA's country-year losses.

**Who bears the uninsured share?** The data identify *where* losses fall and how heavy they are relative to each economy (section 4.3), not the split between agents. Combined with the scheme sheet and the course framework, they point to three bearers of the €580bn:

- **Households and firms** absorb it as lost wealth, reducing consumption and investment: the physical-risk channel on people and capital (Seghini, 2026, section 5.1). Where policy limits are low, as for Austrian floods, this includes insured households.
- **Governments** pay through relief, ad hoc in 16 of 30 countries, so uninsured losses become a fiscal liability that adds to public debt (Seghini, 2026, section 5.4). In Slovenia, Greece and Italy, at 2–5‰ of GDP a year, the amounts are fiscally material.
- **Banks** hold the residual risk on uninsured mortgaged property. The ACPR pilot exercise found banks indirectly exposed to physical risk through how insurers adapt their policies (Seghini, 2026, section 6.2.1).

**Our position.** The protection gap is a market failure with a public cost, and with more frequent and severe extremes (IPCC, 2023) a constant gap means a growing uninsured amount, part of the cost of inaction (Seghini, 2026, section 4.1):

- **Demand is too low.** Households underestimate rare events, a form of the *tragedy of horizons* (Seghini, 2026, section 4.1). Ad-hoc relief may lead them to expect the state to pay anyway: a charity hazard.
- **Supply is expensive where risk is concentrated.** Catastrophe losses hit many policyholders at once, so insurers must hold costly capital or reinsurance, and risk-based premiums are highest where cover is most needed.

The evidence points to the design of the system rather than to how hard a country is hit. Three of the course's four families of policy instruments (Seghini, 2026, section 4.3) map onto the remedies. A *mandate* (compulsory cover) answers low demand, and our data say it works only when enforced: Romania. *Public support* (state reinsurance, public-private partnerships) answers costly supply. A *price-based* design keeps risk-based premiums. The three lowest gaps (France, Denmark, Iceland) all rely on public support.

The trade-off is the one the course stresses for price instruments: a price signal gives dynamic incentives. Flat premiums close the gap by cross-subsidising high-risk homes, but they remove the signal that rewards building outside flood zones or flood-proofing: a moral hazard that can raise future losses. Without compulsion they also invite adverse selection, as only high-risk households buy. Our preferred design is therefore compulsory cover, public reinsurance of the catastrophic layer and premiums that keep some risk differentiation or are tied to prevention. This is the logic of the ECB and EIOPA proposal of an EU public-private reinsurance scheme paired with a disaster fund conditional on risk reduction (ECB and EIOPA, 2023; EIOPA and ECB, 2024). Our data cannot prove that it would close Italy's or Slovenia's gap. They do show where it would matter most: flood and earthquake, in Southern and Eastern Europe.

## References

**Data**

- EIOPA (2025b). *Dashboard on insurance protection gap for natural catastrophes — Data used as input for the dashboard* (file EIOPA-BoS-24-474, xlsx). European Insurance and Occupational Pensions Authority. File dated 4 December 2025; dashboard last updated 5 December 2025. <https://www.eiopa.europa.eu/tools-and-data/dashboard-insurance-protection-gap-natural-catastrophes_en>, accessed 12 October 2026.
- Underlying sources, as documented by EIOPA (2025a): RiskLayer GmbH, *CATDAT* natural-disaster loss database, obtained by EIOPA via the European Environment Agency; CRED, UCLouvain, *EM-DAT: The International Disaster Database*; Consorcio de Compensación de Seguros (CCS), loss statistics for Spain; Norwegian natural perils pool, loss data for Norway.

**Literature and policy reports**

- ACPR (2024). *Main results of the climate stress-testing exercise in the insurance sector*. Autorité de contrôle prudentiel et de résolution, Banque de France, May 2024. <https://acpr.banque-france.fr/sites/default/files/medias/documents/20240527_main_results_of_the_climate_exercise_insurance_sector_2024_en.pdf>, accessed 12 October 2026.
- ECB and EIOPA (2023). *Policy options to reduce the climate insurance protection gap*. Staff paper, European Central Bank and European Insurance and Occupational Pensions Authority, 24 April 2023. <https://www.eiopa.europa.eu/publications/staff-paper-policy-options-reduce-climate-insurance-protection-gap_en>, accessed 12 October 2026.
- EEA (2025). *Economic losses from weather- and climate-related extremes in Europe*. European Environment Agency, indicator. <https://www.eea.europa.eu/en/analysis/indicators/economic-losses-from-climate-related>, accessed 14 October 2026.
- EIOPA (2025a). *Technical description — Dashboard on insurance protection gap for natural catastrophes*. EIOPA-BoS-25/565, 6 October 2025. Available from the dashboard page cited above.
- EIOPA and ECB (2024). *Towards a European system for natural catastrophe risk management*. Joint paper, 18 December 2024. <https://www.eiopa.europa.eu/publications/eiopa-and-ecb-joint-paper-towards-european-system-natural-catastrophe-risk-management_en>, accessed 12 October 2026.
- IPCC (2014). *Climate Change 2014: Impacts, Adaptation, and Vulnerability. Summary for Policymakers*. Contribution of Working Group II to the Fifth Assessment Report. Cambridge University Press.
- IPCC (2023). *Climate Change 2023: Synthesis Report*. Contribution of Working Groups I, II and III to the Sixth Assessment Report. Core Writing Team, H. Lee and J. Romero (eds.). IPCC, Geneva. doi:10.59327/IPCC/AR6-9789291691647.
- Seghini, C. (2026). *Environmental Economics*. Lecture slides, BSc AIDAMS, ESSEC Business School.
- Swiss Re Institute (2025). *Natural catastrophes: insured losses on trend to USD 145 billion in 2025*. sigma 1/2025, 29 April 2025. <https://www.swissre.com/institute/research/sigma-research/sigma-2025-01-natural-catastrophes-trend.html>, accessed 14 October 2026.

## Use of AI and reproducibility

**Use of AI.** We used Claude (Anthropic, model Claude Opus 5.5) for four tasks:

1. to write and debug the Python code (`analysis.py`) that cleans the data, computes all statistics and draws the figures;
2. to identify how the variables in the EIOPA file are built;
3. to find and verify part of the policy references;
4. to draft and edit the text, which the group then reviewed and revised.

Every number in the paper is produced by the script from the raw EIOPA file (the Swiss Re and EEA figures excepted, read off their reports), and we checked the headline totals independently against the raw spreadsheet. The group reviewed all figures, interpretations and references and takes responsibility for them. *[Group: adjust this paragraph to describe exactly how you used AI and what you changed yourselves.]*

**Reproducibility.** `python analysis.py` reproduces every table, figure and regression from the raw file exactly as downloaded (`raw/EIOPA-BoS-24-474_PowerBI input dashboard on insurance protectiongap.xlsx`, 240 KB, included; the script checks its SHA-256). Package versions are in `requirements.txt`. `output/paper_numbers.csv` lists every number quoted in the paper with the output file it comes from, and `build_pdf.sh` rebuilds this PDF.
