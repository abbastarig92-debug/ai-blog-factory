"""الوكيل 1 — كشّاف الكلمات المفتاحية.
يولّد فرص كلمات مطابقة لقواعد النيتش، ويستبعد ما نُشر أو ما هو في الطابور.
يرجّح الأدوات التي لدينا روابط أفلييت فعّالة لها — الكتابة عن أداة بلا رابط عمل بلا مقابل.
"""
from .base import LLM, NICHE, cfg, load_state, save_state, log, slugify

L = log("keyword_scout")

SYSTEM = """You are a senior SEO strategist for a brand-new website with zero domain authority.
You only propose keywords a new site can realistically rank for within 3-6 months:
long-tail, low competition, clear searcher intent, and commercially useful.
You never propose head terms dominated by G2, Zapier, HubSpot or Wikipedia.
This is a commercial affiliate site: a keyword that cannot lead to a commission is a wasted article."""


def _paid_tools() -> list[dict]:
    """الأدوات التي لها رابط أفلييت فعلي في config/affiliates.yaml."""
    try:
        programs = cfg("affiliates").get("programs", [])
    except Exception as e:                      # الملف مفقود أو تالف — لا نُسقط التشغيل
        L.warning("تعذّر قراءة affiliates.yaml (%s) — المتابعة بلا ترجيح تجاري", e)
        return []
    return [p for p in programs if (p.get("url") or "").strip()]


def _match_paid(keyword: str, paid: list[dict]) -> str:
    """اسم الأداة المدفوعة المذكورة في الكلمة، أو سلسلة فارغة."""
    low = keyword.lower()
    for p in paid:
        for name in [p["tool"]] + list(p.get("aliases") or []):
            if name.lower() in low:
                return p["tool"]
    return ""


def run(limit: int = 20) -> list[dict]:
    llm = LLM()
    rules = NICHE["keyword_rules"]
    clusters = NICHE["clusters"]
    seen = set(load_state("keywords_seen", []))

    paid = _paid_tools()
    # سقف مزدوج: 60% من الدفعة، وبحد أقصى كلمتان لكل أداة مدفوعة.
    # بأداتين فقط لا نريد عشرين مقالاً عنهما — تتنافس مقالاتنا مع بعضها وتخسر جميعاً.
    quota = max(1, min(round(limit * 0.6), len(paid) * 2)) if paid else 0
    money_block = ""
    if paid:
        money_block = f"""

MONETIZATION PRIORITY — treat this as a hard rule, not a preference:
This site earns a commission ONLY on these tools: {', '.join(p['tool'] for p in paid)}.
At least {quota} of the {limit} keywords you return MUST name one of those tools directly
inside the keyword itself — as a review, a head-to-head comparison, or an alternatives query.
Shapes that work: "<paid tool> vs <rival>", "<paid tool> review for <audience>",
"best <paid tool> alternatives for <use case>", "is <paid tool> worth it for <use case>".
Never return more than 2 keywords naming the same paid tool: near-duplicate pages compete
with each other in search and both lose. Vary the audience, the use case and the rival.
The rest may target any topic, but prefer ones where a paid tool above is the natural
recommendation. Never invent a tool that does not exist, and never force a paid tool into
a keyword where a reader would not expect it — a mismatched article ranks for nothing."""

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
- Do NOT repeat any of these already-used keywords: {sorted(seen)[:120]}{money_block}

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
        it["paid_tool"] = _match_paid(kw, paid)     # يقرأه رئيس التحرير لترجيح الاختيار
        fresh.append(it)
        seen.add(kw)

    save_state("keywords_seen", sorted(seen))
    pool = load_state("keyword_pool", [])
    pool.extend(fresh)
    save_state("keyword_pool", pool)
    monetized = sum(1 for k in fresh if k.get("paid_tool"))
    L.info("أضيفت %s كلمة جديدة منها %s قابلة للتربح (المخزون: %s)", len(fresh), monetized, len(pool))
    if paid and not monetized:
        L.warning("لا كلمة واحدة تذكر أداة مدفوعة — راجع صياغة الترجيح التجاري")
    return fresh


if __name__ == "__main__":
    run()
