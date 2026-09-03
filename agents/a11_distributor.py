"""الوكيل 11 — الموزّع.
يحوّل كل مقال منشور إلى منشورات جاهزة لكل منصة ويضعها في صندوق الصادر.
إن وُجدت مفاتيح النشر (Buffer/X/LinkedIn) يمكن ربطها لاحقاً بلا تغيير في البنية.
"""
from .base import LLM, SITE, load_state, save_state, log

L = log("distributor")

SYSTEM = """You write social copy that earns the click without clickbait.
Each platform gets native phrasing, never the same text pasted five times.
No hashtag spam: two hashtags maximum, and only if they're real communities."""


def run(slug: str, title: str, takeaway: str) -> dict:
    url = f"{SITE['site']['domain'].rstrip('/')}/blog/{slug}/"
    prompt = f"""Article: {title}
Key takeaway: {takeaway}
URL: {url}

Return JSON:
{{"x": "<=270 chars, a specific claim or number first, then the link",
  "linkedin": "3 short paragraphs, practitioner tone, ends with the link",
  "reddit": {{"subreddit_suggestions": [str], "title": str, "comment_first_body": "value-first, link only if allowed"}},
  "newsletter": "120-word blurb",
  "pinterest": "<=200 chars description",
  "quora_targets": [str]}}"""
    pack = LLM().json(SYSTEM, prompt, max_tokens=2000)
    pack.update({"slug": slug, "url": url, "status": "queued"})
    box = load_state("outbox", [])
    box.append(pack)
    save_state("outbox", box)
    L.info("حزمة توزيع جاهزة لـ %s", slug)
    return pack
