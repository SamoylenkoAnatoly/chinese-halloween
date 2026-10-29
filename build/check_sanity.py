# -*- coding: utf-8 -*-
"""Разовая проверка после смены набора знаков."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import GLYPHS, WORDS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = "月夕日明木林目口心白人名自想息众朋"

problems = []

# 1. аудио: каждый заявленный файл существует и не пустой
for it in GLYPHS + WORDS:
    p = os.path.join(ROOT, "audio", it["audio"])
    if not os.path.exists(p) or os.path.getsize(p) < 4000:
        problems.append("audio bad/missing: %s" % it["audio"])

# 2. папки уроков ровно 25 и совпадают с набором
lesson_dir = os.path.join(ROOT, "lesson")
dirs = sorted(d for d in os.listdir(lesson_dir) if os.path.isdir(os.path.join(lesson_dir, d)))
expect = sorted([g["char"] for g in GLYPHS] + [w["word"] for w in WORDS])
if dirs != expect:
    problems.append("lesson dirs mismatch: %s vs %s" % (dirs, expect))

# 3. старые знаки не встречаются в собранных страницах
targets = [os.path.join(ROOT, "index.html")]
for sub in ("lesson", "finale", "story", "tones", "bonus-siege", "shared"):
    base = os.path.join(ROOT, sub)
    for dirpath, _, files in os.walk(base):
        for f in files:
            if f.endswith((".html", ".js")):
                targets.append(os.path.join(dirpath, f))
for p in targets:
    with open(p, encoding="utf-8") as fh:
        c = fh.read()
    for ch in OLD:
        if ch in c:
            problems.append("old char %s in %s" % (ch, os.path.relpath(p, ROOT)))
            break

# 4. модель курса: 25 уроков знаков/слов, викторина, тоны и т.д.
model = json.load(open(os.path.join(ROOT, "build", "course_model.json"), encoding="utf-8"))
kinds = {}
sec_titles = []
for s in model["sections"]:
    sec_titles.append(s["title"])
    for l in s["lessons"]:
        kinds[l["kind"]] = kinds.get(l["kind"], 0) + 1
print("sections:", sec_titles)
print("lesson kinds:", kinds)
if kinds.get("glyph", 0) != 17 or kinds.get("word", 0) != 8:
    problems.append("model glyph/word count wrong: %s" % kinds)
if "大门" not in model["finale"]["paras"][2]:
    problems.append("finale does not mention 大门")

# 5. на странице урока 大 есть ссылки на shared-стили и аудио
page = open(os.path.join(ROOT, "lesson", "大", "index.html"), encoding="utf-8").read()
for marker in ("../../shared/spooky.css", "da.mp3"):
    if marker not in page:
        problems.append("lesson 大 page missing marker: %s" % marker)

# 6. в играх урока правильный ответ всегда среди вариантов
for grp, pool in (("glyph", [g["char"] for g in GLYPHS]), ("word", [w["word"] for w in WORDS])):
    for s in model["sections"]:
        for l in s["lessons"]:
            if l["kind"] != grp:
                continue
            for rnd in l["data"]["game"]:
                if rnd["ans"] not in rnd["opts"]:
                    problems.append("game answer missing in opts: %s (%s)" % (l["title"], rnd["kind"]))
                if len(set(rnd["opts"])) != len(rnd["opts"]):
                    problems.append("dup opts: %s (%s)" % (l["title"], rnd["kind"]))

if problems:
    print("PROBLEMS (%d):" % len(problems))
    for p in problems:
        print(" -", p)
    sys.exit(1)
print("ALL CHECKS PASSED")
