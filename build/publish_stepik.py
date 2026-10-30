import json
import os
import random
import subprocess
import sys
import tempfile
import time
from urllib.parse import quote

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(ROOT, "build", "course_model.json")
MANIFEST_PATH = os.path.join(ROOT, "build", "stepik_manifest.json")
TOKEN_PATH = os.path.join(tempfile.gettempdir(), "rufp", "qm_stepik_token.txt")
CLIENT_PATH = os.path.join(tempfile.gettempdir(), "rufp", "qm_stepik_client.json")
API = "https://stepik.org/api/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

NIGHT = "#120b24"
PANEL = "#241744"
LINE = "#3a2a5e"
PUMPKIN = "#ff8c2b"
GOLD = "#ffd54f"
INK = "#efe9dc"
DIM = "#b3a8d4"
KOKO = "#8a5fd6"
POISON = "#86c232"
BLOOD = "#e64533"

HAN = "font-family:'Noto Sans SC','Microsoft YaHei',sans-serif;"


def get_token():
    tok = open(TOKEN_PATH, encoding="utf-8").read().strip()
    if tok:
        status = curl("GET", "courses/303598", None, tok)[0]
        if 200 <= status < 300:
            return tok
    creds = json.load(open(CLIENT_PATH, encoding="utf-8"))
    out = subprocess.check_output([
        "curl.exe", "-s", "-X", "POST",
        "-u", creds["id"] + ":" + creds["secret"],
        "-d", "grant_type=client_credentials",
        "https://stepik.org/oauth2/token/",
    ]).decode()
    tok = json.loads(out)["access_token"]
    os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
    open(TOKEN_PATH, "w", encoding="utf-8").write(tok)
    return tok


def curl(method, path, payload, token, attempts=4):
    args = ["curl.exe", "-s", "-w", "\n%{http_code}", "--max-time", "90",
            "-A", UA, "-H", "Authorization: Bearer " + token]
    body_file = None
    if payload is not None:
        body_file = os.path.join(tempfile.gettempdir(), "qm_payload.json")
        with open(body_file, "w", encoding="utf-8", newline="") as f:
            json.dump(payload, f, ensure_ascii=True)
        args += ["-H", "Content-Type: application/json; charset=utf-8",
                 "--data-binary", "@" + body_file]
    if method != "GET":
        args += ["-X", method]
    url = path if path.startswith("http") else API + path
    last = (0, "")
    for i in range(1, attempts + 1):
        r = subprocess.run(args + [url], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        out = r.stdout.strip()
        lines = out.rsplit("\n", 1)
        try:
            status = int(lines[-1].strip())
        except ValueError:
            status = 0
        body = lines[0] if len(lines) > 1 else ""
        if 200 <= status < 300:
            try:
                return status, json.loads(body)
            except ValueError:
                return status, body
        last = (status, body[:300])
        retry = status in (0, 429, 502, 503, 504) or "Access Blocked" in body
        if not retry:
            break
        time.sleep(15 * i)
    raise RuntimeError("HTTP %s %s %s -> %s" % (method, path, last[0], last[1]))


class Stepik:
    def __init__(self):
        self.token = get_token()

    def api(self, method, path, payload=None):
        return curl(method, path, payload, self.token)[1]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def big_char(s, size=64):
    return '<span style="%sfont-size:%dpx;line-height:1.1;color:%s;">%s</span>' % (
        HAN, size, INK, esc(s))


def wrap(inner, accent=KOKO):
    return ('<div style="padding:10px;color:%s;background-color:%s;border:4px solid %s;">'
            % (INK, NIGHT, accent)) + inner + "</div>"


def audio_html(url):
    return ('<audio controls preload="none" src="%s" style="vertical-align:middle;"></audio> '
            '<a href="%s" target="_blank" rel="noopener noreferrer" style="color:%s;font-size:13px;">↗ звук</a>') % (
        url, url, PUMPKIN)


def page_url(base, path):
    p = quote(str(path).strip("/"))
    return base.rstrip("/") + "/" + (p + "/" if p else "")


def frame_step(base, path, h, accent=KOKO, subtitle=None, v="17"):
    b = base.rstrip("/")
    url = page_url(base, path) + "?v=" + v
    pill = ""
    if subtitle:
        pill = ('<p style="margin:0 0 10px;text-align:center;"><span '
                'style="display:inline-block;padding:4px 14px;border:2px solid %s;'
                'border-radius:14px;font-size:13px;color:%s;"><b>%s</b></span></p>'
                % (accent, PANEL, subtitle))
    frame = (
        '<div style="font-size:0;">'
        '<img alt="" src="%s/shared/frame/top.svg?v=3" width="100%%" height="112" '
        'style="width:100%%;height:112px;border:0;"></div>'
        '<div style="background-color:%s;padding:6px;border:6px solid %s;">'
        '<iframe height="%d" src="%s" width="100%%" '
        'style="width:100%%;height:%dpx;border:0;background-color:%s;">'
        "Ваш браузер не поддерживает iframe — открой урок по ссылке под рамкой.</iframe></div>"
        '<div style="font-size:0;">'
        '<img alt="" src="%s/shared/frame/bottom.svg?v=3" width="100%%" height="52" '
        'style="width:100%%;height:52px;border:0;"></div>'
        '<p style="margin:8px 0 0;text-align:center;"><a href="%s" target="_blank" '
        'rel="noopener noreferrer" style="color:#5d4a86;font-size:12px;">'
        "↗ открыть урок на отдельной странице</a></p>"
    ) % (b, NIGHT, accent, h, url, h, NIGHT, b, url)
    return {"block": {"name": "text", "text": pill + frame}}


def choice_step(question_html, options, correct, accent=GOLD):
    opts = [{"text": o, "is_correct": o == correct,
             "feedback": "Верно! Фонарик вспыхнул." if o == correct else ""}
            for o in options]
    return {"block": {"name": "choice",
                      "text": wrap('<div style="padding:14px;text-align:center;border:3px solid %s;'
                                   'background-color:%s;">%s</div>' % (accent, PANEL, question_html), accent),
                      "source": {"options": opts, "is_multiple_choice": False,
                                 "is_always_correct": False, "preserve_order": False,
                                 "sample_size": len(options), "is_html_enabled": True,
                                 "is_options_feedback": True}}}


def glyph_lesson_steps(lesson, base):
    d = lesson["data"]
    num = lesson["num"]
    han = d.get("char") or d.get("word")
    audio_url = base.rstrip("/") + "/audio/" + quote(d["audio"])
    kind = "знак" if d.get("char") else "слово"
    g = d["game"]
    meaning_round = g[1]
    pinyin_round = g[2]
    s1 = frame_step(base, lesson["url"], 1500, KOKO,
                    "Фонарик %d · все 4 фазы · от Тумана до Сладости" % num)
    s2 = choice_step(
        "<p style='margin:0 0 8px;font-size:15px;color:%s;'>Какой %s означает "
        "<b style='color:%s;'>«%s»</b>?</p>%s"
        % (DIM, kind, GOLD, esc(meaning_round["prompt"]), audio_html(audio_url)),
        meaning_round["opts"], meaning_round["ans"], GOLD)
    s3 = choice_step(
        "<p style='margin:0 0 8px;'>%s</p><p style='margin:0 0 10px;font-size:15px;color:%s;'>"
        "Выбери правильное чтение:</p>%s" % (big_char(han, 56), DIM, audio_html(audio_url)),
        pinyin_round["opts"], pinyin_round["ans"], PUMPKIN)
    return [s1, s2, s3]


def story_lesson_steps(lesson, base, model):
    return [frame_step(base, lesson["url"], 1800, KOKO,
                       "История двора · 6 сцен", v="16")]


def tones_lesson_steps(lesson, base, model):
    t = model["tones"]
    tone_names = {1: "1-й тон — высокий ровный (мā)", 2: "2-й тон — вверх (мá)",
                  3: "3-й тон — вниз и обратно (мǎ)", 4: "4-й тон — резко вниз (мà)"}
    steps = [frame_step(base, lesson["url"], 1800, KOKO,
                        "Четыре чиха Коко · слушай и повторяй")]
    for i, q in enumerate(t["quiz"], 1):
        au = base + "/audio/" + quote(q["audio"])
        steps.append(choice_step(
            "<p style='margin:0 0 10px;font-size:15px;color:%s;'>Укол колокольни %d/6: какой тон ты услышал?</p>%s"
            % (DIM, i, audio_html(au)),
            [tone_names[n] for n in (1, 2, 3, 4)], tone_names[q["answer"]], KOKO))
    return steps


def quiz_lesson_steps(lesson, base, model):
    items = []
    for sec in model["sections"]:
        for l in sec["lessons"]:
            if l["kind"] in ("glyph", "word"):
                items.append(l)
    rng = random.Random(303598)
    picks = [items[k * 2] for k in range(12)] + [items[24]]
    picks = picks[:12]
    rng.shuffle(picks)
    kinds_pool = ["meaning", "pinyin", "audio_pinyin"]
    intro = wrap(
        "<p style='margin:0 0 8px;'><b style='color:%s;'>Осада почти отбита!</b> Великая викторина "
        "«Сладость или гадость»: 12 вопросов по всем 25 фонарикам. За каждый — балл; если ошибся — "
        "вернись к фонарику на <a href='%s' target='_blank' rel='noopener noreferrer' style='color:%s;'>карте двора</a>.</p>"
        "<p style='margin:0;font-size:13px;color:%s;'>Вопросы трёх видов: смысл знака, чтение знака, "
        "чтение на слух — включи звук!</p>" % (GOLD, base + "/", PUMPKIN, DIM), PUMPKIN)
    steps = [{"block": {"name": "text", "text": intro}}]
    for i, l in enumerate(picks, 1):
        d = l["data"]
        han = d.get("char") or d.get("word")
        au = base + "/audio/" + quote(d["audio"])
        kind = kinds_pool[i % 3]
        if kind == "meaning":
            r = d["game"][1]
            q = "<p style='margin:0 0 10px;font-size:15px;color:%s;'>Вопрос %d/12: какой знак означает " \
                "<b style='color:%s;'>«%s»</b>?</p>" % (DIM, i, GOLD, esc(r["prompt"]))
            opts, ans = r["opts"], r["ans"]
        elif kind == "pinyin":
            r = d["game"][2]
            q = "<p style='margin:0 0 8px;'>%s</p><p style='margin:0 0 10px;font-size:15px;color:%s;'>Вопрос %d/12: " \
                "как это читается?</p>" % (big_char(han, 52), DIM, i)
            opts, ans = r["opts"], r["ans"]
        else:
            r = d["game"][4]
            q = "<p style='margin:0 0 10px;font-size:15px;color:%s;'>Вопрос %d/12: послушай и выбери чтение:</p>%s" \
                % (DIM, i, audio_html(au))
            opts, ans = r["opts"], r["ans"]
        steps.append(choice_step(q, opts, ans, PUMPKIN))
    return steps


def finale_lesson_steps(lesson, base, model):
    return [frame_step(base, lesson["url"], 1800, GOLD,
                       "Финал истории и грамота")]


def bonus_lesson_steps(lesson, base, model):
    return [frame_step(base, lesson["url"], 1100, POISON,
                       "12 волн · 3 ❤️ · 18 секунд на волну")]


def build_lesson(lesson, base, model):
    if lesson["kind"] in ("glyph", "word"):
        return glyph_lesson_steps(lesson, base)
    if lesson["kind"] == "story":
        return story_lesson_steps(lesson, base, model)
    if lesson["kind"] == "tones":
        return tones_lesson_steps(lesson, base, model)
    if lesson["kind"] == "quiz":
        return quiz_lesson_steps(lesson, base, model)
    if lesson["kind"] == "finale":
        return finale_lesson_steps(lesson, base, model)
    if lesson["kind"] == "bonus":
        return bonus_lesson_steps(lesson, base, model)
    raise ValueError(lesson["kind"])


def lesson_title(lesson):
    return lesson["title"]


def load_manifest():
    if os.path.exists(MANIFEST_PATH):
        return json.load(open(MANIFEST_PATH, encoding="utf-8"))
    return {"sections": {}}


def save_manifest(m):
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)


def post_lesson(api, lesson, base, model):
    steps = [s["block"] for s in build_lesson(lesson, base, model)]
    r = api.api("POST", "lessons", {"lesson": {"title": lesson_title(lesson)}})
    lesson_id = r["lessons"][0]["id"]
    try:
        step_ids = []
        for pos, block in enumerate(steps, 1):
            sr = {"lesson": lesson_id, "position": pos, "block": block}
            if block["name"] == "choice":
                sr["cost"] = 1
            sr = api.api("POST", "step-sources", {"stepSource": sr})
            step_ids.append(sr["step-sources"][0]["id"])
    except Exception:
        api.api("DELETE", "lessons/%d" % lesson_id)
        raise
    created = api.api("GET", "lessons/%d" % lesson_id)["lessons"][0]
    created["step_ids"] = step_ids
    return created


def main():
    test = "--test" in sys.argv
    model = json.load(open(MODEL_PATH, encoding="utf-8"))
    base = model["base_url"].rstrip("/")
    api = Stepik()
    course = api.api("GET", "courses/303598")["courses"][0]
    print("course:", course["title"], "| sections:", len(course.get("sections") or []))
    man = load_manifest()
    sections = model["sections"] if not test else model["sections"][:1]
    for pos, sec in enumerate(sections, 1):
        key = sec["title"]
        if key in man["sections"]:
            sec_id = man["sections"][key]["id"]
            print("section exists:", key, sec_id)
        else:
            r = api.api("POST", "sections", {"section": {"course": 303598, "title": key, "position": pos}})
            sec_id = r["sections"][0]["id"]
            man["sections"][key] = {"id": sec_id, "lessons": {}}
            save_manifest(man)
            print("section created:", key, sec_id)
            time.sleep(0.3)
        for lpos, lesson in enumerate(sec["lessons"], 1):
            lkey = lesson_title(lesson)
            entry = man["sections"][key]["lessons"].get(lkey)
            if entry and "lesson_id" in entry:
                print("  lesson exists:", lkey)
                continue
            created = post_lesson(api, lesson, base, model)
            lesson_id = created["id"]
            u = api.api("POST", "units", {"unit": {"section": sec_id, "lesson": lesson_id, "position": lpos}})
            man["sections"][key]["lessons"][lkey] = {
                "lesson_id": lesson_id, "unit_id": u["units"][0]["id"],
                "step_ids": created.get("steps", [])}
            save_manifest(man)
            print("  lesson created:", lkey, "lesson=%s unit=%s steps=%d"
                  % (lesson_id, u["units"][0]["id"], len(created.get("steps") or [])))
            time.sleep(0.3)
        if test:
            print("TEST MODE: останавливаюсь после первой секции")
            return
    from make_desc import build_styled, put_course
    put_course(api, summary=model["summary"], description=build_styled())
    print("course patched (summary+description)")
    c = api.api("GET", "courses/303598")["courses"][0]
    print("final sections:", len(c["sections"]))


if __name__ == "__main__":
    main()
