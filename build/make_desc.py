# -*- coding: utf-8 -*-
"""Хэллоуин-описание курса «Двор Тихой Луны» для страницы /course/303598/info.

Режимы:
  python build/make_desc.py --dry       — показать HTML обеих версий
  python build/make_desc.py             — бэкап старого описания, PATCH styled,
                                          проверка санитайзера; при вырезанных
                                          стилях — авто-PATCH fallback-версии
  python build/make_desc.py --fallback  — сразу простая версия (p/b/ul/li)
"""
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import publish_stepik as ps
from publish_stepik import DIM, GOLD, INK, KOKO, LINE, NIGHT, PANEL, POISON, PUMPKIN

COURSE_ID = 303598
INTERIOR = "https://samoylenkoanatoly.github.io/chinese-halloween/shared/interior"


def img(name, alt):
    return ('<img src="%s/%s?v=1" alt="%s" style="width:100%%;height:auto;">'
            % (INTERIOR, name, alt))

MARKERS = [
    "ДОБРО ПОЖАЛОВАТЬ ВО ДВОР ТИХОЙ ЛУНЫ",
    "Обитатели двора",
    "Что ждёт внутри",
    "Как зажигается фонарик",
    "Программа праздника",
    "Сладость или гадость",
    "Осада домика",
    "Зажги все 25",
]

INSIDE = [
    "🏮 25 Фонариков Памяти — 17 иероглифов и 8 слов-заклинаний",
    "🎧 живое аудио и все четыре тона полуночи",
    "✍️ прописи «Мел и камень»",
    "📖 мини-сказки двора",
    "🍬 большая викторина «Сладость или гадость» — 12 вопросов",
    "🕹️ бонус-игра «Осада домика» — 12 волн и 3 ❤️",
    "✨ всё прямо в уроках — ничего устанавливать не нужно",
]

CHARS = [
    ("🧙", "Магистр Коко", "чихнул с неправильным тоном — и кладбище ожило", KOKO),
    ("💀", "Костик", "скелет-экскурсовод, знает каждую тропинку двора", LINE),
    ("👻", "Люми", "призрак-фонарщик, зажигает Фонарики Памяти", GOLD),
    ("🐭", "Эхо", "мышь с колокольни, повторяет каждое слово", POISON),
]

PROG = [
    ("🌙", "Пробуждение", "Чих Магистра Коко и Тоны полуночи", False),
    ("🌕", "Крыло Луны", "天 中 上 下 大 小", True),
    ("❤️", "Крыло Сердца", "山 水 火 土 石", True),
    ("🕯️", "Крыло Памяти", "田 女 子 马 车 门", True),
    ("✨", "Слова-заклинания", "大小 · 上下 · 山水 · 火山 · 水田 · 女子 · 马车 · 大门", True),
    ("🎃", "Праздник Тыквенной Луны", "большая викторина, финал истории и бонус «Осада домика»", False),
]

FOR_WHOM = ("Курс для тех, кто начинает китайский с нуля: первые иероглифы, "
            "пиньинь и тоны — в компании дружных призраков. Уроки короткие, "
            "бояться нечего. 🖤")

FINALE = ("Костик уже держит фонарик наготове.<br>"
          "Зажги все 25 — и двор озарится! 🏮🏮🏮")

PHASES = "🌫 Туман → 🎧 Голос Коко → ✏️ Мел и камень → 🍬 Сладость или гадость"


def load_summary():
    m = json.load(open(ps.MODEL_PATH, encoding="utf-8"))
    return m["summary"]


def han(chars, color=INK, size=17):
    return '<span style="font-size:%dpx;color:%s;">%s</span>' % (size, color, chars)


def divider(kind):
    name, alt = (("divider-a.svg", "Разделитель: свечи") if kind == "a"
                 else ("divider-b.svg", "Разделитель: мыши и луна"))
    return '<p style="margin:14px 0;text-align:center;">%s</p>' % img(name, alt)


def h(text, color):
    return ('<p style="margin:16px 0 8px;text-align:center;font-size:17px;color:%s;"><b>%s</b></p>'
            % (color, text))


def card(emoji, name, role, border):
    return ('<td style="width:50%%;padding:10px 8px;background-color:%s;border:3px solid %s;'
            'text-align:center;">'
            '<p style="margin:0 0 4px;font-size:15px;color:%s;"><b>%s %s</b></p>'
            '<p style="margin:0;font-size:13px;color:%s;">%s</p></td>'
            % (PANEL, border, INK, emoji, name, DIM, role))


def build_styled():
    inner = []
    inner.append(img("border-top.svg", "Хэллоуинская рамка: свечи, мыши, тыквы и призрак"))
    inner.append(
        '<p style="margin:14px 0 0;text-align:center;font-size:21px;color:%s;">'
        '<b>🎃 ДОБРО ПОЖАЛОВАТЬ ВО ДВОР ТИХОЙ ЛУНЫ 🌙</b></p>'
        '<p style="margin:8px 0 0;text-align:center;font-size:14px;color:%s;">'
        'хэллоуин-интенсив китайского для начинающих</p>'
        '<p style="margin:14px 0 0;">%s</p>'
        % (GOLD, DIM, img("heroes.svg", "Обитатели двора: Магистр Коко, Костик, Люми и Эхо")))
    inner.append(divider("a"))
    inner.append('<div style="padding:12px 14px;background-color:%s;border:3px solid %s;">%s</div>'
                 % (PANEL, LINE, ps.esc(load_summary())))
    inner.append(h("🕯️ Обитатели двора", PUMPKIN))
    inner.append('<table style="width:100%;"><tbody>')
    for row in (CHARS[:2], CHARS[2:]):
        inner.append("<tr>")
        for emoji, name, role, border in row:
            inner.append(card(emoji, name, role, border))
        inner.append("</tr>")
    inner.append("</tbody></table>")
    inner.append(h("🍬 Что ждёт внутри", GOLD))
    inner.append('<ul style="margin:8px 0;">')
    for item in INSIDE:
        inner.append('<li style="margin:6px 0;color:%s;">%s</li>' % (INK, item))
    inner.append("</ul>")
    inner.append(h("🏮 Как зажигается фонарик", POISON))
    inner.append('<p style="margin:6px 0;text-align:center;font-size:15px;color:%s;">%s</p>' % (INK, PHASES))
    inner.append('<p style="margin:6px 0;text-align:center;font-size:13px;color:%s;">'
                 'четыре фазы и два испытания — и во дворе загорается ещё один фонарик, '
                 'например %s [tiān] — «небо»</p>' % (DIM, han("天", GOLD, 16)))
    inner.append(h("🗺 Программа праздника", PUMPKIN))
    for emoji, title, tail, is_han in PROG:
        shown = han(tail) if is_han else '<span style="color:%s;">%s</span>' % (DIM, tail)
        inner.append('<p style="margin:7px 0;font-size:15px;color:%s;">%s <b>%s</b> — %s</p>'
                     % (INK, emoji, title, shown))
    inner.append(divider("b"))
    inner.append('<p style="margin:10px 0;text-align:center;font-size:14px;color:%s;">%s</p>'
                 % (DIM, FOR_WHOM))
    inner.append('<div style="padding:14px 10px;text-align:center;background-color:%s;'
                 'border:4px solid %s;"><p style="margin:0;font-size:17px;color:%s;">'
                 '<b>%s</b></p></div>' % (PANEL, GOLD, GOLD, FINALE))
    inner.append('<p style="margin:16px 0 0;">%s</p>'
                 % img("border-bottom.svg", "Хэллоуинская рамка: тыквы, свечи и череп"))
    return ('<div style="padding:20px 22px;background-color:%s;border:4px solid %s;color:%s;">%s</div>'
            % (NIGHT, KOKO, INK, "".join(inner)))


def build_fallback():
    parts = []
    parts.append('<p><b>🎃 ДОБРО ПОЖАЛОВАТЬ ВО ДВОР ТИХОЙ ЛУНЫ 🌙</b><br>'
                 'хэллоуин-интенсив китайского для начинающих</p>')
    parts.append("<p>· 🦇 · ⚰️ · 🕷️ · 🕯️ ·</p>")
    parts.append("<p>%s</p>" % ps.esc(load_summary()))
    parts.append("<p><b>🕯️ Обитатели двора</b></p>")
    for emoji, name, role, _b in CHARS:
        parts.append("<p>%s <b>%s</b> — %s</p>" % (emoji, name, role))
    parts.append("<p><b>🍬 Что ждёт внутри</b></p>")
    parts.append("<ul>%s</ul>" % "".join("<li>%s</li>" % t for t in INSIDE))
    parts.append("<p><b>🏮 Как зажигается фонарик</b></p>")
    parts.append("<p>%s</p>" % PHASES)
    parts.append("<p>четыре фазы и два испытания — и во дворе загорается ещё один фонарик, "
                 "например 天 [tiān] — «небо»</p>")
    parts.append("<p><b>🗺 Программа праздника</b></p>")
    for emoji, title, tail, _is_han in PROG:
        parts.append("<p>%s <b>%s</b> — %s</p>" % (emoji, title, tail))
    parts.append("<p>%s</p>" % FOR_WHOM)
    parts.append("<p><b>%s</b></p>" % FINALE.replace("<br>", " "))
    return "".join(parts)


def put_course(api, **fields):
    """WAF Stepik блокирует PATCH courses/…, но пропускает PUT полного объекта."""
    full = dict(api.api("GET", "courses/%d" % COURSE_ID)["courses"][0])
    full.update(fields)
    api.api("PUT", "courses/%d" % COURSE_ID, {"course": full})


def report(new):
    print("stored bytes:", len(new.encode("utf-8")))
    print("div kept:", "<div" in new, "| style kept:", "style=" in new,
          "| ul kept:", "<ul" in new, "| b kept:", "<b" in new)
    for m in MARKERS:
        print(("OK  " if m in new else "MISS"), m)


def main():
    dry = "--dry" in sys.argv
    force_fb = "--fallback" in sys.argv
    styled, fb = build_styled(), build_fallback()
    if dry:
        print("=== STYLED (%d bytes) ===" % len(styled.encode("utf-8")))
        print(styled)
        print()
        print("=== FALLBACK (%d bytes) ===" % len(fb.encode("utf-8")))
        print(fb)
        return
    api = ps.Stepik()
    old = api.api("GET", "courses/%d" % COURSE_ID)["courses"][0].get("description") or ""
    backup = os.path.join(os.path.dirname(ps.TOKEN_PATH), "desc_backup_303598.html")
    with open(backup, "w", encoding="utf-8") as f:
        f.write(old)
    print("backup:", backup, "(%d bytes)" % len(old.encode("utf-8")))
    put_course(api, description=fb if force_fb else styled)
    new = api.api("GET", "courses/%d" % COURSE_ID)["courses"][0].get("description") or ""
    if not force_fb and ("style=" not in new or "background-color" not in new):
        print("sanitizer stripped styles -> patching fallback")
        put_course(api, description=fb)
        new = api.api("GET", "courses/%d" % COURSE_ID)["courses"][0].get("description") or ""
    print("final version:", "styled" if "background-color" in new else "fallback")
    report(new)


if __name__ == "__main__":
    main()
