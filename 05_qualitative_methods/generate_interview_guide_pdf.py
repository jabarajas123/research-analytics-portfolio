"""
Qualitative Research Methods Showcase PDF — Interview Guide
------------------------------------------------------------
Demonstrates 6 interview question techniques with structure, rationale, and client value.
Modeled on needfinding / semi-structured interview best practices.

Run:  python3 generate_interview_guide_pdf.py
Output: interview_methods_showcase.pdf
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
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUTPUT = Path("interview_methods_showcase.pdf")

BLUE        = colors.HexColor("#2D6A9F")
BLUE_LIGHT  = colors.HexColor("#E8F2FB")
ORANGE      = colors.HexColor("#E87722")
ORANGE_LIGHT= colors.HexColor("#FEF3E8")
GREEN       = colors.HexColor("#2E7D52")
GREEN_LIGHT = colors.HexColor("#E8F5EE")
PURPLE      = colors.HexColor("#6A4C93")
PURPLE_LIGHT= colors.HexColor("#EDE8F8")
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
        "probe": ParagraphStyle("pr", fontName="Helvetica-Oblique", fontSize=9.5,
            textColor=colors.HexColor("#444466"), leading=14, leftIndent=18, spaceAfter=3),
        "probe_label": ParagraphStyle("prl", fontName="Helvetica-Bold", fontSize=8.5,
            textColor=BLUE, spaceAfter=2, leftIndent=18),
        "q_note": ParagraphStyle("qn", fontName="Helvetica-Oblique", fontSize=8.5,
            textColor=ORANGE, spaceAfter=4),
        "callout_head": ParagraphStyle("ch", fontName="Helvetica-Bold", fontSize=9,
            textColor=BLUE, spaceAfter=3),
        "callout_head_o": ParagraphStyle("cho", fontName="Helvetica-Bold", fontSize=9,
            textColor=ORANGE, spaceAfter=3),
        "callout_head_g": ParagraphStyle("chg", fontName="Helvetica-Bold", fontSize=9,
            textColor=GREEN, spaceAfter=3),
        "callout_body": ParagraphStyle("cb", fontName="Helvetica", fontSize=9,
            textColor=DARK, leading=13),
        "intro_body": ParagraphStyle("ib", fontName="Helvetica", fontSize=10.5,
            textColor=DARK, leading=16, spaceAfter=8),
        "toc_item": ParagraphStyle("ti", fontName="Helvetica", fontSize=10.5,
            textColor=DARK, leading=18, leftIndent=20),
        "guide_head": ParagraphStyle("gh", fontName="Helvetica-Bold", fontSize=10,
            textColor=WHITE, spaceAfter=2),
        "guide_body": ParagraphStyle("gb", fontName="Helvetica", fontSize=9.5,
            textColor=DARK, leading=14, spaceAfter=3),
        "guide_italic": ParagraphStyle("gi", fontName="Helvetica-Oblique", fontSize=9,
            textColor=GRAY_TEXT, leading=13, spaceAfter=2),
        "table_cell": ParagraphStyle("tc", fontName="Helvetica", fontSize=9, leading=12),
        "table_cell_bold": ParagraphStyle("tcb", fontName="Helvetica-Bold", fontSize=9, leading=12),
    }


def hr(color=GRAY_LINE, sb=4, sa=8):
    return HRFlowable(width="100%", thickness=0.5, color=color, spaceBefore=sb, spaceAfter=sa)


def callout(head, body, bg=BLUE_LIGHT, head_key="callout_head", styles=None):
    t = Table([[Paragraph(head, styles[head_key]),
                Paragraph(body, styles["callout_body"])]],
              colWidths=[1.1 * inch, W - 1.1 * inch - 0.3 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def section_divider(num, title, styles):
    badge = Table([[Paragraph(f"METHOD {num:02d}", styles["method_title"])]],
                  colWidths=[W])
    inner = Table([[
        Table([[Paragraph(f"METHOD {num:02d}", ParagraphStyle(
            "mb", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, alignment=TA_CENTER))]],
              colWidths=[0.85 * inch],
              style=TableStyle([("BACKGROUND", (0,0),(-1,-1), BLUE),
                                ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
                                ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6)])),
        Paragraph(title, styles["method_title"]),
    ]])
    t = Table([[
        Table([[Paragraph(f"METHOD {num:02d}", ParagraphStyle(
            "mb2", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, alignment=TA_CENTER))]],
              colWidths=[0.85*inch],
              style=TableStyle([("BACKGROUND",(0,0),(-1,-1),BLUE),
                                ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
                                ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6)])),
        Paragraph(title, styles["method_title"]),
    ]], colWidths=[0.95*inch, W-0.95*inch])
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                           ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
                           ("LEFTPADDING",(0,0),(-1,-1),0)]))
    return t


def guide_block(section_title, content_rows, bg=BLUE):
    rows = [[Paragraph(section_title, ParagraphStyle(
        "gh2", fontName="Helvetica-Bold", fontSize=10, textColor=WHITE))]]
    t_header = Table(rows, colWidths=[W])
    t_header.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),
                                   ("TOPPADDING",(0,0),(-1,-1),7),
                                   ("BOTTOMPADDING",(0,0),(-1,-1),7),
                                   ("LEFTPADDING",(0,0),(-1,-1),12)]))
    style_inner = ParagraphStyle("gi2", fontName="Helvetica", fontSize=9.5,
                                  textColor=DARK, leading=14)
    style_italic = ParagraphStyle("gi3", fontName="Helvetica-Oblique", fontSize=9,
                                   textColor=GRAY_TEXT, leading=13)
    inner_rows = []
    for row_type, text in content_rows:
        s = style_italic if row_type == "italic" else style_inner
        inner_rows.append([Paragraph(text, s)])
    t_body = Table(inner_rows, colWidths=[W])
    t_body.setStyle(TableStyle([
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.HexColor("#F5F8FC"), WHITE]),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("GRID",(0,0),(-1,-1),0.3,GRAY_LINE),
    ]))
    return [t_header, t_body]


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(GRAY_LINE)
    canvas.setLineWidth(0.5)
    canvas.line(0.85*inch, 0.65*inch, 7.65*inch, 0.65*inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY_TEXT)
    canvas.drawString(0.85*inch, 0.48*inch,
                      "Jeremy Barajas | Qualitative Research Methods Showcase | barajas@alumni.usc.edu")
    canvas.drawRightString(7.65*inch, 0.48*inch, f"Page {doc.page}")
    canvas.restoreState()


def build():
    styles = S()
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter,
                            rightMargin=0.85*inch, leftMargin=0.85*inch,
                            topMargin=0.85*inch, bottomMargin=1.0*inch)
    story = []

    # ── Cover ─────────────────────────────────────────────────────────────────
    cover = Table([[Paragraph("Qualitative Research<br/>Methods Showcase", styles["cover_title"])]],
                  colWidths=[W])
    cover.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),BLUE),
                                ("TOPPADDING",(0,0),(-1,-1),48),("BOTTOMPADDING",(0,0),(-1,-1),20),
                                ("LEFTPADDING",(0,0),(-1,-1),24),("RIGHTPADDING",(0,0),(-1,-1),24)]))
    story.append(cover)

    sub = Table([[Paragraph(
        "Six interview techniques — with example questions, probe sequences, rationale, and client value.<br/>"
        "Includes a complete annotated semi-structured interview guide.",
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
        "This document demonstrates six qualitative interview techniques I use in research engagements. "
        "The first section presents a complete annotated semi-structured interview guide — showing "
        "how an interview is structured from rapport to close. The following sections demonstrate "
        "individual question types with rationale and client value. Examples draw from AI adoption "
        "research, product needfinding, and policy evaluation work.",
        styles["intro_body"]
    ))
    for item in [
        "Part I   —  Annotated Semi-Structured Interview Guide (full structure)",
        "Method 01  —  Grand Tour Question",
        "Method 02  —  Laddering / Why Probe",
        "Method 03  —  Critical Incident Technique",
        "Method 04  —  Hypothetical / Future Scenario",
        "Method 05  —  Think-Aloud / Cognitive Walkthrough",
        "Method 06  —  Member Check Question",
    ]:
        story.append(Paragraph(item, styles["toc_item"]))

    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PART I — Annotated Interview Guide
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    story.append(Paragraph("PART I", ParagraphStyle("pi", fontName="Helvetica-Bold", fontSize=9,
                                                     textColor=ORANGE, spaceAfter=2)))
    story.append(Paragraph("Annotated Semi-Structured Interview Guide", styles["method_title"]))
    story.append(hr())
    story.append(Paragraph(
        "A semi-structured interview uses a prepared guide as a scaffold — not a script. "
        "The interviewer follows the respondent's lead while ensuring key topics are covered. "
        "The annotations below explain the purpose of each section and what to listen for.",
        styles["method_desc"]
    ))
    story.append(Spacer(1, 0.05*inch))

    guide_meta = [
        ("normal", "Study:  AI Platform Adoption — Employee Listening Study"),
        ("normal", "Estimated duration:  45–60 minutes"),
        ("normal", "Interviewer:  Jeremy Barajas, RAND Corporation"),
        ("italic", "Note: This guide is a scaffold, not a script. Follow the respondent's lead. "
                   "Probe on what's interesting or unexpected. You do not need to ask every question."),
    ]
    for rows in guide_block("GUIDE METADATA", guide_meta, bg=colors.HexColor("#555555")):
        story.append(rows)
    story.append(Spacer(1, 0.1*inch))

    intro_rows = [
        ("normal", "Thank you for taking the time to speak with me today. My name is Jeremy and I'm "
                   "a researcher studying how people at this organization experience AI tools in their work."),
        ("normal", "There are no right or wrong answers. I'm here to learn from your perspective — "
                   "your honest experience is exactly what we need."),
        ("normal", "With your permission, I'd like to record our conversation so I can focus on "
                   "listening rather than note-taking. The recording will only be used for my notes."),
        ("italic", "Interviewer note: Wait for verbal consent before recording. "
                   "Allow silence after consent — let the respondent settle in before the first question."),
    ]
    for rows in guide_block("SECTION 1 — INTRODUCTION & CONSENT  (3–5 min)", intro_rows):
        story.append(rows)
    story.append(Spacer(1, 0.1*inch))

    warmup_rows = [
        ("normal", "Q:  Can you tell me a little about your role here — what you work on day-to-day?"),
        ("italic", "Purpose: Establishes rapport and gives the interviewer context for interpreting "
                   "later responses. Listen for task types that AI might be relevant to."),
        ("normal", "Q:  How long have you been in this role, and how has your work changed over that time?"),
        ("italic", "Purpose: Opens a historical frame that makes it natural to discuss change — "
                   "including the introduction of new tools."),
    ]
    for rows in guide_block("SECTION 2 — WARM-UP  (5 min)", warmup_rows, bg=GREEN):
        story.append(rows)
    story.append(Spacer(1, 0.1*inch))

    core_rows = [
        ("normal", "GRAND TOUR:  Walk me through a typical week of analytical work. What does that look like from start to finish?"),
        ("italic", "Listen for: where time is spent, what feels tedious vs. meaningful, "
                   "any tools mentioned (AI or otherwise). Do not interrupt."),
        ("normal", "PROBE:  You mentioned [X task]. Tell me more about how you do that."),
        ("normal", "CRITICAL INCIDENT:  Think of a specific time recently when you had a lot of data "
                   "to process or a tight deadline. What happened?"),
        ("italic", "Listen for: coping strategies, workarounds, frustration points — these are "
                   "the highest-signal moments for understanding unmet needs."),
        ("normal", "PROBE:  What did you wish you had in that moment that you didn't have?"),
        ("normal", "TRANSITION TO AI:  Have you used any AI tools in your work — things like "
                   "ChatGPT, Copilot, or anything similar?"),
        ("italic", "Branch A (used AI): Continue to adoption section.\n"
                   "Branch B (not used): Jump to non-adoption section."),
        ("normal", "[IF USED] Tell me about the first time you used one of those tools for work. "
                   "What were you trying to do?"),
        ("normal", "[IF NOT USED] What's kept you from trying one of those tools?"),
        ("italic", "Do NOT prompt with a list of barriers. Let them generate the answer first. "
                   "If they say 'I don't know,' try: 'What would have to be true for you to try it?'"),
    ]
    for rows in guide_block("SECTION 3 — CORE QUESTIONS  (25–30 min)", core_rows, bg=BLUE):
        story.append(rows)
    story.append(Spacer(1, 0.1*inch))

    deep_rows = [
        ("normal", "LADDERING:  You said [reason for/against AI use]. Why does that matter to you?"),
        ("italic", "Repeat 3x to get from surface reason to underlying value. "
                   "Stop when you reach an emotional or identity-level response."),
        ("normal", "HYPOTHETICAL:  Imagine the tool was perfect — it never made a mistake and "
                   "you could trust it completely. Would you use it more? For what?"),
        ("italic", "This removes the 'accuracy' objection and reveals whether reluctance is "
                   "really about accuracy or about something else (identity, culture, irrelevance)."),
        ("normal", "VIGNETTE:  [Show scenario card] A colleague sends you a 10-page brief "
                   "that you later find out was drafted by AI and lightly edited. "
                   "Would you use it? What would you do with it?"),
        ("italic", "Listen for: trust differentiation (output quality vs. source), "
                   "social/reputational concern, calibration strategies."),
    ]
    for rows in guide_block("SECTION 4 — DEEP DIVE  (10–15 min)", deep_rows, bg=PURPLE):
        story.append(rows)
    story.append(Spacer(1, 0.1*inch))

    close_rows = [
        ("normal", "MEMBER CHECK:  Based on what you've shared, it sounds like [your summary]. "
                   "Does that capture it accurately?"),
        ("italic", "This is one of the most important questions in the guide. "
                   "It surfaces misinterpretations before they become findings. "
                   "Update your interpretation based on any correction."),
        ("normal", "Is there anything else about your experience with AI tools that we haven't covered?"),
        ("normal", "Is there someone else at this organization you think I should talk to?"),
        ("italic", "Theoretical sampling: ask who would see things differently, not just who agrees."),
        ("normal", "Thank you so much. [Stop recording.] Here's how findings will be used..."),
    ]
    for rows in guide_block("SECTION 5 — CLOSE & MEMBER CHECK  (5 min)", close_rows, bg=colors.HexColor("#555555")):
        story.append(rows)

    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # METHOD 01 — Grand Tour
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    block = []
    block.append(section_divider(1, "Grand Tour Question", styles))
    block.append(hr())
    block.append(Paragraph(
        "A grand tour question invites the respondent to narrate their world without the "
        "interviewer imposing categories. It is always the first substantive question. "
        "The interviewer stays silent and listens — the topics, vocabulary, and sequence "
        "the respondent chooses are themselves data.",
        styles["method_desc"]
    ))
    block.append(Paragraph("EXAMPLE QUESTION", styles["q_label"]))
    block.append(Paragraph(
        "\"Walk me through a typical week of analytical work — from the moment you start "
        "a project to when you hand something off. What does that actually look like?\"",
        styles["q_text"]
    ))
    block.append(Paragraph("FOLLOW-ON PROBES", styles["q_label"]))
    for probe in [
        "\"You mentioned [X] — tell me more about how you do that.\"",
        "\"What part of that takes the most time?\"",
        "\"Is there anything in that process that feels like a workaround?\"",
        "\"What would an ideal version of that process look like?\"",
    ]:
        block.append(Paragraph(probe, styles["probe"]))
    block.append(Spacer(1, 0.08*inch))
    block.append(callout("WHY THIS\nMETHOD",
        "Imposes no categories on the respondent. You find out what matters to them, not "
        "just whether what matters to you matters to them. The grand tour reveals the "
        "workflow structure, vocabulary, and priorities that inform all subsequent probing.",
        bg=BLUE_LIGHT, head_key="callout_head", styles=styles))
    block.append(Spacer(1, 0.06*inch))
    block.append(callout("CLIENT\nVALUE",
        "Surfaces needs, frustrations, and workarounds the client didn't know to ask about. "
        "The most valuable insights in needfinding almost always come from grand tour "
        "responses, not from pre-specified question topics.",
        bg=ORANGE_LIGHT, head_key="callout_head_o", styles=styles))
    story.append(KeepTogether(block))
    story.append(Spacer(1, 0.25*inch))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # METHOD 02 — Laddering
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    block = []
    block.append(section_divider(2, "Laddering / Why Probe", styles))
    block.append(hr())
    block.append(Paragraph(
        "Laddering moves from a surface-level belief or behavior to the underlying value "
        "driving it by repeatedly asking 'why does that matter to you?' Each iteration "
        "climbs one rung from attribute → consequence → terminal value. Three iterations "
        "usually reaches the value level.",
        styles["method_desc"]
    ))
    block.append(Paragraph("EXAMPLE SEQUENCE", styles["q_label"]))

    ladder_data = [
        ["Turn", "Question", "Likely Response Level"],
        ["1", "\"You said you don't fully trust the AI outputs. Why does that matter to you?\"",
         "Attribute — 'it makes mistakes'"],
        ["2", "\"And why does it matter that it makes mistakes in your context?\"",
         "Consequence — 'I'd have to check everything'"],
        ["3", "\"Why is having to check everything a problem for you?\"",
         "Consequence — 'it defeats the purpose'"],
        ["4", "\"What's the purpose you'd want it to serve?\"",
         "Terminal value — 'I want to trust my own work'"],
    ]
    lt = Table(ladder_data, colWidths=[0.4*inch, 3.2*inch, 2.3*inch])
    lt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),BLUE), ("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"), ("FONTSIZE",(0,0),(-1,-1),8.5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[BLUE_LIGHT,WHITE]),
        ("GRID",(0,0),(-1,-1),0.3,GRAY_LINE),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),6),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    block.append(lt)
    block.append(Spacer(1, 0.1*inch))
    block.append(callout("WHY THIS\nMETHOD",
        "Surface reasons are rarely actionable. Knowing someone dislikes AI 'because it makes "
        "mistakes' tells you nothing about what to do. Knowing they distrust it because it "
        "threatens their sense of professional identity tells you exactly what the intervention needs to address.",
        bg=BLUE_LIGHT, head_key="callout_head", styles=styles))
    block.append(Spacer(1, 0.06*inch))
    block.append(callout("CLIENT\nVALUE",
        "Reveals the real reason for resistance — which is almost never the stated reason. "
        "Interventions designed against surface reasons fail. Laddering gives you the level at "
        "which change actually needs to happen.",
        bg=ORANGE_LIGHT, head_key="callout_head_o", styles=styles))
    story.append(KeepTogether(block))
    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # METHOD 03 — Critical Incident
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    block = []
    block.append(section_divider(3, "Critical Incident Technique", styles))
    block.append(hr())
    block.append(Paragraph(
        "The Critical Incident Technique (CIT) asks respondents to recount a specific, "
        "memorable event — positive or negative — rather than summarizing their general experience. "
        "People are far more accurate about concrete events than about abstract impressions. "
        "The episode structure (situation → action → outcome) generates rich, analyzable data.",
        styles["method_desc"]
    ))
    block.append(Paragraph("EXAMPLE QUESTIONS", styles["q_label"]))
    for q in [
        "\"Think of a specific time recently when you used an AI tool and it went really well. "
        "Walk me through exactly what happened — what were you trying to do, what did you do, and what was the result?\"",
        "\"Now think of a time it didn't go well, or when you tried to use it and gave up. "
        "What was happening? What did you try? What made you stop?\"",
    ]:
        block.append(Paragraph(q, styles["q_text"]))
        block.append(Spacer(1, 0.05*inch))
    block.append(Paragraph("KEY PROBES", styles["q_label"]))
    for probe in [
        "\"What exactly did you do next?\"  (keeps the narrative specific)",
        "\"What were you thinking at that moment?\"  (surfaces the cognitive layer)",
        "\"What would you have done differently?\"  (reveals latent preferences)",
        "\"Has that happened more than once?\"  (tests whether this is typical or anomalous)",
    ]:
        block.append(Paragraph(probe, styles["probe"]))
    block.append(Spacer(1, 0.08*inch))
    block.append(callout("WHY THIS\nMETHOD",
        "General questions produce general answers. 'I use it sometimes, it's okay' is not "
        "analyzable. A specific incident produces a behavior sequence you can map, code, and "
        "compare across participants. CIT is especially powerful for identifying failure modes "
        "and unmet needs that respondents have normalized and would never surface unprompted.",
        bg=BLUE_LIGHT, head_key="callout_head", styles=styles))
    block.append(Spacer(1, 0.06*inch))
    block.append(callout("CLIENT\nVALUE",
        "Generates concrete use cases, failure scenarios, and success conditions that "
        "product teams, trainers, and communicators can act on directly. "
        "Much higher signal than 'what do you think about X?' questions.",
        bg=ORANGE_LIGHT, head_key="callout_head_o", styles=styles))
    story.append(KeepTogether(block))
    story.append(Spacer(1, 0.25*inch))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # METHOD 04 — Hypothetical
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    block = []
    block.append(section_divider(4, "Hypothetical / Future Scenario", styles))
    block.append(hr())
    block.append(Paragraph(
        "A hypothetical removes a known constraint — accuracy, cost, trust, time — to reveal "
        "whether that constraint is the real barrier or whether reluctance lives deeper. "
        "It is also used to elicit desired future states: what would the ideal look like if "
        "the current limitation didn't exist?",
        styles["method_desc"]
    ))
    block.append(Paragraph("EXAMPLE QUESTIONS", styles["q_label"]))
    for q in [
        "\"Imagine the AI tool was perfect — it never made a factual error and you could trust "
        "every output completely. How would that change how you use it, if at all?\"",
        "\"If you could redesign your analytical workflow from scratch — no legacy systems, "
        "no organizational constraints — what would it look like?\"",
        "\"Five years from now, what do you think your job looks like if AI tools have become "
        "standard in your field?\"",
    ]:
        block.append(Paragraph(q, styles["q_text"]))
        block.append(Spacer(1, 0.05*inch))
    block.append(callout("WHY THIS\nMETHOD",
        "Hypotheticals are a diagnostic tool. If removing the stated barrier (accuracy) doesn't "
        "change the answer — 'I still wouldn't trust it even if it were perfect' — then you know "
        "the real issue is identity, culture, or relevance, not quality. The hypothetical cleanly "
        "separates symptom from root cause.",
        bg=BLUE_LIGHT, head_key="callout_head", styles=styles))
    block.append(Spacer(1, 0.06*inch))
    block.append(callout("CLIENT\nVALUE",
        "Reveals unspoken objections and latent demand. 'I'd use it for X but not Y' from a "
        "hypothetical question is high-signal product feedback that no closed survey item would produce.",
        bg=ORANGE_LIGHT, head_key="callout_head_o", styles=styles))
    story.append(KeepTogether(block))
    story.append(PageBreak())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # METHOD 05 — Think-Aloud
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    block = []
    block.append(section_divider(5, "Think-Aloud / Cognitive Walkthrough", styles))
    block.append(hr())
    block.append(Paragraph(
        "In a think-aloud, the respondent performs a real task while narrating their thought "
        "process. The interviewer observes and asks minimal, non-leading questions. It is the "
        "most direct method for understanding how someone actually uses a tool or interface — "
        "not how they remember using it or how they think they use it.",
        styles["method_desc"]
    ))
    block.append(Paragraph("SETUP", styles["q_label"]))
    block.append(Paragraph(
        "\"I'm going to ask you to use the AI platform to complete a task you'd normally do in "
        "your work. As you do it, please talk out loud — tell me what you're thinking, what "
        "you're looking at, and what you expect to happen. There's no right way to do this. "
        "I'm not testing you — I'm testing the tool.\"",
        styles["q_text"]
    ))
    block.append(Paragraph("DURING-TASK PROBES (minimal intervention)", styles["q_label"]))
    for probe in [
        "\"What are you looking for right now?\"",
        "\"What did you expect to happen there?\"",
        "\"You paused — what were you thinking?\"",
        "\"What would you normally do at this point?\"  (if they get stuck)",
    ]:
        block.append(Paragraph(probe, styles["probe"]))
    block.append(Paragraph("POST-TASK PROBES", styles["q_label"]))
    for probe in [
        "\"Was there a moment where you felt confused or uncertain?\"",
        "\"What would have made that easier?\"",
        "\"Is that how you'd normally approach this task, or did you do it differently because I was watching?\"",
    ]:
        block.append(Paragraph(probe, styles["probe"]))
    block.append(Spacer(1, 0.08*inch))
    block.append(callout("WHY THIS\nMETHOD",
        "People cannot accurately self-report their cognitive processes after the fact. "
        "Think-aloud captures the real-time confusion, hesitation, and workaround behavior "
        "that post-hoc interviews miss. It is the gold standard for UX research and "
        "cognitive task analysis.",
        bg=BLUE_LIGHT, head_key="callout_head", styles=styles))
    block.append(Spacer(1, 0.06*inch))
    block.append(callout("CLIENT\nVALUE",
        "Surfaces specific UI/UX failure points, mental model mismatches, and comprehension "
        "gaps with precision a survey cannot achieve. Every pause is a data point. "
        "I used this method in 16 cognitive interviews for JP Morgan Private Bank and "
        "9 sessions for TD Bank — both produced actionable product design recommendations.",
        bg=ORANGE_LIGHT, head_key="callout_head_o", styles=styles))
    story.append(KeepTogether(block))
    story.append(Spacer(1, 0.25*inch))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # METHOD 06 — Member Check
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    block = []
    block.append(section_divider(6, "Member Check Question", styles))
    block.append(hr())
    block.append(Paragraph(
        "A member check asks the respondent to verify the interviewer's interpretation of "
        "what they've said. It is a validity technique — it catches misinterpretations before "
        "they become findings, and it often produces the most honest, corrective language "
        "in the entire interview. It is not leading; it is confirming.",
        styles["method_desc"]
    ))
    block.append(Paragraph("EXAMPLE QUESTIONS", styles["q_label"]))
    for q in [
        "\"Based on what you've shared, it sounds like your main concern isn't accuracy "
        "per se — it's more about whether you can defend the work if someone questions it. "
        "Does that capture it?\"",
        "\"I want to make sure I'm understanding correctly — when you say you 'don't trust it,' "
        "are you saying the outputs are wrong, or that you can't tell whether they're wrong?\"",
        "\"If I were to summarize your experience as: [summary], would you say that's accurate? "
        "What would you change about that?\"",
    ]:
        block.append(Paragraph(q, styles["q_text"]))
        block.append(Spacer(1, 0.05*inch))
    block.append(callout("WHY THIS\nMETHOD",
        "Researcher interpretation bias is the most common source of error in qualitative research. "
        "The member check is the most direct check on it. A respondent who says 'no, that's not "
        "quite right — it's more like...' has just given you your finding. Without the check, "
        "you'd have published the wrong conclusion.",
        bg=BLUE_LIGHT, head_key="callout_head", styles=styles))
    block.append(Spacer(1, 0.06*inch))
    block.append(callout("CLIENT\nVALUE",
        "Increases credibility of findings. When you can tell a client 'we ran this interpretation "
        "back to 28 participants and they confirmed it,' the recommendation carries significantly "
        "more weight than findings derived entirely from the researcher's reading of transcripts.",
        bg=ORANGE_LIGHT, head_key="callout_head_o", styles=styles))

    # Closing
    block.append(Spacer(1, 0.3*inch))
    block.append(hr())
    closing = Table([[Paragraph(
        "<b>About this document:</b>  Interview techniques demonstrated here draw from professional "
        "research conducted at RAND Corporation (AI adoption, FEMA building codes), the Gates Foundation "
        "EMO study (cognitive interviews), and behavioral science consulting engagements at JP Morgan "
        "Private Bank and TD Bank. All content anonymized for portfolio use. Full interview design, "
        "facilitation, transcription, and analysis available as project services.",
        ParagraphStyle("clos", fontName="Helvetica", fontSize=9,
                       textColor=GRAY_TEXT, leading=13)
    )]], colWidths=[W])
    closing.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F5F5F5")),
                                  ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
                                  ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12)]))
    block.append(closing)
    story.append(KeepTogether(block))

    doc.build(story, onLaterPages=on_page)
    print(f"Interview guide PDF saved to {OUTPUT}")


if __name__ == "__main__":
    build()
