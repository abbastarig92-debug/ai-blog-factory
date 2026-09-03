"""الوكيل 8 — المصمّم.
ينتج صورة غلاف SVG بهوية الموقع (مجاناً، بلا أي API) لكل مقال:
شبكة هندسية + وسم المحور + العنوان. متسقة بصرياً عبر كل الموقع.
"""
import hashlib, html, pathlib, textwrap
from .base import SITE, ROOT, log

L = log("illustrator")
OUT = ROOT / "site" / "public" / "covers"


def _wrap(title: str, width: int = 26) -> list[str]:
    return textwrap.wrap(title, width=width)[:3]


def run(title: str, slug: str, cluster_label: str) -> str:
    OUT.mkdir(parents=True, exist_ok=True)
    b = SITE["brand"]
    seed = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)
    lines = _wrap(title)
    tspans = "".join(
        f'<tspan x="80" dy="{0 if i == 0 else 78}">{html.escape(l)}</tspan>'
        for i, l in enumerate(lines)
    )
    # شبكة أعمدة عشوائية مستقرة مشتقة من السلَق
    bars = "".join(
        f'<rect x="{760 + i*38}" y="{560 - ((seed >> (i*3)) % 9 + 2) * 34}" width="22" '
        f'height="{((seed >> (i*3)) % 9 + 2) * 34}" rx="4" fill="{b["color_accent"]}" '
        f'opacity="{0.25 + (i % 5) * 0.15:.2f}"/>'
        for i in range(9)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-label="{html.escape(title)}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{b['color_primary']}"/><stop offset="1" stop-color="#1E293B"/>
</linearGradient></defs>
<rect width="1200" height="630" fill="url(#g)"/>
<g opacity="0.07" stroke="#FFFFFF" stroke-width="1">
{"".join(f'<line x1="0" y1="{y}" x2="1200" y2="{y}"/>' for y in range(0, 631, 42))}
{"".join(f'<line x1="{x}" y1="0" x2="{x}" y2="630"/>' for x in range(0, 1201, 42))}
</g>
{bars}
<rect x="80" y="86" width="{len(cluster_label)*11 + 40}" height="38" rx="19" fill="{b['color_accent']}"/>
<text x="{100}" y="112" font-family="{b['font_heading']}, Segoe UI, sans-serif" font-size="18" font-weight="700" fill="{b['color_primary']}" letter-spacing="1">{html.escape(cluster_label.upper())}</text>
<text x="80" y="270" font-family="{b['font_heading']}, Segoe UI, sans-serif" font-size="64" font-weight="800" fill="#FFFFFF">{tspans}</text>
<text x="80" y="565" font-family="{b['font_body']}, Segoe UI, sans-serif" font-size="24" font-weight="600" fill="{b['color_accent']}">{html.escape(SITE['site']['name'])}</text>
</svg>'''
    path = OUT / f"{slug}.svg"
    path.write_text(svg, encoding="utf-8")
    L.info("غلاف: %s", path.name)
    return f"/covers/{slug}.svg"
