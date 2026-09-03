"""الوكيل 5 — المدقّق والرقيب.
يمسح المقال بحثاً عن أرقام بلا مصدر، ادعاءات مطلقة، ومواضيع محظورة،
ثم يعيد نسخة مصححة. هذا هو صمّام الأمان في نظام بلا مراجعة بشرية.
"""
import re
from .base import LLM, NICHE, log

L = log("fact_checker")

SYSTEM = """You are a fact-checking editor with veto power. You remove risk without flattening the writing.
You fix, you don't rewrite from scratch. You return the corrected article only."""

RISKY = [
    (r"\bguarantee(d|s)?\b", "وعد مطلق"),
    (r"\b(100%|always works|never fails)\b", "ادعاء مطلق"),
    (r"\b(cure|diagnos|treat)\w*\b", "ادعاء طبي"),
    (r"\b(invest|stock|trading) (advice|tips)\b", "نصيحة مالية"),
]


def scan(body: str) -> list[str]:
    flags = []
    for pat, label in RISKY:
        if re.search(pat, body, re.I):
            flags.append(label)
    for topic in NICHE["keyword_rules"]["banned_topics"]:
        if re.search(rf"\b{re.escape(topic)}\b", body, re.I):
            flags.append(f"موضوع محظور: {topic}")
    return flags


def run(body: str, research: dict) -> tuple[str, list[str]]:
    src = research.get("sources", [])
    src_txt = "\n".join(f"[{i+1}] {s['title']} — {s['url']}: {s['snippet'][:300]}"
                        for i, s in enumerate(src)) or "NO SOURCES PROVIDED."
    flags = scan(body)

    prompt = f"""Check this article against the sources and fix problems in place.

Fix these, and nothing else:
1. Any price, percentage, limit, date or statistic NOT supported by the sources -> replace with a
   qualitative statement, or delete the sentence. Never invent a replacement number.
2. Absolute claims ("guaranteed", "always", "the best for everyone") -> hedge or make conditional.
3. Medical, legal or financial advice framing -> remove.
4. Named-person quotes or fabricated case studies -> remove.
5. Broken internal logic or contradictions between sections.

Automated flags to address: {flags or 'none'}

SOURCES:
{src_txt}

ARTICLE:
{body}

Return the corrected article in Markdown only."""

    fixed = LLM().chat(SYSTEM, prompt, max_tokens=8000, temperature=0.2)
    remaining = scan(fixed)
    L.info("التدقيق تم — تنبيهات قبل: %s / بعد: %s", len(flags), len(remaining))
    return fixed, remaining
