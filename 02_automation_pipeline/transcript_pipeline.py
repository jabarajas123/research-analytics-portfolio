"""
Qualitative Research Automation Pipeline
=========================================
Automates transcript ingestion, cleaning, chunking, LLM-based thematic coding,
and structured output generation for large-scale qualitative studies.

This script is written as a teaching document. Each section explains what the
code does, why it's designed that way, the expected inputs and outputs at each
step, and how to verify that the results are correct.

The pipeline takes a directory of cleaned interview transcripts and produces:
  output/coded_transcripts.csv     — one row per theme per chunk, with quote + memo
  output/thematic_summary.md       — human-readable summary with theme frequencies

Design philosophy: we send the LLM one chunk at a time (not the whole transcript
at once) because:
  1. Transcripts can exceed the context window of less capable models
  2. Smaller chunks force the model to focus on a specific passage rather than
     making vague high-level attributions
  3. Chunked output is easier to trace back to specific quotes

Run:
    python3 transcript_pipeline.py

Dependencies: openai, python-docx, pandas
Set OPENAI_API_KEY as an environment variable before running.
"""

# ── Imports ───────────────────────────────────────────────────────────────────
# Standard library first, then third-party. This ordering is a Python convention
# (PEP 8) that makes it easy to see which packages need to be installed.

import os        # used to check for the OPENAI_API_KEY environment variable
import re        # regular expressions for timestamp removal in clean_text()
import json      # parsing the LLM's JSON response and serializing the codebook
import pandas as pd           # structuring the coded output as a DataFrame for CSV export
from pathlib import Path      # platform-safe file paths
from openai import OpenAI     # the OpenAI Python SDK; communicates with the API


# ── API Client ────────────────────────────────────────────────────────────────
# The OpenAI client reads OPENAI_API_KEY from the environment automatically.
# We never hardcode API keys in source code — that would expose credentials
# if the file is shared or committed to version control.
#
# Verify: if the key is missing, client.chat.completions.create() will raise
# an AuthenticationError before any transcript is processed.

client = OpenAI()


# ── Configuration ─────────────────────────────────────────────────────────────
# All tuneable parameters live here. Changing MODEL or MAX_CHUNK_TOKENS affects
# every API call downstream — centralizing them means one edit, not many.

TRANSCRIPT_DIR   = Path("transcripts/")
OUTPUT_CSV       = Path("output/coded_transcripts.csv")
OUTPUT_REPORT    = Path("output/thematic_summary.md")

MODEL            = "gpt-4o"
# gpt-4o is chosen for its strong instruction-following and JSON output reliability.
# For cost-sensitive runs, gpt-4o-mini is a reasonable substitute — accuracy drops
# slightly for nuanced theme attribution but is acceptable for exploratory coding.

MAX_CHUNK_TOKENS = 1500
# 1,500 words per chunk is a practical ceiling. Above ~2,000 words, the model
# tends to over-assign themes (anchoring on salient early content). Below ~500
# words, chunks lose enough context that inter-rater agreement with human coders
# drops. 1,500 is approximately 10–15 minutes of interview transcript.


# ── Codebook ──────────────────────────────────────────────────────────────────
# The codebook defines the universe of themes the LLM is allowed to assign.
# Using a closed codebook (rather than letting the model generate free-form labels)
# ensures comparability across participants and researchers — a requirement for
# any study that will report inter-rater reliability or theme frequencies.
#
# To adapt this pipeline to a different study, replace these themes with your own.
# Keep the list to 8–12 items: too few forces overgeneralization; too many
# produces sparse coding where most themes appear in only 1–2 transcripts.
#
# "Other" is intentionally included as a catch-all. After the first pass,
# review what lands in "Other" — those segments often reveal a theme you didn't
# anticipate and should be promoted to a named code for the next iteration.

CODEBOOK = [
    "Adoption Barriers",
    "Workflow Integration",
    "Trust & Reliability Concerns",
    "Training & Onboarding",
    "Perceived Efficiency Gains",
    "Resistance to Change",
    "Data Privacy Concerns",
    "Leadership & Culture",
    "Other",
]


# ── System Prompt ─────────────────────────────────────────────────────────────
# The system prompt is the instruction set the LLM receives before any transcript
# content. It defines the task, the output format, and the codebook.
#
# Key design decisions:
#   - We ask for a verbatim quote, not a paraphrase. Paraphrases introduce
#     analyst interpretation at the extraction stage; verbatim quotes let the
#     reader verify the coding against the original.
#   - We cap quotes at 2 sentences to prevent the model from returning an
#     entire paragraph as a "quote" — which defeats the purpose of focused coding.
#   - We require a 1-sentence memo explaining WHY the theme applies, not WHAT
#     the text says. This forces the model to articulate the analytical logic,
#     which makes the output auditable.
#   - response_format=json_object (set in the API call below) ensures the
#     response parses cleanly without regex hacks.
#
# json.dumps(CODEBOOK) embeds the current codebook list as a JSON array directly
# in the prompt, so if you update CODEBOOK above, the prompt updates automatically.

SYSTEM_PROMPT = f"""
You are a qualitative research analyst applying thematic coding to interview transcripts.
You will receive a chunk of interview text and assign one or more themes from the codebook below.
For each assigned theme, extract a representative verbatim quote (max 2 sentences) and write
a 1-sentence analytic memo explaining why this theme applies.

Codebook: {json.dumps(CODEBOOK)}

Respond in JSON with this structure:
{{
  "codes": [
    {{
      "theme": "<theme from codebook>",
      "quote": "<verbatim quote>",
      "memo": "<1-sentence analytic note>"
    }}
  ]
}}
Only assign themes that clearly apply. If nothing applies, return {{"codes": []}}.
""".strip()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: TRANSCRIPT LOADING AND CLEANING
# ─────────────────────────────────────────────────────────────────────────────

def load_transcript(filepath: Path) -> str:
    """
    Load a .txt or .docx transcript to a plain string.

    For .docx files, we use python-docx to extract paragraph text — reading
    the raw file bytes would return XML. We filter empty paragraphs so blank
    lines in the Word document don't produce empty strings in our joined text.

    For .txt files, read_text() handles encoding automatically. If you have
    Latin-1 or Windows-1252 encoded files, add encoding='latin-1' here.

    Verify: the returned string should contain recognizable speaker turns
    and dialogue, not XML tags or binary characters.
    """
    if filepath.suffix == ".docx":
        from docx import Document
        doc = Document(filepath)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return filepath.read_text(encoding="utf-8")


def clean_text(text: str) -> str:
    """
    Strip timestamps, remove filler tokens, and normalize whitespace.

    We perform three targeted substitutions:
    1. Remove [HH:MM:SS] timestamps — common in Teams and Zoom exports.
       The regex matches the exact [00:00:00] format with brackets.
       Note: this is less aggressive than the cleaner's strip_noise() function,
       which also handles MM:SS and optional brackets. For transcripts that
       have already been through transcript_cleaner.py, this step is redundant
       but harmless.
    2. Remove (inaudible) markers — these aren't meaningful for theme coding
       and would appear in extracted quotes, reducing their readability.
    3. Collapse multiple consecutive spaces — left behind after the removals
       above. re.sub(r'\\s{2,}', ' ', text) replaces 2+ whitespace chars with
       one space. \\s matches spaces, tabs, and other whitespace characters.

    Verify: there should be no [HH:MM:SS] patterns or "(inaudible)" strings
    in the output. Whitespace should be consistent single spaces.
    """
    text = re.sub(r"\[\d{2}:\d{2}:\d{2}\]", "", text)
    text = re.sub(r"\(inaudible\)", "", text, flags=re.I)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: CHUNKING
# ─────────────────────────────────────────────────────────────────────────────

def chunk_text(text: str, max_tokens: int = MAX_CHUNK_TOKENS) -> list[str]:
    """
    Split a transcript into chunks at paragraph boundaries.

    Why paragraph boundaries? We want to avoid cutting a speaker's utterance
    in half — an incomplete thought passed to the LLM produces unreliable coding.
    Paragraph breaks (blank lines in the transcript) are natural turn boundaries.

    The "token" estimate here is a word count, not a true tokenizer count.
    On average, one word ≈ 1.3 tokens for English text, so a 1,500-word
    chunk is roughly 1,950 tokens. For tighter control, replace len(para.split())
    with tiktoken.encoding_for_model(MODEL).encode(para) — but for most
    transcripts, word count is close enough and avoids an extra dependency.

    Algorithm:
    - Split the text on newlines; strip each paragraph; drop empty strings.
    - Walk paragraphs one by one, adding them to the current chunk until
      adding the next paragraph would exceed max_tokens.
    - When the limit is reached, flush the current chunk to the list and
      start a new one.
    - After the loop, flush any remaining paragraphs as the final chunk.

    Verify: no individual chunk should have more than max_tokens words.
    sum(len(c.split()) for c in chunks) should approximately equal
    len(text.split()) — we're partitioning, not dropping content.
    """
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks, current, current_len = [], [], 0

    for para in paragraphs:
        tokens = len(para.split())
        if current_len + tokens > max_tokens and current:
            # Flush the current chunk before starting a new one
            chunks.append(" ".join(current))
            current, current_len = [], 0
        current.append(para)
        current_len += tokens

    if current:
        chunks.append(" ".join(current))

    return chunks


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: LLM CODING
# ─────────────────────────────────────────────────────────────────────────────

def code_chunk(chunk: str, participant_id: str, chunk_index: int) -> list[dict]:
    """
    Send one transcript chunk to the LLM and return coded rows.

    The API call uses temperature=0.2 (near-deterministic) because we want
    consistent, reproducible coding — not creative variation. Higher temperature
    would produce different codes on repeated runs of the same transcript, which
    undermines auditability.

    response_format={"type": "json_object"} tells the model to always return
    valid JSON. Without this, the model occasionally wraps the JSON in markdown
    code fences (```json ... ```) which break json.loads(). This parameter
    guarantees a clean parse.

    We store a chunk_preview (first 120 chars of the chunk) in each row so that
    when reviewing the coded CSV, the analyst can immediately see what passage
    generated each code without opening the original transcript.

    Error handling: we let API errors bubble up to the caller (run_pipeline).
    For production use, you'd wrap this in a try/except with exponential backoff
    to handle rate limits. For a portfolio demonstration with a small number of
    transcripts, letting it fail loudly is clearer than silently suppressing errors.

    Verify: result["codes"] should be a list. Each item should have "theme",
    "quote", and "memo" keys. The theme value should be one of the CODEBOOK strings —
    if the model hallucinates a new theme name, it won't match any codebook entry
    and should be treated as a data quality issue.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": chunk},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    raw    = response.choices[0].message.content
    result = json.loads(raw)
    rows   = []

    for code in result.get("codes", []):
        rows.append({
            "participant_id": participant_id,
            "chunk_index":    chunk_index,
            "theme":          code.get("theme"),
            "quote":          code.get("quote"),
            "memo":           code.get("memo"),
            "chunk_preview":  chunk[:120] + "...",
        })

    return rows


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: MAIN PIPELINE
# ─────────────────────────────────────────────────────────────────────────────

def run_pipeline():
    """
    Orchestrate the full pipeline: load → clean → chunk → code → export.

    We loop over all transcript files, process each one, accumulate coded rows
    into a single list, then write two outputs:
      1. A CSV with one row per theme assignment — the primary analytic dataset
      2. A Markdown summary report — a quick-read synthesis for the client

    The summary report uses pandas groupby operations:
      - value_counts() for theme frequency (how often each theme appeared)
      - groupby().first() to grab a representative quote per theme

    Why first() and not a "best" quote? In exploratory research, the first
    instance of a theme in the dataset is often the clearest example — it's
    the segment that triggered the analyst's (or model's) recognition of the
    pattern. More sophisticated selection (e.g., highest confidence score) would
    require additional fields from the LLM response.

    Verify: OUTPUT_CSV should have one row per code assignment. The number of
    rows should be >= number of transcripts (each transcript generates at least
    one code). OUTPUT_REPORT should have a header, theme frequency table, and
    at least one quote per theme that appeared in the data.
    """
    all_rows = []
    transcript_files = (
        list(TRANSCRIPT_DIR.glob("*.txt")) +
        list(TRANSCRIPT_DIR.glob("*.docx"))
    )

    if not transcript_files:
        print(f"No transcripts found in {TRANSCRIPT_DIR}. Add .txt or .docx files and re-run.")
        return

    for filepath in sorted(transcript_files):
        participant_id = filepath.stem   # use filename (without extension) as the ID
        print(f"Processing: {participant_id}")

        raw    = load_transcript(filepath)
        clean  = clean_text(raw)
        chunks = chunk_text(clean)

        for i, chunk in enumerate(chunks):
            rows = code_chunk(chunk, participant_id, i)
            all_rows.extend(rows)
            print(f"  Chunk {i+1}/{len(chunks)}: {len(rows)} codes applied.")

    if not all_rows:
        print("No codes generated.")
        return

    # ── Export 1: Coded CSV ───────────────────────────────────────────────────
    # Create the output directory if it doesn't exist, then write the DataFrame.
    # index=False omits the row number column that pandas adds by default —
    # it's meaningless to the analyst and clutters the CSV.

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(all_rows)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nCoded output saved to {OUTPUT_CSV} ({len(df)} rows).")

    # ── Export 2: Thematic Summary Report ─────────────────────────────────────
    # We build the Markdown report as a list of strings and join at the end.
    # This is easier to reason about than string concatenation — each append()
    # call adds one logical section, and the final join produces valid Markdown.

    theme_counts = df["theme"].value_counts()
    top_quotes   = df.groupby("theme").first()["quote"]

    report_lines = [
        "# Thematic Analysis Summary\n",
        f"**Total coded segments:** {len(df)}  ",
        f"**Participants processed:** {df['participant_id'].nunique()}  ",
        f"**Themes identified:** {df['theme'].nunique()}\n",
        "## Theme Frequency\n",
        "| Theme | Count |",
        "|---|---|",
    ]

    for theme, count in theme_counts.items():
        report_lines.append(f"| {theme} | {count} |")

    report_lines.append("\n## Representative Quotes by Theme\n")
    for theme, quote in top_quotes.items():
        report_lines.append(f"**{theme}**")
        report_lines.append(f"> {quote}\n")

    OUTPUT_REPORT.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Summary report saved to {OUTPUT_REPORT}.")


if __name__ == "__main__":
    # Guard ensures the pipeline only runs when this file is executed directly.
    # Importing the file (e.g., to use load_transcript() in a notebook) won't
    # trigger run_pipeline() automatically.
    run_pipeline()
