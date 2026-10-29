# -*- coding: utf-8 -*-
"""Разовое удаление уроков Stepik, сменивших содержимое при замене набора знаков.

Оставляет story («Чих Магистра Коко»), tones («Тоны полуночи»)
и bonus («Бонус: Осада домика») — их контент не зависит от знаков.
Удаляет юнит и урок, вычищает записи из манифеста.
Запуск: python build/restart_lessons.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from publish_stepik import Stepik, load_manifest, save_manifest

KEEP = {"Чих Магистра Коко", "Тоны полуночи", "Бонус: Осада домика"}


def main():
    dry = "--dry" in sys.argv
    api = Stepik()
    man = load_manifest()
    deleted = kept = 0
    for sec_title, sec in list(man["sections"].items()):
        for lkey, entry in list(sec["lessons"].items()):
            if lkey in KEEP:
                kept += 1
                continue
            unit_id = entry.get("unit_id")
            lesson_id = entry.get("lesson_id")
            if dry:
                print("DRY delete: %-40s lesson=%s unit=%s" % (lkey[:40], lesson_id, unit_id))
                deleted += 1
                continue
            try:
                if unit_id:
                    api.api("DELETE", "units/%d" % unit_id)
                    time.sleep(0.4)
                if lesson_id:
                    api.api("DELETE", "lessons/%d" % lesson_id)
                    time.sleep(0.4)
                del man["sections"][sec_title]["lessons"][lkey]
                save_manifest(man)
                deleted += 1
                print("deleted: %-46s (lesson=%s unit=%s)" % (lkey[:46], lesson_id, unit_id))
            except RuntimeError as e:
                print("FAILED: %s -> %s" % (lkey, e))
                return 1
    print("done: deleted=%d kept=%d" % (deleted, kept))
    return 0


if __name__ == "__main__":
    sys.exit(main())
