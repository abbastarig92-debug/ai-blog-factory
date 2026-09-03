#!/usr/bin/env python3
"""
====================================================================
  المنسّق — العقل المدبّر الذي يشغّل الوكلاء بالترتيب الصحيح
====================================================================
  python orchestrator.py scout      # يملأ مخزون الكلمات المفتاحية
  python orchestrator.py plan       # يحوّل الكلمات إلى بريفات
  python orchestrator.py publish    # يكتب وينشر مقالات اليوم
  python orchestrator.py optimize   # الصيانة الأسبوعية
  python orchestrator.py daily      # scout (عند الحاجة) + plan + publish
====================================================================
"""
import sys, traceback
from agents.base import log, load_state, save_state, NICHE, SITE
from agents import (a01_keyword_scout as scout, a02_editor_planner as planner,
                    a03_researcher as researcher, a04_writer as writer,
                    a05_fact_checker as checker, a06_seo_optimizer as seo,
                    a07_monetizer as money, a08_illustrator as art,
                    a09_publisher as pub, a10_internal_linker as linker,
                    a11_distributor as dist, a12_performance_optimizer as perf)

L = log("orchestrator")
MIN_POOL = 8


def cmd_scout():
    return scout.run(limit=20)


def cmd_plan():
    if len(load_state("keyword_pool", [])) < MIN_POOL:
        L.info("المخزون منخفض — تشغيل كشّاف الكلمات")
        cmd_scout()
    return planner.run()


def _cluster_label(cid: str) -> str:
    c = next((c for c in NICHE["clusters"] if c["id"] == cid), None)
    return c["title"] if c else SITE["site"]["name"]


def publish_one(brief: dict) -> str | None:
    kw = brief["keyword"]["keyword"]
    L.info("──── بدء الإنتاج: %s", kw)
    research = researcher.run(brief)                    # 3
    body = writer.run(brief, research)                  # 4
    body, flags = checker.run(body, research)           # 5
    if flags:
        L.warning("تنبيهات باقية بعد التدقيق: %s", flags)
    meta = seo.run(body, brief)                         # 6
    body, extras = money.run(body)                      # 7
    cover = art.run(meta["title"], meta["slug"], _cluster_label(brief["keyword"].get("cluster")))  # 8
    extras["sources"] = research["sources"]
    slug = pub.run(brief, body, meta, cover, extras)    # 9
    dist.run(slug, meta["title"], meta.get("key_takeaway", ""))  # 11
    return slug


def cmd_publish():
    queue = load_state("brief_queue", [])
    if not queue:
        L.info("الطابور فارغ — تشغيل رئيس التحرير")
        queue = cmd_plan()
    done, failed = [], []
    remaining = list(queue)
    for brief in list(queue):
        try:
            done.append(publish_one(brief))
            remaining.remove(brief)
        except Exception as e:  # noqa: BLE001
            L.error("فشل «%s»: %s", brief.get("working_title"), e)
            L.debug(traceback.format_exc())
            failed.append({"title": brief.get("working_title"), "error": str(e)})
            remaining.remove(brief)
    save_state("brief_queue", remaining)
    if done:
        linker.run()                                    # 10
    save_state("last_run", {"published": done, "failed": failed})
    L.info("انتهى النشر — نجح %s / فشل %s", len(done), len(failed))
    return done


def cmd_optimize():
    perf.run()                                          # 12
    linker.run()
    if len(load_state("keyword_pool", [])) < MIN_POOL * 2:
        cmd_scout()


def cmd_daily():
    cmd_plan()
    cmd_publish()


COMMANDS = {"scout": cmd_scout, "plan": cmd_plan, "publish": cmd_publish,
            "optimize": cmd_optimize, "daily": cmd_daily}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "daily"
    if cmd not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    COMMANDS[cmd]()
