---
title: "Who Pays When Nature Strikes? The Insurance Protection Gap for Natural Catastrophes in Europe, 1980–2024"
subtitle: "Environmental Economics, BSc AIDAMS, ESSEC · Track 9 · Group 9: Amine Benbachir, Ylias Guetari, Marius Rang, Edouard Souied"
date: "2 November 2026"
---

## Abstract

Between 1980 and 2024, natural catastrophes in the 30 countries of the European Economic Area caused €802bn of economic losses, of which €222bn was insured: 72% of the damage stayed with households, firms and governments. We measure this protection gap by peril and by country with the input data of the EIOPA protection-gap dashboard (2025 version), and over time with the EEA's country-year series built on the same CATDAT losses. Earthquake (96% uninsured), wildfire (90%) and river and pluvial flood (79%) are the least covered perils, and windstorm the best covered (48%). Flood alone accounts for 53% of the €580bn uninsured. Italy, Germany and Spain carry 67% of it in euros; relative to GDP, Slovenia, Greece and Italy bear the most. Year by year, the uninsured share of every 10-year window since 1990 lies between 75% and 84%, and its fitted trend (−2.2 points per decade, SE 1.5) is not significant, while annual losses have roughly tripled since the 1980s. Countries that lose more relative to GDP are not better insured. Country–peril cells with public involvement in insurance or reinsurance have gaps about 37 points lower; the association holds for flood alone, without France and on the pre-correction 2024 data, but it shrinks to 22 points without France, Denmark and Iceland and disappears when cells are weighted by losses and France is left out. All results are descriptive or correlational.

## 1. The question

**Which natural catastrophe losses in Europe were insured, which were not, how has that changed over time, and where does the uninsured part fall?** We ask three precise questions, each with a measurable answer:

1. How large is the gap between economic and insured losses in the EEA, how does it differ by peril, and how has it moved since 1980?
2. How does it differ across countries, and which country–peril combinations are least covered?
3. Who carries the uninsured share, and is the gap related to how exposed a country is and to how its insurance system is organised?

We define the **protection gap** of a country *c* and a peril *p* as the share of economic losses that was not insured:

$$\text{Gap}_{c,p} = 1 - \frac{\text{Insured losses}_{c,p}}{\text{Economic losses}_{c,p}}$$

This is the measure EIOPA uses in its historical view (EIOPA, 2025a). An answer is a number between 0 and 100% for each country, peril, period and group, and a ranking of who bears the uninsured euros.

**Why it matters.** In the course framework, the damage of a disaster depends on the *hazard*, the *exposure* of people and assets, and their *vulnerability* (IPCC, 2014; Seghini, 2026, section 3.2). Insurance leaves the damage unchanged and decides **who pays for it**. An insured loss is pooled across policyholders and reinsurers. An uninsured loss stays with the household or firm that suffered it, or is shifted to the government budget through relief.

The question matters for households and firms, who absorb the uninsured part in their wealth, and for governments, for whom it becomes a fiscal liability: the course's stylized model makes GDP depend on climate damages and adaptive capacity, and lists spending on disaster management among the forces raising public debt (Seghini, 2026, sections 4.2 and 5.4). It also matters for banks, whose real-estate collateral loses value when insurance becomes scarce or expensive (Seghini, 2026, section 5.1), and for supervisors: the ACPR found that French insurers' natural-catastrophe claims could roughly double between 2022 and 2050 in an adverse scenario (ACPR, 2024). Extreme events are becoming more frequent and severe with every increment of warming (IPCC, 2023), and the ECB and EIOPA have proposed EU-level schemes to close the gap (ECB and EIOPA, 2023; EIOPA and ECB, 2024).

## 2. Description of the data

**Main source.** We use the input file of EIOPA's *Dashboard on insurance protection gap for natural catastrophes* (EIOPA, 2025b; file EIOPA-BoS-24-474, dated 4 December 2025, accessed 12 October 2026). EIOPA is the EU supervisor of insurers and pension funds; its *Technical description* documents how every variable is built (EIOPA, 2025a). The file has two sheets: losses by country, peril and dashboard version, and a qualitative description of each national insurance system filled in by national supervisors.

**Underlying loss data.** EIOPA takes losses from two disaster databases: **CATDAT**, compiled by the private firm RiskLayer and received through the European Environment Agency, and **EM-DAT**, the open database of CRED, UCLouvain. Spain's insured losses come from the public insurer Consorcio de Compensación de Seguros (CCS), Norway's from the Norwegian natural perils pool, and more than 13 national supervisors supplied corrections (EIOPA, 2025a).

**Coverage.** The 30 EEA countries (the 27 EU members plus Iceland, Liechtenstein and Norway) and five perils: river and pluvial flood (EIOPA's "Flood\*"), coastal flood, windstorm, wildfire and earthquake. **Hail** is not a separate peril: it is counted in windstorm, which covers extra-tropical cyclones and convective storms. **Drought** is absent, although the project brief lists both. Earthquake is the only peril EIOPA does not regard as climate-related; we keep it because it is a large part of the gap.

**Time, frequency and units.** Losses are **cumulative totals from 1980 to the year before the dashboard version**, in million euros at current prices (CPI-adjusted), not annual values (EIOPA, 2025a). The file holds four versions, 2022 to 2025 (155 rows each: 30 countries plus an EEA aggregate, × 5 perils), and each version **re-prices all past losses**: between consecutive versions, 44–65% of cells change by exactly the same factor (×1.080, ×1.041, ×1.030). Our cross-section uses the 2025 version (1980–2024) alone. The file also gives average annual economic losses per mille of GDP, which we call **loss intensity**; dividing EIOPA's numbers back out shows that the denominator is a single recent GDP (for Slovenia €67bn, close to its 2024 GDP), so the ratio compares a 45-year average loss with today's economy and is unaffected by the creation of Slovenia, Croatia or Czechia in 1991–93. Finally, the file gives EIOPA's *modelled* scores of current risk (0–4, from catastrophe models of the 200-year loss relative to GDP) and of insurance penetration (1 = 75–100% insured to 4 = 0–25%).

**Annual series.** To answer the time question we add the EEA dataset *Economic losses from climate-related extremes in Europe (1980–2024)*, October 2025 revision 1 (EEA, 2026; published 16 March 2026, accessed 26 October 2026). It is built on the same CATDAT data and gives total and insured losses **per country and year**, in 2024 prices. We keep the 30 EIOPA countries and the series that includes geophysical events. It differs from EIOPA in three ways: it counts heatwaves and droughts, it is not broken down by EIOPA's perils (only by four broad hazard types, and only for country groups), and it does not include the supervisors' corrections. It contains €957bn of losses, 82% uninsured.

**Our cleaning choices.** All are coded in `analysis.py` and change no raw value.

1. **Main source.** CATDAT records losses in 98 country–peril cells, against 61 in EM-DAT, so it is our main source and EM-DAT a check. Where the two disagree we keep CATDAT: for Croatian earthquakes, €1.3bn rather than EM-DAT's €13.8bn (section 4.3 shows what changes with the EM-DAT figure).
2. **Undefined gaps.** A cell with no recorded economic loss has an undefined gap. EIOPA codes it as 100% uninsured; we set it to missing, since "no event" is not "no insurance".
3. **Missing insured losses.** In EM-DAT, 21 of the 61 cells with losses report no insured loss, which may be missing data rather than a true zero. They hold only 6% of EM-DAT's economic losses: leaving them out moves EM-DAT's gap from 81% to 79%.
4. **Insured above economic.** In two cells, Swedish flood (€326m against €241m) and French coastal flood (€21.0m against €20.8m), we floor the gap at 0 and flag them.
5. **Loss-weighted aggregates.** Group gaps are 1 − Σ insured / Σ economic, so they describe the euros. We also report the median cell, which describes the typical country. We drop EIOPA's own "EEA" row, which does not equal the sum of its countries for insured flood (€74.2bn against €82.8bn) or earthquake losses.
6. **Insurance regime.** A cell has **public involvement** if residential primary insurance or reinsurance *for that peril* is public, public-private or state-guaranteed (2025 scheme sheet). This flags France (state reinsurer CCR), Spain (CCS), Belgium, Denmark, Iceland and Norway for some perils, and Malta for windstorm.

**Known limitations.**

- **Single events dominate.** One storm or earthquake can make up most of a 45-year total: 26 of the 98 cells hold less than €100m. In the annual data, the ten costliest years hold 48% of all 1980–2024 losses.
- **Revisions are large.** Between the 2024 and 2025 versions, France's insured losses were revised up by €62.8bn (windstorm +€45.6bn, flood +€16.4bn, earthquake +€0.7bn) while its economic losses rose by only €6.0bn, so France's gap fell from 69% to 22%. In the 2025 version, 99% of French windstorm losses are insured. The EEA series, without this correction, puts France at 65%.
- **Losses reflect the past.** They depend on past exposure and cover; EIOPA's modelled "current" gap is a different concept, which it warns is not comparable (EIOPA, 2025a).
- **Only materialised risk.** The data record disasters, not hazards (Seghini, 2026, section 3). Six cells have at least a "medium" modelled risk but no recorded loss, among them Dutch and German coastal flood.
- **Consistency checks.** EIOPA's penetration score, built from surveys rather than loss records, ranks cells as our gap does (Spearman correlation 0.57; Table 3). The EEA's own headline, "less than 20%" privately insured (EEA, 2025), is lower than our 28% for identifiable reasons: it counts heatwaves and droughts, which are barely insured, and it lacks EIOPA's French and Spanish corrections (insured losses of €48.5bn for France against €101bn).

## 3. Summary statistics

**Of €802bn of economic losses in 1980–2024, €222bn (28%) was insured; the gap is 72%, or €580bn.** Table 1 breaks this down by peril. The **loss-weighted gap** says what share of the euros lost was uninsured; the **cell statistics** say how the typical country fared.

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

*Source: EIOPA (2025b), 2025 version, CATDAT, CPI-adjusted million euros. Own calculations. A cell is one country–peril pair; cell statistics are computed over the 98 cells with recorded losses. EM-DAT records no coastal-flood losses.*

- **The typical cell is almost fully uninsured.** The median cell gap is 91.5%, far above the 72% aggregate, which a few large, well-insured cells (French and German windstorm) pull down.
- **The ranking of perils is robust to the source.** EM-DAT gives higher gaps for every peril, by 1 to 11 points, in the same order.
- **Countries differ more than perils.** For flood and windstorm, country gaps range from 0 to 100%, with standard deviations near 30 points.
- **Uninsured losses are concentrated.** Five cells (Italian earthquake and flood, German flood and windstorm, Spanish flood) hold 59% of the €580bn.

\needspace{7cm}

**Table 2. Selected countries: largest and smallest gaps, largest amounts and heaviest burdens, 1980–2024**

| Country | Economic losses (€bn) | Insured losses (€bn) | Gap (%) | Share of EEA uninsured losses (%) | Uninsured losses per year, 1980–2024 average (‰ of GDP) |
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

*Source: as Table 1. Last column: EIOPA's average annual economic losses per mille of a recent GDP, summed over perils after multiplying each by its gap. All 30 countries: `output/table2_by_country.csv`.*

## 4. Results

### 4.1 Which perils are least covered?

\begin{figure}[tbp]\centering
\includegraphics[width=0.72\linewidth]{../output/fig1_gap_by_peril.png}\par\smallskip
\begin{minipage}{0.96\linewidth}\small\textit{\textbf{Figure 1.} Share of economic losses not insured, by peril, 30 EEA countries, 1980–2024 (loss-weighted). Filled dots: CATDAT (main source); open dots: EM-DAT. Earthquake, wildfire and flood losses were 79–96\% uninsured; windstorm, at 48\%, is the only major peril where most losses were insured.}\end{minipage}
\end{figure}

The ranking follows the insurability of each peril. Windstorm is commonly included in standard property policies, so many buildings are covered without a separate decision. Flood and earthquake are often optional extensions, and their losses are concentrated in identifiable high-risk zones, which makes risk-based premiums expensive exactly where cover is most needed. Coastal flood has a low gap (31%) on tiny losses (€1.7bn in 45 years, mostly Danish), which we do not interpret.

In absolute terms, **river and pluvial flood is Europe's main protection-gap problem**: €308bn uninsured, 53% of the total. Earthquake (€125bn, 22%) and windstorm (€122bn, 21%) follow.

### 4.2 Which countries and combinations are least covered?

\begin{figure}[tbp]\centering
\includegraphics[width=0.53\linewidth]{../output/fig2_heatmap_country_peril.png}\par\smallskip
\begin{minipage}{0.96\linewidth}\small\textit{\textbf{Figure 2.} Uninsured share of economic losses (\%) by country and peril, 1980–2024; countries sorted by their all-peril gap. Grey cells: no recorded loss. † marks cells with under €100m of total losses, ‡ the Swedish flood cell where insured exceeds economic losses. Southern and Eastern Europe left 93–98\% of losses uninsured across almost every peril; only France and Denmark kept the all-peril gap below a third.}\end{minipage}
\end{figure}

- **Near-total gaps in the South and East.** Romania, Bulgaria, Croatia, Italy, Slovenia, Greece and Portugal all exceed 95%, across perils. Italy lost €224bn and recovered 3.6% from insurers, for flood (97% uninsured) as well as earthquake (98%).
- **Low gaps in the North-West.** The smallest all-peril gaps are in France (22%), Denmark (31%) and Iceland (38%). France's figure comes mostly from windstorm (1% uninsured, after the 2025 correction); its flood gap is 46%.
- **Within-country contrasts.** Germany insured 44% of its windstorm losses but only 26% of its flood losses.

### 4.3 Who carries the uninsured losses?

\begin{figure}[tbp]\centering
\includegraphics[width=0.86\linewidth]{../output/fig3_uninsured_by_country.png}\par\smallskip
\begin{minipage}{0.96\linewidth}\small\textit{\textbf{Figure 3.} Uninsured economic losses by country and peril, 1980–2024: (a) in € billion, CPI-adjusted, with the share of the EEA total; (b) average per year, in per mille of GDP. Italy, Germany and Spain carry 67\% of the €580bn in euros, but relative to the size of their economies Slovenia, Greece and Italy bear the heaviest burden.}\end{minipage}
\end{figure}

The countries with the highest *rates* are not those with the largest *amounts*. Romania, Bulgaria and Croatia have the worst gaps but hold only 3% of uninsured euros together. Italy alone holds 37% (€216bn, half of it from earthquakes), Germany 19% (€110bn) and Spain 11% (€63bn).

Relative to GDP the ranking changes (panel b). On average over 1980–2024, Slovenia lost 5.2‰ of its GDP a year to uninsured catastrophes, nine times Germany's 0.57‰. This average rests largely on one event: the August 2023 floods. 2023 alone accounts for 55% of Slovenia's 1980–2024 losses in the EEA data, and in the dashboard version that stops in 2022 Slovenia's burden was 2.2‰, below Greece (2.6‰). The source matters too: with EM-DAT's figure for Croatian earthquakes, Croatia's burden rises from 1.0‰ to 4.3‰, second only to Slovenia. For small economies, single uninsured disasters are macroeconomic and fiscal shocks.

The loss data say *where* uninsured losses fall, not *which agent* bears them, but two other sources give orders of magnitude:

- **The EU budget pays little of it.** The EU Solidarity Fund mobilised €8.6bn between 2002 and early 2024 for 109 natural disasters and 20 health emergencies (European Commission, 2024). In the EEA data, uninsured losses in the 30 countries over 2002–2023 were €459bn, so EU aid covered roughly 2% of them at most (the Fund also paid the UK, candidate countries and health emergencies); the rest fell on national budgets, households and firms.
- **National relief is mostly discretionary.** In 16 of the 30 countries post-disaster relief is ad hoc, decided after each event; 8 have a systematic mechanism and 6 none (scheme sheet).
- **Insured is not fully covered.** In Austria a flood or earthquake policy pays at most 2–3% of the sum insured, in Croatia 29% and in Italy 36% for flood; Romania's compulsory policies are capped at €10,000–20,000 per dwelling (EIOPA, 2025b). There, insured households keep most of a large loss.

### 4.4 Is the gap related to exposure and to the insurance regime?

\begin{figure}[tbp]\centering
\includegraphics[width=0.7\linewidth]{../output/fig4_loss_intensity_vs_gap.png}\par\smallskip
\begin{minipage}{0.96\linewidth}\small\textit{\textbf{Figure 4.} River and pluvial flood: protection gap (\%) against flood loss intensity, average annual flood losses in per mille of GDP (log scale), one dot per country, 1980–2024. Orange: public or public-private flood insurance or reinsurance. Countries that lose more to floods are not better insured. The six public-involvement countries have flood gaps from 4\% (Iceland) to 78\% (Belgium); Spain and Belgium sit next to Germany and Czechia.}\end{minipage}
\end{figure}

If insurance markets responded to risk, the countries hit hardest would buy the most cover. Figure 4 shows no such pattern for flood: Slovenia, the most flood-intensive country (4.8‰ of GDP a year), left 96% of flood losses uninsured. Plotting flood only matters, because the regime colour and the gap then refer to the same peril. On flood, the public-involvement group is less homogeneous than the all-peril numbers suggest: Iceland (4%), Denmark (36%), France (46%) and Norway (50%) have low gaps, but Spain (75%) and Belgium (78%) are close to Germany (74%).

\needspace{12cm}

**Table 3. Protection gap by feature of the national insurance system, country–peril cells with losses, 1980–2024**

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
| | … with public involvement (BE, FR, NO) | 11 | 3 | 28.7 | |
| | … without (AT, BG, EL, LI, RO) | 12 | 5 | 92.6 | |
| | Ad hoc | 52 | 17 | 89.1 | 94.0 |
| | … without public involvement | 45 | 16 | 92.6 | |
| | None | 18 | 8 | 65.1 | 88.2 |

\endgroup

*Source: EIOPA (2025b), country insurance scheme sheet (residential) merged with the loss data. A country can appear under several values when its rules differ by peril. Cells with unreported features are left out.*

- **Mandatory cover goes with low gaps, but only where it is enforced.** Cover is compulsory in France, Iceland, Liechtenstein and Romania. In Romania the pool PAID, set up in 2009 under Law 260/2008, sells the compulsory home policies, yet supervisors report low uptake, 25–75% of the population finding cover unaffordable, and a penetration of 0–25% (EIOPA, 2025b); 98% of its flood losses were uninsured.
- **Flat premiums go with low gaps only through the schemes they belong to.** Eleven countries charge a flat rate for at least one peril, such as France's 12% surcharge on property insurance (EIOPA, 2025a). Flat premiums almost always come with public involvement or compulsion, and holding those fixed their own association vanishes (section 5).
- **Systematic relief goes with lower gaps only because of public schemes.** Where a systematic relief mechanism sits inside a public scheme (Belgium's Calamities Fund, France's CatNat, Norway's pool), the gap is 29%. Where it does not (Austria, Bulgaria, Greece, Liechtenstein, Romania), the gap is 93%, the same as under ad-hoc relief. So the data are consistent with a *charity hazard* (expected state aid lowers demand for insurance) outside public schemes, and they do not show that relief itself raises coverage.
- **Spain is an outlier the other way.** EIOPA rates its current penetration at 75–100% for every peril, yet its historical gap is 77%. Coverage may have improved since the large losses, or CCS payouts may be under-recorded.

### 4.5 How has the gap changed over time?

\begin{figure}[tbp]\centering
\includegraphics[width=0.72\linewidth]{../output/fig5_annual_gap_eea.png}\par\smallskip
\begin{minipage}{0.96\linewidth}\small\textit{\textbf{Figure 5.} (a) Insured and uninsured losses per year, € billion at 2024 prices; (b) protection gap per year (dots) and over the 10 years ending in each year (line), 30 EIOPA countries, 1980–2024, all weather-, climate-related and geophysical hazards. Single years range from 52\% to 100\% uninsured, but every 10-year window since 1990 lies between 75\% and 84\%. The fitted trend, −2.2 points per decade, is not significantly different from zero.}\end{minipage}
\end{figure}

The EIOPA file cannot answer the time question: its four versions are overlapping 45-year totals, and the changes between them are dominated by re-pricing and corrections (of the €185bn rise in cumulative economic losses between the 2022 and 2025 versions, €99bn is re-pricing). We therefore use the EEA's annual series (Figure 5). Following the brief's warning about single events, we read it through 10-year windows and decades rather than single years.

- **The share is stable; the amount is not.** Average annual losses were €15bn in the 1980s, €22bn in the 2010s and €46bn in 2020–2024, while the uninsured share of each decade moved between 75% and 84% after the 1980s (94%, a decade dominated by the uninsured 1980 Irpinia earthquake). A stable gap on rising losses means a rising uninsured amount.
- **No significant trend.** Regressing the annual gap on the year gives −2.2 points per decade (Newey-West SE 1.5, p = 0.14), or −2.0 (SE 1.7) when years are weighted by their losses.
- **Hazards move in opposite directions.** For the EEA-32 group (our 30 countries plus Switzerland and Türkiye), the flood gap fell from 90% in the 1980s–1990s to 79% in 2020–2024, while the storm gap rose from 51% in the 1990s to 73%. Drought and heatwave losses stayed 78–95% uninsured in every decade.
- **Extremes dominate.** The ten costliest years hold 48% of all 1980–2024 losses.

This annual series also allows a like-for-like comparison with world figures: in 2024, the 30 countries left 73% of losses uninsured in the EEA data, against 57% worldwide according to Swiss Re (Swiss Re Institute, 2025).

## 5. Econometrics

**Holding the peril fixed, neither realised nor modelled exposure is linked with the gap, while public involvement in insurance is associated with a gap about 37 points lower; that figure depends on a few countries.** We estimate by ordinary least squares (OLS), on the cross-section of the 98 country–peril cells with recorded losses:

$$\text{Gap}_{c,p} = \alpha_p + \beta \, X_{c,p} + \gamma \,\text{Public}_{c,p} + \varepsilon_{c,p}$$

- **Gap** of country *c* and peril *p*: in percentage points, 0 to 100 (CATDAT, 1980–2024). Each cell counts once (unweighted), and cells under €100m (†) are kept in the baseline.
- $\alpha_p$: peril fixed effects, so that countries are compared within the same peril.
- $X_{c,p}$, exposure: in Models 1–2, **log10 of loss intensity** (average annual losses for that peril, ‰ of GDP). Recorded economic losses enter both the gap and this variable, so an error in recorded losses moves both together (division bias). Model 3 therefore uses **EIOPA's modelled risk score** (0–4), built from catastrophe models of hazard and exposure, not from recorded losses.
- **Public**: 1 if residential primary insurance or reinsurance *for that peril* is public, public-private or state-guaranteed; it varies across perils within a country. It equals 1 in 20 cells, in 7 countries.

Standard errors are clustered by country (30 clusters), because cells of one country share an insurance market.

\needspace{7cm}

**Table 4. OLS estimates; dependent variable: protection gap (pp)**

| | Model 1 | Model 2 | Model 3 |
|:--|--:|--:|--:|
| log10(loss intensity, ‰ of GDP) | 4.97 (3.91) | 4.81 (3.22) | |
| EIOPA modelled risk score (0–4) | | | 1.41 (2.85) |
| Public involvement (0/1) | | **−37.08 (11.38)** | **−36.76 (11.58)** |
| Peril fixed effects | yes | yes | yes |
| Observations (clusters) | 98 (30) | 98 (30) | 98 (30) |
| R² | 0.22 | 0.42 | 0.40 |

*Standard errors clustered by country in parentheses. Full output in `output/regression.txt`.*

**Interpretation in the units of the problem.** A cell with **ten times** higher annual losses relative to GDP has a gap about **5 points higher**, not lower (SE 3.2, p = 0.14). One step up EIOPA's modelled risk scale goes with 1.4 points more gap (SE 2.9). We cannot reject that exposure and coverage are unrelated, and we can reject a strong negative link: −10 lies 4.6 standard errors from the Model 2 estimate. Comparing cells of the same peril and similar exposure, those with public involvement have a gap **37 points lower** (95% interval −59 to −15), close to the distance between Germany (65%) and France (22%).

\needspace{8cm}

**Table 5. Robustness of the public-involvement coefficient (pp); each row re-estimates Model 2**

\begingroup\small\setlength{\tabcolsep}{3pt}

| Specification | Coefficient (SE) | p | Cells | Countries |
|:--------------------------------|:-----------------------|---:|----:|----:|
| Baseline: 2025 version, CATDAT | −37.1 (11.4) | 0.001 | 98 | 30 |
| *Does France drive it?* | | | | |
| 2024 version, before the French correction | −31.2 (8.6) | <0.001 | 97 | 30 |
| 2024 version, without France | −31.4 (10.5) | 0.003 | 92 | 29 |
| 2025 version, without France | −29.8 (10.5) | 0.005 | 93 | 29 |
| French windstorm coded as private | −33.6 (10.4) | 0.001 | 98 | 30 |
| Without France, Denmark and Iceland | −21.8 (10.2) | 0.033 | 87 | 27 |
| *Flood only* | | | | |
| River and pluvial flood cells | −37.7 (9.9) | <0.001 | 29 | 29 |
| Flood cells, without France | −36.4 (11.5) | 0.002 | 28 | 28 |
| *Weighting and sample* | | | | |
| Cells weighted by economic losses | −32.6 (16.2) | 0.044 | 98 | 30 |
| Weighted, without France | −5.6 (6.0) | 0.35 | 93 | 29 |
| Weighted, French windstorm coded as private | −13.4 (12.2) | 0.27 | 98 | 30 |
| Only cells with €100m of losses or more | −32.1 (11.8) | 0.007 | 72 | 27 |
| EM-DAT losses instead of CATDAT | −17.9 (8.4) | 0.033 | 61 | 26 |
| *Model and regime definition* | | | | |
| Fractional logit, average marginal effect | −35.0 (11.1) | 0.002 | 98 | 30 |
| All three in one model: public / mandatory / flat | −32.7 / −25.3 / +2.9 | 0.002 / 0.001 / 0.65 | 98 | 30 |
| Regime = mandatory, without Romania | −44.8 (7.8) | <0.001 | 95 | 29 |

\endgroup

*Standard errors clustered by country (fractional logit: country-cluster bootstrap, 500 draws). Weighted rows: weighted least squares with cell economic losses as weights. Full list in `output/regression_robustness.csv`.*

Three checks answer the main objection, that the result rests on France:

- **Without France, and before the French correction,** the coefficient stays between −30 and −31 points and significant. It also survives recoding French windstorm as private: CatNat covers wind only at cyclone strength, so ordinary storms are insured privately, although EIOPA codes the cell as public reinsurance.
- **On flood alone,** where the regime and the gap refer to the same peril, it is −38 points (−36 without France), on 29 countries of which 6 are public.
- **Weighted by losses,** the result is fragile. It is −33 points with France and −6 (not significant) without it: in euro terms, the association rests on France's large, well-insured cells. Without France, Denmark and Iceland, the unweighted coefficient falls to −22 points (p = 0.03).

The baseline uses clustered errors with only 7 "treated" countries out of 30, which can make standard errors too small. A permutation test, which reassigns the seven countries' regime patterns at random across the 30 countries 2,000 times, finds a coefficient as large as −37 in 1 of 2,000 draws (p = 0.0005). A fractional logit, built for shares bounded by 0 and 1 (30% of cells sit at 100%), gives −35. Compulsion also counts: in a joint model public involvement keeps −33 points and compulsion −25, while the flat-premium term falls to +3.

## 6. What we can and cannot conclude

\begingroup\small

| Result | Method | Nature of the claim |
|:----------------------------------------|:-------------------|:-----------------|
| 72% of 1980–2024 losses uninsured; flood, earthquake and wildfire 79–96% | Ratios of summed losses | **Description** |
| South and East 93–98%; Italy, Germany and Spain hold 67% of uninsured euros; Slovenia, Greece and Italy the heaviest burden relative to GDP | Ratios and sums by country | **Description** |
| Uninsured share of 10-year windows 75–84% since 1990, no significant trend; losses rising | Annual EEA series, fitted trend with HAC errors | **Description**, with a trend estimate |
| Exposure unrelated to the gap; public involvement and compulsion associated with lower gaps | OLS with peril fixed effects, fractional logit, permutation test | **Correlation**, sensitive to France when weighted by losses |

\endgroup

We can state with confidence that **most natural catastrophe losses in Europe since 1980 were uninsured**, in both CATDAT (72%) and EM-DAT (81%), and in EIOPA's and the EEA's versions of the data; that the gap is concentrated in flood and earthquake and in Southern and Eastern Europe; and that its share has not measurably changed since 1990 while losses have grown.

**Why the regression is not causal.** The permutation test shows that the association is unlikely to be chance, not that schemes cause coverage. France, Spain, Belgium and Denmark differ from Italy or Romania in income, history and risk culture, any of which can raise insurance demand and also make a public scheme more likely (selection). Large uninsured disasters can push governments to create schemes, and a scheme changes how insured losses are recorded, as Spain's CCS correction shows (reverse causality and measurement). And the regime variable is a 2025 snapshot applied to losses since 1980.

**What a causal claim would need.** An annual series by country and peril, and a reform to exploit in a difference-in-differences design: the gap of the reforming country before and after, against similar countries that did not reform. Candidates are Romania's compulsory cover through PAID (2009–2010), Belgium's inclusion of flood in standard fire policies in the mid-2000s, and Italy's 2024 law, in force since 2025, which obliges non-agricultural firms to insure against earthquake, flood and landslide, with the public reinsurer SACE taking up to 50% of claims (EIOPA, 2025b). The Italian reform is the cleanest future test, because it starts from a 96% gap.

**Who bears the uninsured share?** The data identify *where* losses fall and how heavy they are for each economy, not the split between agents. Combined with the scheme sheet and the course framework, they point to households and firms first, who absorb the loss as lost wealth (Seghini, 2026, section 5.1), including insured households where policy limits are low. Governments come second: EU aid covered at most about 2% of uninsured losses since 2002, and national relief is ad hoc in 16 of 30 countries, so uninsured losses become a contingent fiscal liability (Seghini, 2026, section 5.4), material in Slovenia, Greece and Italy. Banks hold the residual risk on uninsured mortgaged property; the ACPR pilot exercise found banks indirectly exposed to physical risk through how insurers adapt their policies (Seghini, 2026, section 6.2.1).

**Our position.** The protection gap is a market failure with a public cost. Demand is too low: households are myopic about rare events and underestimate their probability, and where relief is ad hoc and outside any scheme they may expect the state to pay anyway (charity hazard). Supply is expensive where risk is concentrated, because catastrophes hit many policyholders at once and insurers must hold costly capital or reinsurance.

The evidence points to the design of the system rather than to how hard a country is hit, with the caveat of section 5 that it rests on a handful of countries. Three of the course's four families of policy instruments (Seghini, 2026, section 4.3) map onto the remedies. A *mandate* answers low demand, and Romania shows it only works with affordable cover and enforcement. *Public support*, such as state reinsurance of the catastrophic layer, answers costly supply. A *price-based* design keeps premiums partly tied to risk. On flat premiums our two findings are consistent: they go with low gaps only because they come bundled with compulsion and public schemes, and on their own they do not reduce the gap. Since they also remove the signal that rewards building outside flood zones, they create moral hazard and, without compulsion, adverse selection. Our preferred design is therefore compulsory cover, public reinsurance of the catastrophic layer and premiums that keep some risk differentiation or are tied to prevention, the logic of the ECB and EIOPA proposal of an EU public-private reinsurance scheme paired with a disaster fund conditional on risk reduction (ECB and EIOPA, 2023; EIOPA and ECB, 2024). Our data cannot prove that it would close Italy's or Slovenia's gap; they show where it would matter most: flood and earthquake, in Southern and Eastern Europe.

## References

**Data**

- EEA (2026). *Economic losses from climate-related extremes in Europe (1980–2024)*, October 2025 revision 1 (xlsx in zip). European Environment Agency, published 16 March 2026. doi:10.2909/569291df-7bec-44cc-b829-285671f5f238, accessed 26 October 2026.
- EIOPA (2025b). *Dashboard on insurance protection gap for natural catastrophes: data used as input for the dashboard* (file EIOPA-BoS-24-474, xlsx). European Insurance and Occupational Pensions Authority. File dated 4 December 2025; dashboard last updated 5 December 2025. <https://www.eiopa.europa.eu/tools-and-data/dashboard-insurance-protection-gap-natural-catastrophes_en>, accessed 12 October 2026.
- Underlying sources, as documented by EIOPA (2025a): RiskLayer GmbH, *CATDAT* natural-disaster loss database, obtained via the European Environment Agency; CRED, UCLouvain, *EM-DAT: The International Disaster Database*; Consorcio de Compensación de Seguros (CCS), loss statistics for Spain; Norwegian natural perils pool, loss data for Norway.

**Literature and policy reports**

- ACPR (2024). *Main results of the climate stress-testing exercise in the insurance sector*. Autorité de contrôle prudentiel et de résolution, Banque de France, May 2024. <https://acpr.banque-france.fr/sites/default/files/medias/documents/20240527_main_results_of_the_climate_exercise_insurance_sector_2024_en.pdf>, accessed 12 October 2026.
- ECB and EIOPA (2023). *Policy options to reduce the climate insurance protection gap*. Staff paper, 24 April 2023. <https://www.eiopa.europa.eu/publications/staff-paper-policy-options-reduce-climate-insurance-protection-gap_en>, accessed 12 October 2026.
- EEA (2025). *Economic losses from weather- and climate-related extremes in Europe*. European Environment Agency, indicator. <https://www.eea.europa.eu/en/analysis/indicators/economic-losses-from-climate-related>, accessed 14 October 2026.
- EIOPA (2025a). *Technical description: Dashboard on insurance protection gap for natural catastrophes*. EIOPA-BoS-25/565, 6 October 2025. Available from the dashboard page cited above.
- EIOPA and ECB (2024). *Towards a European system for natural catastrophe risk management*. Joint paper, 18 December 2024. <https://www.eiopa.europa.eu/publications/eiopa-and-ecb-joint-paper-towards-european-system-natural-catastrophe-risk-management_en>, accessed 12 October 2026.
- European Commission (2024). *The EU Solidarity Fund: a commitment to help*. Panorama, DG Regional and Urban Policy, 31 January 2024. <https://ec.europa.eu/regional_policy/whats-new/panorama/2024/01/31-01-2024-the-eu-solidarity-fund-a-commitment-to-help_en>, accessed 26 October 2026.
- IPCC (2014). *Climate Change 2014: Impacts, Adaptation, and Vulnerability. Summary for Policymakers*. Contribution of Working Group II to the Fifth Assessment Report. Cambridge University Press.
- IPCC (2023). *Climate Change 2023: Synthesis Report*. Contribution of Working Groups I, II and III to the Sixth Assessment Report. Core Writing Team, H. Lee and J. Romero (eds.). IPCC, Geneva. doi:10.59327/IPCC/AR6-9789291691647.
- Seghini, C. (2026). *Environmental Economics*. Lecture slides, BSc AIDAMS, ESSEC Business School.
- Swiss Re Institute (2025). *Natural catastrophes: insured losses on trend to USD 145 billion in 2025*. sigma 1/2025, 29 April 2025. <https://www.swissre.com/institute/research/sigma-research/sigma-2025-01-natural-catastrophes-trend.html>, accessed 14 October 2026.

## Use of AI and reproducibility

**Use of AI.** We used Claude (Anthropic, model Claude Opus 5.5) for five tasks:

1. to write and debug the Python code (`analysis.py`) that cleans the data, computes all statistics and draws the figures;
2. to identify how the variables in the EIOPA file are built;
3. to find and verify part of the policy references, and to locate the EEA annual dataset;
4. to draft and edit the text, which the group then reviewed and revised;
5. to check the paper and slides against a peer review by a classmate and implement the corrections.

Every number in the paper is produced by the script from the two raw files (the Swiss Re and EU Solidarity Fund figures excepted, read off their reports), and we checked the headline totals independently against the raw spreadsheets. The group reviewed all figures, interpretations and references and takes responsibility for them. *[Group: adjust this paragraph to describe exactly how you used AI and what you changed yourselves.]*

**Reproducibility.** `python analysis.py` reproduces every table, figure and regression from the raw files exactly as downloaded (`raw/EIOPA-BoS-24-474_PowerBI input dashboard on insurance protectiongap.xlsx` and `raw/eea_t_losses-from-climate-related-extremes_p_1980-2024_v01_r01.zip`, both included; the script checks their SHA-256). Package versions are in `requirements.txt`. `output/paper_numbers.csv` lists every number quoted in the paper with the output file it comes from, and `build_pdf.sh` rebuilds this PDF.
