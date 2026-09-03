"""الوكيل 4 — الكاتب.
يحوّل البريف + المصادر إلى مقال كامل بصيغة Markdown، بصوت خبير عملي لا صوت روبوت.
"""
from .base import LLM, NICHE, SITE, log

L = log("writer")

SYSTEM = """You write for practitioners. Rules you never break:

VOICE
- First-hand and specific. "In a 40-clip batch, the render queue stalled twice" beats "it can be slow".
- No AI throat-clearing: never open with "In today's fast-paced world", "In the ever-evolving landscape",
  "Whether you're a beginner or a pro", or a definition of a term the reader already knows.
- Never use: delve, leverage (as a verb), robust, seamless, game-changer, unlock, elevate, tapestry,
  landscape (figurative), "it's important to note", "let's dive in".
- Short paragraphs (1-3 sentences). Vary sentence length. Contractions are fine.

SUBSTANCE
- Answer the search promise in the first 60 words. No preamble.
- Every claim about pricing, limits or features must come from the provided sources.
  If you have no source for a number, write the qualitative fact instead and never invent a figure.
- Include real trade-offs and at least one honest downside per tool. Credibility is the product.
- Concrete workflows, settings, and numbers the reader can copy.

FORMAT
- Markdown only. Start with the first H2 — never repeat the title as an H1.
- Use tables for comparisons, bold for scannable takeaways, and short bullet lists.
- End with a "Frequently asked questions" H2 with 4 concise Q&A pairs as H3s."""


def run(brief: dict, research: dict) -> str:
    kw = brief["keyword"]
    src = research.get("sources", [])
    src_txt = "\n".join(f"[{i+1}] {s['title']} — {s['url']}\n{s['snippet']}" for i, s in enumerate(src)) \
        or "NO SOURCES AVAILABLE. Do not state any price, limit, or dated statistic."

    outline = "\n".join(
        f"## {s['h2']}\n" + "\n".join(f"   - {p}" for p in s.get("points", []))
        for s in brief.get("outline", [])
    )

    prompt = f"""Write the article.

Title: {brief['working_title']}
Target keyword: "{kw['keyword']}" (use naturally: title area, first 100 words, one H2, conclusion — never stuffed)
Format: {kw.get('format')}
Angle: {brief.get('angle')}
Reader's job: {brief.get('reader_job')}
Differentiator: {brief.get('differentiator')}
Author perspective: {NICHE['niche']['expertise_angle']}
Length: {SITE['publishing']['min_words']}-{SITE['publishing']['max_words']} words.

Outline to follow:
{outline}

Must answer: {'; '.join(brief.get('must_answer_questions', []))}
Comparison table needed: {brief.get('comparison_table', {}).get('needed')} — columns: {brief.get('comparison_table', {}).get('columns')}

SOURCES (the only place numbers may come from):
{src_txt}

Output: the article body in Markdown. Nothing else."""

    body = LLM().chat(SYSTEM, prompt, max_tokens=8000, temperature=0.75)
    L.info("كُتب المقال (%s كلمة تقريباً)", len(body.split()))
    return body


if __name__ == "__main__":
    print("module")
