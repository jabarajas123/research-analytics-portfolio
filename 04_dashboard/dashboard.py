"""
Research Deployment & Findings Dashboard
------------------------------------------
Interactive Plotly Dash dashboard for monitoring survey deployment,
tracking response rates, and communicating key findings to stakeholders.

Run:  python3 dashboard.py
      Open browser at http://127.0.0.1:8050
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

try:
    import dash
    from dash import dcc, html
    DASH_AVAILABLE = True
except ImportError:
    DASH_AVAILABLE = False

# ── Synthetic Data ────────────────────────────────────────────────────────────

np.random.seed(42)

DEPARTMENTS = [
    "Research", "Operations", "IT", "Policy", "Communications",
    "Finance", "HR", "Legal", "Executive", "External Affairs"
]

SURVEY_ITEMS = [
    "I understand how to use the AI tool.",
    "The AI tool saves me time on routine tasks.",
    "I trust the accuracy of AI-generated outputs.",
    "I am concerned about data privacy.",
    "My manager encourages AI adoption.",
    "I would recommend this tool to a colleague.",
]

ADOPTION_BARRIER_LABELS = [
    "Hallucination / accuracy concerns",
    "Lack of training",
    "No clear use case for my work",
    "Privacy / security concerns",
    "Tool is too slow",
    "Manager hasn't encouraged use",
    "Already have adequate tools",
]

def make_deployment_data():
    dates = pd.date_range("2025-10-01", periods=28, freq="D")
    cumulative = np.clip(np.cumsum(np.random.poisson(28, 28)), 0, 780)
    return pd.DataFrame({"date": dates, "responses": cumulative})

def make_dept_data():
    records = []
    dept_n = [45, 38, 52, 41, 29, 33, 47, 22, 18, 55]
    for dept, n in zip(DEPARTMENTS, dept_n):
        for item in SURVEY_ITEMS:
            records.append({
                "department": dept,
                "item": item,
                "mean_score": round(np.random.uniform(2.4, 4.6), 2),
                "n": n,
            })
    return pd.DataFrame(records)

def make_barrier_data():
    pcts = [38, 22, 17, 12, 6, 3, 2]
    return pd.DataFrame({"barrier": ADOPTION_BARRIER_LABELS, "pct": pcts})

def make_sentiment_data():
    return pd.DataFrame({
        "department": DEPARTMENTS,
        "adoption_rate": [72, 58, 81, 64, 70, 55, 63, 49, 88, 67],
        "trust_score":   [3.8, 3.2, 4.1, 3.5, 3.7, 3.0, 3.4, 2.9, 4.3, 3.6],
    })


# ── Static Export (no Dash required) ─────────────────────────────────────────

def export_static_dashboard():
    """Produces a single-file HTML dashboard without running a server."""
    deploy  = make_deployment_data()
    dept_df = make_dept_data()
    barriers = make_barrier_data()
    sentiment = make_sentiment_data()

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Cumulative Survey Responses Over Time",
            "Primary Adoption Barriers (% of non-adopters)",
            "Adoption Rate by Department (%)",
            "Trust Score vs. Adoption Rate by Department",
        ),
        vertical_spacing=0.18,
        horizontal_spacing=0.12,
    )

    # Panel 1: Response curve
    fig.add_trace(
        go.Scatter(
            x=deploy["date"], y=deploy["responses"],
            mode="lines+markers", name="Cumulative Responses",
            line=dict(color="#2D6A9F", width=2.5),
            marker=dict(size=5),
        ),
        row=1, col=1
    )
    fig.add_hline(y=780, line_dash="dash", line_color="#E87722",
                  annotation_text="Target N=780", row=1, col=1)

    # Panel 2: Barrier bar chart
    fig.add_trace(
        go.Bar(
            x=barriers["pct"], y=barriers["barrier"],
            orientation="h",
            marker_color=["#9B2335" if i == 0 else "#2D6A9F" for i in range(len(barriers))],
            name="Adoption Barriers",
            text=[f"{p}%" for p in barriers["pct"]],
            textposition="outside",
        ),
        row=1, col=2
    )

    # Panel 3: Adoption rate by dept
    fig.add_trace(
        go.Bar(
            x=sentiment["department"], y=sentiment["adoption_rate"],
            marker_color=[
                "#9B2335" if v < 60 else "#E87722" if v < 75 else "#2E8B57"
                for v in sentiment["adoption_rate"]
            ],
            name="Adoption Rate %",
            text=[f"{v}%" for v in sentiment["adoption_rate"]],
            textposition="outside",
        ),
        row=2, col=1
    )
    fig.add_hline(y=65, line_dash="dot", line_color="#888",
                  annotation_text="Org avg 65%", row=2, col=1)

    # Panel 4: Scatter trust vs adoption
    fig.add_trace(
        go.Scatter(
            x=sentiment["trust_score"],
            y=sentiment["adoption_rate"],
            mode="markers+text",
            text=sentiment["department"],
            textposition="top center",
            marker=dict(size=10, color="#2D6A9F", opacity=0.8),
            name="Dept",
        ),
        row=2, col=2
    )

    fig.update_layout(
        title=dict(
            text="<b>AI Platform Adoption — Employee Listening Dashboard</b><br>"
                 "<sup>Organization-wide deployment monitoring | N=780 respondents</sup>",
            font=dict(size=18),
            x=0.5,
        ),
        height=820,
        showlegend=False,
        font=dict(family="Arial", size=11),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    fig.update_xaxes(showgrid=True, gridcolor="#eee")
    fig.update_yaxes(showgrid=True, gridcolor="#eee")

    out_path = "dashboard_static.html"
    fig.write_html(out_path, include_plotlyjs="cdn")
    print(f"Static dashboard saved to {out_path}. Open in any browser.")
    return fig


# ── Dash App (interactive) ────────────────────────────────────────────────────

def run_dash_app():
    app = dash.Dash(__name__, title="AI Adoption Dashboard")

    deploy   = make_deployment_data()
    barriers = make_barrier_data()
    sentiment = make_sentiment_data()

    app.layout = html.Div(style={"fontFamily": "Arial", "padding": "20px"}, children=[
        html.H2("AI Platform Adoption — Employee Listening Dashboard",
                style={"textAlign": "center", "color": "#2D6A9F"}),
        html.P("Organization-wide deployment monitoring | N=780",
               style={"textAlign": "center", "color": "#666"}),

        html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"}, children=[
            dcc.Graph(figure=px.line(deploy, x="date", y="responses",
                                     title="Cumulative Responses",
                                     color_discrete_sequence=["#2D6A9F"])),
            dcc.Graph(figure=px.bar(barriers, x="pct", y="barrier", orientation="h",
                                    title="Adoption Barriers",
                                    color="pct", color_continuous_scale="RdYlGn_r")),
            dcc.Graph(figure=px.bar(sentiment, x="department", y="adoption_rate",
                                    title="Adoption Rate by Department",
                                    color="adoption_rate", color_continuous_scale="RdYlGn")),
            dcc.Graph(figure=px.scatter(sentiment, x="trust_score", y="adoption_rate",
                                        text="department", title="Trust Score vs. Adoption Rate")),
        ]),
    ])

    app.run(debug=False)


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if DASH_AVAILABLE:
        print("Generating static HTML export...")
        export_static_dashboard()
        print("\nTo run the interactive Dash app: uncomment run_dash_app() below.")
        # run_dash_app()
    else:
        print("Dash not installed. Install with: pip install dash")
        print("Generating static plotly export instead...")
        export_static_dashboard()
