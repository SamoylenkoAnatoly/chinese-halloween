import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from publish_stepik import MANIFEST_PATH, curl, get_token

SITE = "https://samoylenkoanatoly.github.io/chinese-halloween/"
CHUNK = 20
DELAY = 0.5


def collect_steps(manifest):
    ids = []
    seen = set()
    sections = manifest.get("sections") or {}
    sec_items = sections.values() if isinstance(sections, dict) else sections
    for sec in sec_items:
        lessons = sec.get("lessons") or {}
        les_items = lessons.values() if isinstance(lessons, dict) else lessons
        for les in les_items:
            for sid in les.get("step_ids") or []:
                if sid not in seen:
                    seen.add(sid)
                    ids.append(sid)
    return ids


def fix_text(text, version):
    # не вставляем слэш: файлам нужен "name.svg?v=N", папкам — "dir/?v=N"
    bust = '?v=%d"' % version
    new = re.sub(r'\?v=\d+"', bust, text)
    new = re.sub(r'("https://samoylenkoanatoly\.github\.io/chinese-halloween/[^"?]*)"', r'\1' + bust, new)
    return new


def main():
    version = 2
    only_steps = []
    if len(sys.argv) > 1:
        version = int(sys.argv[1])
        only_steps = [int(x) for x in sys.argv[2:]]
    manifest = json.load(open(MANIFEST_PATH, encoding="utf-8"))
    if only_steps:
        step_ids = only_steps
        print("target steps: %s (v=%d)" % (step_ids, version))
    else:
        step_ids = collect_steps(manifest)
        print("steps in manifest: %d" % len(step_ids))
    token = get_token()

    sources = []
    for i in range(0, len(step_ids), CHUNK):
        chunk = step_ids[i:i + CHUNK]
        query = "&".join("ids%%5B%%5D=%d" % s for s in chunk)
        status, body = curl("GET", "step-sources?" + query, None, token)
        items = (body.get("step-sources") or []) if isinstance(body, dict) else []
        sources.extend(items)
        print("fetched chunk %d/%d: %d items (HTTP %d)" % (i // CHUNK + 1, -(-len(step_ids) // CHUNK), len(items), status))
        time.sleep(DELAY)
    print("total step-sources fetched: %d" % len(sources))

    changed = []
    for ss in sources:
        block = ss.get("block") or {}
        text = block.get("text") or ""
        if SITE not in text or 'src="' not in text:
            continue
        new_text = fix_text(text, version)
        if new_text != text:
            changed.append((ss, new_text))
    print("steps needing cache-buster: %d" % len(changed))

    ok = fail = 0
    for ss, new_text in changed:
        block = dict(ss["block"])
        block["text"] = new_text
        payload = {"stepSource": {
            "lesson": ss["lesson"],
            "position": ss["position"],
            "block": block,
        }}
        try:
            curl("PUT", "step-sources/%d" % ss["id"], payload, token)
            ok += 1
            print("PUT %d (lesson %d, pos %d) OK" % (ss["id"], ss["lesson"], ss["position"]))
        except RuntimeError as e:
            fail += 1
            print("PUT %d FAILED: %s" % (ss["id"], e))
        time.sleep(DELAY)

    print("done: ok=%d fail=%d" % (ok, fail))
    if changed:
        sid = changed[0][0]["id"]
        status, body = curl("GET", "step-sources?ids%%5B%%5D=%d" % sid, None, token)
        items = (body.get("step-sources") or []) if isinstance(body, dict) else []
        if items:
            text = (items[0].get("block") or {}).get("text") or ""
            m = re.search(r'src="([^"]+)"', text)
            print("verify step %d iframe src -> %s" % (sid, m.group(1) if m else "NOT FOUND"))


if __name__ == "__main__":
    main()
