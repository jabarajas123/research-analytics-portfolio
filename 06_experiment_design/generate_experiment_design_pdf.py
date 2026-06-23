"""
Experimental Design Showcase PDF
-----------------------------------
Demonstrates 5 research design approaches with structure, rationale, and client value.
Covers between-subjects, within-subjects, survey experiment, pre/post with control,
and a behavioral nudge A/B test.

Run:  python3 generate_experiment_design_pdf.py
Output: experiment_design_showcase.pdf
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

OUTPUT = Path("experiment_design_showcase.pdf")

BLUE        = colors.HexColor("#2D6A9F")
BLUE_LIGHT  = colors.HexColor("#E8F2FB")
ORANGE      = colors.HexColor("#E87722")
ORANGE_LIGHT= colors.HexColor("#FEF3E8")
GREEN       = colors.HexColor("#2E7D52")
GREEN_LIGHT = colors.HexColor("#E8F5EE")
PURPLE      = colors.HexColor("#6A4C93")
PURPLE_LIGHT= colors.HexColor("#EDE8F8")
RED         = colors.HexColor("#9B2335")
RED_LIGHT   = colors.HexColor("#FAEAEC")
GRAY_LINE   = colors.HexColor("#D0D8E4")
GRAY_TEXT   = colors.HexColor("#555555")
DARK        = colors.HexColor("#1A1A2E")
WHITE       = colors.white

W = 6.3 * inch


def S():
    return {
        "cover_title": ParagraphStyle("ct", fontName="Helvetica-Bold", fontSize=28,
            textColor=WHITE, alignment=TA_CENTER, leading=36, spaceAfter=6),
        "cover_sub": ParagraphStyle("cs", fontName="Helvetica", fontSize=11,
            textColor=colors.HexColor("#C8D8EC"), alignment=TA_CENTER, leading=17),
        "cover_name": ParagraphStyle("cn", fontName="Helvetica-Bold", fontSize=13,
            textColor=WHITE, alignment=TA_CENTER, spaceAfter=4),
        "cover_tagline": ParagraphStyle("cg", fontName="Helvetica-Oblique", fontSize=10,
            textColor=colors.HexColor("#A8C0DC"), alignment=TA_CENTER),
        "method_title": ParagraphStyle("mt", fontName="Helvetica-Bold", fontSize=15,
            textColor=BLUE, spaceAfter=4, spaceBefore=4),
        "method_desc": ParagraphStyle("md", fontName="Helvetica", fontSize=10,
            textColor=GRAY_TEXT, leading=15, spaceAfter=8),
        "q_label": ParagraphStyle("ql", fontName="Helvetica-Bold", fontSize=9,
            textColor=ORANGE, spaceAfter=2, spaceBefore=10),
        "q_text": ParagraphStyle("qt", fontName="Helvetica", fontSize=10.5,
            textColor=DARK, leading=15, spaceAfter=4),
        "q_note": ParagraphStyle("qn", fontName="Helvetica-Oblique", fontSize=8.5,
            textColor=ORANGE, spaceAfter=4),
        "callout_head": ParagraphStyle("ch", fontName="Helvetica-Bold", fontSize=9,
            textColor=BLUE, spaceAfter=3),
        "callout_head_o": ParagraphStyle("cho", fontName="Helvetica-Bold", fontSize=9,
            textColor=ORANGE, spaceAfter=3),
        "callout_head_g": ParagraphStyle("chg", fontName="Helvetica-Bold", fontSize=9,
            textColor=GREEN, spaceAfter=3),
        "callout_head_r": ParagraphStyle("chr", fontName="Helvetica-Bold", fontSize=9,
            textColor=RED, spaceAfter=3),
        "callout_body": ParagraphStyle("cb", fontName="Helvetica", fontSize=9,
            textColor=DARK, leading=13),
        "intro_body": ParagraphStyle("ib", fontName="Helvetica", fontSize=10.5,
            textColor=DARK, leading=16, spaceAfter=8),
        "toc_item": ParagraphStyle("ti", fontName="Helvetica", fontSize=10.5,
            textColor=DARK, leading=18, leftIndent=20),
        "table_cell": ParagraphStyle("tc", fontName="Helvetica", fontSize=9, leading=12),
        "table_cell_bold": ParagraphStyle("tcb", fontName="Helvetica-Bold", fontSize=9, leading=12),
        "design_cell": ParagraphStyle("dc", fontName="Helvetica", fontSize=9.5,
            textColor=DARK, leading=14),
        "design_cell_bold": ParagraphStyle("dcb", fontName="Helvetica-Bold", fontSize=9.5,
            textColor=DARK, leading=14),
    }


def hr(color=GRAY_LINE, sb=4, sa=8):
    return HRFlowable(width="100%", thickness=0.5, color=color, spaceBefore=sb, spaceAfter=sa)


def callout(head, body, bg=BLUE_LIGHT, head_key="callout_head", styles=None):
    t = Table([[Paragraph(head, styles[head_key]),
                Paragraph(body, styles["callout_body"])]],
              colWidths=[1.1*inch, W - 1.1*inch - 0.3*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),bg),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
    ]))
    return t


def section_divider(num, title, styles):
    t = Table([[
        Table([[Paragraph(f"DESIGN {num:02d}", ParagraphStyle(
            "mb", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, alignment=TA_CENTER))]],
              colWidths=[0.85*inch],
              style=TableStyle([("BACKGROUND",(0,0),(-1,-1),BLUE),
                                ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
                                ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6)])),
        Paragraph(title, styles["method_title"]),
    ]], colWidths=[0.95*inch, W - 0.95*inch])
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                           ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
                           ("LEFTPADDING",(0,0),(-1,-1),0)]))
    return t


def design_table(rows_data, col_widths=None, header_color=BLUE):
    if col_widths is None:
        col_widths = [1.5*inch, W - 1.5*inch]
    data = []
    for row_type, cells in rows_data:
        if row_type == "header":
            data.append([Paragraph(c, ParagraphStyle("th", fontName="Helvetica-Bold",
                fontSize=9, textColor=WHITE)) for c in cells])
        elif row_type == "bold":
            data.append([Paragraph(c, ParagraphStyle("rb", fontName="Helvetica-Bold",
                fontSize=9, textColor=DARK)) for c in cells])
        else:
            data.append([Paragraph(c, ParagraphStyle("rn", fontName="Helvetica",
                fontSize=9, textColor=DARK, leading=13)) for c in cells])

    num_headers = sum(1 for r, _ in rows_data if r == "header")
    t = Table(data, colWidths=col_widths)
    style_cmds = [
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("GRID",(0,0),(-1,-1),0.3,GRAY_LINE),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),8),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]
    for i, (row_type, _) in enumerate(rows_data):
        if row_type == "header":
            style_cmds.append(("BACKGROUND",(0,i),(-1,i),header_color))
            style_cmds.append(("TEXTCOLOR",(0,i),(-1,i),WHITE))
        elif i % 2 == 0:
            style_cmds.append(("BACKGROUND",(0,i),(-1,i),BLUE_LIGHT))
    t.setStyle(TableStyle(style_cmds))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(GRAY_LINE)
    canvas.setLineWidth(0.5)
    canvas.line(0.85*inch, 0.65*inch, 7.65*inch, 0.65*inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY_TEXT)
    canvas.drawString(0.85*inch, 0.48*inch,
                      "Jeremy Barajas | Experimental Design Showcase | barajas@alumni.usc.edu")
    canvas.drawRightString(7.65*inch, 0.48*inch, f"Page {doc.page}")
    canvas.restoreState()


def build():
    styles = S()
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter,
                            rightMargin=0.85*inch, leftMargin=0.85*inch,
                            topMargin=0.85*inch, bottomMargin=1.0*inch)
    story = []

    # ── Cover ─────────────────────────────────────────────────────────────────
    cover = Table([[Paragraph("Experimental &\nResearch Design Showcase", styles["cover_title"])]],
                  colWidths=[W])
    cover.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),BLUE),
                                ("TOPPADDING",(0,0),(-1,-1),44),("BOTTOMPADDING",(0,0),(-1,-1),20),
                                ("LEFTPADDING",(0,0),(-1,-1),24),("RIGHTPADDING",(0,0),(-1,-1),24)]))
    story.append(cover)
    sub = Table([[Paragraph(
        "Five research design approaches — with structure, hypotheses, power analysis rationale,<br/>"
        "and what each design can and cannot tell you.",
        styles["cover_sub"])]],
        colWidths=[W])
    sub.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#1E4F7A")),
                              ("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),18),
                              ("LEFTPADDING",(0,0),(-1,-1),24),("RIGHTPADDING",(0,0),(-1,-1),24)]))
    story.append(sub)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Jeremy Barajas  |  Behavioral Scientist & Mixed-Methods Researcher", styles["cover_name"]))
    story.append(Paragraph("RAND Corporation  ·  University of Pennsylvania (M.B.D.S.)  ·  USC (B.A. Psychology, Honors)", styles["cover_tagline"]))
    story.append(Spacer(1, 0.3*inch))
    story.append(hr())
    story.append(Paragraph(
        "This document demonstrates five experimental and quasi-experimental research designs. "
        "Each exhibit includes the design logic, a worked example, power analysis considerations, "
        "threats to validity, and what the design is and is not suited to answer. "
        "Examples draw from AI adoption research, behavioral economics, and public policy evaluation.",
        styles["intro_body"]
    ))
    for item in [
        "Design 01  —  Between-Subjects Randomized Controlled Trial (RCT)",
        "Design 02  —  Within-Subjects / Repeated Measures",
        "Design 03  —  Survey Experiment (Vignette Factorial)",
        "Design 04  —  Pre/Post with Control Group (Quasi-Experimental)",
        "Design 05  —  Behavioral Nudge A/B Test",
    ]:
        story.append(Paragraph(item, styles["toc_item"]))
    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # DESIGN 01 — RCT
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    block = []
    block.append(section_divider(1, "Between-Subjects Randomized Controlled Trial", styles))
    block.append(hr())
    block.append(Paragraph(
        "The RCT is the gold standard for causal inference. Participants are randomly assigned "
        "to treatment or control conditions, eliminating systematic confounding. The between-subjects "
        "design means each participant sees only one condition — avoiding carryover effects "
        "but requiring larger samples than within-subjects designs.",
        styles["method_desc"]
    ))
    block.append(Paragraph("WORKED EXAMPLE", styles["q_label"]))
    block.append(Paragraph(
        "<b>Research question:</b>  Does a peer-testimonial onboarding message increase AI platform "
        "adoption rates more than a standard feature-focused message?",
        styles["q_text"]
    ))
    design_rows = [
        ("header", ["Component", "Specification"]),
        ("normal", ["Hypothesis", "Participants receiving peer-testimonial onboarding will show higher "
                    "7-day platform activation rates than those receiving feature-focused onboarding (one-tailed, α=.05)."]),
        ("normal", ["Conditions", "Control: standard feature walkthrough email (n=250)\n"
                    "Treatment: peer testimonial email — same length, same CTA (n=250)"]),
        ("normal", ["Randomization", "Stratified by department and seniority level to ensure balance across conditions."]),
        ("normal", ["Primary outcome", "Platform activation within 7 days of onboarding email (binary)."]),
        ("normal", ["Secondary outcomes", "Login frequency at 30 days; self-reported trust score (post-survey)."]),
        ("normal", ["Analysis", "Chi-square test on activation rate; logistic regression controlling for department, "
                    "tenure, and prior tool use."]),
        ("normal", ["Power", "Detecting Δ=10pp (30%→40% activation) with 80% power at α=.05 requires n=194/group. "
                    "N=250/group provides buffer for attrition."]),
        ("normal", ["IRB / Ethics", "Randomization to communication variants is standard organizational practice. "
                    "No deception; no sensitive data. Exempt review likely."]),
    ]
    block.append(design_table(design_rows, col_widths=[1.5*inch, W-1.5*inch]))
    block.append(Spacer(1, 0.1*inch))
    block.append(callout("WHY THIS\nDESIGN",
        "Only an RCT can establish that the peer message caused the difference in activation, "
        "rather than that high-adopters self-selected into peer-facing content. "
        "Without randomization, any observed difference is confounded by pre-existing motivation.",
        bg=BLUE_LIGHT, head_key="callout_head", styles=styles))
    block.append(Spacer(1, 0.06*inch))
    block.append(callout("LIMITATIONS",
        "Cannot be used when random assignment is logistically impossible (e.g., whole teams must "
        "receive the same treatment) or ethically problematic. Requires sufficient N. "
        "External validity depends on whether the sample represents the full population of interest.",
        bg=RED_LIGHT, head_key="callout_head_r", styles=styles))
    story.append(KeepTogether(block))
    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # DESIGN 02 — Within-Subjects
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    block = []
    block.append(section_divider(2, "Within-Subjects / Repeated Measures", styles))
    block.append(hr())
    block.append(Paragraph(
        "In a within-subjects design, each participant experiences all conditions. "
        "This eliminates between-person variance from the error term, dramatically increasing "
        "statistical power — the same effect is detectable with roughly half the sample of a "
        "between-subjects design. The key risk is carryover: exposure to one condition "
        "contaminates responses to subsequent conditions.",
        styles["method_desc"]
    ))
    block.append(Paragraph("WORKED EXAMPLE", styles["q_label"]))
    block.append(Paragraph(
        "<b>Research question:</b>  Do users rate AI-assisted document summaries differently "
        "when they know the source (AI vs. human analyst) than when they don't?",
        styles["q_text"]
    ))
    design_rows = [
        ("header", ["Component", "Specification"]),
        ("normal", ["Hypothesis", "Participants will rate identical summaries lower when labeled 'AI-generated' "
                    "than when labeled 'analyst-written,' controlling for actual quality (H₁: label effect > 0)."]),
        ("normal", ["Conditions", "Each participant rates 6 summaries:\n"
                    "  · 2 labeled 'AI-generated'\n"
                    "  · 2 labeled 'written by analyst'\n"
                    "  · 2 unlabeled (baseline)\n"
                    "Order counterbalanced via Latin square."]),
        ("normal", ["Stimuli", "Summaries are held constant for quality across conditions — same text, different label. "
                    "3 high-quality, 3 mediocre to test label × quality interaction."]),
        ("normal", ["Outcome", "Perceived quality rating (1–7); willingness to use in work product (binary)."]),
        ("normal", ["Analysis", "Repeated-measures ANOVA (label × quality); planned contrasts for AI vs. analyst label."]),
        ("normal", ["Carryover control", "Minimum 2 filler summaries between each target summary; "
                    "order randomized per participant."]),
        ("normal", ["Power", "Within-subjects correlation ≈.5 assumed; Cohen's d=0.4 detectable with n=52 at 80% power."]),
    ]
    block.append(design_table(design_rows, col_widths=[1.5*inch, W-1.5*inch]))
    block.append(Spacer(1, 0.1*inch))
    block.append(callout("WHY THIS\nDESIGN",
        "Each participant serves as their own control — removing individual differences in "
        "general quality standards from the analysis. The label effect is cleaner because we're "
        "measuring the same person's response to the same content under different attribution conditions.",
        bg=BLUE_LIGHT, head_key="callout_head", styles=styles))
    block.append(Spacer(1, 0.06*inch))
    block.append(callout("LIMITATIONS",
        "Demand characteristics: participants may guess the hypothesis after seeing multiple "
        "conditions and adjust responses. Carryover effects require careful stimulus sequencing. "
        "Not appropriate when treatment has permanent effects (training, learning) that cannot be undone.",
        bg=RED_LIGHT, head_key="callout_head_r", styles=styles))
    story.append(KeepTogether(block))
    story.append(Spacer(1, 0.25*inch))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # DESIGN 03 — Survey Experiment
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    block = []
    block.append(section_divider(3, "Survey Experiment (Vignette Factorial)", styles))
    block.append(hr())
    block.append(Paragraph(
        "A survey experiment embeds a randomized manipulation inside a survey instrument. "
        "Respondents are randomly assigned to receive different versions of a vignette — "
        "varying one or more factors — and their responses are compared. "
        "It combines the scale of a survey with the causal logic of an experiment, "
        "making it ideal for sensitive topics where observational methods can't separate cause from effect.",
        styles["method_desc"]
    ))
    block.append(Paragraph("WORKED EXAMPLE — 2×2 FACTORIAL DESIGN", styles["q_label"]))
    block.append(Paragraph(
        "<b>Research question:</b>  Does the source of a policy recommendation (expert vs. peer) "
        "and its framing (gain vs. loss) independently affect building code adoption intentions?",
        styles["q_text"]
    ))

    factorial_data = [
        ["", "<b>Gain Frame</b>\n('you could save $12K in repairs')", "<b>Loss Frame</b>\n('you risk $12K in damages')"],
        ["<b>Expert Source</b>\n(engineer/FEMA)", "Cell A\nn=125", "Cell B\nn=125"],
        ["<b>Peer Source</b>\n(neighbor/community member)", "Cell C\nn=125", "Cell D\nn=125"],
    ]
    ft_data = []
    for row in factorial_data:
        ft_data.append([Paragraph(c, ParagraphStyle("fc", fontName="Helvetica", fontSize=9,
                                                     textColor=DARK, leading=13, alignment=TA_CENTER))
                        for c in row])
    ft = Table(ft_data, colWidths=[1.9*inch, 2.2*inch, 2.2*inch])
    ft.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),BLUE), ("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("BACKGROUND",(0,0),(0,-1),BLUE), ("TEXTCOLOR",(0,0),(0,-1),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("GRID",(0,0),(-1,-1),0.5,GRAY_LINE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[BLUE_LIGHT, GREEN_LIGHT]),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))
    block.append(ft)
    block.append(Spacer(1, 0.08*inch))

    design_rows2 = [
        ("header", ["Component", "Specification"]),
        ("normal", ["Main effects tested", "H₁: Loss framing increases adoption intention vs. gain framing.\n"
                    "H₂: Expert source increases adoption intention vs. peer source."]),
        ("normal", ["Interaction effect", "H₃: Source × frame interaction — peer source may amplify loss framing "
                    "through social norm activation."]),
        ("normal", ["Outcome", "Adoption intention (1–7 Likert); willingness to invest in upgrade (binary)."]),
        ("normal", ["Analysis", "2×2 ANOVA; effect sizes (η²); planned contrasts for interaction."]),
        ("normal", ["Sample", "N=500 total (125/cell). ALP nationally representative panel targeting homeowners."]),
        ("normal", ["Power", "Main effect d=0.25 detectable with 80% power at n=100/cell. "
                    "125/cell provides adequate power for interaction term."]),
    ]
    block.append(design_table(design_rows2, col_widths=[1.5*inch, W-1.5*inch]))
    block.append(Spacer(1, 0.1*inch))
    block.append(callout("WHY THIS\nDESIGN",
        "Separates the effect of framing from the effect of source in a single study. "
        "Observational data cannot disentangle these because expert messengers tend to use "
        "evidence-based framing in practice. The factorial design provides clean estimates of each factor "
        "and their interaction at survey scale without a lab setting.",
        bg=BLUE_LIGHT, head_key="callout_head", styles=styles))
    block.append(Spacer(1, 0.06*inch))
    block.append(callout("LIMITATIONS",
        "Survey responses may not predict real behavior (intention-action gap). "
        "Vignettes simplify complex real-world decisions. Demand characteristics possible "
        "if the manipulation is transparent. Interaction effects require larger N than main effects.",
        bg=RED_LIGHT, head_key="callout_head_r", styles=styles))
    story.append(KeepTogether(block))
    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # DESIGN 04 — Pre/Post with Control
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    block = []
    block.append(section_divider(4, "Pre/Post with Control Group (Quasi-Experimental)", styles))
    block.append(hr())
    block.append(Paragraph(
        "When randomization is not feasible, a pre/post design with a non-equivalent control group "
        "uses the difference-in-differences (DiD) framework: comparing change in the treatment group "
        "to change in the control group removes shared temporal trends (regression to the mean, "
        "external events) from the causal estimate.",
        styles["method_desc"]
    ))
    block.append(Paragraph("WORKED EXAMPLE", styles["q_label"]))
    block.append(Paragraph(
        "<b>Research question:</b>  Did a targeted AI literacy training program increase "
        "platform adoption rates in the departments that received it, net of organization-wide trends?",
        styles["q_text"]
    ))

    # DiD table
    did_data = [
        ["", "<b>Pre-training\n(T1)</b>", "<b>Post-training\n(T2)</b>", "<b>Change (T2–T1)</b>"],
        ["<b>Treatment departments</b>\n(received training)", "31%", "52%", "+21pp"],
        ["<b>Control departments</b>\n(waitlisted)", "33%", "38%", "+5pp"],
        ["<b>DiD Estimate</b>\n(causal effect of training)", "", "", "<b>+16pp</b>"],
    ]
    did_rows = []
    for row in did_data:
        did_rows.append([Paragraph(c, ParagraphStyle("dd", fontName="Helvetica",
            fontSize=9, textColor=DARK, leading=13, alignment=TA_CENTER)) for c in row])
    didt = Table(did_rows, colWidths=[2.1*inch, 1.3*inch, 1.3*inch, 1.6*inch])
    didt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),BLUE),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("BACKGROUND",(0,0),(0,-1),BLUE),("TEXTCOLOR",(0,0),(0,-1),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("GRID",(0,0),(-1,-1),0.5,GRAY_LINE),
        ("ROWBACKGROUNDS",(0,1),(-1,-2),[BLUE_LIGHT,GREEN_LIGHT]),
        ("BACKGROUND",(0,-1),(-1,-1),colors.HexColor("#D4EDDA")),
        ("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold"),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
    ]))
    block.append(didt)
    block.append(Spacer(1, 0.08*inch))

    design_rows3 = [
        ("header", ["Component", "Specification"]),
        ("normal", ["Key assumption", "Parallel trends: in the absence of training, treatment and control "
                    "departments would have changed at the same rate. Validated by plotting pre-period trends."]),
        ("normal", ["Threats to validity", "Selection bias (treatment departments may differ in motivation); "
                    "spillover effects (control staff learn from treated colleagues); Hawthorne effect."]),
        ("normal", ["Analysis", "DiD regression with department and time fixed effects; "
                    "cluster-robust standard errors at department level."]),
        ("normal", ["Data required", "Adoption rate (or login data) at two time points for all departments; "
                    "training assignment records."]),
    ]
    block.append(design_table(design_rows3, col_widths=[1.5*inch, W-1.5*inch]))
    block.append(Spacer(1, 0.1*inch))
    block.append(callout("WHY THIS\nDESIGN",
        "Organizations rarely randomize training rollouts. The DiD design extracts a credible "
        "causal estimate from naturally occurring variation in who received the program first. "
        "The control group isolates the counterfactual — what would have happened without the training.",
        bg=BLUE_LIGHT, head_key="callout_head", styles=styles))
    block.append(Spacer(1, 0.06*inch))
    block.append(callout("LIMITATIONS",
        "Parallel trends assumption is untestable for the post-period and can be violated if "
        "treatment was assigned based on anticipated need. Cannot control for unobserved "
        "department-level changes coinciding with training rollout.",
        bg=RED_LIGHT, head_key="callout_head_r", styles=styles))
    story.append(KeepTogether(block))
    story.append(Spacer(1, 0.25*inch))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # DESIGN 05 — Behavioral Nudge A/B Test
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    block = []
    block.append(section_divider(5, "Behavioral Nudge A/B Test", styles))
    block.append(hr())
    block.append(Paragraph(
        "A nudge A/B test applies choice architecture principles — default settings, "
        "social proof, implementation intentions, loss framing — to shift behavior "
        "without restricting options. The A/B structure allows clean measurement of "
        "nudge effectiveness at scale. Rooted in Thaler & Sunstein (2008), "
        "Cialdini's social influence principles, and administrative burden theory.",
        styles["method_desc"]
    ))
    block.append(Paragraph("WORKED EXAMPLE — THREE-ARM TEST", styles["q_label"]))
    block.append(Paragraph(
        "<b>Research question:</b>  Which nudge type most effectively increases completion "
        "of optional AI platform training among non-adopter employees?",
        styles["q_text"]
    ))

    nudge_data = [
        ("header", ["Arm", "Nudge Type", "Message Version", "Mechanism", "n"]),
        ("normal", ["A (Control)", "None", "Standard reminder email: 'Training available.'", "—", "200"]),
        ("normal", ["B", "Social proof", "'78% of your colleagues in Research have already completed this training.'",
                    "Descriptive norm", "200"]),
        ("normal", ["C", "Implementation\nintention",
                    "'Block 30 minutes on your calendar this week to complete training.\n[Add to Calendar button]'",
                    "Planning prompt", "200"]),
        ("normal", ["D", "Loss frame",
                    "'Employees who haven\'t completed training by [date] will miss early access to new features.'",
                    "Loss aversion", "200"]),
    ]
    nt = Table([[Paragraph(c, ParagraphStyle("nc", fontName="Helvetica",
                fontSize=8.5, textColor=DARK, leading=13)) for c in row]
               for _, row in nudge_data],
               colWidths=[0.75*inch, 1.0*inch, 2.55*inch, 1.0*inch, 0.4*inch])
    nt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),BLUE),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTSIZE",(0,0),(-1,-1),8.5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[BLUE_LIGHT,WHITE,GREEN_LIGHT,ORANGE_LIGHT]),
        ("GRID",(0,0),(-1,-1),0.3,GRAY_LINE),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),6),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    block.append(nt)
    block.append(Spacer(1, 0.08*inch))

    design_rows4 = [
        ("header", ["Component", "Specification"]),
        ("normal", ["Primary outcome", "Training completion within 14 days of email (binary)."]),
        ("normal", ["Analysis", "Chi-square omnibus test across arms; pairwise comparisons with Bonferroni correction "
                    "(α=.05/3=.017 per comparison)."]),
        ("normal", ["Power", "Baseline completion rate ~20%. Detecting Δ=10pp with 80% power requires n=176/arm. "
                    "N=200/arm provides adequate buffer."]),
        ("normal", ["Ethics note", "Loss framing arm requires legal/HR review — language implying penalty must be "
                    "accurate and approved. Deception is not involved; all messages reflect real consequences."]),
        ("normal", ["Behavioral theory", "Arm B targets social proof (Cialdini, 1984); Arm C targets implementation "
                    "intention effect (Gollwitzer, 1999); Arm D targets loss aversion (Kahneman & Tversky, 1979)."]),
    ]
    block.append(design_table(design_rows4, col_widths=[1.5*inch, W-1.5*inch]))
    block.append(Spacer(1, 0.1*inch))
    block.append(callout("WHY THIS\nDESIGN",
        "Nudges are cheap to implement and, if effective, scale at near-zero marginal cost. "
        "The multi-arm test lets you identify which mechanism is doing the work — not just "
        "whether any intervention helps. Implementation intention theory predicts Arm C outperforms "
        "Arm B in high-intention / low-follow-through populations.",
        bg=BLUE_LIGHT, head_key="callout_head", styles=styles))
    block.append(Spacer(1, 0.06*inch))
    block.append(callout("LIMITATIONS",
        "Nudge effects often attenuate over time (habituation). This test measures short-term "
        "completion — sustained behavior change requires follow-up measurement. "
        "Social proof messages require accurate figures; fabricated norms backfire.",
        bg=RED_LIGHT, head_key="callout_head_r", styles=styles))

    # Closing
    block.append(Spacer(1, 0.3*inch))
    block.append(hr())
    closing = Table([[Paragraph(
        "<b>About this document:</b>  Design examples are informed by published research and "
        "professional evaluation work at RAND Corporation, including the RAND-EDA AI adoption study, "
        "FEMA building code adoption research, and the Gates Foundation behavioral segmentation project. "
        "All examples are illustrative. Full experimental design, IRB coordination, power analysis, "
        "and statistical analysis available as project services.",
        ParagraphStyle("clos", fontName="Helvetica", fontSize=9, textColor=GRAY_TEXT, leading=13)
    )]], colWidths=[W])
    closing.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F5F5F5")),
                                  ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
                                  ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12)]))
    block.append(closing)
    story.append(KeepTogether(block))

    doc.build(story, onLaterPages=on_page)
    print(f"Experiment design PDF saved to {OUTPUT}")


if __name__ == "__main__":
    build()
