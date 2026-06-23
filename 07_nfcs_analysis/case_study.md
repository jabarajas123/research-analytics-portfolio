# NFCS 2024 Financial Capability Analysis

## Overview

Replication and extension of the National Financial Capability Study (NFCS) 2024,
a nationally representative survey of U.S. adults conducted by the FINRA Investor
Education Foundation (n ≈ 25,500; ~500 respondents per state).

The analysis demonstrates weighted survey analysis, construct scoring from item-level
responses, and publication-quality visualization of disparities across demographic groups.

---

## Data

**Source:** FINRA Foundation, 2024 State-by-State Data File  
**Sample:** 25,539 U.S. adults; ~500 per state  
**Weights:** All estimates use `wgt_n2` (national post-stratification weight)

The NFCS over-samples smaller states to ensure state-level precision. National
estimates require weighting to restore representativeness — unweighted figures
would over-represent Wyoming and under-represent California by roughly 70x.

---

## Analyses

### 1. Financial Literacy Score
Constructed from a 7-item objective knowledge quiz. Each item scored 1 (correct)
or 0 (incorrect); "don't know" and "refused" coded as incorrect per FINRA convention.

**Key finding:** Mean national score is 3.26 / 7. Men outscore women by 0.65 points.
Bachelor's degree holders score 4.10 vs. 1.75 for those without a high school diploma.
Scores rise monotonically from 2.55 (ages 18–24) to 3.85 (ages 65+).

### 2. Financial Fragility
Measured by J20: "How confident are you that you could come up with $2,000 within
the next month if an unexpected need arose?" Fragile = "probably" or "certainly could not."

**Key finding:** 36.4% of U.S. adults are financially fragile. The rate is 68% among
households earning under $25K, compared to 11% among households earning $100K+.
Among adults without a high school diploma, 71% are fragile.

### 3. Emergency Fund Coverage
Measured by J5: whether the respondent has a rainy-day fund to cover 3 months of expenses.

**Key finding:** 52% of U.S. adults have no emergency fund. The gap is widest by education:
80% of adults without a high school diploma vs. 34% of college graduates lack a buffer.
Women are consistently less likely than men to have an emergency fund within every
education tier — a gap that persists even after education is held constant.

### 4. Retirement Savings Gap
Measured by C1_2012 (employer plan) and C4_2012 (IRA ownership).

**Key finding:** 58-percentage-point gap in employer plan participation between
college graduates (75%) and adults without a high school diploma (16%). IRA ownership
follows the same gradient: 51% vs. 4%.

---

## Methods

All estimates are weighted means using `np.average(values, weights=wgt_n2)`.
Subgroup estimates drop rows with missing values on both the grouping variable and
the outcome variable before computing — this is conservative and avoids attributing
"don't know" responses to either side of a contrast.

No statistical significance testing is reported here; the NFCS sample is large
enough that virtually all subgroup differences are statistically significant.
The more meaningful question is effect size — the magnitudes reported above.

---

## Files

| File | Description |
|---|---|
| `nfcs_analysis.py` | Full annotated analysis script; produces all four figures |
| `output_figures/nfcs_fig_01_literacy.png` | Financial literacy by gender, education, age |
| `output_figures/nfcs_fig_02_fragility.png` | Financial fragility by income and education |
| `output_figures/nfcs_fig_03_emergency_fund.png` | Emergency fund coverage by education and gender |
| `output_figures/nfcs_fig_04_retirement.png` | Retirement savings participation by education |
