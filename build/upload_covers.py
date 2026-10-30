# -*- coding: utf-8 -*-
"""Обложки уроков: верификация и (опционально) загрузка через Uploadcare.

Stepik принимает в cover_url только https://ucarecdn.com/<uuid>/ (и зеркала
ucarecdn.stepik.net) — файлы обложек живут в Uploadcare-проекте Stepik; ключ
виден только в залогиненном редакторе. Поэтому:

  python build/upload_covers.py                 — чеклист: у каких уроков cover_url пуст
  python build/upload_covers.py --uc-key KEY    — загрузить PNG (демо/проектный ключ),
                                                  PUT cover_url, GET-верификация

PNG лежат в build/covers/ с человекочитаемыми именами (порядок = порядок курса)."""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_covers import MODEL_PATH, MANIFEST_PATH, OUT as COVERS, human_name, SPECIAL_KINDS
from publish_stepik import API, UA, curl, get_token


def lesson_sequence():
    model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    man = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    by_title = {}
    for sec in model["sections"]:
        for l in sec["lessons"]:
            by_title[l["title"]] = l
    out = []
    pos = 0
    for s in man["sections"].values():
        for ltitle, le in s["lessons"].items():
            lid = le.get("lesson_id")
            if not lid:
                continue
            l = by_title.get(ltitle)
            if l and l["kind"] in ("glyph", "word"):
                kind = l["kind"]
                target = l["data"].get("char") or l["data"].get("word")
            else:
                kind = SPECIAL_KINDS.get(ltitle)
                target = None
            if not kind:
                continue
            pos += 1
            out.append((pos, lid, "%02d %s.png" % (pos, human_name(ltitle, kind, target)), ltitle))
    return out


def ucare_upload(png, key):
    r = subprocess.run(["curl.exe", "-s", "--max-time", "120",
                        "-F", "UPLOADCARE_PUB_KEY=" + key,
                        "-F", "UPLOADCARE_STORE=auto",
                        "-F", "file=@" + str(png) + ";type=image/png",
                        "https://upload.uploadcare.com/base/"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        return json.loads(r.stdout)["file"]
    except (ValueError, KeyError):
        print("uploadcare FAIL:", r.stdout[:200])
        return None


def main():
    args = sys.argv[1:]
    uc_key = None
    if "--uc-key" in args:
        uc_key = args[args.index("--uc-key") + 1]
    seq = lesson_sequence()
    print("уроков:", len(seq))
    token = get_token()
    done = failed = 0
    for pos, lid, fname, ltitle in seq:
        cur = curl("GET", "lessons/%d" % lid, None, token)[1]["lessons"][0].get("cover_url")
        if uc_key:
            if cur:
                print(fname, "| уже есть — пропуск")
                continue
            uuid = ucare_upload(COVERS / fname, uc_key)
            if not uuid:
                failed += 1
                continue
            url = "https://ucarecdn.com/%s/" % uuid
            st, data = curl("PUT", "lessons/%d" % lid,
                            {"lesson": {"title": ltitle, "cover_url": url}}, token)
            if st >= 300:
                failed += 1
                print(fname, "| PUT FAIL", st, str(data)[:150])
                continue
            time.sleep(0.3)
            cur = curl("GET", "lessons/%d" % lid, None, token)[1]["lessons"][0].get("cover_url")
        done += 1 if cur else 0
        print("%s | lesson %d | %s" % (fname, lid, "OK " + cur if cur else "обложки НЕТ"))
    print("итог: с обложкой %d из %d, ошибок %d" % (done, len(seq), failed))


if __name__ == "__main__":
    main()
