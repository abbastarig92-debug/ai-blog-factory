"""الوكيل 3 — الباحث.
يجمع حقائق حديثة عن الأدوات المذكورة. يستخدم Tavily أو Serper إن وُجد مفتاح،
وإلا يعمل بلا بحث ويُعلِم الكاتب بعدم الاستشهاد بأرقام غير مؤكدة.
"""
import os, json, urllib.request
from .base import log

L = log("researcher")


def _tavily(query: str, key: str) -> list[dict]:
    req = urllib.request.Request(
        "https://api.tavily.com/search",
        data=json.dumps({"api_key": key, "query": query, "max_results": 5,
                         "search_depth": "basic"}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    return [{"title": x.get("title"), "url": x.get("url"), "snippet": x.get("content", "")[:600]}
            for x in data.get("results", [])]


def _serper(query: str, key: str) -> list[dict]:
    req = urllib.request.Request(
        "https://google.serper.dev/search",
        data=json.dumps({"q": query, "num": 5}).encode(),
        headers={"X-API-KEY": key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    return [{"title": x.get("title"), "url": x.get("link"), "snippet": x.get("snippet", "")}
            for x in data.get("organic", [])]


def search(query: str) -> list[dict]:
    tav, ser = os.getenv("TAVILY_API_KEY", ""), os.getenv("SERPER_API_KEY", "")
    try:
        if tav:
            return _tavily(query, tav)
        if ser:
            return _serper(query, ser)
    except Exception as e:  # noqa: BLE001
        L.warning("فشل البحث (%s) — المتابعة بدون مصادر", e)
    return []


def run(brief: dict) -> dict:
    kw = brief["keyword"]["keyword"]
    queries = [kw, f"{kw} pricing 2026"] + [f"{t} review pricing" for t in brief.get("tools_to_cover", [])[:4]]
    sources, seen = [], set()
    for q in queries:
        for s in search(q):
            if s["url"] in seen:
                continue
            seen.add(s["url"])
            sources.append(s)
    L.info("%s مصدر لـ «%s»", len(sources), kw)
    return {"sources": sources[:18], "has_sources": bool(sources)}


if __name__ == "__main__":
    print(search("best ai video generator 2026"))
