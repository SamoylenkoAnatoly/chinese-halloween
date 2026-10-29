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


def header(title, subtitle, accent=KOKO):
    return ('<div style="padding:16px;text-align:center;border:3px solid %s;'
            'background-color:%s;"><h2 style="margin:0 0 8px;color:%s;">%s</h2>'
            '<p style="margin:0;color:%s;font-size:14px;">%s</p></div>') % (
        accent, PANEL, INK, title, DIM, subtitle)


def open_btn(url):
    return ('<p style="margin:10px 0;"><a href="%s" target="_blank" rel="noopener noreferrer" '
            'style="display:inline-block;padding:10px 24px;background-color:%s;color:%s;'
            'font-weight:bold;font-size:15px;border:3px solid %s;border-radius:10px;'
            'text-decoration:none;">↗ Открыть на отдельной странице</a></p>'
            '<p style="margin:0;font-size:11px;color:%s;">Если страница не открывается внутри '
            'шага — нажми кнопку сверху.</p>') % (url, PUMPKIN, NIGHT, GOLD, DIM)


def iframe(url, h, accent=KOKO):
    return ('<div style="margin-top:10px;"><iframe height="%d" src="%s" '
            'style="width:100%%;height:%dpx;border:3px solid %s;background-color:%s;" width="100%%">'
            "Ваш браузер не поддерживает iframe — воспользуйся кнопкой выше.</iframe></div>") % (
        h, url, h, accent, NIGHT)


def chip(label, value):
    return ('<span style="display:inline-block;margin:3px 4px;padding:4px 10px;'
            'border:2px solid %s;border-radius:8px;color:%s;font-size:13px;background-color:%s;">'
            "<b>%s:</b> %s</span>") % (LINE, GOLD, PANEL, label, value)


def body_block(html, accent=LINE):
    return '<div style="padding:14px;border:3px solid %s;background-color:%s;margin-top:10px;">%s</div>' % (
        accent, PANEL, html)


def tale_html(tale):
    return "".join("<p style='margin:0 0 8px;'>%s</p>" % t for t in tale)


def audio_html(url):
    return ('<audio controls preload="none" src="%s" style="vertical-align:middle;"></audio> '
            '<a href="%s" target="_blank" rel="noopener noreferrer" style="color:%s;font-size:13px;">↗ звук</a>') % (
        url, url, PUMPKIN)


def text_step(title, subtitle, blocks, url=None, h=1500, accent=KOKO):
    inner = header(title, subtitle, accent)
    for b in blocks:
        inner += b
    if url:
        inner += open_btn(url) + iframe(url, h, accent)
    return {"block": {"name": "text", "text": wrap(inner, accent)}}


def choice_step(question_html, options, correct, accent=GOLD):
    opts = [{"text": o, "is_correct": o == correct,
             "feedback": "Верно! Фонарик вспыхнул." if o == correct
             else "Мимо. Загляни в урок ещё раз."}
            for o in options]
    return {"block": {"name": "choice",
                      "text": wrap('<div style="padding:14px;text-align:center;border:3px solid %s;'
                                   'background-color:%s;">%s</div>' % (accent, PANEL, question_html), accent),
                      "source": {"options": opts, "is_multiple_choice": False,
                                 "is_always_correct": False, "preserve_order": False,
                                 "sample_size": len(options), "is_html_enabled": True,
                                 "is_options_feedback": True}}}


def glyph_passport(d, num, base):
    who = "Костик" if d.get("wing") else ""
    han = d.get("char") or d.get("word")
    py = d["pinyin"]
    mean = d["meaning"]
    passport = body_block(
        '<p style="margin:0 0 10px;text-align:center;">%s</p><p style="margin:0 0 10px;text-align:center;">'
        '<span style="color:%s;font-size:26px;"><b>%s</b></span></p><p style="margin:0;text-align:center;">%s</p>'
        % (big_char(han, 72), GOLD, esc(py), esc(mean)),
        KOKO)
    facts = ""
    if d.get("key"):
        facts += chip("Ключ", esc(d["key"]))
    if d.get("strokes"):
        facts += chip("Черт", str(d["strokes"]))
    facts += chip("Фонарик", "%d из %d" % (num, d["total"]))
    if d.get("parts"):
        facts += chip("Состав", esc(" + ".join(d["parts"])))
    steps_html = body_block(
        "<p style='margin:0 0 8px;'><b style='color:%s;'>Как зажечь фонарик (фазы урока):</b></p>"
        "<ol style='margin:0 0 8px;padding-left:20px;'>"
        "<li><b>Туман</b> — паспорт знака: разглядим его в лунном тумане.</li>"
        "<li><b>Голос Коко</b> — послушай звук, изучи тон и мини-сказку.</li>"
        "<li><b>Мел и камень</b> — обведи знак 3 раза в тренажёре письма.</li>"
        "<li><b>Сладость или гадость</b> — 5 раундов игры, и фонарик загорается.</li></ol>"
        "<p style='margin:0;font-size:12px;color:%s;'>На этом шаге открой фазы 1–2. Дальше — два задания Stepik, "
        "а фазы 3–4 ждут в последнем шаге урока.</p>" % (GOLD, DIM))
    tale = body_block(
        "<p style='margin:0 0 6px;'><b style='color:%s;'>Мини-сказка %s:</b></p>%s"
        "<p style='margin:6px 0 0;font-size:12px;color:%s;'>Полная версия — в уроке.</p>"
        % (PUMPKIN, esc(who) if who else "Костика", tale_html([d["tale"][0]]), DIM),
        PUMPKIN)
    return passport + facts + steps_html + tale


def glyph_lesson_steps(lesson, base):
    d = lesson["data"]
    num = lesson["num"]
    han = d.get("char") or d.get("word")
    url = base + "/" + quote(lesson["url"]) + "/"
    audio_url = base + "/audio/" + quote(d["audio"])
    kind = "знак" if d.get("char") else "слово"
    g = d["game"]
    meaning_round = g[1]
    pinyin_round = g[2]
    s1 = text_step(
        "Фонарик %d: %s" % (num, esc(lesson["title"].split(" — ")[0])),
        "Костик ведёт к фонарику · фазы 1–2",
        [glyph_passport(d, num, base)],
        url, 1500, KOKO)
    s2 = choice_step(
        "<p style='margin:0 0 8px;font-size:15px;color:%s;'>Какой %s означает "
        "<b style='color:%s;'>«%s»</b>?</p>%s"
        % (DIM, kind, GOLD, esc(meaning_round["prompt"]), audio_html(audio_url)),
        meaning_round["opts"], meaning_round["ans"], GOLD)
    s3 = choice_step(
        "<p style='margin:0 0 8px;'>%s</p><p style='margin:0 0 10px;font-size:15px;color:%s;'>"
        "Выбери правильное чтение:</p>%s" % (big_char(han, 56), DIM, audio_html(audio_url)),
        pinyin_round["opts"], pinyin_round["ans"], PUMPKIN)
    s4 = text_step(
        "Сладость или гадость · финал фонарика",
        "Вернись в урок и пройди фазы 3–4",
        [body_block(
            "<p style='margin:0 0 8px;'><b style='color:%s;'>Осталось:</b></p>"
            "<ul style='margin:0 0 8px;padding-left:20px;'>"
            "<li><b>Мел и камень</b> — обведи %s три раза.</li>"
            "<li><b>Сладость или гадость</b> — 5 раундов игры.</li></ul>"
            "<p style='margin:0;font-size:13px;'>Когда раунды пройдены, фонарик <b>%s</b> загорается, "
            "и двор на <a href='%s' target='_blank' rel='noopener noreferrer' style='color:%s;'>карте двора</a> "
            "становится светлее. Прогресс сохраняется в браузере.</p>"
            % (GOLD, big_char(han, 22), esc(han), base + "/", PUMPKIN), POISON)],
        url, 1500, POISON)
    return [s1, s2, s3, s4]


def story_lesson_steps(lesson, base, model):
    url = base + lesson["url"]
    chars_row = "".join(
        '<img alt="%s" height="72" width="72" src="%s" style="margin:0 3px;border:3px solid %s;border-radius:10px;">'
        % (n, base + "/shared/characters/" + f, KOKO)
        for n, f in [("Костик", "kostik-portrait.svg"), ("Люми", "lumi-portrait.svg"),
                     ("Эхо", "echo-portrait.svg"), ("Магистр Коко", "wizard.svg")])
    intro = body_block(
        "<p style='margin:0 0 10px;'>Добро пожаловать в <b>Двор Тихой Луны</b>! Магистр Коко варил "
        "хэллоуинское зелье «Тыквенная улыбка», но чихнул с неправильным тоном — и заклинание "
        "воскресило обитателей старого кладбища, заодно стерев всем память.</p>"
        "<p style='margin:0 0 10px;'>Чтобы всё исправить, нужно зажечь <b>25 Фонариков Памяти</b>: "
        "каждый загорается от выученного китайского знака или слова. В путь!</p>"
        "<p style='margin:0 0 6px;text-align:center;'>%s</p>"
        "<p style='margin:6px 0 0;text-align:center;font-size:13px;color:%s;'>"
        "<b>Костик</b> — экскурсовод и бывший учитель каллиграфии · <b>Люми</b> — застенчивый "
        "призрак-фонарщик · <b>Эхо</b> — мышь с колокольни, помнит все звуки · <b>Коко</b> — мастер звука и тонов"
        "</p>" % (chars_row, DIM), KOKO)
    plan = body_block(
        "<p style='margin:0 0 8px;'><b style='color:%s;'>Как устроен курс</b></p>"
        "<ul style='margin:0 0 8px;padding-left:20px;'>"
        "<li><b>Пробуждение</b> — история чиха и тоны полуночи.</li>"
        "<li><b>Крыло Луны, Крыло Сердца, Крыло Памяти</b> — 17 иероглифов: у каждого свой урок-фонарик.</li>"
        "<li><b>Слова-заклинания</b> — 8 слов из уже знакомых знаков.</li>"
        "<li><b>Праздник Тыквенной Луны</b> — большая викторина, финал истории и бонус-игра.</li></ul>"
        "<p style='margin:0;font-size:13px;color:%s;'>Внутри уроков — прописи, аудио, мини-сказки и игры. "
        "Прогресс сохраняется, фонарики горят. 🎃</p>" % (GOLD, DIM), GOLD)
    return [text_step("Чих Магистра Коко", "История двора · 6 сцен",
                      [intro, plan], url, 1800, KOKO)]


def tones_lesson_steps(lesson, base, model):
    url = base + lesson["url"]
    t = model["tones"]
    intro = body_block(
        "<p style='margin:0 0 10px;'>%s</p><p style='margin:0;'>%s</p>" % (
            t["intro"][0].replace("<b>", "<b style='color:%s;'>" % GOLD),
            t["intro"][1].replace("<b>", "<b style='color:%s;'>" % GOLD)), KOKO)
    tone_names = {1: "1-й тон — высокий ровный (мā)", 2: "2-й тон — вверх (мá)",
                  3: "3-й тон — вниз и обратно (мǎ)", 4: "4-й тон — резко вниз (мà)"}
    steps = [text_step("Тоны полуночи", "Четыре чиха Коко · слушай и повторяй",
                       [intro], url, 1800, KOKO)]
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
    intro = body_block(
        "<p style='margin:0 0 8px;'><b style='color:%s;'>Осада почти отбита!</b> Великая викторина "
        "«Сладость или гадость»: 12 вопросов по всем 25 фонарикам. За каждый — балл; если ошибся — "
        "вернись к фонарику на <a href='%s' target='_blank' rel='noopener noreferrer' style='color:%s;'>карте двора</a>.</p>"
        "<p style='margin:0;font-size:13px;color:%s;'>Вопросы трёх видов: смысл знака, чтение знака, "
        "чтение на слух. Не забудь включить звук!</p>" % (GOLD, base + "/", PUMPKIN, DIM), PUMPKIN)
    steps = [text_step("Большая викторина «Сладость или гадость»",
                       "12 вопросов · все 25 фонариков", [intro], None, 0, PUMPKIN)]
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
    f = model["finale"]
    paras = "".join("<p style='margin:0 0 8px;'>%s</p>" % p for p in f["paras"][:2])
    tail = body_block(
        "<p style='margin:0 0 8px;'>%s</p><p style='margin:0 0 8px;'>Чем закончилась история — читай "
        "на странице финала: там грамота <b>«%s»</b> на твое имя.</p>"
        "<p style='margin:0;font-size:13px;color:%s;'>Спасибо, что зажёг все фонари двора!</p>"
        % (f["paras"][2], esc(f["certificate"]), DIM), GOLD)
    return [text_step("Праздник Тыквенной Луны", "Финал истории и грамота",
                      [body_block(paras, KOKO), tail], base + lesson["url"], 1800, GOLD)]


def bonus_lesson_steps(lesson, base, model):
    intro = body_block(
        "<p style='margin:0 0 8px;'><b style='color:%s;'>Бонус: Осада домика!</b> Полночь, к конфетному "
        "домику стягиваются гости: призраки, тыквы, мыши. Отбей <b>12 волн</b>, узнавая знаки и слова. "
        "Три ❤️, на волну — 18 секунд.</p>"
        "<p style='margin:0;font-size:13px;color:%s;'>Баллов не даёт — только слава. Эхо наблюдает с колокольни.</p>"
        % (GOLD, DIM), POISON)
    return [text_step("Бонус: Осада домика", "12 волн · 3 ❤️ · 18 секунд на волну",
                      [intro], base + lesson["url"], 1100, POISON)]


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
    if lesson["kind"] in ("glyph", "word"):
        return "%d. %s" % (lesson["num"], lesson["title"])
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
            sr = api.api("POST", "step-sources",
                         {"stepSource": {"lesson": lesson_id, "position": pos, "block": block}})
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
    desc = ('<div><p>%s</p><p><b>Внутри:</b> 17 иероглифов и 8 слов, прописи, аудио, тоны, '
            'мини-сказки, викторина из 12 вопросов и бонус-игра «Осада домика». '
            'Все игры открываются прямо в уроках.</p><p>Персонажи: <b>Костик</b> (скелет-экскурсовод), '
            '<b>Люми</b> (призрак-фонарщик), <b>Эхо</b> (мышь с колокольни) и <b>Магистр Коко</b>.</p></div>'
            % esc(model["summary"]))
    api.api("PATCH", "courses/303598", {"course": {"summary": model["summary"], "description": desc}})
    print("course patched (summary+description)")
    c = api.api("GET", "courses/303598")["courses"][0]
    print("final sections:", len(c["sections"]))


if __name__ == "__main__":
    main()
