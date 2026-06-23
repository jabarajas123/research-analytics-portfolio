# Research & Analytics Portfolio

Applied research portfolio demonstrating quantitative analysis, qualitative methods,
automation pipelines, and experimental design. Work draws on methods from behavioral
science, survey research, and policy analysis.

---

## Projects

### 01 | Survey Research Methods
Showcase document demonstrating question design, response scale construction, sampling
strategy, and validity considerations for survey-based research.

**Skills:** Questionnaire design; Likert and semantic differential scales; sampling frames;
cognitive interviewing; construct validity.

→ `01_survey_research/Survey Methods Showcase.docx`

---

### 02 | Qualitative Research Automation Pipeline
Two-script pipeline for processing and coding large volumes of interview transcripts.

**`transcript_cleaner.py`** — Pre-processing for Atlas.ti / Dedoose / LLM pipelines.
Ingests raw .txt or .docx exports from Teams, Zoom, or Otter; strips timestamps and
noise artifacts; detects speaker turns via regex; merges consecutive same-speaker turns;
supports interactive speaker rename; exports three formats (Atlas.ti plain text,
Atlas.ti Word, Dedoose CSV).

**`transcript_pipeline.py`** — LLM-based thematic coding at scale.
Chunks transcripts to fit within model context limits; sends each chunk to GPT-4o with
a structured codebook prompt; returns verbatim quotes and analytic memos per theme;
exports a coded CSV and a Markdown thematic summary report.

**Skills:** Regex parsing; NLP pre-processing; LLM prompting with structured output;
qualitative codebook design; Atlas.ti and Dedoose compatibility.

→ `02_automation_pipeline/`

---

### 03 | Experimental Data Analysis
Five figures demonstrating analysis and visualization for common experimental designs
encountered in applied behavioral and product research.

| Figure | Design | Key Technique |
|---|---|---|
| RCT — Social Proof | Between-subjects | Chi-square, effect size |
| Within-Subjects Order Effect | Counterbalanced | Contrast effect, order testing |
| 2×2 Factorial | Full factorial | Interaction plot |
| Difference-in-Differences | Panel data | DiD estimator, parallel trends |
| 5-Arm Behavioral Nudge Test | Multi-arm RCT | Bonferroni correction |

**Skills:** Experimental design; matplotlib publication figures; effect size reporting;
multiple comparison correction; DiD estimation.

→ `03_data_analysis/experiment_figures.py`

---

### 04 | Interactive Dashboard
Static HTML dashboard demonstrating data visualization layout for stakeholder-facing
reporting.

→ `04_dashboard/`

---

### 05 | Qualitative Methods Showcase
Four analytical visualizations produced from qualitative research:

- **Intervention Opportunity Matrix** — 2×2 urgency vs. impact prioritization
- **Stakeholder Typology** — four-quadrant archetype map from interview coding
- **Experience Journey Map** — sentiment trajectory with retention funnel
- **Affinity Cluster Diagram** — thematic groupings from 28 coded interviews

**Skills:** Thematic analysis; stakeholder mapping; journey mapping; inductive coding
(Strauss & Corbin); matplotlib custom diagrams.

→ `05_qualitative_methods/`

---

### 06 | Experiment Design Showcase
Design documents for five experiments spanning behavioral, product, and policy research
contexts. Each design includes research question, arms/conditions, outcome measures,
power calculations, analysis plan, and the specific behavioral mechanism being tested.

Behavioral mechanisms covered: descriptive norms (Cialdini), implementation intentions
(Gollwitzer), loss aversion (Kahneman & Tversky), temporal landmarks (Milkman & Dai).

→ `06_experiment_design/Experiment Design Showcase.docx`

---

### 07 | NFCS 2024 Financial Capability Analysis
Weighted analysis of the 2024 National Financial Capability Study (n ≈ 25,500).
Replicates and extends core findings on financial literacy, fragility, emergency savings,
and retirement participation across demographic subgroups.

All estimates use the FINRA-provided national post-stratification weight (`wgt_n2`).
Script is written as an annotated teaching document — every analytical decision
is explained inline.

**Key findings:**
- Mean financial literacy score: 3.26 / 7 nationally; 4.10 for college graduates vs. 1.75 for adults without a HS diploma
- 36% of U.S. adults cannot cover a $2,000 emergency; 68% among households under $25K
- 52% have no emergency fund; gap persists within every education tier by gender
- 58pp gap in employer retirement plan participation between college grads and no-HS diploma holders

**Skills:** Weighted survey analysis; construct scoring; numpy weighted mean; subgroup
estimation; demographic disparity visualization.

→ `07_nfcs_analysis/`

---

## Technical Stack

| Domain | Tools |
|---|---|
| Data Analysis | Python, pandas, numpy |
| Visualization | matplotlib |
| Document Generation | python-docx, reportlab |
| NLP / LLM | OpenAI API (GPT-4o), structured JSON output |
| Qualitative Tools | Atlas.ti compatible, Dedoose compatible |
| Survey | Qualtrics-compatible design |

---

## Contact

Available for quantitative research, qualitative analysis, survey design, automation
pipelines, and experiment design and analysis.
