"""الوكيل 6 — مهندس السيو.
ينتج العنوان والوصف والسلَق والوسوم وبيانات schema.org، ويتحقق من البنية على الصفحة.
"""
import re
from .base import LLM, SITE, log, slugify

L = log("seo")

SYSTEM = """You are a technical SEO specialist. Titles are written for the click, not for the crawler.
Meta descriptions state the payoff, not the topic. You never keyword-stuff."""


def run(body: str, brief: dict) -> dict:
    kw = brief["keyword"]["keyword"]
    prompt = f"""Target keyword: "{kw}"
Working title: {brief['working_title']}
Format: {brief['keyword'].get('format')}

Article (first 1200 chars):
{body[:1200]}

Return JSON:
{{"title": "<=60 chars, contains the keyword naturally, written for the click",
  "slug": "kebab-case, <=6 words, contains the keyword",
  "description": "140-158 chars, states the payoff, contains the keyword once",
  "og_title": "<=70 chars, punchier than the title",
  "tags": [4-6 lowercase tags],
  "faq": [{{"q": str, "a": "<=45 words"}}] taken from the article's FAQ section,
  "key_takeaway": "one sentence a reader could quote"}}"""

    meta = LLM().json(SYSTEM, prompt, max_tokens=2000)
    meta["slug"] = slugify(meta.get("slug") or kw)
    meta["title"] = meta["title"][:65]
    meta["description"] = meta["description"][:158]

    # فحوصات بنيوية على الصفحة
    audit = {
        "h2_count": len(re.findall(r"^## ", body, re.M)),
        "word_count": len(body.split()),
        "has_table": "|" in body and "---" in body,
        "keyword_in_first_100": kw.lower() in " ".join(body.split()[:100]).lower(),
        "has_faq": bool(re.search(r"^##\s+.*question", body, re.I | re.M)),
    }
    audit["passes"] = (
        audit["h2_count"] >= 4
        and audit["word_count"] >= SITE["publishing"]["min_words"] * 0.8
        and audit["keyword_in_first_100"]
    )
    meta["audit"] = audit
    L.info("سيو: %s كلمة، %s عناوين H2، اجتاز=%s",
           audit["word_count"], audit["h2_count"], audit["passes"])
    return meta
