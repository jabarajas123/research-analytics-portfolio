"""
Generates 5 clean results figures tied to the 5 experiment designs
in the Experiment Design Showcase. All synthetic data.
Output: output_figures/exp_*.png
Run from: 03_data_analysis/
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

OUT = Path("output_figures")
OUT.mkdir(exist_ok=True)

# ── Shared style ───────────────────────────────────────────────────────────────
BLUE       = "#2D6A9F"
BLUE_LIGHT = "#9AC4E0"
ORANGE     = "#E87722"
GREEN      = "#2E7D52"
RED        = "#9B2335"
GRAY       = "#888888"
GRID_COLOR = "#E5EAF0"

def base_style(ax):
    ax.set_facecolor("#FAFBFC")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CCCCCC")
    ax.spines["bottom"].set_color("#CCCCCC")
    ax.tick_params(colors="#444444", labelsize=10)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Figure 1 — RCT: Cart Abandonment (Social Proof)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def fig_rct():
    fig, ax = plt.subplots(figsize=(6, 4.5))
    base_style(ax)

    conditions = ["Control\n(No Reviews)", "Social Proof\n(Star Ratings)"]
    rates = [12.1, 17.4]
    colors = [BLUE_LIGHT, BLUE]
    bars = ax.bar(conditions, rates, color=colors, width=0.45, zorder=3, edgecolor="white", linewidth=1.2)

    # Value labels
    for bar, rate in zip(bars, rates):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.4,
                f"{rate}%", ha="center", va="bottom", fontsize=12, fontweight="bold", color="#222222")

    # Delta annotation
    ax.annotate("", xy=(1, rates[1] + 0.3), xytext=(0, rates[0] + 0.3),
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1.5, linestyle="dashed"))
    ax.text(0.5, max(rates) + 2.2, "+5.3pp  (p = .003)", ha="center", fontsize=10,
            color=ORANGE, fontweight="bold")

    ax.set_ylabel("Purchase Completion Rate (%)", fontsize=10, color="#444444")
    ax.set_ylim(0, 26)
    ax.set_title("Design 01 — RCT: Social Proof on Checkout Page\nPurchase Completion Rate by Condition  (n=500/group)",
                 fontsize=11, fontweight="bold", color="#1A1A2E", pad=12)
    ax.text(0.99, 0.02, "Synthetic data — illustrative only", transform=ax.transAxes,
            fontsize=7, color=GRAY, ha="right", va="bottom", style="italic")

    fig.tight_layout()
    fig.savefig(OUT / "exp_01_rct_social_proof.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved: exp_01_rct_social_proof.png")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Figure 2 — Within-Subjects: SaaS Order / Contrast Effect
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def fig_within_subjects():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    base_style(ax)

    products = ["Client Product", "Competitor Interface"]
    order_client_first = [5.2, 4.4]
    order_competitor_first = [6.1, 4.6]

    x = np.arange(len(products))
    w = 0.32
    b1 = ax.bar(x - w/2, order_client_first, width=w, color=BLUE_LIGHT, label="Client product seen first",
                zorder=3, edgecolor="white", linewidth=1.2)
    b2 = ax.bar(x + w/2, order_competitor_first, width=w, color=BLUE, label="Competitor seen first",
                zorder=3, edgecolor="white", linewidth=1.2)

    for bar in list(b1) + list(b2):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.06,
                f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=10,
                fontweight="bold", color="#222222")

    # Contrast effect callout on client product bars
    ax.annotate("", xy=(x[0] + w/2, order_competitor_first[0]),
                xytext=(x[0] + w/2, order_client_first[0]),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5))
    ax.text(x[0] + w/2 + 0.08, (order_client_first[0] + order_competitor_first[0]) / 2,
            "+0.9\ncontrast\neffect", fontsize=8.5, color=ORANGE, fontweight="bold", va="center")

    ax.set_xticks(x)
    ax.set_xticklabels(products, fontsize=11)
    ax.set_ylabel("Mean Usability Rating  (1–7 scale)", fontsize=10, color="#444444")
    ax.set_ylim(0, 8)
    ax.legend(fontsize=9, framealpha=0.7, loc="upper right")
    ax.set_title("Design 02 — Within-Subjects: Order Effect on Usability Ratings\nMean Rating by Product and Presentation Order  (n=52)",
                 fontsize=11, fontweight="bold", color="#1A1A2E", pad=12)
    ax.text(0.99, 0.02, "Synthetic data — illustrative only", transform=ax.transAxes,
            fontsize=7, color=GRAY, ha="right", va="bottom", style="italic")

    fig.tight_layout()
    fig.savefig(OUT / "exp_02_within_subjects_order.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved: exp_02_within_subjects_order.png")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Figure 3 — Survey Experiment: 2×2 Calorie Label Factorial
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def fig_factorial():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    base_style(ax)

    # Mean calories selected per 2x2 cell
    # Rows: label absent / label present
    # Cols: low motivation / high motivation
    cells = {
        "No Label\nLow Motivation":   820,
        "No Label\nHigh Motivation":  710,
        "Calorie Label\nLow Motivation":  790,
        "Calorie Label\nHigh Motivation": 595,
    }
    labels = list(cells.keys())
    values = list(cells.values())
    colors = [BLUE_LIGHT, BLUE_LIGHT, BLUE, BLUE]
    hatches = ["", "///", "", "///"]

    bars = ax.bar(range(4), values, color=colors, hatch=hatches, width=0.5,
                  zorder=3, edgecolor="white", linewidth=1.2)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 8,
                f"{val} cal", ha="center", va="bottom", fontsize=10, fontweight="bold", color="#222222")

    ax.set_xticks(range(4))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Mean Calories Selected", fontsize=10, color="#444444")
    ax.set_ylim(400, 980)

    # Interaction annotation — placed above the lowest bar to avoid watermark
    ax.annotate("Strongest effect:\nlabel × high motivation",
                xy=(3, 595), xytext=(1.6, 470),
                fontsize=8.5, color=ORANGE, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

    # Legend patches
    p1 = mpatches.Patch(color=BLUE_LIGHT, label="No Calorie Label")
    p2 = mpatches.Patch(color=BLUE, label="Calorie Label Present")
    ax.legend(handles=[p1, p2], fontsize=9, framealpha=0.7, loc="upper right")

    ax.set_title("Design 03 — Survey Experiment: 2×2 Calorie Label Factorial\nMean Calories Selected by Label Condition and Health Motivation  (n=150/cell)",
                 fontsize=11, fontweight="bold", color="#1A1A2E", pad=12)
    ax.text(0.01, 0.02, "Synthetic data — illustrative only", transform=ax.transAxes,
            fontsize=7, color=GRAY, ha="left", va="bottom", style="italic")

    fig.tight_layout()
    fig.savefig(OUT / "exp_03_factorial_calorie_label.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved: exp_03_factorial_calorie_label.png")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Figure 4 — DiD: Retail Incentive Program
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def fig_did():
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    base_style(ax)

    months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
              "Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    x = np.arange(len(months))
    rollout = 6  # index where program starts (Jan)

    # Synthetic monthly revenue ($K)
    treated = [142, 138, 145, 141, 144, 140,  # pre
               155, 162, 168, 171, 165, 174]  # post
    control = [108, 106, 110, 107, 109, 108,  # pre
               112, 114, 116, 115, 113, 116]  # post

    ax.plot(x, treated, color=BLUE, linewidth=2.2, marker="o", markersize=5, label="Treated stores (n=12)", zorder=3)
    ax.plot(x, control, color=GRAY, linewidth=2.2, marker="s", markersize=5, label="Control stores (n=8)", zorder=3)

    # Rollout line
    ax.axvline(x=rollout - 0.5, color=ORANGE, linewidth=1.5, linestyle="--", zorder=2)
    ax.text(rollout - 0.4, max(treated) + 2, "Incentive\nprogram\nrollout",
            fontsize=8.5, color=ORANGE, fontweight="bold", va="top")

    # DiD gap annotation at last point
    gap_x = len(months) - 1
    ax.annotate("", xy=(gap_x, treated[-1]), xytext=(gap_x, control[-1] + (treated[-1] - control[-1]) / 2 + 15),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))
    ax.annotate("", xy=(gap_x, control[-1]), xytext=(gap_x, control[-1] + (treated[-1] - control[-1]) / 2 - 15),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))
    ax.text(gap_x + 0.1, (treated[-1] + control[-1]) / 2,
            "DiD\nestimate\n+$58K", fontsize=8.5, color=RED, fontweight="bold", va="center")

    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=9)
    ax.set_ylabel("Monthly Revenue ($K)", fontsize=10, color="#444444")
    ax.set_ylim(85, 200)
    ax.legend(fontsize=9, framealpha=0.7, loc="upper left")
    ax.set_title("Design 04 — Quasi-Experimental DiD: Retail Incentive Program\nMonthly Revenue by Store Group, Pre/Post Rollout",
                 fontsize=11, fontweight="bold", color="#1A1A2E", pad=12)
    ax.text(0.99, 0.02, "Synthetic data — illustrative only", transform=ax.transAxes,
            fontsize=7, color=GRAY, ha="right", va="bottom", style="italic")

    fig.tight_layout()
    fig.savefig(OUT / "exp_04_did_retail_incentive.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved: exp_04_did_retail_incentive.png")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Figure 5 — Five-Arm Nudge A/B Test
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def fig_nudge():
    fig, ax = plt.subplots(figsize=(7.5, 5))
    base_style(ax)
    ax.yaxis.grid(False)
    ax.xaxis.grid(True, color=GRID_COLOR, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    arms = [
        "A — Control\n(Standard upgrade message)",
        "B — Social Proof\n(Descriptive norm)",
        "C — Implementation\nIntention (planning prompt)",
        "D — Loss Frame\n(Feature expiry)",
        "E — Fresh Start\n(Temporal landmark)",
    ]
    rates = [19.8, 24.3, 31.2, 27.6, 29.1]
    colors = [GRAY, BLUE_LIGHT, BLUE, RED, GREEN]

    y = np.arange(len(arms))
    bars = ax.barh(y, rates, color=colors, height=0.52, zorder=3, edgecolor="white", linewidth=1.0)
    ax.invert_yaxis()

    for bar, rate in zip(bars, rates):
        ax.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height() / 2,
                f"{rate}%", va="center", fontsize=10, fontweight="bold", color="#222222")

    # Baseline dotted line — arm A label already says "Control", no text needed
    ax.axvline(x=rates[0], color=GRAY, linewidth=1.2, linestyle=":", zorder=2)

    # Best performer callout — arm C (implementation intention)
    ax.annotate("Best performer\n(+11.4pp vs. control)",
                xy=(31.2, 2), xytext=(34, 3.5),
                fontsize=8.5, color=BLUE, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))

    ax.set_yticks(y)
    ax.set_yticklabels(arms, fontsize=9.5)
    ax.set_xlabel("7-Day Free-to-Paid Conversion Rate (%)", fontsize=10, color="#444444")
    ax.set_xlim(0, 42)
    ax.set_title("Design 05 — Five-Arm Behavioral Nudge Test\nConversion Rate by Message Framing  (n=200/arm)",
                 fontsize=11, fontweight="bold", color="#1A1A2E", pad=12)
    ax.text(0.99, 0.02, "Synthetic data — illustrative only", transform=ax.transAxes,
            fontsize=7, color=GRAY, ha="right", va="bottom", style="italic")

    fig.tight_layout()
    fig.savefig(OUT / "exp_05_nudge_five_arm.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved: exp_05_nudge_five_arm.png")


if __name__ == "__main__":
    fig_rct()
    fig_within_subjects()
    fig_factorial()
    fig_did()
    fig_nudge()
    print("\nAll 5 experiment figures saved to output_figures/")
