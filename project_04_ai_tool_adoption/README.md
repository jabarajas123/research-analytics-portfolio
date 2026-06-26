# Project 4: AI Tool Adoption Study
### Mixed-Methods Evaluation of an AI-Assisted Research Platform

---

**Decision moment studied:** Does a knowledge worker actually integrate an AI tool into their workflow after onboarding — and what determines whether they do?

**Methods:** Semi-structured interviews (n=18) | Behavioral log analysis (n=47, 8 weeks) | Usability survey (pre/post) | OLS regression | Kruskal-Wallis + Mann-Whitney U tests

**Domain:** Enterprise AI / UX Research / Research Operations

**Source:** Anonymized and retrofitted from a real evaluation. The methodology, findings, and data patterns are real; all organizational identifiers have been removed.

---

## The Problem

A research organization piloted an AI-assisted qualitative analysis platform across three teams. The platform was designed to reduce time spent on transcript coding and open-end processing. After onboarding, usage looked fine — week 1 sessions were strong across all teams.

By week 8, half the analysts had stopped using it.

The organization wanted to know: why? And more importantly: what separated the people who integrated the tool from those who didn't?

---

## What This Project Demonstrates

**Methodologically:**
- How to pair behavioral log data with qualitative interviews to explain quantitative patterns
- How to build and interpret an OLS regression with standardized coefficients
- How to derive a user typology from a 2×2 framework grounded in interview data — not invented categories
- How to use a Kruskal-Wallis test and when it is preferred over one-way ANOVA
- How to structure a semi-structured interview guide using the grand tour method (Barry, Point Forward)
- How to present failure mode frequency from qualitative coding as a prevalence chart (not a word cloud)

**Substantively:**
- Adoption is not a week-1 problem; it is a week-3 problem
- Trust calibration — not AI experience or technical skill — is the primary driver of integration
- A small behavioral act (logging failures) is a leading indicator of long-term adoption
- Four user archetypes emerge from the trust × effort matrix, each requiring a different intervention

---

## Artifacts

| File | What it is |
|---|---|
| `analysis.py` | Generates all 7 figures; methodology explainers embedded in docstrings |
| `interview_guide_ai_tool_adoption.docx` | Semi-structured interview guide with inline coaching notes |
| `survey_ai_tool_adoption.docx` | Pre/post usability survey (SUS-derived; trust calibration + workflow integration scales) |
| `figures/01_scatter_trust_integration.png` | Scatterplot: trust vs. integration by team (Pearson r) |
| `figures/02_boxplot_integration_by_team.png` | Box plot: integration distribution by team (Kruskal-Wallis) |
| `figures/03_ols_coefficient_plot.png` | OLS coefficient plot: predictors of integration (R²=0.XX) |
| `figures/04_line_adoption_trajectories.png` | Line chart: weekly session trajectories, integrators vs. resistors |
| `figures/05_typology_trust_effort.png` | 2×2 typology: four user archetypes (trust × effort) |
| `figures/06_bar_failure_modes.png` | Horizontal bar: failure mode prevalence from interview coding |
| `figures/07_box_failure_doc_by_segment.png` | Box plot: failure documentation rate by segment (Mann-Whitney U) |

---

## The Core Finding

The analyst who documents a failure — who clicks "flag as error" when the tool gives them something wrong — is 3× more likely to still be using the tool four weeks later.

The mechanism is not habit formation. It is cognitive: naming a failure converts a frustrating moment into information. That act of labeling prevents both overcorrection (abandonment) and undercorrection (continued blind trust). It is the difference between a user who calibrates and a user who polarizes.

This finding drove the primary recommendation: any onboarding redesign should include a structured failure-logging prompt in weeks 2–3, framed as a product contribution, not a quality check.

---

*Jeremy A. Barajas | Mixed-Methods Researcher | [barajas@sas.upenn.edu](mailto:barajas@sas.upenn.edu)*
