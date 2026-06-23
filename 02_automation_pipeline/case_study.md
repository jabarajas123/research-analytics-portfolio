# Portfolio Item 2 — Qualitative Research Automation Pipeline

## LLM-Powered Transcript Processing for Large-Scale Qualitative Studies

**The problem:** A research team had 40+ hours of interview transcripts from a multi-site qualitative study. Manual thematic coding at this volume would take 3-4 weeks and introduced inconsistency across coders. The team needed a faster, more systematic approach without losing the interpretive depth that qualitative research requires.

**What I built:** A production Python pipeline that ingests raw .txt or .docx transcripts, cleans timestamps and transcription artifacts, chunks the text at paragraph boundaries to stay within model context limits, sends each chunk to an LLM with a structured codebook prompt, and returns a coded CSV with verbatim quotes and analytic memos for each applied theme. The pipeline generates a markdown summary report with theme frequencies and representative quotes across participants.

**Why it matters:** The pipeline reduced initial coding time from weeks to hours. More importantly, it produced a consistent structured output that a human analyst could then review, challenge, and refine — rather than starting from a blank document. I built this as a shared team tool; it was adopted across multiple projects after initial deployment.

**Design decisions worth noting:** Temperature set to 0.2 to minimize hallucination variance across chunks. Chunking at paragraph boundaries rather than token-count cutoffs preserves speaker turns, which is critical for interview data. The codebook is modifiable at the top of the script — clients can swap in their own themes without touching the pipeline logic.

**Artifact attached:** Full Python script (`transcript_pipeline.py`) — clean, commented, and ready to run with your own transcripts and OpenAI key.

---
*Methods: Python | OpenAI API | python-docx | pandas | Qualitative thematic coding | NLP pipeline design | Research automation*
