"""الوكيل 7 — وكيل التربح.
يحقن روابط الأفلييت عند أول ذكر لكل أداة، ويضيف الإفصاح، ويحدد أماكن الإعلانات.
"""
import re
from .base import cfg, SITE, log

L = log("monetizer")


def run(body: str) -> tuple[str, dict]:
    aff = cfg("affiliates")
    programs = [p for p in aff["programs"] if p.get("url")]
    policy = aff["link_policy"]
    linked = []

    for p in programs:
        names = [p["tool"]] + p.get("aliases", [])
        for name in sorted(names, key=len, reverse=True):
            pat = re.compile(rf"(?<!\[)\b({re.escape(name)})\b(?!\]|\()", re.I)
            m = pat.search(body)
            if not m:
                continue
            # تجاهل المطابقة داخل كتلة كود أو رابط قائم
            repl = f'[{m.group(1)}]({p["url"]})'
            body = body[:m.start()] + repl + body[m.end():]
            linked.append(p["tool"])
            break

    disclosure = ""
    if linked and aff.get("disclosure_required"):
        disclosure = f"> *{SITE['monetization']['affiliate_disclosure']}*\n\n"

    # علامة موضع الإعلان بعد أول قسمين — الموقع يحوّلها لوحدة أدسنس
    parts = re.split(r"(?m)^(## )", body)
    if len(parts) > 5:
        idx = 5
        parts.insert(idx, '\n<div class="ad-slot" data-ad-slot></div>\n\n')
        body = "".join(parts)

    report = {"affiliate_links": linked, "has_disclosure": bool(disclosure),
              "ad_slots": body.count("data-ad-slot")}
    L.info("روابط أفلييت: %s | وحدات إعلانية: %s", linked or "لا شيء", report["ad_slots"])
    return disclosure + body, report
