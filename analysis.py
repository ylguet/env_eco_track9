"""
Track 9 - Insurance and the protection gap (Environmental Economics, ESSEC BSc AIDAMS, 2026-27)

Reproduces every number, table and figure from the raw EIOPA file, as downloaded:
    EIOPA-BoS-24-474_PowerBI input dashboard on insurance protectiongap.xlsx
    (EIOPA, Dashboard on insurance protection gap for natural catastrophes,
     input data, last updated 4-5 December 2025; accessed 12 October 2026)

Usage:  python analysis.py ["raw/<file as downloaded>.xlsx"]  [output_dir]
        (requirements: see requirements.txt; the raw file is checked against its SHA-256 below)

Definitions (see technical description EIOPA-BoS-25/565, 6 Oct 2025, ch. 4):
  - Losses are cumulative over 1980 to (DB version - 1), in million EUR, CPI-adjusted.
  - Protection gap (our measure) = 1 - insured losses / economic losses.
    Main source: CATDAT (RiskLayer, via EEA; CCS for Spain, NNP for Norway; NCA corrections).
    EM-DAT is used as a robustness check.
  - Aggregates are LOSS-WEIGHTED: 1 - sum(insured) / sum(economic).
  - A cell with zero recorded economic losses has an UNDEFINED gap (EIOPA codes it 100% / score -9;
    we set it to missing).
"""
import sys, os, hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import statsmodels.formula.api as smf

RAW = sys.argv[1] if len(sys.argv) > 1 else \
    "raw/EIOPA-BoS-24-474_PowerBI input dashboard on insurance protectiongap.xlsx"
OUT = sys.argv[2] if len(sys.argv) > 2 else "output"
os.makedirs(OUT, exist_ok=True)
# Traceability: the exact file we downloaded (4 Dec 2025 version, accessed 12 Oct 2026)
RAW_SHA256 = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "SHA256.txt")).read().split()[0] \
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "SHA256.txt")) else None
sha = hashlib.sha256(open(RAW, "rb").read()).hexdigest()
if RAW_SHA256 and sha != RAW_SHA256:
    sys.exit(f"Raw file differs from the one used in the paper (SHA-256 {sha} != {RAW_SHA256}).")
NUMBERS = []          # every number quoted in the paper, with the output it comes from
def record(name, value, source):
    NUMBERS.append({"quantity": name, "value": value, "output_file": source})
MAIN_VERSION = 2025
SOURCE_NOTE = ("Source: EIOPA, Dashboard on insurance protection gap for natural catastrophes, "
               "input data (Dec. 2025), CATDAT losses 1980-2024, CPI-adjusted. Own calculations.")

# ---------- style (reference palette, light mode) ----------
SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
PERILS = ["Flood*", "Windstorm", "Earthquake", "Wildfire", "Coastal Flood"]
PCOL = dict(zip(PERILS, CAT))
plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "text.color": INK, "font.size": 9, "axes.titlesize": 11, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
})


def note(fig, text=SOURCE_NOTE, y=0.005):
    fig.text(0.01, y, text, fontsize=7, color=INK2, ha="left", va="bottom", wrap=True)


# ---------- 1. load & clean ----------
raw = pd.read_excel(RAW, sheet_name="Historical and estimated pg")
raw.columns = ["version", "id", "country", "iso", "peril",
               "econ_cd", "ins_cd", "econ_em", "ins_em", "pins_cd", "pins_em",
               "uninsured_pct_eiopa", "hist_score", "norm_cd", "norm_em", "norm",
               "log_norm", "risk_est", "ins_penetration", "est_score", "comment_hist", "comment_est"]
raw = raw.drop(columns=["comment_hist", "comment_est"])
eea_row = raw[raw.country == "EEA"].copy()          # EIOPA's own EEA aggregate (kept for checks)
df = raw[raw.country != "EEA"].copy()                # 30 countries

def gap(ins, econ):
    """1 - ins/econ, missing if econ == 0, floored at 0 when insured > economic."""
    g = np.where(econ > 0, 1 - ins / econ.where(econ > 0), np.nan)
    return np.clip(g, 0, None)

df["gap_cd"] = gap(df.ins_cd, df.econ_cd)
df["gap_em"] = gap(df.ins_em, df.econ_em)
df["insured_gt_economic"] = (df.econ_cd > 0) & (df.ins_cd > df.econ_cd)
df["uninsured_cd"] = (df.econ_cd - df.ins_cd).clip(lower=0)   # million EUR
df["years"] = df.version - 1980                               # 1980..version-1
df.loc[df.uninsured_pct_eiopa.eq(100) & df.econ_cd.eq(0) & df.econ_em.eq(0), "uninsured_pct_eiopa"] = np.nan
df.to_csv(f"{OUT}/clean_data_all_versions.csv", index=False)

d = df[df.version == MAIN_VERSION].copy()

# insurance-scheme sheet: public involvement in primary insurance (residential)
sch = pd.read_excel(RAW, sheet_name="Country insurance scheme")
sch = sch[(sch["DB Version"] == MAIN_VERSION) & (sch.Asset == "Residential")]
sch["peril_key"] = sch.Peril.str.lower()
prim_col = [c for c in sch.columns if c.startswith("national primary insurance scheme")][0]
mand_col = [c for c in sch.columns if c.startswith("mandatory by law")][0]
pen_col = [c for c in sch.columns if c.startswith("estimation of the insurance penetration")][0]
reins_col = [c for c in sch.columns if c.startswith("national reinsurance scheme")][0]
PUBLIC = ["Public", "Private-Public", "State guarantee"]
# public involvement = public or public-private primary insurance OR reinsurance (e.g. France: CCR state reinsurer)
sch["public_scheme"] = (sch[prim_col].isin(PUBLIC) | sch[reins_col].isin(PUBLIC)).astype(int)
sch["mandatory"] = sch[mand_col].eq("Yes").astype(int)
prem_col = [c for c in sch.columns if c.startswith("Risk-based or flat premium")][0]
relief_col = [c for c in sch.columns if c.startswith("systematic mechanism in place")][0]
sch["flat_premium"] = sch[prem_col].eq("Flat").astype(int)
sch = sch.rename(columns={pen_col: "penetration_band", "Country": "country", prem_col: "premium_type",
                          relief_col: "post_disaster_relief", "Deductible": "deductible_pct",
                          "Limit": "insurer_amount_pct", "reste": "policyholder_excess_pct"})
d["peril_key"] = d.peril.str.lower()
d = d.merge(sch[["country", "peril_key", "public_scheme", "mandatory", "flat_premium", "premium_type",
                 "post_disaster_relief", "penetration_band", "deductible_pct", "insurer_amount_pct",
                 "policyholder_excess_pct", prim_col]],
            on=["country", "peril_key"], how="left")
d = d.rename(columns={prim_col: "primary_scheme"})
# uninsured losses relative to the economy: average annual economic losses / GDP (per mille, EIOPA) x gap
d["uninsured_per_mil_gdp"] = d.norm_cd * d.gap_cd.fillna(0)
d.to_csv(f"{OUT}/clean_data_2025.csv", index=False)

# ---------- 2. aggregates ----------
def agg(g, e, i):
    return g.agg(econ=(e, "sum"), ins=(i, "sum")).assign(gap=lambda t: 1 - t.ins / t.econ)

by_peril = agg(d.groupby("peril"), "econ_cd", "ins_cd")
by_peril_em = agg(d.groupby("peril"), "econ_em", "ins_em")
by_peril["gap_em"] = by_peril_em.gap
by_peril["n_countries_with_losses"] = d[d.econ_cd > 0].groupby("peril").size()
by_peril["median_country_gap"] = d.groupby("peril").gap_cd.median()
by_peril["uninsured"] = by_peril.econ - by_peril.ins
by_peril["share_of_all_uninsured"] = by_peril.uninsured / by_peril.uninsured.sum()
by_peril["annual_econ_mEUR"] = by_peril.econ / (MAIN_VERSION - 1980)
by_peril = by_peril.loc[PERILS]
total = d[["econ_cd", "ins_cd"]].sum()
total_gap = 1 - total.ins_cd / total.econ_cd

by_country = agg(d.groupby("country"), "econ_cd", "ins_cd")
by_country["uninsured"] = by_country.econ - by_country.ins
by_country["annual_loss_per_mil_gdp"] = d.groupby("country").norm_cd.sum()
by_country["n_perils_with_losses"] = d[d.econ_cd > 0].groupby("country").size()
by_country["share_of_eea_uninsured"] = by_country.uninsured / by_country.uninsured.sum()
by_country["uninsured_per_mil_gdp"] = d.groupby("country").uninsured_per_mil_gdp.sum()
flood_regime = d[d.peril == "Flood*"].set_index("country")[["public_scheme", "primary_scheme"]]
by_country = by_country.join(flood_regime)
by_country = by_country.sort_values("gap", ascending=False)

# Summary-statistics table (Table 1)
cells = d[d.econ_cd > 0]
t1 = pd.DataFrame({
    "Countries with losses": cells.groupby("peril").size(),
    "Economic losses (EUR bn)": cells.groupby("peril").econ_cd.sum() / 1e3,
    "Insured losses (EUR bn)": cells.groupby("peril").ins_cd.sum() / 1e3,
    "Gap, loss-weighted (%)": 100 * by_peril.gap,
    "Gap, EM-DAT (%)": 100 * by_peril.gap_em,
    "Country gap: mean (%)": 100 * cells.groupby("peril").gap_cd.mean(),
    "Country gap: s.d. (pp)": 100 * cells.groupby("peril").gap_cd.std(),
    "Country gap: min (%)": 100 * cells.groupby("peril").gap_cd.min(),
    "Country gap: median (%)": 100 * cells.groupby("peril").gap_cd.median(),
    "Country gap: max (%)": 100 * cells.groupby("peril").gap_cd.max(),
}).loc[PERILS]
t1.loc["All perils"] = [
    cells.country.nunique(), cells.econ_cd.sum() / 1e3, cells.ins_cd.sum() / 1e3,
    100 * total_gap,
    100 * (1 - d.ins_em.sum() / d.econ_em.sum()),
    100 * cells.gap_cd.mean(), 100 * cells.gap_cd.std(), 100 * cells.gap_cd.min(),
    100 * cells.gap_cd.median(), 100 * cells.gap_cd.max()]
clim = cells[cells.peril != "Earthquake"]; clim_all = d[d.peril != "Earthquake"]
t1.loc["Climate-related perils (excl. earthquake)"] = [
    clim.country.nunique(), clim.econ_cd.sum() / 1e3, clim.ins_cd.sum() / 1e3,
    100 * (1 - clim.ins_cd.sum() / clim.econ_cd.sum()),
    100 * (1 - clim_all.ins_em.sum() / clim_all.econ_em.sum()),
    100 * clim.gap_cd.mean(), 100 * clim.gap_cd.std(), 100 * clim.gap_cd.min(),
    100 * clim.gap_cd.median(), 100 * clim.gap_cd.max()]
t1.round(1).to_csv(f"{OUT}/table1_summary_by_peril.csv")

t2 = by_country[["econ", "ins", "uninsured", "gap", "share_of_eea_uninsured",
                 "annual_loss_per_mil_gdp", "uninsured_per_mil_gdp", "n_perils_with_losses", "primary_scheme"]].copy()
t2[["econ", "ins", "uninsured"]] /= 1e3
t2["gap"] *= 100; t2["share_of_eea_uninsured"] *= 100
t2.columns = ["Economic (EUR bn)", "Insured (EUR bn)", "Uninsured (EUR bn)", "Gap (%)",
              "Share of EEA uninsured (%)", "Annual econ. losses / GDP (per mille)",
              "Annual uninsured losses / GDP (per mille)", "Perils with losses", "Flood* primary scheme"]
t2.round(2).to_csv(f"{OUT}/table2_by_country.csv")

# Source comparison (CATDAT vs EM-DAT) for the largest cells
src = d[(d.econ_cd > 0) | (d.econ_em > 0)][["country", "peril", "econ_cd", "econ_em", "ins_cd", "ins_em", "gap_cd", "gap_em"]]
src["econ_ratio_em_cd"] = src.econ_em / src.econ_cd.replace(0, np.nan)
src.sort_values("econ_cd", ascending=False).round(3).to_csv(f"{OUT}/table3_catdat_vs_emdat.csv", index=False)

# Vintage comparison (cumulative windows)
vint = (df.groupby(["version", "peril"])[["econ_cd", "ins_cd"]].sum()
          .assign(gap=lambda t: 1 - t.ins_cd / t.econ_cd).reset_index())
vint.round(4).to_csv(f"{OUT}/table4_vintages.csv", index=False)

# EIOPA EEA row vs our sum of countries (consistency check)
chk = (eea_row[eea_row.version == MAIN_VERSION].set_index("peril")[["econ_cd", "ins_cd"]]
       .join(d.groupby("peril")[["econ_cd", "ins_cd"]].sum(), rsuffix="_sum_countries"))
chk.round(1).to_csv(f"{OUT}/check_eea_row_vs_country_sum.csv")

# Re-pricing between vintages: each version re-expresses ALL past losses at a newer price level.
# The common factor is the modal cell-level ratio of economic losses between consecutive versions.
piv = df.pivot_table(index=["country", "peril"], columns="version", values="econ_cd")
rows = []
vers = sorted(df.version.unique())
tot = df.groupby("version")[["econ_cd", "ins_cd"]].sum()
for a, b in zip(vers[:-1], vers[1:]):
    ok = piv[(piv[a] > 0) & (piv[b] > 0)]
    ratio = (ok[b] / ok[a]).round(4)
    f = ratio.mode().iloc[0]
    rows.append({"from": a, "to": b, "repricing_factor": f, "share_cells_exactly_repriced": (ratio == f).mean(),
                 "econ_change_bn": (tot.loc[b, "econ_cd"] - tot.loc[a, "econ_cd"]) / 1e3,
                 "econ_repricing_bn": tot.loc[a, "econ_cd"] * (f - 1) / 1e3,
                 "econ_new_or_revised_bn": (tot.loc[b, "econ_cd"] - f * tot.loc[a, "econ_cd"]) / 1e3,
                 "ins_change_bn": (tot.loc[b, "ins_cd"] - tot.loc[a, "ins_cd"]) / 1e3,
                 "ins_repricing_bn": tot.loc[a, "ins_cd"] * (f - 1) / 1e3,
                 "ins_new_or_revised_bn": (tot.loc[b, "ins_cd"] - f * tot.loc[a, "ins_cd"]) / 1e3})
reprice = pd.DataFrame(rows)
reprice.round(4).to_csv(f"{OUT}/table8_repricing_between_versions.csv", index=False)

# Gap by insurance-system feature (residential scheme sheet, 2025) and by EIOPA's modelled penetration score
def gap_by(col, data):
    g = data.groupby(data[col].fillna("not reported"))
    return pd.DataFrame({"cells": g.size(), "countries": g.country.nunique(),
                         "gap_loss_weighted_pct": 100 * (1 - g.ins_cd.sum() / g.econ_cd.sum()),
                         "gap_median_cell_pct": 100 * g.gap_cd.median()})
feat = []
cells2 = d[d.econ_cd > 0].copy()
cells2["mandatory_lbl"] = cells2.mandatory.map({1: "Yes", 0: "No"})
cells2["pen_score_lbl"] = cells2.ins_penetration.map({1: "1: 75-100% insured", 2: "2: 50-75%", 3: "3: 25-50%", 4: "4: 0-25%"})
for col, name in [("pen_score_lbl", "EIOPA modelled penetration score"), ("mandatory_lbl", "Cover mandatory by law"),
                  ("premium_type", "Premium type"), ("post_disaster_relief", "Post-disaster state relief")]:
    t = gap_by(col, cells2); t.insert(0, "feature", name); feat.append(t)
feat = pd.concat(feat)
feat.round(1).to_csv(f"{OUT}/table5_gap_by_scheme_feature.csv")
pen_corr = cells2[["ins_penetration", "gap_cd"]].corr("spearman").iloc[0, 1]

# Insurance limits: maximum share of the sum insured an insurer pays (residential), by peril
lim = sch[sch.insurer_amount_pct > 0]
limits = lim.groupby("Peril")[["deductible_pct", "insurer_amount_pct", "policyholder_excess_pct"]].median()
limits["countries_with_data"] = lim.groupby("Peril").size()
limits.round(1).to_csv(f"{OUT}/table6_policy_limits_by_peril.csv")
low_limits = lim[lim.insurer_amount_pct < 60][["country", "Peril", "deductible_pct", "insurer_amount_pct", "policyholder_excess_pct"]]
low_limits.to_csv(f"{OUT}/table6b_low_insurer_limits.csv", index=False)
relief_mode = sch.groupby("country").post_disaster_relief.agg(lambda x: x.dropna().mode().iloc[0] if x.dropna().size else "not reported")

# Modelled risk without recorded losses ("hidden" gap the historical view cannot see)
hidden = d[(d.risk_est >= 2) & (d.econ_cd == 0)][["country", "peril", "risk_est", "ins_penetration"]]
hidden.to_csv(f"{OUT}/table7_modelled_risk_without_recorded_losses.csv", index=False)

# ---------- 3. econometrics ----------
reg = d[(d.econ_cd > 0)].copy()
reg["gap_pp"] = 100 * reg.gap_cd
reg["log10_loss_intensity"] = np.log10(reg.norm_cd)       # annual econ. losses / GDP, per mille
reg = reg.dropna(subset=["gap_pp", "log10_loss_intensity", "public_scheme"])
m1 = smf.ols("gap_pp ~ log10_loss_intensity + C(peril)", data=reg).fit(
    cov_type="cluster", cov_kwds={"groups": reg.country.astype("category").cat.codes})
m2 = smf.ols("gap_pp ~ log10_loss_intensity + public_scheme + C(peril)", data=reg).fit(
    cov_type="cluster", cov_kwds={"groups": reg.country.astype("category").cat.codes})
with open(f"{OUT}/regression.txt", "w") as f:
    f.write("Cross-section of country x peril cells with recorded economic losses (CATDAT, 1980-2024)\n")
    f.write("Dependent variable: protection gap in percentage points (0-100)\n")
    f.write("Standard errors clustered by country\n\n")
    f.write(f"Observations: {int(m2.nobs)}  Countries: {reg.country.nunique()}\n\n")
    f.write("MODEL 1: gap = a_peril + b*log10(annual losses/GDP, per mille)\n")
    f.write(str(m1.summary()) + "\n\n")
    f.write("MODEL 2: gap = a_peril + b*log10(annual losses/GDP) + c*public_or_PPP_insurance_or_reinsurance\n")
    f.write(f"Cells with public involvement: {int(reg.public_scheme.sum())} of {len(reg)}\n")
    f.write(str(m2.summary()) + "\n")
coef = pd.DataFrame({
    "M1 coef": m1.params, "M1 se": m1.bse, "M2 coef": m2.params, "M2 se": m2.bse})
coef.round(2).to_csv(f"{OUT}/regression_coefficients.csv")

# Robustness of Model 2. The regime variables (2025 scheme sheet) are attached to every version.
regime = d.set_index(["country", "peril"])[["public_scheme", "mandatory", "flat_premium"]]

def build(version, src="cd"):
    x = df[df.version == version].copy()
    x = x.join(regime, on=["country", "peril"])
    e, i, n = f"econ_{src}", f"ins_{src}", f"norm_{src}"
    x = x[x[e] > 0].copy()
    x["gap_pp"] = 100 * np.clip(1 - x[i] / x[e], 0, None)
    x["log10_loss_intensity"] = np.log10(x[n])
    return x[np.isfinite(x.log10_loss_intensity)].dropna(subset=["public_scheme"])

def est(x, formula="gap_pp ~ log10_loss_intensity + public_scheme + C(peril)", var="public_scheme", weights=None):
    grp = x.country.astype("category").cat.codes
    mod = smf.wls(formula, x, weights=weights) if weights is not None else smf.ols(formula, x)
    m = mod.fit(cov_type="cluster", cov_kwds={"groups": grp})
    return m.params[var], m.bse[var], m.pvalues[var], int(m.nobs), x.country.nunique()

base = build(MAIN_VERSION)
specs = [
    ("Baseline: 2025 version, CATDAT", base, {}),
    ("2024 version (before the 2025 corrections)", build(2024), {}),
    ("2022 version", build(2022), {}),
    ("EM-DAT losses instead of CATDAT", build(MAIN_VERSION, "em"), {}),
    ("Without France", base[base.country != "France"], {}),
    ("Without France and Spain", base[~base.country.isin(["France", "Spain"])], {}),
    ("Only cells with losses of EUR 100m or more", base[base.econ_cd >= 100], {}),
    ("Cells weighted by economic losses", base, {"weights": base.econ_cd}),
    ("Risk measured by EIOPA modelled risk score (0-4)", base, {"formula": "gap_pp ~ risk_est + public_scheme + C(peril)"}),
    ("Regime = cover mandatory by law", base, {"formula": "gap_pp ~ log10_loss_intensity + mandatory + C(peril)", "var": "mandatory"}),
    ("Regime = cover mandatory by law, without Romania", base[base.country != "Romania"],
     {"formula": "gap_pp ~ log10_loss_intensity + mandatory + C(peril)", "var": "mandatory"}),
    ("Regime = flat (not risk-based) premium", base, {"formula": "gap_pp ~ log10_loss_intensity + flat_premium + C(peril)", "var": "flat_premium"}),
]
rob = pd.DataFrame([(name, *est(x, **kw)) for name, x, kw in specs],
                   columns=["specification", "coef_pp", "se", "p_value", "cells", "countries"])

# All three regime features together (they overlap: correlations 0.3-0.5 across cells)
regime_corr = base[["public_scheme", "mandatory", "flat_premium"]].corr()
regime_corr.round(2).to_csv(f"{OUT}/regime_feature_correlations.csv")
grp = base.country.astype("category").cat.codes
mj = smf.ols("gap_pp ~ log10_loss_intensity + public_scheme + mandatory + flat_premium + C(peril)", base).fit(
    cov_type="cluster", cov_kwds={"groups": grp})
joint = [(f"All three regime dummies together: {v}", mj.params[v], mj.bse[v], mj.pvalues[v], int(mj.nobs),
          base.country.nunique()) for v in ["public_scheme", "mandatory", "flat_premium"]]

# Fractional logit (Papke-Wooldridge): the gap is a share bounded by 0 and 1, 30% of cells sit at 1.
# Average marginal effect of public involvement, with a country-cluster bootstrap SE (500 draws).
import statsmodels.api as sm
def frac_ame(x):
    f = smf.glm("share ~ log10_loss_intensity + public_scheme + C(peril)", x.assign(share=x.gap_pp / 100),
                family=sm.families.Binomial()).fit()
    return 100 * (f.predict(x.assign(public_scheme=1)) - f.predict(x.assign(public_scheme=0))).mean(), f
ame, ffit = frac_ame(base)
rng_b = np.random.default_rng(7); boots = []
countries_b = base.country.unique()
for _ in range(500):
    pick = rng_b.choice(countries_b, len(countries_b), replace=True)
    bb = pd.concat([base[base.country == c] for c in pick])
    if bb.public_scheme.nunique() > 1 and bb.peril.nunique() == base.peril.nunique():
        boots.append(frac_ame(bb)[0])
ame_se = float(np.std(boots))
frac = [("Fractional logit, average marginal effect", ame, ame_se,
         2 * (1 - __import__("scipy").stats.norm.cdf(abs(ame / ame_se))), len(base), base.country.nunique())]
rob = pd.concat([rob, pd.DataFrame(frac + joint, columns=rob.columns)], ignore_index=True)
share_at_100 = float((base.gap_pp >= 99.5).mean())
# Permutation inference: re-assign the countries' regime patterns across countries 2,000 times
rng = np.random.default_rng(42)
ctry = sorted(base.country.unique())
pattern = d.pivot(index="country", columns="peril", values="public_scheme")
obs = smf.ols("gap_pp ~ log10_loss_intensity + public_scheme + C(peril)", base).fit().params["public_scheme"]
perm = []
for _ in range(2000):
    mp = dict(zip(ctry, rng.permutation(ctry)))
    b = base.copy()
    b["public_scheme"] = [pattern.loc[mp[c], p] for c, p in zip(b.country, b.peril)]
    if b.public_scheme.nunique() > 1:
        perm.append(smf.ols("gap_pp ~ log10_loss_intensity + public_scheme + C(peril)", b).fit().params["public_scheme"])
perm = np.array(perm)
perm_p = float(np.mean(np.abs(perm) >= abs(obs)))
rob.round(3).to_csv(f"{OUT}/regression_robustness.csv", index=False)
with open(f"{OUT}/regression.txt", "a") as f:
    f.write("\nROBUSTNESS OF THE REGIME COEFFICIENT (clustered SE by country)\n" + rob.round(3).to_string(index=False) + "\n")
    f.write(f"\nPermutation test: {len(perm)} random re-assignments of countries' regime patterns; "
            f"two-sided p = {perm_p:.4f} (observed coefficient {obs:.2f})\n")

# ---------- 4. figures ----------
# Fig 1: gap by peril, two sources
fig, ax = plt.subplots(figsize=(7, 3.4))
y = np.arange(len(PERILS))[::-1]
for yi, p in zip(y, PERILS):
    g1, g2 = 100 * by_peril.loc[p, "gap"], 100 * by_peril.loc[p, "gap_em"]
    if not np.isnan(g2):
        ax.plot([g1, g2], [yi, yi], color=GRID, lw=2, zorder=1)
        ax.scatter(g2, yi, s=60, facecolor=SURF, edgecolor=PCOL[p], lw=2, zorder=3)
    ax.scatter(g1, yi, s=70, color=PCOL[p], edgecolor=SURF, lw=1.5, zorder=4)
    ax.text(103, yi, f"{g1:.0f}%  (EUR {by_peril.loc[p,'econ']/1e3:,.0f}bn lost)",
            va="center", fontsize=8, color=INK2)
ax.set_yticks(y, [p.replace("Flood*", "River & pluvial flood") for p in PERILS])
ax.set_xlim(0, 100); ax.set_xlabel("Share of economic losses not insured, 1980-2024 (%)")
ax.scatter([], [], s=60, color=INK2, label="CATDAT (main)")
ax.scatter([], [], s=60, facecolor=SURF, edgecolor=INK2, lw=2, label="EM-DAT (check)")
ax.legend(loc="lower center", bbox_to_anchor=(0.62, 0.0), ncol=1, frameon=False, fontsize=8)
ax.set_title("Fig. 1  Earthquake, wildfire and flood losses are mostly uninsured;\nwindstorm is the best-covered major peril", loc="left")
ax.grid(axis="y", visible=False)
fig.subplots_adjust(left=0.22, right=0.72, bottom=0.25, top=0.82)
note(fig, SOURCE_NOTE + " Gap = 1 - insured/economic, summed over 30 EEA countries (loss-weighted). "
     "EM-DAT has no coastal-flood losses.")
fig.savefig(f"{OUT}/fig1_gap_by_peril.png", dpi=220); plt.close(fig)

# Fig 2: heatmap country x peril
order_c = by_country.sort_values("gap", ascending=False).index.tolist()
H = d.pivot(index="country", columns="peril", values="gap_cd").reindex(index=order_c, columns=PERILS) * 100
L = d.pivot(index="country", columns="peril", values="econ_cd").reindex(index=order_c, columns=PERILS)
Over = d.pivot(index="country", columns="peril", values="insured_gt_economic").reindex(index=order_c, columns=PERILS).fillna(False)
cmap = LinearSegmentedColormap.from_list("seq", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
fig, ax = plt.subplots(figsize=(6.6, 9.2))
im = ax.imshow(H.values, cmap=cmap, vmin=0, vmax=100, aspect="auto")
cb = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=0.025, pad=0.02, aspect=40)
cb.set_label("Uninsured share of economic losses (%)", fontsize=7.5, color=INK2); cb.ax.tick_params(labelsize=7)
cb.outline.set_visible(False)
for i in range(H.shape[0]):
    for j in range(H.shape[1]):
        v = H.values[i, j]
        if np.isnan(v):
            ax.text(j, i, "–", ha="center", va="center", color="#9a9994", fontsize=8)
            ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, color="#f0efec", zorder=0.5))
        else:
            small = L.values[i, j] < 100
            over = bool(Over.values[i, j])
            ax.text(j, i, f"{v:.0f}" + ("†" if small else "") + ("‡" if over else ""), ha="center", va="center", fontsize=7.5,
                    color="white" if v > 55 else INK)
ax.set_xticks(range(len(PERILS)), [p.replace("Flood*", "River/pluvial\nflood").replace("Coastal Flood", "Coastal\nflood") for p in PERILS])
ax.xaxis.tick_top()
ylab = [f"{c}  ({100*by_country.loc[c,'gap']:.0f}%)" for c in order_c]
ax.set_yticks(range(len(order_c)), ylab)
ax.grid(False); [s.set_visible(False) for s in ax.spines.values()]
fig.suptitle("Fig. 2  Uninsured share of economic losses (%), 1980-2024\n"
             "Countries sorted by their all-peril gap (in brackets)", x=0.02, ha="left", fontsize=11, fontweight="bold")
fig.subplots_adjust(left=0.30, right=0.97, top=0.89, bottom=0.135)
note(fig, SOURCE_NOTE + "\n– = no recorded economic loss (gap undefined).  † = cumulative economic loss below EUR 100m: "
     "small totals, so one or a few events drive the figure.\n‡ = recorded insured losses exceed economic losses (data inconsistency); gap set to 0.", y=0.004)
fig.savefig(f"{OUT}/fig2_heatmap_country_peril.png", dpi=220); plt.close(fig)

# Fig 3: who bears it - uninsured losses by country, stacked by peril
U = d.pivot(index="country", columns="peril", values="uninsured_cd").reindex(columns=PERILS) / 1e3
U["total"] = U.sum(axis=1); U = U.sort_values("total", ascending=False)
top = U.head(12).drop(columns="total")
rest = U.iloc[12:].drop(columns="total").sum().rename(f"Other {len(U)-12} countries")
top = pd.concat([top, rest.to_frame().T])[::-1]
G = d.pivot(index="country", columns="peril", values="uninsured_per_mil_gdp").reindex(columns=PERILS)
G["total"] = G.sum(axis=1); G = G.sort_values("total", ascending=False)
gtop = G.head(12).drop(columns="total")
grest = G.iloc[12:].drop(columns="total").mean().rename(f"Other {len(G)-12} (average)")
gtop = pd.concat([gtop, grest.to_frame().T])[::-1]
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9, 4.9), gridspec_kw={"wspace": 0.55})
tot_unins = U.total.sum()
for axis, data, fmt in [(ax, top, "abs"), (ax2, gtop, "gdp")]:
    left = np.zeros(len(data))
    for p in PERILS:
        axis.barh(data.index, data[p], left=left, color=PCOL[p], edgecolor=SURF, linewidth=1.0, height=0.7,
                  label=p.replace("Flood*", "River & pluvial flood"))
        left += data[p].values
    for i, v in enumerate(left):
        lab = f"{v:,.0f} ({100*v/tot_unins:.0f}%)" if fmt == "abs" else f"{v:.1f}"
        axis.text(v + left.max() * 0.02, i, lab, va="center", fontsize=7, color=INK2)
    axis.set_xlim(0, left.max() * 1.3)
    axis.grid(axis="y", visible=False)
    axis.tick_params(axis="y", labelsize=8)
ax.set_xlabel("EUR bn, CPI-adjusted, 1980-2024\n(share of EEA total in brackets)")
ax2.set_xlabel("Per mille of GDP per year, 1980-2024\n(average annual losses x gap)")
ax.set_title("(a) Amount uninsured", loc="left", fontsize=9.5)
ax2.set_title("(b) Uninsured losses relative to GDP", loc="left", fontsize=9.5)
ax.legend(ncol=5, loc="upper center", bbox_to_anchor=(1.25, -0.2), frameon=False, fontsize=7.5)
fig.suptitle(f"Fig. 3  Italy, Germany and Spain carry {100*U.total.head(3).sum()/tot_unins:.0f}% of the EUR "
             f"{tot_unins:,.0f}bn uninsured; relative to GDP,\nthe burden is heaviest in Slovenia, Greece and Italy",
             x=0.01, ha="left", fontsize=11, fontweight="bold")
fig.subplots_adjust(left=0.13, right=0.97, bottom=0.27, top=0.83)
note(fig)
fig.savefig(f"{OUT}/fig3_uninsured_by_country.png", dpi=220); plt.close(fig)

# Fig 4: loss intensity vs gap, country level, by flood regime
bc = by_country.dropna(subset=["gap"]).copy()
bc = bc[bc.annual_loss_per_mil_gdp > 0]
fig, ax = plt.subplots(figsize=(7, 4.6))
for k, (lab, col) in {0: ("Private flood insurance", CAT[0]),
                      1: ("Public or public-private flood insurance or reinsurance", CAT[1])}.items():
    s = bc[bc.public_scheme == k]
    ax.scatter(s.annual_loss_per_mil_gdp, 100 * s.gap, s=55, color=col, edgecolor=SURF, lw=1.5, label=lab, zorder=3)
for c, r in bc.iterrows():
    ax.annotate(d.loc[d.country == c, "iso"].iloc[0], (r.annual_loss_per_mil_gdp, 100 * r.gap),
                xytext=(4, -9) if c == "Portugal" else (4, 3), textcoords="offset points", fontsize=7, color=INK2)
ax.set_xscale("log")
ax.set_xlabel("Loss intensity: average annual economic losses, all perils (per mille of GDP, log scale)")
from matplotlib.ticker import FixedLocator, FixedFormatter
ax.xaxis.set_major_locator(FixedLocator([0.05, 0.1, 0.2, 0.5, 1, 2, 5]))
ax.xaxis.set_major_formatter(FixedFormatter(["0.05", "0.1", "0.2", "0.5", "1", "2", "5"]))
ax.xaxis.set_minor_formatter(FixedFormatter([]))
ax.set_ylabel("Protection gap, all perils (%)")
ax.set_ylim(-3, 103)
ax.legend(loc="lower left", frameon=False, fontsize=8)
ax.set_title("Fig. 4  Countries that lose more relative to GDP are not better insured; the three\n"
             "lowest gaps (FR, DK, IS) are in countries with public involvement in flood cover", loc="left")
fig.subplots_adjust(left=0.1, right=0.97, bottom=0.2, top=0.86)
note(fig, SOURCE_NOTE + " Regime = public or public-private primary insurance or reinsurance for residential "
     "river/pluvial flood (EIOPA country insurance scheme sheet, 2025).")
fig.savefig(f"{OUT}/fig4_loss_intensity_vs_gap.png", dpi=220); plt.close(fig)

# Fig 5: vintages - sensitivity to revisions
fig, ax = plt.subplots(figsize=(7, 3.6))
for p in PERILS:
    s = vint[vint.peril == p]
    ax.plot(s.version, 100 * s.gap, color=PCOL[p], lw=2, marker="o", ms=6, mec=SURF, mew=1.5)
    ax.text(MAIN_VERSION + 0.08, 100 * s.gap.iloc[-1], p.replace("Flood*", "River/pluvial flood"),
            va="center", fontsize=8, color=INK2)
ax.set_xticks([2022, 2023, 2024, 2025], ["2022\n(1980-2021)", "2023\n(1980-2022)", "2024\n(1980-2023)", "2025\n(1980-2024)"])
ax.set_xlim(2021.8, 2025.8); ax.set_ylim(0, 100)
ax.set_ylabel("Protection gap (%)"); ax.set_xlabel("Dashboard version (loss window covered)")
wind_drop = 100 * (vint.query("version == 2024 and peril == 'Windstorm'").gap.iloc[0]
                   - vint.query("version == 2025 and peril == 'Windstorm'").gap.iloc[0])
ax.set_title("Fig. 5  The measured gap moves more with data revisions than with new years:\n"
             f"windstorm drops {wind_drop:.1f} points in 2025 after corrections to past insured losses", loc="left")
fig.subplots_adjust(left=0.1, right=0.8, bottom=0.27, top=0.83)
note(fig, "Source: EIOPA dashboard input data, versions 2022-2025, CATDAT. Each point is a cumulative window, not a single year; "
     "each version also re-prices all past losses (x" + ", x".join(f"{f:.3f}" for f in reprice.repricing_factor) + ").")
fig.savefig(f"{OUT}/fig5_vintages.png", dpi=220); plt.close(fig)

# ---------- 5. every number quoted in the paper, traced to its output ----------
record("Economic losses 1980-2024, EUR bn", total.econ_cd / 1e3, "table1_summary_by_peril.csv")
record("Insured losses 1980-2024, EUR bn", total.ins_cd / 1e3, "table1_summary_by_peril.csv")
record("Protection gap, all perils, %", 100 * total_gap, "table1_summary_by_peril.csv")
record("Uninsured losses, EUR bn", (total.econ_cd - total.ins_cd) / 1e3, "table1_summary_by_peril.csv")
for p in PERILS:
    record(f"Gap {p}, CATDAT, %", 100 * by_peril.loc[p, "gap"], "table1_summary_by_peril.csv")
    record(f"Gap {p}, EM-DAT, %", 100 * by_peril.loc[p, "gap_em"], "table1_summary_by_peril.csv")
    record(f"Share of all uninsured losses, {p}, %", 100 * by_peril.loc[p, "share_of_all_uninsured"], "table1_summary_by_peril.csv")
record("Gap, climate-related perils (excl. earthquake), %", t1.loc["Climate-related perils (excl. earthquake)", "Gap, loss-weighted (%)"], "table1_summary_by_peril.csv")
record("Median cell gap, %", 100 * cells.gap_cd.median(), "table1_summary_by_peril.csv")
record("Share of uninsured losses held by Italy+Germany+Spain, %", 100 * U.total.head(3).sum() / U.total.sum(), "table2_by_country.csv")
top5 = d.nlargest(5, "uninsured_cd").uninsured_cd.sum() / d.uninsured_cd.sum()
record("Share of uninsured losses in the 5 largest cells, %", 100 * top5, "clean_data_2025.csv")
for c in ["Slovenia", "Greece", "Italy", "Germany", "France"]:
    record(f"Uninsured losses per year, {c}, per mille of GDP", by_country.loc[c, "uninsured_per_mil_gdp"], "table2_by_country.csv")
record("Re-pricing between 2022 and 2025 versions, EUR bn", reprice.econ_repricing_bn.sum(), "table8_repricing_between_versions.csv")
record("New or revised economic losses 2022->2025 versions, EUR bn", reprice.econ_new_or_revised_bn.sum(), "table8_repricing_between_versions.csv")
record("Windstorm gap drop, 2024->2025 version, points", wind_drop, "table4_vintages.csv")
frg = df[df.country == "France"].groupby("version")[["econ_cd", "ins_cd"]].sum()
for v in [2024, 2025]:
    record(f"France all-peril gap, {v} version, %", 100 * (1 - frg.loc[v, "ins_cd"] / frg.loc[v, "econ_cd"]), "clean_data_all_versions.csv")
record("Spearman correlation, EIOPA penetration score vs gap", pen_corr, "table5_gap_by_scheme_feature.csv")
record("Model 2: public involvement coefficient, pp", m2.params["public_scheme"], "regression.txt")
record("Model 2: public involvement SE", m2.bse["public_scheme"], "regression.txt")
record("Model 2: loss intensity coefficient, pp per tenfold", m2.params["log10_loss_intensity"], "regression.txt")
record("Model 2: loss intensity SE", m2.bse["log10_loss_intensity"], "regression.txt")
record("Model 1 R2", m1.rsquared, "regression.txt"); record("Model 2 R2", m2.rsquared, "regression.txt")
record("Permutation test p-value", perm_p, "regression.txt")
record("Fractional logit AME of public involvement, pp", ame, "regression_robustness.csv")
record("Share of cells with a 100% gap", 100 * share_at_100, "regression_robustness.csv")
pd.DataFrame(NUMBERS).assign(value=lambda t: t.value.round(4)).to_csv(f"{OUT}/paper_numbers.csv", index=False)
with open(f"{OUT}/regression.txt", "a") as f:
    f.write(f"\nFractional logit AME of public involvement: {ame:.2f} pp (cluster-bootstrap SE {ame_se:.2f}, {len(boots)} draws)\n")
    f.write("Regime features correlation:\n" + regime_corr.round(2).to_string() + "\n")
    f.write(f"Raw file SHA-256: {sha}\n")

# ---------- 5. console summary ----------
print(f"All perils, 1980-2024: economic EUR {total.econ_cd/1e3:,.0f}bn, insured EUR {total.ins_cd/1e3:,.0f}bn, gap {100*total_gap:.1f}%")
print(t1.round(1).to_string())
print(t2.round(1).to_string())
print(coef.round(2).to_string())
print("insured>economic cells:", d[d.insured_gt_economic][["country", "peril", "econ_cd", "ins_cd"]].to_string())
print(chk.round(0).to_string())
print(vint.pivot(index="version", columns="peril", values="gap").round(3).to_string())
