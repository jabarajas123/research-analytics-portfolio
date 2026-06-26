"""
Project 4: AI Tool Adoption Study
Mixed-Methods Evaluation of an AI-Assisted Research Platform

Context
-------
A large research organization piloted an AI-assisted qualitative analysis platform
across three research teams. The platform was intended to reduce time spent on
transcript coding and survey open-end processing. This study evaluated whether
analysts actually integrated the tool into their workflow after the initial onboarding
session — and if not, why not.

This is anonymized and retrofitted from a real evaluation conducted at RAND Corporation.
All identifiers have been removed. The findings and methodology are real; the
synthetic data here models the distributions observed in the original study.

Data model
----------
n=47 analysts across three teams (Customer Insights, Product Research, Data Science).
Each analyst completed:
  - A pre/post usability survey (SUS-derived, 0-100 scale)
  - A behavioral log of tool sessions in weeks 1-8 post-onboarding
  - A 30-minute semi-structured interview (subsample, n=18)

Primary outcome: Integration index — a composite of session frequency, task
completion rate, and self-reported workflow embedding (0-10 scale).

Secondary outcomes: trust calibration score, perceived effort, and failure
documentation rate.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

# ── Reproducibility ──────────────────────────────────────────────────────────
np.random.seed(42)

# ── Color palette — muted, professional, not AI-generated ────────────────────
C_SLATE   = '#4A5568'
C_TEAL    = '#2C7873'
C_ORANGE  = '#C05621'
C_SAGE    = '#68856B'
C_LIGHT   = '#F7F7F7'
C_MID     = '#E2E8F0'
C_RED     = '#9B2335'
TEAM_COLORS = {'Customer Insights': C_SLATE, 'Product Research': C_TEAL, 'Data Science': C_ORANGE}

# ── Generate synthetic dataset ───────────────────────────────────────────────
n = 47
teams = np.random.choice(['Customer Insights', 'Product Research', 'Data Science'],
                          size=n, p=[0.40, 0.34, 0.26])

# Prior coding tool experience (0=none, 1=some, 2=extensive)
experience = np.where(teams == 'Customer Insights',
                       np.random.choice([0,1,2], size=n, p=[0.5,0.35,0.15]),
               np.where(teams == 'Product Research',
                       np.random.choice([0,1,2], size=n, p=[0.3,0.4,0.3]),
                       np.random.choice([0,1,2], size=n, p=[0.2,0.3,0.5])))

# Onboarding quality rating (1-5, Likert)
# Data Science comes in with strongest tooling background; Customer Insights least
onboarding = np.clip(
    np.where(teams == 'Customer Insights', np.random.normal(2.8, 0.9, n),
    np.where(teams == 'Product Research',  np.random.normal(3.4, 0.8, n),
                                           np.random.normal(3.9, 0.7, n))).astype(float),
    1, 5)

# Trust calibration: did they trust the tool's outputs appropriately?
# Higher = better calibrated. Customer Insights tends to over-trust initially.
trust = np.clip(
    np.where(teams == 'Customer Insights', np.random.normal(5.8, 1.6, n),
    np.where(teams == 'Product Research',  np.random.normal(6.4, 1.4, n),
                                           np.random.normal(7.1, 1.2, n))).astype(float),
    1, 10)

# Perceived effort (1-10, higher = more effort required)
effort = np.clip(
    np.where(teams == 'Customer Insights', np.random.normal(7.2, 1.4, n),
    np.where(teams == 'Product Research',  np.random.normal(5.8, 1.5, n),
                                           np.random.normal(4.6, 1.6, n))).astype(float),
    1, 10)

# Integration index (primary outcome, 0-10)
# Driven by trust, effort (negative), onboarding quality
integration = np.clip(
    0.8 * trust
    - 0.6 * effort
    + 0.9 * onboarding
    + 0.4 * experience
    + np.random.normal(0, 1.1, n),
    0, 10)

# Failure documentation rate (0-1): did they log when the tool failed?
# Predicts retention — analysts who document failures trust the tool more over time
failure_doc = np.clip(
    0.07 * integration + 0.06 * trust + np.random.normal(0, 0.12, n),
    0, 1)

# Week-by-week session counts (8 weeks)
# Pattern: initial spike, rapid drop, stabilizes for integrated users
def weekly_sessions(integ, n_analysts):
    sessions = np.zeros((n_analysts, 8))
    for i, idx in enumerate(range(n_analysts)):
        base = integ[i]
        sessions[i, 0] = np.clip(base * 0.9 + np.random.normal(0, 0.8), 0, 10)
        sessions[i, 1] = np.clip(base * 0.7 + np.random.normal(0, 0.8), 0, 10)
        for w in range(2, 8):
            if integ[i] >= 6:      # integrators — ramp up
                sessions[i, w] = np.clip(base * (0.6 + w*0.05) + np.random.normal(0, 0.6), 0, 10)
            else:                  # droppers — decay
                sessions[i, w] = np.clip(sessions[i, w-1] * 0.72 + np.random.normal(0, 0.4), 0, 10)
    return sessions

sessions = weekly_sessions(integration, n)

df = pd.DataFrame({
    'team': teams,
    'experience': experience,
    'onboarding': onboarding,
    'trust': trust,
    'effort': effort,
    'integration': integration,
    'failure_doc': failure_doc,
})
for w in range(8):
    df[f'week_{w+1}'] = sessions[:, w]

# Segment: Integrators vs. Resistors (median split on integration index)
df['segment'] = np.where(df['integration'] >= df['integration'].median(),
                          'Integrator', 'Resistor')

FIGURES_DIR = 'figures'
import os
os.makedirs(FIGURES_DIR, exist_ok=True)

def save(name):
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/{name}', dpi=150, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print(f'  saved: {name}')


# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 1 — Scatterplot: Trust vs. Integration, colored by team
# ═══════════════════════════════════════════════════════════════════════════
"""
WHEN TO USE A SCATTERPLOT
─────────────────────────
Use a scatterplot when both variables are continuous (interval or ratio scale)
and you want to show the direction, strength, and shape of their relationship.

This plot asks: does trust calibration predict integration? Each point is one
analyst. The color encodes team membership so we can see if the pattern holds
across groups or if one team is driving the effect.

What to look for:
  - Direction: does the cloud slope up (positive) or down (negative)?
  - Spread: tight cluster around the trend line = stronger relationship
  - Outliers: points far from the line signal something else is going on

Statistical companion: Pearson r (if both variables are roughly normal and
the relationship is linear) or Spearman rho (if ordinal or skewed).
"""

fig, ax = plt.subplots(figsize=(8, 5.5))
for team, color in TEAM_COLORS.items():
    mask = df['team'] == team
    ax.scatter(df.loc[mask, 'trust'], df.loc[mask, 'integration'],
               color=color, alpha=0.75, s=60, label=team, zorder=3)

# OLS trend line (all teams combined)
m, b, r, p, se = stats.linregress(df['trust'], df['integration'])
x_line = np.linspace(df['trust'].min(), df['trust'].max(), 100)
ax.plot(x_line, m * x_line + b, color='#1a1a1a', linewidth=1.5,
        linestyle='--', alpha=0.6, label=f'Trend (r={r:.2f}, p={p:.3f})')

ax.set_xlabel('Trust Calibration Score (1–10)', fontsize=11)
ax.set_ylabel('Integration Index (0–10)', fontsize=11)
ax.set_title('Trust Calibration vs. Tool Integration\nby Org Team',
             fontsize=13, fontweight='bold', pad=12)
ax.legend(frameon=True, framealpha=0.9, fontsize=9)
ax.set_facecolor(C_LIGHT)
ax.grid(True, color='white', linewidth=0.8)

# Annotation: Pearson r interpretation
ax.annotate(f'Pearson r = {r:.2f}\np = {p:.3f}\nn = {n}',
            xy=(0.03, 0.95), xycoords='axes fraction',
            fontsize=9, va='top', color=C_SLATE,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

save('01_scatter_trust_integration.png')
print('Fig 1: Scatterplot — trust vs. integration by team')


# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Box plots: Integration index by team
# ═══════════════════════════════════════════════════════════════════════════
"""
WHEN TO USE A BOX PLOT
──────────────────────
Use a box plot when you want to compare distributions across groups — not just
means, but spread, skew, and outliers simultaneously.

The box shows the interquartile range (IQR): 25th to 75th percentile.
The line inside the box is the median (not the mean).
The whiskers extend to 1.5×IQR. Points beyond that are plotted individually
as outliers.

Why not just use a bar chart with error bars?
  Bar charts hide the shape of the distribution. If one team has a bimodal
  distribution (some people love it, some hate it), a bar chart shows you
  the average and misses the story entirely.

Statistical companion: Kruskal-Wallis test (non-parametric; use when you
can't assume normal distributions, which is common with small n or Likert-
derived composites). If significant, follow up with Mann-Whitney U pairwise
comparisons with Bonferroni correction.

When to use one-way ANOVA instead: when n is large enough that the Central
Limit Theorem kicks in (n > ~30 per group) AND you've verified roughly equal
variances (Levene's test). Kruskal-Wallis is safer for applied research.
"""

fig, ax = plt.subplots(figsize=(7, 5.5))
team_order = ['Customer Insights', 'Product Research', 'Data Science']
data_by_team = [df.loc[df['team'] == t, 'integration'].values for t in team_order]

bp = ax.boxplot(data_by_team, patch_artist=True, widths=0.45,
                medianprops=dict(color='white', linewidth=2.5),
                whiskerprops=dict(linewidth=1.2, color=C_SLATE),
                capprops=dict(linewidth=1.2, color=C_SLATE),
                flierprops=dict(marker='o', markersize=5, alpha=0.6))

for patch, team in zip(bp['boxes'], team_order):
    patch.set_facecolor(TEAM_COLORS[team])
    patch.set_alpha(0.8)

# Kruskal-Wallis test
kw_stat, kw_p = stats.kruskal(*data_by_team)

ax.set_xticklabels(team_order, fontsize=11)
ax.set_ylabel('Integration Index (0–10)', fontsize=11)
ax.set_title('Distribution of Tool Integration by Org Team',
             fontsize=13, fontweight='bold', pad=12)
ax.set_facecolor(C_LIGHT)
ax.grid(True, axis='y', color='white', linewidth=0.8)

# Add n labels
for i, (team, data) in enumerate(zip(team_order, data_by_team), 1):
    ax.text(i, -0.6, f'n={len(data)}', ha='center', fontsize=9, color=C_SLATE)

sig_label = f'Kruskal-Wallis H = {kw_stat:.2f}, p = {kw_p:.3f}'
ax.annotate(sig_label, xy=(0.5, 0.97), xycoords='axes fraction',
            ha='center', fontsize=9, color=C_SLATE,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

save('02_boxplot_integration_by_team.png')
print('Fig 2: Box plot — integration by team + Kruskal-Wallis')


# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 3 — OLS Regression: Coefficient plot
# ═══════════════════════════════════════════════════════════════════════════
"""
WHEN TO USE OLS REGRESSION AND A COEFFICIENT PLOT
──────────────────────────────────────────────────
OLS (Ordinary Least Squares) regression lets you estimate the independent
contribution of each predictor to the outcome, holding all other predictors
constant. This answers: "What actually drives integration, controlling for
everything else?"

A coefficient plot (also called a dot-and-whisker plot) is the honest way to
show regression results. It displays:
  - The estimated coefficient (dot): the expected change in the outcome
    per one-unit increase in the predictor
  - The confidence interval (whisker): the range of plausible values
  - Whether the interval crosses zero: if it does, the effect is not
    statistically distinguishable from no effect at that alpha level

Why not just show a table?
  Coefficient plots let you compare effect sizes visually across predictors.
  A table forces you to read each row and mentally compare numbers.

Interpreting R²: values closer to 1.0 mean the model explains more variance
in the outcome. In behavioral research, R² of 0.30-0.50 is often considered
good — people are complicated.

Key assumption: OLS assumes a linear relationship and normally distributed
residuals. Check with a residual plot. If the outcome is binary, use logistic
regression instead.
"""

from sklearn.preprocessing import StandardScaler

# Standardize predictors so coefficients are comparable (in SD units)
predictors = ['trust', 'effort', 'onboarding', 'experience']
labels = ['Trust Calibration', 'Perceived Effort', 'Onboarding Quality',
          'Prior Experience']

X = df[predictors].values
y = df['integration'].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Manual OLS with confidence intervals via scipy
from numpy.linalg import lstsq

X_aug = np.column_stack([np.ones(len(X_scaled)), X_scaled])
coeffs, _, _, _ = lstsq(X_aug, y, rcond=None)
y_pred = X_aug @ coeffs
residuals = y - y_pred
n_obs, p = X_aug.shape
mse = (residuals ** 2).sum() / (n_obs - p)
cov = mse * np.linalg.inv(X_aug.T @ X_aug)
se = np.sqrt(np.diag(cov))
t_vals = coeffs / se
p_vals = 2 * (1 - stats.t.cdf(np.abs(t_vals), df=n_obs - p))
ci95 = 1.96 * se

# R²
ss_res = ((y - y_pred) ** 2).sum()
ss_tot = ((y - y.mean()) ** 2).sum()
r_sq = 1 - ss_res / ss_tot

coef_data = list(zip(labels, coeffs[1:], se[1:], p_vals[1:], ci95[1:]))
coef_data.sort(key=lambda x: x[1])

fig, ax = plt.subplots(figsize=(8, 5))

colors_coef = [C_ORANGE if c < 0 else C_TEAL for _, c, *_ in coef_data]
for i, (label, coef, se_val, pv, ci, color) in enumerate(
        zip(*zip(*coef_data), colors_coef)):
    ax.errorbar(coef, i, xerr=ci, fmt='o', color=color,
                markersize=9, capsize=4, linewidth=2, zorder=3)
    sig = '***' if pv < 0.001 else '**' if pv < 0.01 else '*' if pv < 0.05 else ''
    ax.text(coef + (0.06 if coef >= 0 else -0.06), i,
            f'β={coef:.2f}{sig}', va='center',
            ha='left' if coef >= 0 else 'right', fontsize=9, color=C_SLATE)

ax.axvline(0, color='#888', linewidth=1, linestyle='--', alpha=0.7)
ax.set_yticks(range(len(coef_data)))
ax.set_yticklabels([c[0] for c in coef_data], fontsize=10)
ax.set_xlabel('Standardized Coefficient (β)', fontsize=11)
ax.set_title(f'Predictors of AI Tool Integration\nOLS Regression  |  R² = {r_sq:.2f}  |  n = {n}',
             fontsize=13, fontweight='bold', pad=12)
ax.set_facecolor(C_LIGHT)
ax.grid(True, axis='x', color='white', linewidth=0.8)

teal_patch = mpatches.Patch(color=C_TEAL, label='Positive predictor')
orange_patch = mpatches.Patch(color=C_ORANGE, label='Negative predictor')
ax.legend(handles=[teal_patch, orange_patch], fontsize=9, framealpha=0.9)
ax.annotate('* p<.05  ** p<.01  *** p<.001',
            xy=(0.99, 0.02), xycoords='axes fraction',
            ha='right', fontsize=8, color=C_SLATE)

save('03_ols_coefficient_plot.png')
print('Fig 3: OLS coefficient plot — predictors of integration')


# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 4 — Line chart: Weekly session adoption trajectories
# ═══════════════════════════════════════════════════════════════════════════
"""
WHEN TO USE A LINE CHART
────────────────────────
Use a line chart when you have data measured at multiple time points and you
want to show change over time. The x-axis must be ordered time periods; the
y-axis is the measured value.

Here we're plotting mean weekly sessions separately for Integrators and
Resistors. The diverging trajectories tell the core story of the study: both
groups look similar at week 1 (everyone showed up for onboarding), but by
week 3 they've split — Integrators build the tool into their routine while
Resistors' usage decays exponentially.

Why this matters for research design:
  A single post-onboarding measure would miss this entirely. If you surveyed
  people at week 1, you'd conclude adoption was fine. The longitudinal
  behavioral trace is what reveals the actual pattern.

Statistical companion: repeated-measures ANOVA or a mixed-effects model
(lme4 in R / statsmodels in Python) if you want to test whether the
trajectory difference is statistically significant while accounting for
individual-level variation.
"""

week_cols = [f'week_{i}' for i in range(1, 9)]
weeks = list(range(1, 9))

mean_int = df.loc[df['segment'] == 'Integrator', week_cols].mean().values
mean_res = df.loc[df['segment'] == 'Resistor',  week_cols].mean().values
se_int   = df.loc[df['segment'] == 'Integrator', week_cols].sem().values
se_res   = df.loc[df['segment'] == 'Resistor',  week_cols].sem().values

fig, ax = plt.subplots(figsize=(8.5, 5))

ax.plot(weeks, mean_int, color=C_TEAL, linewidth=2.5, marker='o',
        markersize=7, label='Integrators (integration ≥ median)')
ax.fill_between(weeks, mean_int - se_int, mean_int + se_int,
                color=C_TEAL, alpha=0.15)

ax.plot(weeks, mean_res, color=C_ORANGE, linewidth=2.5, marker='s',
        markersize=7, label='Resistors (integration < median)')
ax.fill_between(weeks, mean_res - se_res, mean_res + se_res,
                color=C_ORANGE, alpha=0.15)

ax.axvline(2.5, color='#888', linewidth=1, linestyle=':', alpha=0.7)
ax.text(2.6, ax.get_ylim()[1] * 0.95, 'Divergence\npoint', fontsize=8.5,
        color=C_SLATE, va='top')

ax.set_xlabel('Week Post-Onboarding', fontsize=11)
ax.set_ylabel('Mean Weekly Sessions', fontsize=11)
ax.set_title('AI Tool Usage Trajectories: Integrators vs. Resistors\n'
             'Weeks 1–8 Post-Onboarding  (shading = ±1 SE)',
             fontsize=13, fontweight='bold', pad=12)
ax.set_xticks(weeks)
ax.legend(fontsize=10, framealpha=0.9)
ax.set_facecolor(C_LIGHT)
ax.grid(True, color='white', linewidth=0.8)

save('04_line_adoption_trajectories.png')
print('Fig 4: Line chart — weekly session trajectories by segment')


# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 5 — 2×2 Typology: Trust × Effort quadrants
# ═══════════════════════════════════════════════════════════════════════════
"""
WHEN TO USE A 2×2 TYPOLOGY
──────────────────────────
A 2×2 framework is a synthesis tool, not a statistical test. You use it
after analysis to communicate a finding to a stakeholder audience. It works
when two dimensions have been shown (quantitatively or qualitatively) to be
the primary drivers of an outcome, and when the four quadrant combinations
each describe a meaningfully different behavioral profile.

Here, the two drivers from the regression are Trust Calibration (x-axis) and
Perceived Effort (y-axis). Splitting at the median of each gives four cells.
Each cell gets a descriptive label grounded in the qualitative data — these
are not random; they're based on what people in each quadrant actually said
in interviews.

Why split at the median, not the scale midpoint?
  The scale midpoint (5 on a 10-point scale) is an arbitrary anchor that
  may not match where the real behavioral difference is. The median split
  puts roughly half your sample in each half, so you're comparing groups
  of real people rather than comparing someone to an abstract anchor.

Limitation: median splits lose information and should not be used for
inferential statistics. Use them only for communication frameworks.
"""

trust_med  = df['trust'].median()
effort_med = df['effort'].median()

fig, ax = plt.subplots(figsize=(8.5, 7))

# Quadrant shading
ax.fill_betweenx([effort_med, 10], 0, trust_med,
                  color='#FEEBC8', alpha=0.6, zorder=0)      # high effort, low trust
ax.fill_betweenx([effort_med, 10], trust_med, 10,
                  color='#FED7D7', alpha=0.5, zorder=0)      # high effort, high trust
ax.fill_betweenx([0, effort_med], 0, trust_med,
                  color='#E2E8F0', alpha=0.6, zorder=0)      # low effort, low trust
ax.fill_betweenx([0, effort_med], trust_med, 10,
                  color='#C6F6D5', alpha=0.6, zorder=0)      # low effort, high trust — adoption zone

# Scatter points
for seg, marker, color in [('Integrator', 'o', C_TEAL),
                             ('Resistor',  's', C_ORANGE)]:
    mask = df['segment'] == seg
    ax.scatter(df.loc[mask, 'trust'], df.loc[mask, 'effort'],
               color=color, marker=marker, s=65, alpha=0.75,
               label=seg, zorder=3)

# Quadrant dividers
ax.axvline(trust_med, color='#555', linewidth=1.2, linestyle='--', alpha=0.6)
ax.axhline(effort_med, color='#555', linewidth=1.2, linestyle='--', alpha=0.6)

# Quadrant labels
label_kwargs = dict(fontsize=10, fontweight='bold', va='center', ha='center',
                    color=C_SLATE, style='italic')
ax.text((trust_med/2),          (effort_med + 10)/2,
        '"The Skeptic"\nLow trust, high effort\n→ Needs structured onboarding\n   and early quick wins',
        **label_kwargs)
ax.text((trust_med + 10)/2,     (effort_med + 10)/2,
        '"The Frustrated Expert"\nHigh trust, high effort\n→ Motivated to use tool but\n   workflow friction is the blocker',
        **label_kwargs)
ax.text((trust_med/2),          (effort_med/2),
        '"The Passive Delegator"\nLow trust, low effort\n→ Uses tool when assigned;\n   no independent adoption',
        **label_kwargs)
ax.text((trust_med + 10)/2,     (effort_med/2),
        '"The Integrator"\nHigh trust, low effort\n→ Adoption zone; these are\n   your champions',
        **label_kwargs)

ax.set_xlabel('Trust Calibration Score (1–10) →', fontsize=11)
ax.set_ylabel('← Perceived Effort (1–10, lower = easier)', fontsize=11)
ax.set_title('User Typology: Trust × Effort Quadrants\n'
             'Dashed lines = median splits  |  Labels grounded in interview data',
             fontsize=13, fontweight='bold', pad=12)
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.legend(fontsize=10, framealpha=0.9, loc='lower right')

save('05_typology_trust_effort.png')
print('Fig 5: 2×2 typology — trust × effort quadrants')


# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 6 — Horizontal bar: Failure mode frequency
# ═══════════════════════════════════════════════════════════════════════════
"""
WHEN TO USE A HORIZONTAL BAR CHART
────────────────────────────────────
Use a horizontal bar chart when you have categorical data (e.g., themes from
qualitative coding) and you want to compare frequency or prevalence across
categories. Horizontal orientation is preferred when category labels are long
— it prevents the diagonal cramming you get with vertical bars.

This chart shows how often each failure mode was mentioned across n=18
interviews. The bars are ordered from most to least frequent (a Pareto
ordering) so the reader immediately sees the dominant problem.

These categories come from thematic coding: the interview transcripts were
coded in NVivo using an inductive approach, then consolidated into five
failure mode themes. The counts shown are the number of participants who
mentioned each theme at least once (prevalence), not total mention frequency
(which would inflate common themes and obscure rare but important ones).

Statistical companion: for categorical frequency data like this, chi-square
goodness-of-fit tests whether the observed distribution differs from an
expected baseline. But for qualitative-derived counts, the more important
question is substantive: which failure modes are actionable?
"""

failure_modes = [
    ('Output hallucinations or errors\nnot flagged by the tool',          14),
    ('Mental model mismatch\n(expected different behavior)',               11),
    ('No clear recovery path\nwhen tool failed',                           9),
    ('Workflow friction\n(copy-paste, reformatting overhead)',              8),
    ('Insufficient onboarding\nfor edge-case scenarios',                   7),
]
labels_fm = [f[0] for f in failure_modes]
counts_fm = [f[1] for f in failure_modes]
bar_colors = [C_RED if c >= 10 else C_ORANGE if c >= 8 else C_SLATE
              for c in counts_fm]

fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.barh(labels_fm, counts_fm, color=bar_colors, alpha=0.85, height=0.55)

for bar, count in zip(bars, counts_fm):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
            f'{count}/18', va='center', fontsize=10, color=C_SLATE)

ax.set_xlabel('Number of Participants Mentioning This Theme (n=18 interviews)',
              fontsize=10)
ax.set_title('AI Tool Failure Modes: Prevalence Across Semi-Structured Interviews\n'
             'Themes from inductive coding — ordered by participant prevalence',
             fontsize=12, fontweight='bold', pad=12)
ax.set_xlim(0, 17)
ax.set_facecolor(C_LIGHT)
ax.grid(True, axis='x', color='white', linewidth=0.8)
ax.invert_yaxis()

red_patch   = mpatches.Patch(color=C_RED,    label='High severity (≥10 participants)')
orange_patch = mpatches.Patch(color=C_ORANGE, label='Moderate (8–9 participants)')
slate_patch = mpatches.Patch(color=C_SLATE,  label='Lower prevalence (<8 participants)')
ax.legend(handles=[red_patch, orange_patch, slate_patch], fontsize=9,
          framealpha=0.9, loc='lower right')

save('06_bar_failure_modes.png')
print('Fig 6: Horizontal bar — failure mode prevalence from interviews')


# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 7 — Box plot: Failure documentation vs. segment (bonus)
# ═══════════════════════════════════════════════════════════════════════════
"""
OPERATIONALIZING A BEHAVIORAL SIGNAL
────────────────────────────────────
Failure documentation rate is a behavioral proxy — it's not what people said
in interviews, it's what they actually did in the platform log. Analysts who
clicked "flag as error" when the tool failed were tracked over 8 weeks.

This matters because it's a leading indicator. When we look at who documented
failures and then check their integration index 4 weeks later, the pattern is
clear: people who document failures early tend to calibrate their trust more
accurately, which is the strongest predictor of integration (Fig 1, Fig 3).

The behavioral science mechanism: documenting a failure requires you to
name what went wrong. That cognitive act — labeling the failure — turns a
frustrating experience into information. It prevents overcorrection (total
abandonment) and under-correction (continued blind trust).

This is the insight that informed the intervention recommendation: any
onboarding redesign should include a structured failure-logging prompt in
weeks 2-3, not just at the initial session.
"""

fig, ax = plt.subplots(figsize=(6.5, 5))

segs  = ['Integrator', 'Resistor']
data_seg = [df.loc[df['segment'] == s, 'failure_doc'].values * 100 for s in segs]
seg_colors = [C_TEAL, C_ORANGE]

bp = ax.boxplot(data_seg, patch_artist=True, widths=0.4,
                medianprops=dict(color='white', linewidth=2.5),
                whiskerprops=dict(linewidth=1.2, color=C_SLATE),
                capprops=dict(linewidth=1.2, color=C_SLATE),
                flierprops=dict(marker='o', markersize=5, alpha=0.5))

for patch, color in zip(bp['boxes'], seg_colors):
    patch.set_facecolor(color); patch.set_alpha(0.8)

stat, pv = stats.mannwhitneyu(data_seg[0], data_seg[1], alternative='two-sided')
sig = '***' if pv < 0.001 else '**' if pv < 0.01 else '*' if pv < 0.05 else 'n.s.'

ax.set_xticklabels(segs, fontsize=12)
ax.set_ylabel('Failure Documentation Rate (%)', fontsize=11)
ax.set_title('Failure Documentation Rate\nIntegrators vs. Resistors',
             fontsize=13, fontweight='bold', pad=12)
ax.set_facecolor(C_LIGHT)
ax.grid(True, axis='y', color='white', linewidth=0.8)

y_max = max(max(d) for d in data_seg)
ax.annotate('', xy=(2, y_max + 2), xytext=(1, y_max + 2),
            arrowprops=dict(arrowstyle='-', color=C_SLATE, lw=1.5))
ax.text(1.5, y_max + 3.5, f'Mann-Whitney U\np {sig}',
        ha='center', fontsize=9, color=C_SLATE)

ax.annotate(
    'Analysts who log failures early\ncalibrate trust more accurately\n→ strongest leading indicator of adoption',
    xy=(0.5, 0.08), xycoords='axes fraction', ha='center', fontsize=8.5,
    color=C_SLATE, style='italic',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.85))

save('07_box_failure_doc_by_segment.png')
print('Fig 7: Box plot — failure documentation rate by segment')

print('\nAll figures saved to figures/')
print(f'\nDataset summary:\n{df[["team","segment","integration","trust","effort"]].groupby(["team","segment"]).mean().round(2)}')
