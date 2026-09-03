"""الوكيل 9 — الناشر.
يجمّع الـ frontmatter ويكتب ملف المقال في مجلد المحتوى، ويسجّل النشر في الحالة.
"""
import datetime as dt
from .base import SITE, write_post, load_state, save_state, log

L = log("publisher")


def run(brief: dict, body: str, meta: dict, cover: str, extras: dict) -> str:
    front = {
        "title": meta["title"],
        "slug": meta["slug"],
        "description": meta["description"],
        "pubDate": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "updatedDate": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "author": SITE["site"]["author"],
        "cluster": brief["keyword"].get("cluster"),
        "format": brief["keyword"].get("format"),
        "keyword": brief["keyword"]["keyword"],
        "tags": meta.get("tags", []),
        "cover": cover,
        "ogTitle": meta.get("og_title", meta["title"]),
        "keyTakeaway": meta.get("key_takeaway", ""),
        "faq": meta.get("faq", []),
        "wordCount": meta.get("audit", {}).get("word_count", 0),
        "affiliateLinks": extras.get("affiliate_links", []),
        "sources": [{"title": s["title"], "url": s["url"]} for s in extras.get("sources", [])[:8]],
        "draft": not meta.get("audit", {}).get("passes", False),
    }
    path = write_post(front, body)

    log_ = load_state("published", [])
    log_.append({"slug": front["slug"], "title": front["title"], "date": front["pubDate"],
                 "keyword": front["keyword"], "cluster": front["cluster"],
                 "draft": front["draft"]})
    save_state("published", log_)
    L.info("نُشر: %s (مسودة=%s)", path.name, front["draft"])
    return front["slug"]
