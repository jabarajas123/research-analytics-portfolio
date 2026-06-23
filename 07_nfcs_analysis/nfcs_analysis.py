"""
NFCS 2024 Financial Capability Analysis
========================================
National Financial Capability Study (NFCS) — 2024 State-by-State Data
Source: FINRA Investor Education Foundation
n ≈ 25,500 U.S. adults; ~500 respondents per state

This script is written as a teaching document.
Each section explains what the code does, why we're doing it,
what the data should look like afterward, and how to verify correctness.

The analysis replicates four core findings from the NFCS:
  1. Financial literacy scores vary substantially by gender, education, and age
  2. Financial fragility (inability to cover a $2K emergency) is concentrated
     among low-income and less-educated households
  3. Emergency fund coverage gaps are widest at lower education levels
     and persist even after controlling for gender
  4. Retirement savings participation follows a steep education gradient

Run:
    python3 nfcs_analysis.py

Outputs: output_figures/nfcs_fig_01_literacy.png
         output_figures/nfcs_fig_02_fragility.png
         output_figures/nfcs_fig_03_emergency_fund.png
         output_figures/nfcs_fig_04_retirement.png

Dependencies: pandas, numpy, matplotlib
"""

# ── Imports ───────────────────────────────────────────────────────────────────
# We suppress warnings at the top because pandas sometimes raises FutureWarnings
# for operations that still work correctly in this version. In production code
# you'd want to address the root cause; for a portfolio demo, suppression keeps
# the terminal output clean and focused on our printed summaries.

import warnings
warnings.filterwarnings("ignore")

import numpy as np          # array math; we use np.average() for weighted means
import pandas as pd         # core data wrangling; the DataFrame is our unit of analysis
import matplotlib.pyplot as plt          # figure/axes creation
import matplotlib.patches as mpatches   # for manual legend patches in Fig 4
from pathlib import Path    # platform-safe file paths (works on Mac, Windows, Linux)


# ── File Paths ────────────────────────────────────────────────────────────────
# We define paths as Path objects so we can do things like path.stem, path / "subdir",
# and path.mkdir() without string concatenation. This also makes the script portable —
# change DATA_PATH here and everything else updates automatically.

DATA_PATH = Path(
    "/Users/jbarajas/Documents/Leaving RAND/Job Hunting/Prior Achievements/"
    "NFCS/2024-SxS-Data-and-Data-Info/NFCS 2024 State Data 250623.csv"
)
OUT_DIR = Path("output_figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)
# parents=True: create any missing parent directories
# exist_ok=True: don't raise an error if the folder already exists


# ── Visual Style ──────────────────────────────────────────────────────────────
# Defining colors and rcParams centrally means every figure uses the same palette.
# If a client wants to swap in their brand colors, you change one line, not 40.
# rcParams are matplotlib's global defaults — setting them here overrides the
# library's built-in style for every figure we create below.

BLUE   = "#2D6A9F"   # primary data color; also used for positive/higher-ed groups
ORANGE = "#E87722"   # secondary/contrast; used for risk/lower-ed groups
GREEN  = "#3A7D44"   # reserved for annotations if needed
GRAY   = "#888888"   # footnote text and de-emphasized labels
LGRAY  = "#E8E8E8"   # gridlines — light enough not to compete with data
DGRAY  = "#333333"   # body text on charts
DPI    = 150         # 150 dpi is a good balance: sharp enough for screens and PDFs,
                     # without producing multi-megabyte files like 300 dpi would

plt.rcParams.update({
    "font.family":       "sans-serif",   # cleaner than serif for data viz
    "font.size":         10,             # base size; individual elements scale from here
    "axes.spines.top":   False,          # remove top and right borders (Tufte principle:
    "axes.spines.right": False,          # reduce non-data ink)
    "axes.linewidth":    0.8,
    "xtick.major.size":  3,
    "ytick.major.size":  3,
    "figure.dpi":        DPI,
})


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: DATA LOADING AND CLEANING
# ─────────────────────────────────────────────────────────────────────────────
# This is the most critical section. Every analytical decision downstream
# depends on the choices made here. We narrate each step so a reader can
# follow the logic — and challenge it if something seems wrong.

def load_data() -> pd.DataFrame:
    """
    Load the NFCS 2024 CSV and construct all analysis variables.

    Returns a DataFrame with one row per respondent and new columns for:
      - literacy_score     (0–7 integer)
      - fragile            (0/1 binary)
      - no_emergency_fund  (0/1 binary)
      - has_ret_plan       (0/1 binary)
      - has_ira            (0/1 binary)
      - edu4, age_cohort, gender, income4  (labeled categorical grouping vars)
    """

    # ── Step 1: Read the raw CSV ──────────────────────────────────────────────
    # The file has a UTF-8 BOM (byte-order mark) at the start — a common artifact
    # from Excel exports. encoding='utf-8-sig' strips the BOM automatically so
    # the first column name doesn't come in as "﻿NFCSID" with a garbage prefix.
    # Verify: df.columns[0] should be 'NFCSID', not '﻿NFCSID'.

    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    print(f"  Loaded {len(df):,} rows × {df.shape[1]} columns")

    # ── Step 2: Construct the financial literacy score ────────────────────────
    # The NFCS uses a 7-item quiz to measure objective financial knowledge.
    # Each item presents a multiple-choice question; we know the correct answer
    # from the codebook. We score each item 1 (correct) or 0 (wrong), then sum
    # to get a score from 0 to 7.
    #
    # The answer key from the codebook:
    #   M6  = 1  (compound interest: money grows faster with compounding)
    #   M7  = 3  (inflation: a dollar buys less over time)
    #   M8  = 2  (bond prices: rise when interest rates fall)
    #   M31 = 2  (debt doubling: at 20% APR, debt doubles in ~3.5 years)
    #   M50 = 1  (probability: a coin flip has no memory — each flip is 50/50)
    #   M9  = 1  (mortgage: 15-year has lower total interest than 30-year)
    #   M10 = 2  (diversification: stocks in a single company are riskier than a fund)
    #
    # Codes 98 ("don't know") and 99 ("refused") are NOT correct answers.
    # We convert them to NaN first, then score — so they count as 0 toward the
    # total (respondent did not demonstrate knowledge of that concept).
    # This is the FINRA standard approach; treating 98/99 as missing and dropping
    # the item would overstate scores for respondents who avoided harder questions.

    correct_answers = {"M6": 1, "M7": 3, "M8": 2, "M31": 2, "M50": 1, "M9": 1, "M10": 2}

    for col, right_answer in correct_answers.items():
        # Convert to numeric so 98/99 string codes become NaN if any slipped through
        df[col] = pd.to_numeric(df[col], errors="coerce")
        # Create a binary 0/1 column: 1 if respondent chose the correct answer
        df[f"{col}_correct"] = (df[col] == right_answer).astype(float)
        # NaN inputs produce False from ==, which becomes 0.0 — intended behavior

    # Sum the seven binary columns into a single score
    score_cols = [f"{c}_correct" for c in correct_answers]
    df["literacy_score"] = df[score_cols].sum(axis=1)
    # axis=1 means "sum across columns within each row" (not down the column)
    # Verify: df['literacy_score'].describe() should show min=0, max=7, mean≈3.2

    # ── Step 3: Financial fragility (the $2,000 question) ────────────────────
    # J20 asks: "How confident are you that you could come up with $2,000
    #            within the next month if an unexpected need arose?"
    # Response scale:
    #   1 = I am certain I could come up with the full $2,000
    #   2 = I could probably come up with $2,000
    #   3 = I could probably NOT come up with $2,000
    #   4 = I am certain I could NOT come up with $2,000
    #   98 = Don't know
    #   99 = Prefer not to say
    #
    # We define "financially fragile" as responses 3 or 4 — the respondent
    # does NOT have a realistic path to $2,000 on short notice.
    # 98 and 99 are genuinely ambiguous (some "don't know" respondents may be
    # fragile; others may be wealthy but uncertain), so we code them as missing
    # rather than forcing them into either category.

    df["J20"] = pd.to_numeric(df["J20"], errors="coerce").replace({98: np.nan, 99: np.nan})
    df["fragile"] = df["J20"].isin([3, 4]).astype(float)
    df.loc[df["J20"].isna(), "fragile"] = np.nan
    # Verify: df['fragile'].value_counts() should show roughly 35–40% fragile nationally

    # ── Step 4: Emergency fund (rainy-day savings) ────────────────────────────
    # J5 asks whether the respondent has a "rainy day fund" — savings set aside
    # to cover 3 months of expenses in case of an emergency.
    #   1 = Yes
    #   2 = No
    #   98 = Don't know / 99 = Prefer not to say → missing
    #
    # We create a "no emergency fund" indicator (1 = does NOT have one) so that
    # higher values always mean worse financial health — consistent with fragility.

    df["J5"] = pd.to_numeric(df["J5"], errors="coerce").replace({98: np.nan, 99: np.nan})
    df["no_emergency_fund"] = (df["J5"] == 2).astype(float)
    df.loc[df["J5"].isna(), "no_emergency_fund"] = np.nan
    # Verify: roughly 50% of respondents should have no emergency fund nationally

    # ── Step 5: Retirement savings variables ──────────────────────────────────
    # We use two indicators together to capture retirement savings participation:
    #   C1_2012: Has a retirement account through a current or former employer
    #            (401k, 403b, pension, etc.)  1=yes, 2=no
    #   C4_2012: Owns an Individual Retirement Account (IRA or Roth IRA)
    #            1=yes, 2=no
    #
    # We create separate binary flags for each, and a combined "has_any_retirement"
    # that is 1 if the respondent has either type of account.
    # This is intentionally inclusive — we want to capture anyone who is saving
    # for retirement in any formal vehicle.

    for col in ["C1_2012", "C4_2012"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").replace({98: np.nan, 99: np.nan})

    df["has_ret_plan"] = (df["C1_2012"] == 1).astype(float)
    df.loc[df["C1_2012"].isna(), "has_ret_plan"] = np.nan

    df["has_ira"] = (df["C4_2012"] == 1).astype(float)
    df.loc[df["C4_2012"].isna(), "has_ira"] = np.nan

    # has_any_retirement: True if EITHER account type is present
    # We only mark it missing if BOTH variables are missing — a respondent who
    # answered one and not the other still gave us valid information.
    df["has_any_retirement"] = ((df["C1_2012"] == 1) | (df["C4_2012"] == 1)).astype(float)
    df.loc[df["C1_2012"].isna() & df["C4_2012"].isna(), "has_any_retirement"] = np.nan

    # ── Step 6: Demographic grouping variables ────────────────────────────────
    # These are categorical labels used for group comparisons in each figure.
    # We map raw numeric codes to human-readable strings so chart axes are
    # immediately interpretable without a separate codebook lookup.

    # Gender: A50A (1=male, 2=female)
    # Note: NFCS 2024 uses a binary gender measure. This is a limitation of the
    # survey design, not our analytical choice.
    df["gender"] = df["A50A"].map({1: "Men", 2: "Women"})

    # Education: A5_2015 uses a 7-level scale. We collapse to 4 levels that
    # roughly correspond to meaningful credential thresholds:
    #   No HS diploma (1) — did not complete secondary education
    #   HS / GED (2)      — terminal secondary credential
    #   Some college (3,4,5) — any post-secondary without a bachelor's
    #   Bachelor's+ (6,7)    — four-year degree or graduate degree
    #
    # Collapsing 3/4/5 together reflects the labor market reality that
    # associate degrees and "some college" face similar earnings outcomes.
    # We keep Bachelor's and graduate degrees together because the NFCS
    # sample at post-grad is small enough that splitting would hurt precision.
    df["edu4"] = df["A5_2015"].map({
        1: "No HS diploma",
        2: "HS / GED",
        3: "Some college",
        4: "Some college",
        5: "Some college",
        6: "Bachelor's+",
        7: "Bachelor's+",
    })

    # Age cohort: A3Ar_w uses 6 roughly decade-length bands
    # These are already sensible groupings — we just add readable labels.
    df["age_cohort"] = df["A3Ar_w"].map({
        1: "18–24", 2: "25–34", 3: "35–44",
        4: "45–54", 5: "55–64", 6: "65+",
    })

    # Income: A8_2021 has 10 levels. We collapse to 4 broad brackets.
    # The thresholds ($25K, $50K, $100K) are common reference points in
    # financial research — roughly: poverty-adjacent, working class,
    # middle class, upper-middle class and above.
    df["income4"] = df["A8_2021"].map({
        1: "< $25K",   # < $15K
        2: "< $25K",   # $15–25K
        3: "$25–50K",  # $25–35K
        4: "$25–50K",  # $35–50K
        5: "$50–100K", # $50–75K
        6: "$50–100K", # $75–100K
        7: "$100K+",   # $100–150K
        8: "$100K+",   # $150–200K
        9: "$100K+",   # $200–300K
        10: "$100K+",  # $300K+
    })

    return df


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: WEIGHTED STATISTICS HELPERS
# ─────────────────────────────────────────────────────────────────────────────
# The NFCS over-samples smaller states to ensure each state has ~500 respondents.
# Without weighting, a state like Wyoming (pop. ~580K) would be as influential
# as California (pop. ~39M). wgt_n2 is FINRA's national-level weight that
# corrects for this — it up-weights respondents from large states and
# down-weights those from small states to restore national representativeness.
#
# All estimates in this script use wgt_n2. We never report unweighted numbers
# in the figures; doing so would misrepresent the U.S. adult population.

def wmean(series: pd.Series, weights: pd.Series) -> float:
    """
    Compute a weighted mean of `series` using `weights`.

    We drop rows where either the value or the weight is missing before
    computing — this is conservative but correct. A missing weight means
    FINRA couldn't assign a valid post-stratification weight for that
    respondent, which typically indicates a data quality issue.

    np.average() does the heavy lifting: it computes sum(x * w) / sum(w).
    This is mathematically equivalent to a weighted mean and handles
    non-integer weights correctly (unlike a simple loop approach).

    Verify: wmean applied to a binary variable should return a value in [0, 1].
    wmean applied to literacy_score should return roughly 3.2–3.4 nationally.
    """
    mask = series.notna() & weights.notna()
    s, w = series[mask], weights[mask]
    return float(np.average(s, weights=w))


def wpct(series: pd.Series, weights: pd.Series) -> float:
    """
    Weighted percentage of 1s in a binary series.

    This is just wmean × 100 — a convenience wrapper so call sites can write
    wpct(...) instead of wmean(...) * 100, making intent explicit.

    Verify: wpct on 'fragile' should return ~36% nationally.
    """
    return wmean(series, weights) * 100


def wgroup(df: pd.DataFrame, group_col: str, value_col: str,
           weight_col: str = "wgt_n2", pct: bool = False) -> pd.Series:
    """
    Compute a weighted statistic for each level of a grouping variable.

    Parameters
    ----------
    df         : input DataFrame (pre-filtered to remove rows with missing grouping var)
    group_col  : the column defining groups (e.g., 'edu4', 'gender')
    value_col  : the column to summarize (e.g., 'fragile', 'literacy_score')
    weight_col : survey weight column; defaults to national weight wgt_n2
    pct        : if True, multiply by 100 (use for binary 0/1 outcomes)

    Returns a Series indexed by group label, values are weighted means or percentages.

    Example output for wgroup(df, 'gender', 'fragile', pct=True):
        Men      28.4
        Women    43.1
        dtype: float64

    Verify: the weighted average across all groups (weighting by group size)
    should approximately match the national estimate from wmean().
    """
    result = {}
    for grp, sub in df.groupby(group_col, observed=True):
        if pct:
            result[grp] = wpct(sub[value_col], sub[weight_col])
        else:
            result[grp] = wmean(sub[value_col], sub[weight_col])
    return pd.Series(result)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: FIGURES
# ─────────────────────────────────────────────────────────────────────────────
# Each figure function is self-contained: it receives the full cleaned DataFrame,
# extracts what it needs, builds the plot, and saves it. This makes each figure
# independently reproducible — you can call any one of them in isolation to
# regenerate a single chart without rerunning the others.


# ── Figure 1: Financial Literacy Score by Demographic Group ──────────────────

def fig_literacy(df: pd.DataFrame) -> None:
    """
    Three-panel figure showing the mean 7-item literacy score by:
      Panel A: Gender (bar chart — simple two-group comparison)
      Panel B: Education (bar chart — gradient from no-HS to bachelor's+)
      Panel C: Age cohort (line chart — shows lifecycle accumulation of knowledge)

    Why a line for age but bars for the others?
    Age cohorts have a natural ordering and a meaningful trend to trace
    (knowledge accumulates with age and financial experience). Gender and
    education are categorical contrasts, so bars communicate the comparison
    more directly.

    Expected patterns from prior NFCS waves:
    - Men will outscore women by ~0.5–1.0 points
    - Score will rise monotonically with education
    - Age pattern is typically U-shaped or monotonically rising
    """

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    fig.suptitle("Financial Literacy Score by Demographic Group",
                 fontsize=13, fontweight="bold", color=DGRAY, y=1.01)

    ax_gender, ax_edu, ax_age = axes

    # ── Panel A: Gender ───────────────────────────────────────────────────────
    # We drop rows missing gender before calling wgroup because groupby would
    # otherwise create a NaN group, which would confuse axis labels.
    # The result is a two-element Series: {"Men": x.xx, "Women": x.xx}

    gend = wgroup(df.dropna(subset=["gender"]), "gender", "literacy_score")

    bars = ax_gender.bar(gend.index, gend.values, color=[BLUE, ORANGE],
                         width=0.5, zorder=3)
    # zorder=3 puts bars in front of gridlines (which are at default zorder=0)

    ax_gender.set_ylim(0, 7)
    ax_gender.set_ylabel("Mean score (0–7)", fontsize=9)
    ax_gender.set_title("A.  By Gender", fontsize=10, fontweight="bold", loc="left")
    ax_gender.yaxis.grid(True, color=LGRAY, zorder=0)
    ax_gender.set_axisbelow(True)   # gridlines draw behind, not over, bars

    # Value labels above each bar — we iterate bars and values in parallel
    for bar, val in zip(bars, gend.values):
        ax_gender.text(
            bar.get_x() + bar.get_width() / 2,   # x center of bar
            val + 0.08,                            # slightly above the top of the bar
            f"{val:.2f}",                          # 2 decimal places for precision
            ha="center", va="bottom",
            fontsize=9.5, fontweight="bold", color=DGRAY,
        )

    # Compute and display the gap as an annotation inside the chart area
    gap = gend["Men"] - gend["Women"]
    ax_gender.annotate(
        f"Gap: {gap:.2f} pts",
        xy=(0.5, 0.92), xycoords="axes fraction",   # axes fraction = relative position (0–1)
        ha="center", fontsize=8.5, color=GRAY, style="italic",
    )

    # ── Panel B: Education ────────────────────────────────────────────────────
    # We reindex to a specific order so bars appear left-to-right from
    # least to most education. Without reindex(), groupby returns groups
    # in alphabetical order, which would put "Bachelor's+" before "HS / GED".

    edu_order = ["No HS diploma", "HS / GED", "Some college", "Bachelor's+"]
    edu = wgroup(df.dropna(subset=["edu4"]), "edu4", "literacy_score")
    edu = edu.reindex(edu_order).dropna()

    # Progressive color ramp — lighter shades for lower-education groups
    # draws the reader's eye toward the rightmost (highest) bar
    colors_edu = [LGRAY, "#A0BACC", "#5A9DC8", BLUE]

    bars_edu = ax_edu.bar(range(len(edu)), edu.values,
                          color=colors_edu, width=0.6, zorder=3)
    ax_edu.set_xticks(range(len(edu)))
    ax_edu.set_xticklabels(edu.index, fontsize=8.5, rotation=15, ha="right")
    ax_edu.set_ylim(0, 7)
    ax_edu.set_title("B.  By Education", fontsize=10, fontweight="bold", loc="left")
    ax_edu.yaxis.grid(True, color=LGRAY, zorder=0)
    ax_edu.set_axisbelow(True)

    for bar, val in zip(bars_edu, edu.values):
        ax_edu.text(bar.get_x() + bar.get_width() / 2, val + 0.08,
                    f"{val:.2f}", ha="center", va="bottom",
                    fontsize=9, color=DGRAY)

    # ── Panel C: Age Cohort ───────────────────────────────────────────────────
    # Line chart with shaded area under the curve (fill_between).
    # alpha=0.12 on the fill keeps it subtle — visual weight, not another data layer.

    age_order = ["18–24", "25–34", "35–44", "45–54", "55–64", "65+"]
    age = wgroup(df.dropna(subset=["age_cohort"]), "age_cohort", "literacy_score")
    age = age.reindex(age_order).dropna()

    ax_age.plot(range(len(age)), age.values,
                color=BLUE, linewidth=2.2,
                marker="o", markersize=7, zorder=3)
    ax_age.fill_between(range(len(age)), age.values, alpha=0.12, color=BLUE)

    ax_age.set_xticks(range(len(age)))
    ax_age.set_xticklabels(age.index, fontsize=8.5)
    ax_age.set_ylim(2.0, 4.5)   # tight y-range to make the trend visible
    ax_age.set_title("C.  By Age Cohort", fontsize=10, fontweight="bold", loc="left")
    ax_age.yaxis.grid(True, color=LGRAY, zorder=0)
    ax_age.set_axisbelow(True)

    for i, val in enumerate(age.values):
        ax_age.text(i, val + 0.04, f"{val:.2f}",
                    ha="center", va="bottom", fontsize=8.5, color=DGRAY)

    # ── Shared footnote ───────────────────────────────────────────────────────
    # fig.text() places text relative to the entire figure (not a single axes).
    # y=-0.04 puts it below all three panels. wrap=True allows line breaks if
    # the note is long (useful for narrow figures).

    fig.text(
        0.5, -0.04,
        "Source: NFCS 2024 State-by-State Survey (n≈25,500). Estimates weighted using wgt_n2. "
        "Literacy score = # correct on 7-item quiz (compound interest, inflation, bond prices, "
        "debt doubling, probability, mortgage, diversification).",
        ha="center", fontsize=7.5, color=GRAY, style="italic",
    )

    plt.tight_layout()
    path = OUT_DIR / "nfcs_fig_01_literacy.png"
    plt.savefig(path, dpi=DPI, bbox_inches="tight")
    # bbox_inches="tight" expands the saved area to include all text,
    # including the footnote which extends below the nominal figure boundary
    plt.close()
    print(f"  Saved: {path.name}")


# ── Figure 2: Financial Fragility by Income & Education ───────────────────────

def fig_fragility(df: pd.DataFrame) -> None:
    """
    Two-panel bar chart showing the share of respondents who are financially
    fragile (could probably or certainly NOT come up with $2,000 in 30 days).

    Panel A: By household income — expect a steep gradient; fragility should
             be very high at the bottom and low at the top.
    Panel B: By education — fragility follows education gradient even when
             income effects are not controlled for (education predicts income).

    Color choice: orange-to-blue ramp where orange = higher fragility (risk),
    blue = lower fragility (more secure). This is a visual cue, not just aesthetics.
    """

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    fig.suptitle("Financial Fragility: Unable to Cover $2,000 Emergency",
                 fontsize=13, fontweight="bold", color=DGRAY, y=1.01)

    ax_inc, ax_edu = axes

    # ── Panel A: Income ───────────────────────────────────────────────────────
    # We drop rows missing BOTH the grouping variable AND the outcome variable.
    # Dropping only on one could silently inflate or deflate group estimates
    # if missingness is correlated across the two variables.

    inc_order = ["< $25K", "$25–50K", "$50–100K", "$100K+"]
    inc = wgroup(
        df.dropna(subset=["income4", "fragile"]),
        "income4", "fragile", pct=True
    )
    inc = inc.reindex(inc_order).dropna()

    colors_inc = [ORANGE, "#E8A060", "#A0BACC", BLUE]   # orange → blue = bad → good
    bars = ax_inc.bar(range(len(inc)), inc.values,
                      color=colors_inc, width=0.55, zorder=3)

    ax_inc.set_xticks(range(len(inc)))
    ax_inc.set_xticklabels(inc.index, fontsize=9)
    ax_inc.set_ylim(0, 100)
    ax_inc.set_ylabel("% probably/certainly could not", fontsize=9)
    ax_inc.set_title("A.  By Household Income", fontsize=10, fontweight="bold", loc="left")
    ax_inc.yaxis.grid(True, color=LGRAY, zorder=0)
    ax_inc.set_axisbelow(True)

    for bar, val in zip(bars, inc.values):
        ax_inc.text(bar.get_x() + bar.get_width() / 2, val + 1,
                    f"{val:.0f}%",   # 0 decimal places — percent reads more naturally without decimals
                    ha="center", va="bottom",
                    fontsize=9.5, fontweight="bold", color=DGRAY)

    # ── Panel B: Education ────────────────────────────────────────────────────
    edu_order = ["No HS diploma", "HS / GED", "Some college", "Bachelor's+"]
    edu = wgroup(
        df.dropna(subset=["edu4", "fragile"]),
        "edu4", "fragile", pct=True
    )
    edu = edu.reindex(edu_order).dropna()

    colors_edu = [ORANGE, "#E8A060", "#A0BACC", BLUE]
    bars_edu = ax_edu.bar(range(len(edu)), edu.values,
                          color=colors_edu, width=0.55, zorder=3)

    ax_edu.set_xticks(range(len(edu)))
    ax_edu.set_xticklabels(edu.index, fontsize=8.5, rotation=15, ha="right")
    ax_edu.set_ylim(0, 100)
    ax_edu.set_title("B.  By Education", fontsize=10, fontweight="bold", loc="left")
    ax_edu.yaxis.grid(True, color=LGRAY, zorder=0)
    ax_edu.set_axisbelow(True)

    for bar, val in zip(bars_edu, edu.values):
        ax_edu.text(bar.get_x() + bar.get_width() / 2, val + 1,
                    f"{val:.0f}%", ha="center", va="bottom",
                    fontsize=9.5, fontweight="bold", color=DGRAY)

    fig.text(
        0.5, -0.06,
        "Source: NFCS 2024 State-by-State Survey (n≈25,500). Weighted using wgt_n2. "
        "Fragility = 'probably' or 'certainly could not' come up with $2,000 in 30 days (J20).",
        ha="center", fontsize=7.5, color=GRAY, style="italic",
    )

    plt.tight_layout()
    path = OUT_DIR / "nfcs_fig_02_fragility.png"
    plt.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path.name}")


# ── Figure 3: Emergency Fund Coverage ────────────────────────────────────────

def fig_emergency_fund(df: pd.DataFrame) -> None:
    """
    Two-panel figure showing the share of respondents with NO emergency fund.

    Panel A: Horizontal bar by education — we use horizontal bars here because
             the education labels are long enough to be hard to read at an angle
             on a vertical bar chart. Horizontal layout gives each label room.

    Panel B: Grouped vertical bars by education AND gender — lets us see whether
             the gender gap in emergency fund coverage persists within education
             tiers, or whether it's driven entirely by women being concentrated
             in lower-education groups.

    Design note: the color threshold in Panel A (orange if >55%, blue if <40%,
    medium blue otherwise) is meant to visually encode the risk level of each
    bar without requiring a separate legend.
    """

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    fig.suptitle("Emergency Fund Coverage: % with No Rainy-Day Savings",
                 fontsize=13, fontweight="bold", color=DGRAY, y=1.01)

    ax_edu, ax_gend = axes

    # ── Panel A: Education (horizontal bars) ──────────────────────────────────
    edu_order = ["No HS diploma", "HS / GED", "Some college", "Bachelor's+"]
    edu = wgroup(
        df.dropna(subset=["edu4", "no_emergency_fund"]),
        "edu4", "no_emergency_fund", pct=True
    )
    edu = edu.reindex(edu_order).dropna()

    # Color each bar based on its value — a simple conditional list comprehension
    colors_edu = [
        ORANGE if v > 55 else (BLUE if v < 40 else "#5A9DC8")
        for v in edu.values
    ]

    y = range(len(edu))
    bars = ax_edu.barh(list(y), edu.values,   # barh = horizontal bar chart
                       color=colors_edu, height=0.5, zorder=3)

    ax_edu.set_yticks(list(y))
    ax_edu.set_yticklabels(edu.index, fontsize=9)
    ax_edu.set_xlim(0, 85)
    ax_edu.set_xlabel("% with no emergency fund", fontsize=9)
    ax_edu.set_title("A.  By Education", fontsize=10, fontweight="bold", loc="left")
    ax_edu.xaxis.grid(True, color=LGRAY, zorder=0)
    ax_edu.set_axisbelow(True)

    # For horizontal bars, the value label goes to the right of the bar end
    for bar, val in zip(bars, edu.values):
        ax_edu.text(
            val + 1,                                        # just past the bar end
            bar.get_y() + bar.get_height() / 2,            # vertical center of bar
            f"{val:.0f}%",
            va="center", fontsize=9.5, fontweight="bold", color=DGRAY,
        )

    # ── Panel B: Education × Gender (grouped vertical bars) ───────────────────
    # We compute men's and women's rates separately within each education tier.
    # numpy.arange() generates evenly spaced positions for the group centers;
    # we offset the two bars by ±width/2 to place them side by side.

    edu_order2 = ["HS / GED", "Some college", "Bachelor's+"]
    # Excluded "No HS diploma" here because the gender-within-education comparison
    # is most meaningful at education levels large enough to be policy-relevant.
    # No HS diploma is ~2.5% of the sample; estimates there have wide margins.

    x = np.arange(len(edu_order2))
    width = 0.35   # bar width; two bars at ±0.175 from center leaves small gap between groups

    men_vals, women_vals = [], []
    for ed in edu_order2:
        sub = df[(df["edu4"] == ed)].dropna(subset=["gender", "no_emergency_fund"])
        m = sub[sub["gender"] == "Men"]
        w = sub[sub["gender"] == "Women"]
        men_vals.append(wpct(m["no_emergency_fund"], m["wgt_n2"]))
        women_vals.append(wpct(w["no_emergency_fund"], w["wgt_n2"]))

    b1 = ax_gend.bar(x - width / 2, men_vals,   width,
                     label="Men",   color=BLUE,   zorder=3)
    b2 = ax_gend.bar(x + width / 2, women_vals, width,
                     label="Women", color=ORANGE, zorder=3)

    ax_gend.set_xticks(x)
    ax_gend.set_xticklabels(edu_order2, fontsize=9)
    ax_gend.set_ylim(0, 80)
    ax_gend.set_ylabel("% with no emergency fund", fontsize=9)
    ax_gend.set_title("B.  By Education & Gender", fontsize=10, fontweight="bold", loc="left")
    ax_gend.yaxis.grid(True, color=LGRAY, zorder=0)
    ax_gend.set_axisbelow(True)
    ax_gend.legend(frameon=False, fontsize=9)

    # Label both sets of bars — we concatenate the bar containers and value lists
    # so we can loop once rather than twice
    for bar, val in zip(list(b1) + list(b2), men_vals + women_vals):
        ax_gend.text(bar.get_x() + bar.get_width() / 2, val + 0.8,
                     f"{val:.0f}%", ha="center", va="bottom",
                     fontsize=8.5, color=DGRAY)

    fig.text(
        0.5, -0.06,
        "Source: NFCS 2024 State-by-State Survey (n≈25,500). Weighted using wgt_n2. "
        "Emergency fund = respondent does NOT have rainy-day savings to cover 3 months expenses (J5).",
        ha="center", fontsize=7.5, color=GRAY, style="italic",
    )

    plt.tight_layout()
    path = OUT_DIR / "nfcs_fig_03_emergency_fund.png"
    plt.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path.name}")


# ── Figure 4: Retirement Savings Gap by Education ────────────────────────────

def fig_retirement(df: pd.DataFrame) -> None:
    """
    Two-panel figure showing retirement savings participation by education.

    Panel A: Employer-sponsored plan (401k, 403b, pension)
    Panel B: IRA / Roth IRA ownership

    These are kept separate rather than combined into "has any retirement account"
    because the mechanisms differ. Employer plans depend on job type and employer
    generosity; IRAs require proactive self-enrollment and investment. Together
    they tell a more complete story about access vs. engagement.

    The annotated gap in Panel A is the headline finding: a 58-percentage-point
    difference in workplace plan participation between college graduates and
    those without a high school diploma — the single largest inequality captured
    in this analysis.
    """

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    fig.suptitle("Retirement Savings Gap by Education",
                 fontsize=13, fontweight="bold", color=DGRAY, y=1.01)

    ax_plan, ax_ira = axes

    edu_order  = ["No HS diploma", "HS / GED", "Some college", "Bachelor's+"]
    colors_edu = [ORANGE, "#E8A060", "#5A9DC8", BLUE]

    # ── Panel A: Employer plan ────────────────────────────────────────────────
    ret = wgroup(
        df.dropna(subset=["edu4", "has_ret_plan"]),
        "edu4", "has_ret_plan", pct=True
    )
    ret = ret.reindex(edu_order).dropna()

    bars = ax_plan.bar(range(len(ret)), ret.values,
                       color=colors_edu, width=0.55, zorder=3)
    ax_plan.set_xticks(range(len(ret)))
    ax_plan.set_xticklabels(ret.index, fontsize=8.5, rotation=15, ha="right")
    ax_plan.set_ylim(0, 100)
    ax_plan.set_ylabel("% participating", fontsize=9)
    ax_plan.set_title("A.  Employer Retirement Plan", fontsize=10, fontweight="bold", loc="left")
    ax_plan.yaxis.grid(True, color=LGRAY, zorder=0)
    ax_plan.set_axisbelow(True)

    for bar, val in zip(bars, ret.values):
        ax_plan.text(bar.get_x() + bar.get_width() / 2, val + 1,
                     f"{val:.0f}%", ha="center", va="bottom",
                     fontsize=9.5, fontweight="bold", color=DGRAY)

    # Annotate the gap — the arrow points from the annotation text
    # (upper left of the panel) to the top of the Bachelor's+ bar.
    # xytext is in data coordinates (same axis as the bars);
    # xy is the arrowhead target.
    gap = ret["Bachelor's+"] - ret["No HS diploma"]
    ax_plan.annotate(
        f"{gap:.0f}pp gap\n(college vs. no HS)",
        xy=(3, ret["Bachelor's+"]),
        xytext=(0.1, 88),
        fontsize=8.5, color=BLUE, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.1),
    )

    # ── Panel B: IRA ownership ────────────────────────────────────────────────
    ira = wgroup(
        df.dropna(subset=["edu4", "has_ira"]),
        "edu4", "has_ira", pct=True
    )
    ira = ira.reindex(edu_order).dropna()

    bars_ira = ax_ira.bar(range(len(ira)), ira.values,
                          color=colors_edu, width=0.55, zorder=3)
    ax_ira.set_xticks(range(len(ira)))
    ax_ira.set_xticklabels(ira.index, fontsize=8.5, rotation=15, ha="right")
    ax_ira.set_ylim(0, 100)
    ax_ira.set_title("B.  IRA Ownership", fontsize=10, fontweight="bold", loc="left")
    ax_ira.yaxis.grid(True, color=LGRAY, zorder=0)
    ax_ira.set_axisbelow(True)

    for bar, val in zip(bars_ira, ira.values):
        ax_ira.text(bar.get_x() + bar.get_width() / 2, val + 1,
                    f"{val:.0f}%", ha="center", va="bottom",
                    fontsize=9.5, fontweight="bold", color=DGRAY)

    # Manual legend using mpatches because we're using positional (integer) x-axis,
    # not a labeled categorical axis, so matplotlib's auto-legend won't know the colors.
    patches = [mpatches.Patch(color=c, label=l)
               for c, l in zip(colors_edu, edu_order)]
    ax_ira.legend(handles=patches, frameon=False, fontsize=8.5, loc="upper left")

    fig.text(
        0.5, -0.06,
        "Source: NFCS 2024 State-by-State Survey (n≈25,500). Weighted using wgt_n2. "
        "Employer plan = has retirement account through current/former employer (C1_2012). "
        "IRA = owns individual retirement account (C4_2012).",
        ha="center", fontsize=7.5, color=GRAY, style="italic",
    )

    plt.tight_layout()
    path = OUT_DIR / "nfcs_fig_04_retirement.png"
    plt.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path.name}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: MAIN — ORCHESTRATION AND DESCRIPTIVE SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
# main() is the entry point. It calls load_data() once, passes the cleaned
# DataFrame to each figure function, then prints a descriptive summary table
# to the terminal. The summary serves as a quick sanity check — if the numbers
# look wildly off from prior NFCS waves or published FINRA reports, something
# went wrong in the cleaning steps above.

def main():
    print("Loading NFCS 2024 data...")
    df = load_data()

    print("\nGenerating figures...")
    fig_literacy(df)
    fig_fragility(df)
    fig_emergency_fund(df)
    fig_retirement(df)

    print(f"\nAll figures saved to {OUT_DIR}/")

    # ── Sanity-check summary ──────────────────────────────────────────────────
    # These are nationally weighted point estimates. Compare against published
    # FINRA NFCS reports to verify the cleaning decisions produced correct numbers.
    # Reference: FINRA Foundation NFCS 2021 national report (2024 not yet published
    # in full at time of writing) — expect literacy ~3.0–3.5, fragility ~30–40%.

    w = df["wgt_n2"]
    print("\n── Key Weighted Estimates (National) ────────────────────────────")
    print(f"  Mean literacy score:        {wmean(df['literacy_score'], w):.2f} / 7")
    print(f"  % financially fragile:      {wpct(df['fragile'], w):.1f}%")
    print(f"  % no emergency fund:        {wpct(df['no_emergency_fund'], w):.1f}%")
    print(f"  % w/ employer ret. plan:    {wpct(df['has_ret_plan'], w):.1f}%")
    print(f"  % w/ IRA:                   {wpct(df['has_ira'], w):.1f}%")
    print("──────────────────────────────────────────────────────────────────")


if __name__ == "__main__":
    # This block only runs when you execute the script directly:
    #   python3 nfcs_analysis.py
    # It does NOT run if another script imports this file as a module,
    # which keeps load_data() and the figure functions available for reuse.
    main()
