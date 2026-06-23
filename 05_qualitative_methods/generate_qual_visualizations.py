"""
Qualitative Research Visualizations
--------------------------------------
Generates four publication-quality figures demonstrating qualitative analysis outputs:
  1. 2x2 opportunity matrix (urgency vs. impact)
  2. Stakeholder typology diagram (4 archetypes)
  3. Experience journey map (pain points over time)
  4. Affinity cluster diagram (thematic groupings from coded interviews)

Run:  python3 generate_qual_visualizations.py
Output: figures/ directory
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path

FIGURES = Path("figures")
FIGURES.mkdir(exist_ok=True)

BLUE        = "#2D6A9F"
BLUE_LIGHT  = "#C8DDF2"
ORANGE      = "#E87722"
ORANGE_LIGHT= "#FAD9BC"
GREEN       = "#2E7D52"
GREEN_LIGHT = "#B8DECA"
RED         = "#9B2335"
RED_LIGHT   = "#F2C0C8"
PURPLE      = "#6A4C93"
PURPLE_LIGHT= "#D4C4F0"
GRAY        = "#888888"
GRAY_LIGHT  = "#F2F4F7"
DARK        = "#1A1A2E"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Figure 1 — 2x2 Opportunity Matrix
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def fig_opportunity_matrix():
    fig, ax = plt.subplots(figsize=(9, 7.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Quadrant shading
    ax.fill_between([0, 5], [5, 5], [10, 10], color=ORANGE_LIGHT, alpha=0.5, zorder=0)  # quick wins
    ax.fill_between([5, 10], [5, 5], [10, 10], color=GREEN_LIGHT, alpha=0.5, zorder=0)  # strategic bets
    ax.fill_between([0, 5], [0, 0], [5, 5], color=GRAY_LIGHT, alpha=0.8, zorder=0)      # low priority
    ax.fill_between([5, 10], [0, 0], [5, 5], color=BLUE_LIGHT, alpha=0.5, zorder=0)     # invest/research

    # Divider lines
    ax.axhline(5, color=GRAY, linewidth=1.2, linestyle="--", alpha=0.6)
    ax.axvline(5, color=GRAY, linewidth=1.2, linestyle="--", alpha=0.6)

    # Quadrant labels
    quad_labels = [
        (2.5, 9.2, "QUICK WINS", ORANGE),
        (7.5, 9.2, "STRATEGIC BETS", GREEN),
        (2.5, 0.6, "LOW PRIORITY", GRAY),
        (7.5, 0.6, "INVEST & STUDY", BLUE),
    ]
    for x, y, label, color in quad_labels:
        ax.text(x, y, label, ha="center", va="center",
                fontsize=9, fontweight="bold", color=color, alpha=0.8)

    # Data points — building code stakeholder intervention opportunities
    points = [
        # (urgency, impact, label, color, size)
        (3.5, 8.2, "Plain-language\ncost-benefit summaries", ORANGE, 180),
        (4.2, 7.1, "Targeted social media\ncampaign (homeowners)", ORANGE, 150),
        (2.1, 6.8, "Local official\ntraining workshops", ORANGE, 130),
        (7.8, 8.8, "Peer ambassador\nprogram (builders)", GREEN, 200),
        (8.5, 7.5, "Insurance incentive\nalignment program", GREEN, 170),
        (6.8, 8.1, "Post-disaster\noutreach protocol", GREEN, 160),
        (9.1, 6.2, "Regional enforcement\ntask force", BLUE, 150),
        (7.2, 4.2, "National media\nawareness campaign", BLUE, 130),
        (1.8, 2.4, "Generic FAQ\ndocuments", GRAY, 100),
        (3.1, 1.9, "Annual conference\npresentations only", GRAY, 100),
        (2.8, 3.8, "Internal FEMA\nstaff newsletters", GRAY, 110),
        (5.8, 3.2, "Academic\npublications", BLUE, 110),
    ]

    for urg, imp, label, color, size in points:
        ax.scatter(urg, imp, s=size, color=color, zorder=5, edgecolors="white",
                   linewidth=1.5, alpha=0.9)
        # offset label to avoid overlap
        x_off = 0.25 if urg < 5 else -0.25
        ha = "left" if urg < 5 else "right"
        ax.annotate(label, (urg, imp),
                    xytext=(urg + x_off, imp + 0.45),
                    fontsize=7.5, ha=ha, va="bottom", color=DARK,
                    arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.7))

    ax.set_xlabel("Urgency / Time Sensitivity →", fontsize=11, labelpad=10, color=DARK)
    ax.set_ylabel("Potential Impact →", fontsize=11, labelpad=10, color=DARK)
    ax.set_title(
        "Intervention Opportunity Matrix\nFEMA Building Code Communication Strategies",
        fontsize=13, fontweight="bold", color=DARK, pad=14
    )
    ax.set_xticks([0, 2.5, 5, 7.5, 10])
    ax.set_xticklabels(["Low", "", "Medium", "", "High"], fontsize=9, color=GRAY)
    ax.set_yticks([0, 2.5, 5, 7.5, 10])
    ax.set_yticklabels(["Low", "", "Medium", "", "High"], fontsize=9, color=GRAY)

    # Legend
    legend_patches = [
        mpatches.Patch(color=ORANGE_LIGHT, label="Quick Wins (act now)"),
        mpatches.Patch(color=GREEN_LIGHT, label="Strategic Bets (high investment)"),
        mpatches.Patch(color=BLUE_LIGHT, label="Invest & Study (more research needed)"),
        mpatches.Patch(color=GRAY_LIGHT, label="Low Priority (reconsider)"),
    ]
    ax.legend(handles=legend_patches, loc="lower right", fontsize=8,
              framealpha=0.9, edgecolor=GRAY)

    plt.tight_layout()
    plt.savefig(FIGURES / "01_opportunity_matrix.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: 01_opportunity_matrix.png")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Figure 2 — Stakeholder Typology Diagram
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def fig_typology():
    fig, ax = plt.subplots(figsize=(10, 8.5))
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6.5, 6.5)
    ax.axis("off")

    # Background quadrants
    quad_rects = [
        (-6, 0, 6, 5.5, BLUE_LIGHT),
        (0, 0, 6, 5.5, GREEN_LIGHT),
        (-6, -5.5, 6, 5.5, ORANGE_LIGHT),
        (0, -5.5, 6, 5.5, RED_LIGHT),
    ]
    for x, y, w, h, color in quad_rects:
        rect = plt.Rectangle((x, y), w, h, color=color, alpha=0.4, zorder=0)
        ax.add_patch(rect)

    # Axes lines
    ax.axhline(0, color=DARK, linewidth=1.8, zorder=2)
    ax.axvline(0, color=DARK, linewidth=1.8, zorder=2)

    # Axis arrows
    ax.annotate("", xy=(6.2, 0), xytext=(-6.2, 0),
                arrowprops=dict(arrowstyle="->", color=DARK, lw=1.5))
    ax.annotate("", xy=(0, 5.7), xytext=(0, -5.7),
                arrowprops=dict(arrowstyle="->", color=DARK, lw=1.5))

    # Axis labels — placed outside the card area so they don't overlap
    ax.text(6.3, 0, "High Risk\nAwareness →", ha="left", va="center", fontsize=9, color=DARK)
    ax.text(-6.3, 0, "← Low Risk\nAwareness", ha="right", va="center", fontsize=9, color=DARK)
    ax.text(0, 6.2, "High Code\nCompliance ↑", ha="center", va="bottom", fontsize=9, color=DARK)
    ax.text(0, -6.2, "↓ Low Code\nCompliance", ha="center", va="top", fontsize=9, color=DARK)

    # Typology cards
    typologies = [
        # (x, y, name, subtitle, description, color, dot_color)
        (-3.2, 3.0, "THE CAUTIOUS\nCOMPLIER", "High compliance,\nlow risk awareness",
         "Follows codes because\nit's required, not because\nthey understand the risk.\nMotivated by rules, not beliefs.\nKey message: connect\nbehavior to outcomes.",
         BLUE_LIGHT, BLUE),
        (3.2, 3.0, "THE INFORMED\nADVOCATE", "High compliance,\nhigh risk awareness",
         "Understands why codes matter\nand acts accordingly.\nActs as peer champion.\nLeverage as messenger\nfor other segments.",
         GREEN_LIGHT, GREEN),
        (-3.2, -3.0, "THE DISENGAGED\nRESIDENT", "Low compliance,\nlow risk awareness",
         "Hasn't thought about\nhazard risk or codes.\nNeeds awareness-building\nbefore persuasion.\nKey barrier: salience.",
         ORANGE_LIGHT, ORANGE),
        (3.2, -3.0, "THE AWARE\nNON-ADOPTER", "Low compliance,\nhigh risk awareness",
         "Knows the risk but\ndoesn't comply — cost,\ntrust, or fatalism barrier.\nMost complex to move.\nNeeds tailored intervention.",
         RED_LIGHT, RED),
    ]

    for x, y, name, subtitle, desc, bg, dot_color in typologies:
        box = FancyBboxPatch((x - 2.5, y - 2.2), 5.0, 4.2,
                             boxstyle="round,pad=0.15",
                             facecolor="white", edgecolor=dot_color,
                             linewidth=2, zorder=3)
        ax.add_patch(box)

        ax.scatter([x], [y + 1.5], s=180, color=dot_color, zorder=5, edgecolors="white", linewidth=1.5)
        ax.text(x, y + 0.7, name, ha="center", va="center",
                fontsize=10, fontweight="bold", color=dot_color, zorder=5)
        ax.text(x, y + 0.1, subtitle, ha="center", va="center",
                fontsize=8, style="italic", color=GRAY, zorder=5)
        ax.text(x, y - 0.9, desc, ha="center", va="center",
                fontsize=7.5, color=DARK, zorder=5, linespacing=1.4)

    ax.set_title(
        "Building Code Stakeholder Typology\nDerived from Interview Analysis + Survey Segmentation (N=850)",
        fontsize=13, fontweight="bold", color=DARK, pad=16
    )

    plt.tight_layout()
    plt.savefig(FIGURES / "02_stakeholder_typology.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: 02_stakeholder_typology.png")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Figure 3 — Experience Journey Map
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def fig_journey_map():
    stages = ["Awareness", "Consideration", "Onboarding", "Early Use", "Habitual Use", "Advocacy"]
    n = len(stages)
    x = np.arange(n)

    # Sentiment scores (1=very negative, 5=very positive) for two personas
    adopter      = [2.2, 3.0, 2.5, 3.4, 4.3, 4.7]
    non_adopter  = [2.1, 2.8, 1.8, 1.6, np.nan, np.nan]

    pain_points = [
        "Never heard\nof the tool",
        "No clear use\ncase identified",
        "Confusing\nonboarding docs",
        "First outputs\nneed heavy editing",
        "Workflow\nintegrated",
        "Recommends\nto others",
    ]
    drop_off_points = [
        None,
        None,
        "←  40% drop off\n   here (no training)",
        "←  25% drop off\n   here (quality concerns)",
        None,
        None,
    ]

    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(14, 8.5),
                                   gridspec_kw={"height_ratios": [3, 1]})

    # Journey lines
    ax.plot(x, adopter, "o-", color=GREEN, linewidth=2.5, markersize=9,
            label="Adopter Persona", zorder=4)
    non_x = [i for i, v in enumerate(non_adopter) if not np.isnan(v)]
    non_y = [v for v in non_adopter if not np.isnan(v)]
    ax.plot(non_x, non_y, "s--", color=RED, linewidth=2, markersize=8,
            label="Non-Adopter Persona", zorder=4)

    # Sentiment zone fills
    ax.fill_between(x, adopter, 3, where=[v > 3 for v in adopter],
                    alpha=0.12, color=GREEN, interpolate=True)
    ax.fill_between(x, adopter, 3, where=[v < 3 for v in adopter],
                    alpha=0.12, color=RED, interpolate=True)

    # Pain point annotations — placed with explicit (x, y) targets to avoid overlap.
    # We use absolute data coords rather than relative offsets so each label lands
    # in a predictable position regardless of the line value at that stage.
    label_positions = [
        (0,   4.8),   # Awareness — high above the line
        (1,   1.4),   # Consideration — below the line
        (1.6, 3.8),   # Onboarding — shifted left and above the crowded zone
        (3.4, 1.5),   # Early Use — shifted right and below
        (4,   5.0),   # Habitual Use — above
        (5,   1.4),   # Advocacy — below
    ]
    for i, (pp, (tx, ty)) in enumerate(zip(pain_points, label_positions)):
        ax.annotate(pp, (i, adopter[i]),
                    xytext=(tx, ty),
                    fontsize=7.5, ha="center", color=DARK,
                    arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.5),
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                              edgecolor=GRAY, alpha=0.9, linewidth=0.6))

    # Drop-off annotations
    for i, dp in enumerate(drop_off_points):
        if dp and i < len(non_y):
            ax.annotate(dp, (i, non_y[i]),
                        xytext=(i + 0.6, non_y[i] + 0.1),
                        fontsize=7.5, color=RED,
                        arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))

    ax.set_xlim(-0.4, n - 0.6)
    ax.set_ylim(0.8, 5.8)
    ax.set_xticks(x)
    ax.set_xticklabels(stages, fontsize=10, fontweight="bold")
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["Very\nNegative", "Negative", "Neutral", "Positive", "Very\nPositive"],
                        fontsize=8.5)
    ax.set_ylabel("Experience Sentiment", fontsize=10, labelpad=8)
    ax.axhline(3, color=GRAY, linewidth=1, linestyle=":", alpha=0.7)
    ax.legend(loc="lower right", fontsize=9, framealpha=0.9)
    ax.set_title(
        "AI Platform Adoption Journey Map\nExperience sentiment by stage — Adopter vs. Non-Adopter persona",
        fontsize=13, fontweight="bold", color=DARK, pad=12
    )
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Bottom panel: retention funnel
    n_start = [780, 780, 540, 400, 305, 260]
    pcts = [f"{int(v/780*100)}%" for v in n_start]
    colors_bar = [GREEN if v > 400 else ORANGE if v > 300 else RED for v in n_start]
    ax2.bar(x, n_start, color=colors_bar, alpha=0.75, width=0.5, zorder=3)
    for i, (v, p) in enumerate(zip(n_start, pcts)):
        ax2.text(i, v + 12, f"{p}\n(n={v})", ha="center", fontsize=7.5, color=DARK)
    ax2.set_xticks(x)
    ax2.set_xticklabels(stages, fontsize=9)
    ax2.set_ylabel("Users Remaining", fontsize=9)
    ax2.set_title("Retention Funnel by Stage", fontsize=10, color=DARK, pad=6)
    ax2.set_ylim(0, 950)
    ax2.grid(axis="y", linestyle="--", alpha=0.3)

    plt.tight_layout(h_pad=1.5)
    plt.savefig(FIGURES / "03_journey_map.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: 03_journey_map.png")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Figure 4 — Affinity Cluster Diagram
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def fig_affinity_cluster():
    fig, ax = plt.subplots(figsize=(12, 9.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(-0.5, 10.5)  # extra headroom above top circles and below footnote
    ax.axis("off")

    clusters = [
        # (cx, cy, color, title, n_codes, sub_themes)
        (2.2, 6.8, BLUE, "Trust & Accuracy\nConcerns", 38, [
            '"hallucinations scare me"', '"I always double-check"',
            '"black box problem"', '"liability question"',
        ]),
        (6.0, 7.2, GREEN, "Workflow\nIntegration", 31, [
            '"fits naturally into my process"', '"had to change my habits"',
            '"saves 2 hrs/week on cleanup"', '"not compatible with our systems"',
        ]),
        (9.8, 6.8, ORANGE, "Training &\nOnboarding Gaps", 27, [
            '"no one showed us how"', '"documentation is confusing"',
            '"learned from a colleague"', '"trial and error mostly"',
        ]),
        (2.2, 2.8, PURPLE, "Organizational\nCulture", 24, [
            '"leadership doesn\'t use it either"', '"feels risky to my reputation"',
            '"my team resists change"', '"tacitly encouraged now"',
        ]),
        (6.0, 2.2, RED, "Privacy &\nSecurity", 19, [
            '"put confidential data in?"', '"where does it go?"',
            '"IT hasn\'t approved it"', '"HIPAA / FISMA concern"',
        ]),
        (9.8, 2.8, colors.HexColor("#C8A951") if False else "#C8A951", "Identity &\nExpertise", 15, [
            '"makes my job feel less special"', '"I\'m the expert, not the AI"',
            '"junior staff rely on it too much"', '"changes what I\'m valued for"',
        ]),
    ]

    cluster_colors_hex = [BLUE, GREEN, ORANGE, PURPLE, RED, "#C8A951"]

    for (cx, cy, color, title, n_codes, sub_themes), hex_color in zip(clusters, cluster_colors_hex):
        # Outer bubble
        outer = plt.Circle((cx, cy), 1.85, color=hex_color, alpha=0.12, zorder=1)
        inner = plt.Circle((cx, cy), 1.85, fill=False, edgecolor=hex_color,
                            linewidth=2.0, zorder=2)
        ax.add_patch(outer)
        ax.add_patch(inner)

        # Title
        ax.text(cx, cy + 1.45, title, ha="center", va="center",
                fontsize=9.5, fontweight="bold", color=hex_color, zorder=4)

        # Code count badge
        badge = plt.Circle((cx + 1.4, cy + 1.4), 0.32, color=hex_color, zorder=5)
        ax.add_patch(badge)
        ax.text(cx + 1.4, cy + 1.4, str(n_codes), ha="center", va="center",
                fontsize=8, fontweight="bold", color="white", zorder=6)

        # Sub-theme quotes
        y_offsets = [0.55, 0.05, -0.45, -0.95]
        for quote, y_off in zip(sub_themes, y_offsets):
            ax.text(cx, cy + y_off, f"• {quote}", ha="center", va="center",
                    fontsize=7, color=DARK, style="italic", zorder=4,
                    wrap=True)

    # Connecting lines between related clusters
    connections = [(0, 1), (1, 2), (0, 3), (3, 4), (4, 5), (1, 4)]
    centers = [(c[0], c[1]) for c in clusters]
    for i, j in connections:
        x1, y1 = centers[i]
        x2, y2 = centers[j]
        ax.plot([x1, x2], [y1, y2], "-", color=GRAY, linewidth=0.7,
                alpha=0.4, zorder=0)

    # Title — sits above ylim=10.5 ceiling, clear of the top cluster circles (which peak at ~8.55)
    ax.text(6.0, 10.0,
            "Affinity Cluster Map — AI Adoption Barriers\n"
            "Derived from thematic coding of 28 semi-structured interviews  |  "
            "Badge = number of coded segments",
            ha="center", va="center", fontsize=11, fontweight="bold", color=DARK)

    # Footnote — sits below ylim=-0.5 floor, clear of bottom cluster circles
    ax.text(6.0, -0.2,
            "Clusters identified via inductive open coding → axial coding → selective coding (Strauss & Corbin, 1990).  "
            "Line thickness reflects conceptual proximity identified in memos.",
            ha="center", va="center", fontsize=7.5, color=GRAY, style="italic")

    plt.tight_layout()
    plt.savefig(FIGURES / "04_affinity_clusters.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: 04_affinity_clusters.png")


if __name__ == "__main__":
    fig_opportunity_matrix()
    fig_typology()
    fig_journey_map()
    fig_affinity_cluster()
    print("\nAll qualitative visualization figures generated in figures/")
