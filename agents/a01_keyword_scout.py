"""الوكيل 1 — كشّاف الكلمات المفتاحية.
يولّد فرص كلمات مطابقة لقواعد النيتش، ويستبعد ما نُشر أو ما هو في الطابور.
"""
from .base import LLM, NICHE, load_state, save_state, log, slugify

L = log("keyword_scout")

SYSTEM = """You are a senior SEO strategist for a brand-new website with zero domain authority.
You only propose keywords a new site can realistically rank for within 3-6 months:
long-tail, low competition, clear searcher intent, and commercially useful.
You never propose head terms dominated by G2, Zapier, HubSpot or Wikipedia."""


def run(limit: int = 20) -> list[dict]:
    llm = LLM()
    rules = NICHE["keyword_rules"]
    clusters = NICHE["clusters"]
    seen = set(load_state("keywords_seen", []))

    prompt = f"""Niche: {NICHE['niche']['primary']}
Audience: {NICHE['niche']['audience']}

Topic clusters and seed terms:
{chr(10).join(f"- [{c['id']}] {c['title']}: {', '.join(c['seeds'])}" for c in clusters)}

Rules:
- Max estimated keyword difficulty: {rules['max_difficulty']}/100
- Min estimated monthly volume: {rules['min_monthly_volume']}
- Prefer long-tail (4+ words) with these modifiers: {', '.join(rules['must_include_modifiers'])}
- Intent priority: {', '.join(rules['intent_priority'])}
- Banned: {', '.join(rules['banned_topics'])}
- Do NOT repeat any of these already-used keywords: {sorted(seen)[:120]}

Return {limit} keyword opportunities as a JSON array. Each object:
{{"keyword": str, "cluster": cluster id, "intent": "commercial"|"transactional"|"informational",
  "est_volume": int, "est_difficulty": int, "format": "review"|"comparison"|"how-to"|"listicle"|"alternatives",
  "why_winnable": str, "search_promise": "what the reader must get in the first screen"}}"""

    items = llm.json(SYSTEM, prompt, max_tokens=4000)
    fresh = []
    for it in items:
        kw = it.get("keyword", "").strip().lower()
        if not kw or kw in seen:
            continue
        if it.get("est_difficulty", 100) > rules["max_difficulty"]:
            continue
        it["keyword"] = kw
        it["slug"] = slugify(kw)
        fresh.append(it)
        seen.add(kw)

    save_state("keywords_seen", sorted(seen))
    pool = load_state("keyword_pool", [])
    pool.extend(fresh)
    save_state("keyword_pool", pool)
    L.info("أضيفت %s كلمة مفتاحية جديدة (المخزون: %s)", len(fresh), len(pool))
    return fresh


if __name__ == "__main__":
    run()
