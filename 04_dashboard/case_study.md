# Portfolio Item 4 — Research Deployment & Findings Dashboard

## Real-Time Monitoring and Executive Communication for an Organization-Wide Listening Study

**The problem:** A survey deployed to 780 staff at a large research institution needed live deployment monitoring — leadership wanted to know response rates by department, flag lagging units, and track progress toward target N in real time. After fielding, the same dashboard needed to communicate findings to an executive audience that would not read a 40-page report.

**What I built:** A Plotly-based dashboard (exportable as standalone HTML or runnable as an interactive Dash app) with four panels: (1) cumulative response curve with target-N threshold line, (2) horizontal bar chart of adoption barriers ranked by prevalence, (3) department-level adoption rate bars with color-coded performance zones, (4) scatter plot of trust score vs. adoption rate by department to identify where low trust was driving low adoption versus other factors.

**Design decisions:** Single-file HTML export means any stakeholder can open the dashboard in a browser with no software installed — no Tableau license, no login, no server. Color encoding is deliberate: red/yellow/green on the adoption bars gives leadership an at-a-glance read without requiring them to interpret numbers. The trust-vs-adoption scatter immediately surfaces the departments where a trust intervention (vs. a training intervention) is the right lever.

**Artifact attached:** `dashboard.py` (generates standalone HTML) + `dashboard_static.html` (open directly in browser). Interactive Dash version can be enabled with one line uncomment.

---
*Methods: Python | Plotly | Dash | Data visualization | Executive communication | Survey deployment monitoring | HTML export*
