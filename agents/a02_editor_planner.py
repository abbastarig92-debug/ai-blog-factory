"""الوكيل 2 — رئيس التحرير.
يختار من مخزون الكلمات ما يُكتب اليوم، ويحوّله إلى بريف تحريري كامل.
يوازن بين المحاور حتى لا يتضخم محور على حساب غيره.
"""
from collections import Counter
from .base import LLM, NICHE, SITE, load_state, save_state, log, read_posts

L = log("editor")

SYSTEM = """You are an editor-in-chief who briefs writers. Your briefs are specific enough that
two different writers would produce nearly the same structure. You always define the angle,
the reader's job-to-be-done, and what would make this page better than the current top 3 results."""


def run(count: int | None = None) -> list[dict]:
    count = count or SITE["publishing"]["posts_per_day"]
    pool = load_state("keyword_pool", [])
    if not pool:
        L.warning("مخزون الكلمات فارغ — شغّل a01_keyword_scout أولاً")
        return []

    published = read_posts()
    cluster_counts = Counter(p["front"].get("cluster") for p in published)

    # ترتيب: المحور الأقل تغطية أولاً، ثم النية التجارية، ثم الأسهل
    intent_rank = {"commercial": 0, "transactional": 1, "informational": 2}
    pool.sort(key=lambda k: (
        cluster_counts.get(k.get("cluster"), 0),
        intent_rank.get(k.get("intent"), 3),
        k.get("est_difficulty", 50),
    ))
    picked, rest = pool[:count], pool[count:]
    save_state("keyword_pool", rest)

    briefs = []
    for kw in picked:
        cluster = next((c for c in NICHE["clusters"] if c["id"] == kw.get("cluster")), NICHE["clusters"][0])
        prompt = f"""Target keyword: "{kw['keyword']}"
Format: {kw.get('format')}
Intent: {kw.get('intent')}
Cluster: {cluster['title']}
Audience: {NICHE['niche']['audience']}
Author angle: {NICHE['niche']['expertise_angle']}
Search promise: {kw.get('search_promise', '')}

Produce an editorial brief as JSON:
{{"working_title": str,
  "angle": "the specific point of view, one sentence",
  "reader_job": "what the reader is trying to get done",
  "outline": [{{"h2": str, "points": [str, str, str]}}],
  "tools_to_cover": [str],
  "must_answer_questions": [str],
  "comparison_table": {{"needed": bool, "columns": [str]}},
  "differentiator": "why this beats the current top 3 results",
  "internal_link_targets": [str]}}
Outline must have 5-8 H2 sections. Front-load the answer: the first section must satisfy the search promise."""
        brief = LLM().json(SYSTEM, prompt, max_tokens=3000)
        brief["keyword"] = kw
        briefs.append(brief)
        L.info("بريف جاهز: %s", brief.get("working_title"))

    queue = load_state("brief_queue", [])
    queue.extend(briefs)
    save_state("brief_queue", queue)
    return briefs


if __name__ == "__main__":
    run()
