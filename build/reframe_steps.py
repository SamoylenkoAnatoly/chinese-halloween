import json
import sys
import time

sys.path.insert(0, r"C:\Китайский язык (хэллуин)\build")
import publish_stepik as ps


def main():
    dry = "--dry" in sys.argv
    model = json.load(open(ps.MODEL_PATH, encoding="utf-8"))
    man = ps.load_manifest()
    base = model["base_url"].rstrip("/")
    api = ps.Stepik()

    by_title = {}
    for sec in model["sections"]:
        for l in sec["lessons"]:
            by_title[ps.lesson_title(l)] = l

    puts = 0
    for skey in sorted(man["sections"]):
        sentry = man["sections"][skey]
        for lkey in sorted(sentry["lessons"]):
            entry = sentry["lessons"][lkey]
            lesson = by_title.get(lkey)
            if lesson is None:
                print("SKIP (not in model):", lkey)
                continue
            lesson_id = entry.get("lesson_id")
            step_ids = entry.get("step_ids") or []
            if not lesson_id:
                print("SKIP (no lesson_id):", lkey)
                continue
            if not step_ids:
                step_ids = api.api("GET", "lessons/%d" % lesson_id)["lessons"][0]["steps"]
                entry["step_ids"] = step_ids
                ps.save_manifest(man)
            steps = ps.build_lesson(lesson, base, model)
            if len(steps) != len(step_ids):
                print("SKIP (count %d != %d):" % (len(steps), len(step_ids)), lkey)
                continue
            for pos, (step, sid) in enumerate(zip(steps, step_ids), 1):
                if step["block"]["name"] != "text":
                    continue
                if dry:
                    print("DRY PUT step=%s pos=%d :: %s" % (sid, pos, lkey))
                    continue
                ps.curl("PUT", "step-sources/%d" % sid,
                        {"stepSource": {"lesson": lesson_id, "position": pos,
                                        "block": step["block"]}}, api.token)
                puts += 1
                print("PUT ok=%d step=%s pos=%d :: %s" % (puts, sid, pos, lkey))
                time.sleep(0.4)
    print("done, PUTs:", puts)


if __name__ == "__main__":
    main()
