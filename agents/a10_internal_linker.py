"""الوكيل 10 — رابط الروابط الداخلية.
بعد كل نشر يعيد بناء شبكة الروابط: يضيف روابط سياقية بين المقالات المتقاربة
داخل نفس المحور. الروابط الداخلية أرخص طريقة لرفع الترتيب.
"""
import re
from .base import read_posts, SITE, log

L = log("linker")
MAX_OUT = 4
BASE = (SITE["site"].get("base_path") or "").rstrip("/")


def _overlap(a: dict, b: dict) -> int:
    ta = set((a["front"].get("tags") or []) + [a["front"].get("cluster")])
    tb = set((b["front"].get("tags") or []) + [b["front"].get("cluster")])
    return len(ta & tb)


def run() -> int:
    posts = read_posts()
    if len(posts) < 2:
        return 0
    added = 0
    for post in posts:
        body = post["body"]
        existing = set(re.findall(rf"\]\({re.escape(BASE)}/blog/([a-z0-9-]+)/?\)", body))
        if len(existing) >= MAX_OUT:
            continue
        cands = sorted(
            (p for p in posts if p["front"]["slug"] != post["front"]["slug"]
             and p["front"]["slug"] not in existing and not p["front"].get("draft")),
            key=lambda p: _overlap(post, p), reverse=True,
        )
        for cand in cands[: MAX_OUT - len(existing)]:
            anchor = cand["front"].get("keyword") or cand["front"]["title"]
            pat = re.compile(rf"(?<!\[)\b({re.escape(anchor)})\b(?!\]|\()", re.I)
            m = pat.search(body)
            if m:
                body = body[:m.start()] + f'[{m.group(1)}]({BASE}/blog/{cand["front"]["slug"]}/)' + body[m.end():]
            else:
                body = body.rstrip() + (
                    f"\n\n**Related:** [{cand['front']['title']}]({BASE}/blog/{cand['front']['slug']}/)\n"
                )
            added += 1
        if body != post["body"]:
            txt = post["path"].read_text(encoding="utf-8")
            head = txt.split("---", 2)[1]
            post["path"].write_text(f"---{head}---\n\n{body.strip()}\n", encoding="utf-8")
    L.info("أضيف %s رابط داخلي عبر %s مقال", added, len(posts))
    return added
