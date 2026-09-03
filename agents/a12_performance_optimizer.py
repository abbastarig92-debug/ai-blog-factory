"""الوكيل 12 — محلّل الأداء.
أسبوعياً: يقرأ بيانات Search Console (إن توفّرت الصلاحية) أو يعمل بالإرشاد الزمني،
يحدد المقالات الضعيفة، ويعيد كتابتها/يحدّثها بدل نشر المزيد بلا تحسين.
"""
import os, json, datetime as dt, urllib.request, urllib.parse
from .base import LLM, SITE, read_posts, load_state, save_state, log

L = log("optimizer")

SYSTEM = """You are a content performance analyst. You prescribe the smallest change that moves rankings:
a better title, a missing section, a stronger opening — not a rewrite for its own sake."""


def gsc_rows() -> list[dict]:
    """يتطلب GSC_ACCESS_TOKEN (OAuth). يعيد قائمة فارغة إن لم يتوفر."""
    token = os.getenv("GSC_ACCESS_TOKEN", "")
    site = SITE["site"]["domain"]
    if not token:
        return []
    end = dt.date.today()
    start = end - dt.timedelta(days=28)
    body = json.dumps({
        "startDate": start.isoformat(), "endDate": end.isoformat(),
        "dimensions": ["page", "query"], "rowLimit": 500,
    }).encode()
    req = urllib.request.Request(
        f"https://searchconsole.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(site, safe='')}/searchAnalytics/query",
        data=body, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.load(r).get("rows", [])
    except Exception as e:  # noqa: BLE001
        L.warning("تعذّر قراءة Search Console: %s", e)
        return []


def run() -> list[dict]:
    posts = read_posts()
    rows = gsc_rows()
    perf = {}
    for r in rows:
        page, query = r["keys"][0], r["keys"][1]
        slug = page.rstrip("/").split("/")[-1]
        d = perf.setdefault(slug, {"clicks": 0, "impressions": 0, "queries": []})
        d["clicks"] += r.get("clicks", 0)
        d["impressions"] += r.get("impressions", 0)
        d["queries"].append({"q": query, "pos": round(r.get("position", 0), 1),
                             "imp": r.get("impressions", 0)})

    actions = []
    for p in posts:
        f = p["front"]
        slug = f["slug"]
        age_days = (dt.datetime.now(dt.timezone.utc) -
                    dt.datetime.fromisoformat(str(f["pubDate"]))).days
        d = perf.get(slug)
        if d:
            ctr = d["clicks"] / d["impressions"] if d["impressions"] else 0
            striking = [q for q in d["queries"] if 5 <= q["pos"] <= 20]
            if d["impressions"] > 100 and ctr < 0.015:
                actions.append({"slug": slug, "action": "rewrite_title_meta",
                                "reason": f"ظهور {d['impressions']} ونقر ضعيف {ctr:.1%}",
                                "queries": striking[:5]})
            elif striking and age_days > 21:
                actions.append({"slug": slug, "action": "expand_sections",
                                "reason": "كلمات في المركز 5-20 تحتاج تعميقاً",
                                "queries": striking[:5]})
        elif age_days > 60:
            actions.append({"slug": slug, "action": "refresh_or_merge",
                            "reason": "بلا ظهور بعد 60 يوماً", "queries": []})

    # تنفيذ التوصيات على العناوين — الأرخص والأسرع أثراً
    for a in actions:
        if a["action"] != "rewrite_title_meta":
            continue
        post = next((p for p in posts if p["front"]["slug"] == a["slug"]), None)
        if not post:
            continue
        try:
            new = LLM().json(SYSTEM, f"""Current title: {post['front']['title']}
Current description: {post['front']['description']}
Real queries this page shows for: {json.dumps(a['queries'])}

Rewrite for click-through. Return JSON: {{"title": "<=60 chars", "description": "140-158 chars"}}""",
                             max_tokens=600)
            txt = post["path"].read_text(encoding="utf-8")
            txt = txt.replace(f'title: {post["front"]["title"]}', f'title: {new["title"]}', 1)
            post["path"].write_text(txt, encoding="utf-8")
            a["applied"] = new
        except Exception as e:  # noqa: BLE001
            L.warning("تعذّر تحديث %s: %s", a["slug"], e)

    save_state("optimizer_report", {"date": dt.date.today().isoformat(),
                                    "gsc_connected": bool(rows), "actions": actions})
    L.info("تقرير الأداء: %s إجراء (GSC=%s)", len(actions), bool(rows))
    return actions
