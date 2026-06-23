"""
Survey Research Methods Showcase PDF
--------------------------------------
Demonstrates 7 survey question types with design rationale and client value.
Not a fielded instrument — a portfolio exhibit showing methodology depth.

Run:  python3 generate_survey_pdf.py
Output: survey_methods_showcase.pdf
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak, Flowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus.flowables import HRFlowable

OUTPUT = Path("survey_methods_showcase.pdf")

# ── Brand Colors ──────────────────────────────────────────────────────────────
BLUE       = colors.HexColor("#2D6A9F")
BLUE_LIGHT = colors.HexColor("#E8F2FB")
ORANGE     = colors.HexColor("#E87722")
ORANGE_LIGHT = colors.HexColor("#FEF3E8")
GREEN      = colors.HexColor("#2E7D52")
GREEN_LIGHT = colors.HexColor("#E8F5EE")
GRAY_LINE  = colors.HexColor("#D0D8E4")
GRAY_TEXT  = colors.HexColor("#555555")
DARK       = colors.HexColor("#1A1A2E")
WHITE      = colors.white
BLACK      = colors.black

W = 6.3 * inch  # usable page width


# ── Style Sheet ───────────────────────────────────────────────────────────────

def make_styles():
    base = getSampleStyleSheet()

    styles = {
        "cover_title": ParagraphStyle("cover_title",
            fontName="Helvetica-Bold", fontSize=28,
            textColor=WHITE, alignment=TA_CENTER, leading=36, spaceAfter=8),
        "cover_sub": ParagraphStyle("cover_sub",
            fontName="Helvetica", fontSize=12,
            textColor=colors.HexColor("#C8D8EC"), alignment=TA_CENTER, leading=18),
        "cover_name": ParagraphStyle("cover_name",
            fontName="Helvetica-Bold", fontSize=13,
            textColor=WHITE, alignment=TA_CENTER, spaceAfter=4),
        "cover_tagline": ParagraphStyle("cover_tagline",
            fontName="Helvetica-Oblique", fontSize=10,
            textColor=colors.HexColor("#A8C0DC"), alignment=TA_CENTER),

        "method_badge": ParagraphStyle("method_badge",
            fontName="Helvetica-Bold", fontSize=9,
            textColor=WHITE, alignment=TA_CENTER),
        "method_title": ParagraphStyle("method_title",
            fontName="Helvetica-Bold", fontSize=15,
            textColor=BLUE, spaceAfter=4, spaceBefore=4),
        "method_desc": ParagraphStyle("method_desc",
            fontName="Helvetica", fontSize=10,
            textColor=GRAY_TEXT, leading=15, spaceAfter=8),

        "q_label": ParagraphStyle("q_label",
            fontName="Helvetica-Bold", fontSize=9,
            textColor=ORANGE, spaceAfter=2, spaceBefore=10),
        "q_text": ParagraphStyle("q_text",
            fontName="Helvetica", fontSize=10.5,
            textColor=DARK, leading=15, spaceAfter=6),
        "q_note": ParagraphStyle("q_note",
            fontName="Helvetica-Oblique", fontSize=8.5,
            textColor=colors.HexColor("#E87722"), spaceAfter=4),
        "option": ParagraphStyle("option",
            fontName="Helvetica", fontSize=9.5,
            textColor=DARK, leading=14, leftIndent=14),
        "table_cell": ParagraphStyle("table_cell",
            fontName="Helvetica", fontSize=9, leading=12),
        "table_cell_bold": ParagraphStyle("table_cell_bold",
            fontName="Helvetica-Bold", fontSize=9, leading=12),

        "callout_head": ParagraphStyle("callout_head",
            fontName="Helvetica-Bold", fontSize=9,
            textColor=BLUE, spaceAfter=3),
        "callout_body": ParagraphStyle("callout_body",
            fontName="Helvetica", fontSize=9,
            textColor=DARK, leading=13),
        "callout_head_o": ParagraphStyle("callout_head_o",
            fontName="Helvetica-Bold", fontSize=9,
            textColor=ORANGE, spaceAfter=3),
        "callout_head_g": ParagraphStyle("callout_head_g",
            fontName="Helvetica-Bold", fontSize=9,
            textColor=GREEN, spaceAfter=3),

        "intro_body": ParagraphStyle("intro_body",
            fontName="Helvetica", fontSize=10.5,
            textColor=DARK, leading=16, spaceAfter=8),
        "toc_item": ParagraphStyle("toc_item",
            fontName="Helvetica", fontSize=10.5,
            textColor=DARK, leading=18, leftIndent=20),
        "footer": ParagraphStyle("footer",
            fontName="Helvetica", fontSize=8,
            textColor=GRAY_TEXT, alignment=TA_CENTER),
    }
    return styles


# ── Reusable Builders ─────────────────────────────────────────────────────────

def hr(color=GRAY_LINE, space_before=4, space_after=8):
    return HRFlowable(width="100%", thickness=0.5, color=color,
                      spaceBefore=space_before, spaceAfter=space_after)


def callout(head, body, bg=BLUE_LIGHT, head_style_key="callout_head", styles=None):
    content = [
        [Paragraph(head, styles[head_style_key]),
         Paragraph(body, styles["callout_body"])]
    ]
    t = Table(content, colWidths=[1.1 * inch, W - 1.1 * inch - 0.3 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
    ]))
    return t


def badge_row(label, styles):
    badge_cell = Table([[Paragraph(label, styles["method_badge"])]],
                       colWidths=[1.6 * inch])
    badge_cell.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLUE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [3, 3, 3, 3]),
    ]))
    return badge_cell


def section_divider(num, title, styles):
    label = f"METHOD {num:02d}"
    content = [[
        Table([[Paragraph(label, styles["method_badge"])]],
              colWidths=[0.85 * inch],
              style=TableStyle([
                  ("BACKGROUND", (0, 0), (-1, -1), BLUE),
                  ("TOPPADDING", (0, 0), (-1, -1), 4),
                  ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                  ("LEFTPADDING", (0, 0), (-1, -1), 6),
                  ("RIGHTPADDING", (0, 0), (-1, -1), 6),
              ])),
        Paragraph(title, styles["method_title"]),
    ]]
    t = Table(content, colWidths=[0.95 * inch, W - 0.95 * inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def option_row(options, ncols=2, styles=None):
    rows = [options[i:i+ncols] for i in range(0, len(options), ncols)]
    data = [["  ◯  " + cell for cell in row + [""] * (ncols - len(row))] for row in rows]
    col_w = W / ncols
    t = Table(data, colWidths=[col_w] * ncols)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("TEXTCOLOR", (0, 0), (-1, -1), DARK),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def likert_table(items, scale=None, col_w_override=None, styles=None):
    if scale is None:
        scale = ["Strongly\nDisagree", "Disagree", "Neutral", "Agree", "Strongly\nAgree"]
    n = len(scale)
    col_w = col_w_override if col_w_override else 0.72 * inch
    item_w = W - n * col_w

    header = [Paragraph("", styles["table_cell"])] + \
             [Paragraph(s, styles["table_cell_bold"]) for s in scale]
    data = [header]
    for i, item in enumerate(items):
        bg = BLUE_LIGHT if i % 2 == 0 else WHITE
        data.append([Paragraph(item, styles["table_cell"])] + ["◯"] * n)

    t = Table(data, colWidths=[item_w] + [col_w] * n)
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR",   (0, 0), (-1, 0), WHITE),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 8.5),
        ("ALIGN",       (1, 0), (-1, -1), "CENTER"),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("GRID",        (0, 0), (-1, -1), 0.3, GRAY_LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BLUE_LIGHT, WHITE]),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (0, -1), 8),
    ]))
    return t


def constant_sum_table(categories, styles):
    header = [
        Paragraph("Task / Activity Category", styles["table_cell_bold"]),
        Paragraph("Points Allocated\n(must sum to 100)", styles["table_cell_bold"]),
        Paragraph("Why this matters", styles["table_cell_bold"]),
    ]
    rationales = [
        "Captures cognitive burden of manual formatting work",
        "Core knowledge-work output — most sensitive to AI uplift",
        "Time recovered here signals adoption quality, not just frequency",
        "Often hidden labor; underreported in time-diary studies",
        "Catches residual variance; flags roles with unique workflows",
    ]
    data = [header]
    for cat, rat in zip(categories, rationales):
        data.append([
            Paragraph(cat, styles["table_cell"]),
            Paragraph("______", styles["table_cell"]),
            Paragraph(rat, styles["table_cell"]),
        ])
    data.append([
        Paragraph("TOTAL", styles["table_cell_bold"]),
        Paragraph("100", styles["table_cell_bold"]),
        Paragraph("", styles["table_cell"]),
    ])

    t = Table(data, colWidths=[2.2 * inch, 1.4 * inch, 2.7 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR",   (0, 0), (-1, 0), WHITE),
        ("FONTSIZE",    (0, 0), (-1, -1), 8.5),
        ("GRID",        (0, 0), (-1, -1), 0.3, GRAY_LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [BLUE_LIGHT, WHITE]),
        ("BACKGROUND",  (0, -1), (-1, -1), colors.HexColor("#D0E4F7")),
        ("FONTNAME",    (0, -1), (-1, -1), "Helvetica-Bold"),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


# ── Page Template (header/footer) ─────────────────────────────────────────────

def on_page(canvas, doc):
    canvas.saveState()
    # Footer line
    canvas.setStrokeColor(GRAY_LINE)
    canvas.setLineWidth(0.5)
    canvas.line(0.85 * inch, 0.65 * inch, 7.65 * inch, 0.65 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY_TEXT)
    canvas.drawString(0.85 * inch, 0.48 * inch, "Jeremy Barajas | Survey Research Methods Showcase | barajas@alumni.usc.edu")
    canvas.drawRightString(7.65 * inch, 0.48 * inch, f"Page {doc.page}")
    canvas.restoreState()


def on_first_page(canvas, doc):
    pass  # cover page — no header/footer


# ── Build Document ────────────────────────────────────────────────────────────

def build():
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        rightMargin=0.85 * inch,
        leftMargin=0.85 * inch,
        topMargin=0.85 * inch,
        bottomMargin=1.0 * inch,
    )
    S = make_styles()
    story = []

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # COVER
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    cover_data = [[
        Paragraph("Survey Research", S["cover_title"]),
    ]]
    cover = Table([[
        Paragraph("Survey Research<br/>Methods Showcase", S["cover_title"]),
    ]], colWidths=[W])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLUE),
        ("TOPPADDING", (0, 0), (-1, -1), 48),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
        ("LEFTPADDING", (0, 0), (-1, -1), 24),
        ("RIGHTPADDING", (0, 0), (-1, -1), 24),
    ]))
    story.append(cover)

    sub = Table([[
        Paragraph(
            "Seven question design techniques — with examples, rationale, and client value.<br/>"
            "A working reference for what a skilled survey researcher can do and why it matters.",
            S["cover_sub"]
        ),
    ]], colWidths=[W])
    sub.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1E4F7A")),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
        ("LEFTPADDING", (0, 0), (-1, -1), 24),
        ("RIGHTPADDING", (0, 0), (-1, -1), 24),
    ]))
    story.append(sub)
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph(
        "Jeremy Barajas  |  Behavioral Scientist & Mixed-Methods Researcher",
        S["cover_name"]
    ))
    story.append(Paragraph(
        "RAND Corporation  ·  University of Pennsylvania (M.B.D.S.)  ·  USC (B.A. Psychology, Honors)",
        S["cover_tagline"]
    ))
    story.append(Spacer(1, 0.35 * inch))
    story.append(hr(GRAY_LINE))
    story.append(Spacer(1, 0.15 * inch))

    # Intro
    story.append(Paragraph(
        "This document demonstrates seven survey question formats I use in professional research engagements. "
        "Each exhibit shows a real example question drawn from or inspired by my work at RAND Corporation and "
        "in consulting, followed by a design note explaining why the format was selected and what it "
        "enables analytically. The goal is to show that good survey design is not just writing questions — "
        "it is making deliberate choices about measurement, cognitive load, and the kind of insight the "
        "client actually needs.",
        S["intro_body"]
    ))

    # TOC
    toc_items = [
        "01  Adaptive Branching Logic — routing respondents by eligibility",
        "02  Likert Matrix — compressing correlated attitude items",
        "03  Constant-Sum — eliciting proportional task allocation",
        "04  Vignette / Scenario — measuring acceptance of AI-generated work",
        "05  Semantic Differential — mapping perception on bipolar dimensions",
        "06  Social Network / Social Circle — peer adoption and influence",
        "07  Open-Ended with Structured Probe — qualitative depth at scale",
    ]
    for item in toc_items:
        story.append(Paragraph(item, S["toc_item"]))

    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # METHOD 01 — Adaptive Branching
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    block = []
    block.append(section_divider(1, "Adaptive Branching Logic", S))
    block.append(hr())
    block.append(Paragraph(
        "Branching logic routes respondents through different question paths based on prior answers, "
        "so they only see items relevant to their situation. Done well, it dramatically reduces burden "
        "and improves data quality by eliminating inapplicable items that confuse or frustrate respondents.",
        S["method_desc"]
    ))

    block.append(Paragraph("EXAMPLE QUESTION", S["q_label"]))
    block.append(Paragraph(
        "Q1.  Have you used the AI analytics platform in the past 30 days?",
        S["q_text"]
    ))
    block.append(option_row(["Yes", "No", "I was not aware this tool existed"], ncols=3, styles=S))
    block.append(Paragraph(
        "→  If YES: continue to Section B (Usage & Experience)\n"
        "→  If NO or Unaware: skip to Section C (Barriers & Readiness)",
        S["q_note"]
    ))
    block.append(Spacer(1, 0.08 * inch))

    # Branching flow diagram as a table
    flow_data = [
        ["Q1: Used platform?", "", ""],
        ["YES  →  Section B\nUsage frequency\nTask types\nSatisfaction ratings", "",
         "NO / Unaware  →  Section C\nPrimary barrier\nAwareness source\nReadiness to try"],
    ]
    ft = Table(flow_data, colWidths=[2.5 * inch, 0.4 * inch, 2.5 * inch])
    ft.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (0, 0), BLUE),
        ("BACKGROUND",  (2, 0), (2, 0), BLUE),
        ("SPAN",        (0, 0), (2, 0)),
        ("BACKGROUND",  (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR",   (0, 0), (-1, 0), WHITE),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("ALIGN",       (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND",  (0, 1), (0, 1), BLUE_LIGHT),
        ("BACKGROUND",  (2, 1), (2, 1), ORANGE_LIGHT),
        ("GRID",        (0, 0), (-1, -1), 0.4, GRAY_LINE),
        ("TOPPADDING",  (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    block.append(ft)
    block.append(Spacer(1, 0.1 * inch))

    block.append(callout(
        "WHY THIS\nMETHOD",
        "Branching eliminates the 'not applicable' problem — respondents who've never used a tool "
        "cannot meaningfully rate its usability. Forcing them to answer wastes their time and "
        "introduces noise into the data. Branching also lets you use a single instrument to measure "
        "both adopters and non-adopters without two separate surveys.",
        bg=BLUE_LIGHT, head_style_key="callout_head", styles=S
    ))
    block.append(Spacer(1, 0.06 * inch))
    block.append(callout(
        "CLIENT\nVALUE",
        "You get clean, segment-specific data with one instrument. Adoption barriers can be "
        "analyzed separately from usage patterns. Executive reports can say 'of the 38% who "
        "haven't adopted, here is what's stopping them' — not 'here is the average of everyone "
        "mixed together.'",
        bg=ORANGE_LIGHT, head_style_key="callout_head_o", styles=S
    ))
    story.append(KeepTogether(block))
    story.append(Spacer(1, 0.25 * inch))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # METHOD 02 — Likert Matrix
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    block = []
    block.append(section_divider(2, "Likert Matrix", S))
    block.append(hr())
    block.append(Paragraph(
        "A matrix groups multiple attitude items sharing the same response scale into a compact grid. "
        "It reduces survey length and cognitive switching costs — but only when items are genuinely "
        "related. A poorly constructed matrix creates 'straightlining' (respondents checking the same "
        "column for every row), which destroys data quality.",
        S["method_desc"]
    ))

    block.append(Paragraph("EXAMPLE QUESTION", S["q_label"]))
    block.append(Paragraph(
        "Q2.  How much do you agree with each of the following statements about the AI platform?",
        S["q_text"]
    ))
    block.append(likert_table([
        "I understand how to use the platform effectively.",
        "The platform produces outputs I can trust without verifying.",
        "Using the platform makes me look more capable to colleagues.",
        "I worry that AI tools will reduce the value of my expertise.",
        "My organization has given me adequate training to use the platform.",
    ], styles=S))
    block.append(Spacer(1, 0.1 * inch))

    block.append(callout(
        "WHY THIS\nMETHOD",
        "Five distinct constructs — self-efficacy, trust, social image, threat perception, and "
        "organizational support — are measured efficiently in one grid. Each maps to a different "
        "behavioral science lever. Items are ordered to move from external behavior to internal "
        "beliefs to reduce anchoring effects from the first row.",
        bg=BLUE_LIGHT, head_style_key="callout_head", styles=S
    ))
    block.append(Spacer(1, 0.06 * inch))
    block.append(callout(
        "CLIENT\nVALUE",
        "Pinpoints exactly which belief is blocking adoption — not just 'they don't like it.' "
        "If trust scores are low but self-efficacy is high, the intervention is communications, "
        "not training. If self-efficacy is low and trust is high, it's the opposite.",
        bg=ORANGE_LIGHT, head_style_key="callout_head_o", styles=S
    ))
    story.append(KeepTogether(block))

    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # METHOD 03 — Constant-Sum
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    block = []
    block.append(section_divider(3, "Constant-Sum (Point Allocation)", S))
    block.append(hr())
    block.append(Paragraph(
        "A constant-sum item asks respondents to distribute a fixed number of points (usually 100) "
        "across categories. Unlike Likert scales, it forces trade-offs — saying you spend more time "
        "on one task necessarily means less on another. This produces ratio-level data about "
        "relative weight, not just ordinal rankings.",
        S["method_desc"]
    ))

    block.append(Paragraph("EXAMPLE QUESTION", S["q_label"]))
    block.append(Paragraph(
        "Q3.  Think about a typical work week. Distribute 100 points across the task types below "
        "to reflect how you currently spend your analytical work time. "
        "<i>(Points must sum to exactly 100.)</i>",
        S["q_text"]
    ))
    cats = [
        "Qualitative analysis (interviews, transcripts, thematic coding)",
        "Quantitative analysis (statistical modeling, data cleaning, R/Python)",
        "Administrative / project management tasks",
        "Writing, editing, and communications",
        "Meetings, coordination, and stakeholder work",
    ]
    block.append(constant_sum_table(cats, S))
    block.append(Spacer(1, 0.1 * inch))

    block.append(callout(
        "WHY THIS\nMETHOD",
        "Standard Likert scales let respondents rate everything as 'very important,' which reveals "
        "nothing about priority. A constant-sum forces honest prioritization. In AI adoption research, "
        "this tells you where the time is actually going — and where AI stands to deliver the most "
        "efficiency gain per user segment.",
        bg=BLUE_LIGHT, head_style_key="callout_head", styles=S
    ))
    block.append(Spacer(1, 0.06 * inch))
    block.append(callout(
        "CLIENT\nVALUE",
        "Enables ROI modeling by role: if quantitative analysts allocate 40% to data cleaning "
        "and a tool reduces that to 10%, you can estimate recovered hours per analyst per week. "
        "Surfaces the actual cost of administrative burden on knowledge-work output.",
        bg=ORANGE_LIGHT, head_style_key="callout_head_o", styles=S
    ))
    story.append(KeepTogether(block))
    story.append(Spacer(1, 0.25 * inch))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # METHOD 04 — Vignette
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    block = []
    block.append(section_divider(4, "Vignette / Scenario-Based Item", S))
    block.append(hr())
    block.append(Paragraph(
        "A vignette presents a brief, realistic scenario and asks respondents to react to it. "
        "This is preferable to abstract attitude questions when the construct is sensitive or "
        "hard to self-report accurately — people are better at judging a concrete situation than "
        "their own abstract beliefs. Vignettes also allow systematic variation across conditions "
        "to isolate specific factors (e.g., who produced the work, what kind of output it is).",
        S["method_desc"]
    ))

    block.append(Paragraph("EXAMPLE QUESTION", S["q_label"]))

    # Vignette card
    vignette_text = (
        "<b>Scenario:</b>  Your colleague sends you a 10-page research brief on a policy topic "
        "you've been asked to brief leadership on. The brief is well-organized, clearly written, "
        "and cites relevant sources. You later learn it was drafted entirely by an AI tool, "
        "then reviewed and lightly edited by your colleague before sending."
    )
    vcard = Table([[Paragraph(vignette_text, ParagraphStyle("v",
        fontName="Helvetica", fontSize=10, leading=15, textColor=DARK))]],
        colWidths=[W])
    vcard.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F0F4F9")),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("BOX", (0, 0), (-1, -1), 1.2, BLUE),
    ]))
    block.append(vcard)
    block.append(Spacer(1, 0.1 * inch))

    block.append(Paragraph(
        "Q4a.  How confident would you be using this brief to prepare your leadership presentation?",
        S["q_text"]
    ))
    block.append(likert_table(
        ["I would use it with no additional verification.",
         "I would use it after spot-checking the key claims.",
         "I would not use it without a full independent review."],
        scale=["Not\nConfident", "Slightly\nConfident", "Moderately\nConfident",
               "Very\nConfident", "Fully\nConfident"],
        col_w_override=0.82 * inch,
        styles=S
    ))
    block.append(Spacer(1, 0.08 * inch))
    block.append(Paragraph(
        "Q4b.  Would your answer change if the brief had been drafted by a junior analyst instead of an AI?  "
        "◯ Yes, I would be more confident   ◯ Yes, I would be less confident   ◯ No difference",
        S["q_text"]
    ))
    block.append(Spacer(1, 0.1 * inch))

    block.append(callout(
        "WHY THIS\nMETHOD",
        "Asking 'do you trust AI outputs?' produces socially desirable responses. The vignette bypasses "
        "this by grounding the question in a concrete, plausible situation. Q4b's comparison condition "
        "isolates the AI attribution effect — does the mistrust come from the output quality or from "
        "who/what produced it? That's the critical distinction for designing adoption interventions.",
        bg=BLUE_LIGHT, head_style_key="callout_head", styles=S
    ))
    block.append(Spacer(1, 0.06 * inch))
    block.append(callout(
        "CLIENT\nVALUE",
        "Reveals whether your workforce's AI skepticism is quality-based (fixable with better outputs) "
        "or identity-based (fixable with culture change). These require completely different responses "
        "and investment levels. You can't know which you're dealing with without a vignette.",
        bg=ORANGE_LIGHT, head_style_key="callout_head_o", styles=S
    ))
    story.append(KeepTogether(block))

    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # METHOD 05 — Semantic Differential
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    block = []
    block.append(section_divider(5, "Semantic Differential Scale", S))
    block.append(hr())
    block.append(Paragraph(
        "A semantic differential presents bipolar adjective pairs at opposite ends of a scale, "
        "asking respondents to place their perception between them. It captures the evaluative, "
        "potency, and activity dimensions of attitudes more richly than agree/disagree items — "
        "especially useful for brand perception, product experience, and emotional response research.",
        S["method_desc"]
    ))

    block.append(Paragraph("EXAMPLE QUESTION", S["q_label"]))
    block.append(Paragraph(
        "Q5.  Using the scales below, indicate where your experience with the AI platform falls "
        "between each pair of words.  <i>(Mark the circle that best reflects your perception.)</i>",
        S["q_text"]
    ))

    pairs = [
        ("Confusing", "Intuitive"),
        ("Unreliable", "Dependable"),
        ("Threatening", "Empowering"),
        ("Rigid", "Flexible"),
        ("Impersonal", "Human"),
        ("Slow", "Fast"),
    ]
    scale_labels = ["1", "2", "3", "4", "5", "6", "7"]
    header = [Paragraph("", S["table_cell"])] + \
             [Paragraph(n, S["table_cell_bold"]) for n in scale_labels] + \
             [Paragraph("", S["table_cell"])]
    sd_data = [header]
    for left, right in pairs:
        sd_data.append(
            [Paragraph(f"<b>{left}</b>", S["table_cell"])] +
            ["◯"] * 7 +
            [Paragraph(f"<b>{right}</b>", S["table_cell"])]
        )
    col_w = 0.52 * inch
    left_w = 1.1 * inch
    sd_t = Table(sd_data, colWidths=[left_w] + [col_w] * 7 + [left_w])
    sd_t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR",   (0, 0), (-1, 0), WHITE),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("ALIGN",       (1, 0), (-2, -1), "CENTER"),
        ("ALIGN",       (0, 0), (0, -1), "RIGHT"),
        ("ALIGN",       (-1, 0), (-1, -1), "LEFT"),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BLUE_LIGHT, WHITE]),
        ("GRID",        (0, 0), (-1, -1), 0.3, GRAY_LINE),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    block.append(sd_t)
    block.append(Spacer(1, 0.1 * inch))

    block.append(callout(
        "WHY THIS\nMETHOD",
        "Standard Likert scales are one-directional. A semantic differential captures the full "
        "perceptual space — a tool can be rated as fast AND impersonal, which is a very different "
        "profile than slow AND human. This matters for product positioning and UX communication "
        "strategy in ways that agree/disagree items cannot reveal.",
        bg=BLUE_LIGHT, head_style_key="callout_head", styles=S
    ))
    block.append(Spacer(1, 0.06 * inch))
    block.append(callout(
        "CLIENT\nVALUE",
        "Ideal for brand perception, product experience, and emotional tone research. "
        "The profiles cluster cleanly in analysis — you can visualize the 'personality' of a "
        "product or service and compare it across user segments, time points, or against a competitor.",
        bg=ORANGE_LIGHT, head_style_key="callout_head_o", styles=S
    ))
    story.append(KeepTogether(block))
    story.append(Spacer(1, 0.25 * inch))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # METHOD 06 — Social Network / Social Circle
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    block = []
    block.append(section_divider(6, "Social Circle / Network Influence Item", S))
    block.append(hr())
    block.append(Paragraph(
        "Social circle items ask respondents about the behaviors or attitudes of people in their "
        "immediate network, rather than just their own. Rooted in research on social norms, "
        "descriptive norm effects, and peer influence, these items capture the social context "
        "of behavior — which is often a stronger predictor of individual adoption than attitudes alone.",
        S["method_desc"]
    ))

    block.append(Paragraph("EXAMPLE QUESTION", S["q_label"]))
    block.append(Paragraph(
        "Q6a.  Think about the 5 colleagues you work with most closely. "
        "To the best of your knowledge, how many of them regularly use AI tools in their work?",
        S["q_text"]
    ))
    block.append(option_row(["0 of 5", "1 of 5", "2 of 5", "3 of 5", "4 of 5", "5 of 5"], ncols=3, styles=S))
    block.append(Spacer(1, 0.08 * inch))

    block.append(Paragraph(
        "Q6b.  In the past month, has a colleague recommended an AI tool to you, or have you "
        "recommended one to a colleague?",
        S["q_text"]
    ))
    block.append(option_row([
        "Yes — a colleague recommended one to me",
        "Yes — I recommended one to a colleague",
        "Both",
        "Neither",
    ], ncols=2, styles=S))
    block.append(Spacer(1, 0.08 * inch))

    block.append(Paragraph(
        "Q6c.  How important is it to you that your colleagues view you as someone who stays "
        "current with new professional tools?",
        S["q_text"]
    ))
    block.append(option_row([
        "Not at all important", "Slightly important", "Moderately important", "Very important"
    ], ncols=2, styles=S))
    block.append(Spacer(1, 0.1 * inch))

    block.append(callout(
        "WHY THIS\nMETHOD",
        "Adoption behavior is heavily shaped by what people believe others around them are doing — "
        "descriptive norms. Q6a measures perceived peer adoption rate, which predicts individual "
        "adoption better than most attitude items. Q6c captures identity-based motivation, which "
        "explains why some people adopt tools before they need them and others resist long after "
        "they'd benefit.",
        bg=BLUE_LIGHT, head_style_key="callout_head", styles=S
    ))
    block.append(Spacer(1, 0.06 * inch))
    block.append(callout(
        "CLIENT\nVALUE",
        "If peer adoption is the primary predictor, the right intervention is a champion network, "
        "not more training. These items help clients prioritize: invest in social proof, or invest "
        "in skills? That's a multi-million-dollar strategic question that surveys can actually answer.",
        bg=ORANGE_LIGHT, head_style_key="callout_head_o", styles=S
    ))
    story.append(KeepTogether(block))

    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # METHOD 07 — Open-Ended with Probe
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    block = []
    block.append(section_divider(7, "Open-Ended Item with Structured Probe", S))
    block.append(hr())
    block.append(Paragraph(
        "An open-ended item followed by a structured probe captures qualitative depth within a "
        "quantitative survey. The first item invites free expression; the probe anchors the response "
        "to a specific dimension. This is more efficient than a full qualitative interview for "
        "large samples, while providing richer data than a closed item alone. Responses are analyzed "
        "through automated or manual thematic coding.",
        S["method_desc"]
    ))

    block.append(Paragraph("EXAMPLE QUESTION", S["q_label"]))
    block.append(Paragraph(
        "Q7a.  In your own words, what is the biggest barrier to your organization fully embracing "
        "AI tools in research and analysis work?",
        S["q_text"]
    ))

    textarea = Table([[
        Paragraph(
            "<i>[Open text field — 500 character limit]</i>",
            ParagraphStyle("ta", fontName="Helvetica-Oblique", fontSize=9, textColor=GRAY_TEXT)
        )
    ]], colWidths=[W])
    textarea.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8F8F8")),
        ("BOX",        (0, 0), (-1, -1), 0.5, GRAY_LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 22),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 22),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    block.append(textarea)
    block.append(Spacer(1, 0.1 * inch))

    block.append(Paragraph(
        "Q7b.  <i>[PROBE]</i>  You mentioned a barrier. Which category does it best fit?",
        S["q_text"]
    ))
    block.append(option_row([
        "Technical limitations (quality, accuracy, speed)",
        "Organizational culture or leadership support",
        "Training or skill gaps",
        "Data privacy or security concerns",
        "Unclear use cases for my type of work",
        "Other / cannot categorize",
    ], ncols=2, styles=S))
    block.append(Spacer(1, 0.08 * inch))

    block.append(Paragraph(
        "Q7c.  How long do you think it would take for this barrier to be meaningfully reduced "
        "at your organization?",
        S["q_text"]
    ))
    block.append(option_row([
        "Less than 6 months", "6–12 months", "1–2 years", "More than 2 years", "It won't be"
    ], ncols=3, styles=S))
    block.append(Spacer(1, 0.1 * inch))

    block.append(callout(
        "WHY THIS\nMETHOD",
        "Pure open-ended items are hard to analyze at scale and hard to act on without additional "
        "structure. The probe converts the qualitative response into a categorized data point without "
        "forcing the respondent into a box prematurely. Q7c adds a time-perception dimension that "
        "closed barrier items almost never capture but that matters enormously for planning.",
        bg=BLUE_LIGHT, head_style_key="callout_head", styles=S
    ))
    block.append(Spacer(1, 0.06 * inch))
    block.append(callout(
        "CLIENT\nVALUE",
        "You get the richness of open text for discovery (what unexpected things are people saying?) "
        "and the analyzability of closed categories for reporting (X% cited culture, Y% cited training). "
        "The time-horizon probe tells you how urgent respondents think the problem is — which sets "
        "realistic expectations for change management timelines.",
        bg=ORANGE_LIGHT, head_style_key="callout_head_o", styles=S
    ))

    # Closing note
    block.append(Spacer(1, 0.3 * inch))
    block.append(hr())
    closing = Table([[
        Paragraph(
            "<b>About this document:</b>  All examples are drawn from or inspired by professional "
            "research engagements at RAND Corporation, the Gates Foundation EMO study, and behavioral "
            "science consulting work. Items have been anonymized and adapted for portfolio use. "
            "Full instrument design, programming, cognitive testing, and analysis available as project services.",
            ParagraphStyle("closing", fontName="Helvetica", fontSize=9,
                           textColor=GRAY_TEXT, leading=13)
        )
    ]], colWidths=[W])
    closing.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F5F5")),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    block.append(closing)

    story.append(KeepTogether(block))

    # Build
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_page)
    print(f"Showcase PDF saved to {OUTPUT}")


if __name__ == "__main__":
    build()
