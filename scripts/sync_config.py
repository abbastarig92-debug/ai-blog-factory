#!/usr/bin/env python3
"""يحوّل config/site.yaml إلى site/src/site.json ليقرأه Astro — مصدر واحد للحقيقة."""
import json, pathlib, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
cfg = yaml.safe_load((ROOT / "config" / "site.yaml").read_text(encoding="utf-8"))
niche = yaml.safe_load((ROOT / "config" / "niche.yaml").read_text(encoding="utf-8"))
out = {
    "name": cfg["site"]["name"],
    "tagline": cfg["site"]["tagline"],
    "url": cfg["site"]["domain"],
    "language": cfg["site"]["language"],
    "locale": cfg["site"]["locale"],
    "author": cfg["site"]["author"],
    "email": cfg["site"]["email"],
    "brand": cfg["brand"],
    "adsense": cfg["monetization"],
    "analytics": cfg["analytics"],
    "clusters": [{"id": c["id"], "title": c["title"]} for c in niche["clusters"]],
}
dest = ROOT / "site" / "src" / "site.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {dest}")

# robots.txt بالدومين الحقيقي
robots = ROOT / "site" / "public" / "robots.txt"
robots.parent.mkdir(parents=True, exist_ok=True)
robots.write_text(
    f"User-agent: *\nAllow: /\n\nSitemap: {out['url'].rstrip('/')}/sitemap-index.xml\n",
    encoding="utf-8")
print(f"wrote {robots}")
