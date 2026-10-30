# -*- coding: utf-8 -*-
"""Обложки уроков для Stepik (cover в «Настройках урока»).

Генерирует build/covers/<lesson_id>.png — 1440x480, пиксель-арт в стиле курса:
модель рисуется 480x160 и увеличивается x3 (nearest). Детерминизм: random.Random(title).
25 контентных уроков — крупный знак/слово с тёплым свечением; спец-уроки — эмблемы."""
import json
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_grounds import (Canvas, pumpkin, pumpkin_small, cross, slab, candles,
                          skull, bone, spider, m_ghost, t_big)

MODEL_PATH = ROOT / "build" / "course_model.json"
MANIFEST_PATH = ROOT / "build" / "stepik_manifest.json"
OUT = ROOT / "build" / "covers"
OUT.mkdir(parents=True, exist_ok=True)

LW, LH, SCALE = 480, 160, 3
GROUND_Y = 126
SKY_BANDS = [(0, 32, "#0a0714"), (32, 64, "#110c26"), (64, 96, "#171030"), (96, GROUND_Y, "#1f153d")]
TONE = {1: "#e64533", 2: "#ff8c2b", 3: "#29b6f6", 4: "#86c232"}
PARTY = ["#ffd54f", "#ff8c2b", "#e64533", "#29b6f6", "#86c232", "#ff9ec4"]
FONT_PATHS = [r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\msyh.ttc",
              r"C:\Windows\Fonts\simhei.ttf"]

SPECIAL_KINDS = {
    "Чих Магистра Коко": "story",
    "Тоны полуночи": "tones",
    "Карта двора": "map",
    "Большая викторина «Сладость или гадость»": "quiz",
    "Праздник Тыквенной Луны": "finale",
    "Бонус: Осада домика": "bonus",
}
SPECIAL_NAMES = {
    "Чих Магистра Коко": "История",
    "Тоны полуночи": "Тоны",
    "Карта двора": "Карта двора",
    "Большая викторина «Сладость или гадость»": "Викторина",
    "Праздник Тыквенной Луны": "Финал",
    "Бонус: Осада домика": "Бонус Осада",
}


def human_name(title, kind, target):
    if kind in ("glyph", "word"):
        tail = title.split("—", 1)[1].strip() if "—" in title else ""
        tail = tail.split(";")[0].split(".")[0].strip()
        return "%s %s" % (target, tail)
    return SPECIAL_NAMES.get(title, title)


def font(size):
    for p in FONT_PATHS:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    raise RuntimeError("CJK-шрифт не найден: " + ", ".join(FONT_PATHS))


def blit(d, cv, dx, dy, sx=1):
    for (x, y, w, h, c) in cv.r:
        d.rectangle([dx + x * sx, dy + y * sx,
                     dx + (x + w) * sx - 1, dy + (y + h) * sx - 1], fill=c)


def sky(img, d, rng):
    for (y0, y1, c) in SKY_BANDS:
        d.rectangle([0, y0, LW, y1 - 1], fill=c)
    for _ in range(22):
        x, y = rng.randrange(4, LW - 4), rng.randrange(3, 96)
        d.point((x, y), fill=rng.choice(["#7a6f8a", "#b3a8d4", "#7fd8ff"]))
    for _ in range(4):
        x, y = rng.randrange(8, LW - 10), rng.randrange(4, 60)
        d.rectangle([x, y, x + 1, y + 1], fill="#ffd54f")


def moon(d, cx, cy, r):
    for rr, c in [(r + 5, "#0e0a1d"), (r + 3, "#2a1d4e")]:
        for yy in range(-rr, rr + 1):
            ww = int((rr * rr - yy * yy) ** 0.5)
            d.rectangle([cx - ww, cy + yy, cx + ww, cy + yy], fill=c)
    for yy in range(-r, r + 1):
        ww = int((r * r - yy * yy) ** 0.5)
        d.rectangle([cx - ww, cy + yy, cx + ww, cy + yy], fill="#f2e6c0")
    for (ox, oy, w, h) in [(-8, -6, 7, 6), (4, 2, 8, 7), (-4, 9, 6, 5), (8, -10, 4, 4)]:
        d.rectangle([cx + ox, cy + oy, cx + ox + w, cy + oy + h], fill="#d8c9a3")


def bat(d, x, y):
    c = "#0c0818"
    d.rectangle([x, y, x + 2, y + 1], fill=c)
    d.rectangle([x + 2, y + 1, x + 3, y + 2], fill=c)
    d.rectangle([x + 4, y + 1, x + 6, y + 3], fill=c)
    d.rectangle([x + 4, y, x + 4, y], fill=c)
    d.rectangle([x + 6, y, x + 6, y], fill=c)
    d.rectangle([x + 7, y + 1, x + 8, y + 2], fill=c)
    d.rectangle([x + 8, y, x + 10, y + 1], fill=c)


def ground(d, rng):
    d.rectangle([0, GROUND_Y, LW, GROUND_Y + 1], fill="#3f7a1e")
    d.rectangle([0, GROUND_Y + 2, LW, GROUND_Y + 3], fill="#2c5a14")
    d.rectangle([0, GROUND_Y + 4, LW, LH - 1], fill="#141027")
    d.rectangle([0, 146, LW, LH - 1], fill="#0e0a1d")
    for tx in range(4, LW, 9):
        if rng.random() < 0.3:
            d.rectangle([tx, GROUND_Y - 2, tx, GROUND_Y - 1], fill="#4f9a28")
    items = [(pumpkin, 16), (pumpkin_small, 8), (cross, 8), (slab, 14),
             (candles, 13), (spider, 10)]
    left = [10, 42, 76, 112, 146]
    right = [318, 350, 386, 422, 454]
    rng.shuffle(left)
    rng.shuffle(right)
    slots = [(x, fn, w) for x, (fn, w) in zip(left + right, items[:3] + items[3:6])]
    for x, fn, w in slots[:6]:
        cv = Canvas()
        if fn is skull:
            fn(cv, x, 11)
        elif fn is bone:
            fn(cv, x, 14)
        else:
            fn(cv, x)
        blit(d, cv, 0, GROUND_Y - 16)


def glyph_center(d, text):
    size = 84 if len(text) == 1 else 56
    f = font(size)
    cx, cy = 240, 74
    ring = [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, -2), (-2, 2), (2, 2)]
    for (dx, dy) in ring:
        d.text((cx + dx, cy + dy), text, font=f, fill="#d96a12", anchor="mm")
    for (dx, dy) in [(-1, -1), (1, -1), (-1, 1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
        d.text((cx + dx, cy + dy), text, font=f, fill="#ff8c2b", anchor="mm")
    d.text((cx, cy), text, font=f, fill="#efe9dc", anchor="mm")


def house(d, x, y):
    d.rectangle([x, y, x + 26, y + 17], fill="#6b4a2a")
    d.rectangle([x, y, x + 26, y + 1], fill="#4e351f")
    d.rectangle([x + 2, y + 4, x + 26, y + 5], fill="#4e351f")
    d.rectangle([x + 2, y + 11, x + 26, y + 12], fill="#4e351f")
    for i in range(5):
        d.rectangle([x - 2 + i * 7, y - 5 - i, x + 4 + i * 7, y - 2 - i], fill="#8a1f18")
    d.rectangle([x + 11, y + 7, x + 16, y + 17], fill="#070510")
    d.rectangle([x + 4, y + 6, x + 8, y + 10], fill="#ffd54f")
    d.rectangle([x + 20, y + 6, x + 24, y + 10], fill="#ffd54f")


def tone_mark(d, x, y, n):
    c = TONE[n]
    if n == 1:
        d.rectangle([x, y, x + 8, y + 1], fill=c)
    elif n == 2:
        for i in range(4):
            d.rectangle([x + i * 2, y + 3 - i * 2, x + i * 2 + 2, y + 5 - i * 2], fill=c)
    elif n == 3:
        d.rectangle([x, y, x + 1, y + 2], fill=c)
        d.rectangle([x + 2, y + 2, x + 3, y + 4], fill=c)
        d.rectangle([x + 4, y, x + 5, y + 2], fill=c)
        d.rectangle([x + 6, y - 2, x + 7, y], fill=c)
    else:
        for i in range(4):
            d.rectangle([x + i * 2, y + i * 2, x + i * 2 + 2, y + i * 2 + 2], fill=c)


def emblem(d, rng, kind):
    if kind == "story":
        cv = Canvas()
        m_ghost(cv, 0, 0)
        blit(d, cv, 208, 52, sx=3)
        for _ in range(7):
            x, y = rng.randrange(150, 330), rng.randrange(30, 100)
            d.rectangle([x, y, x + rng.choice([1, 2]), y + 1], fill=rng.choice(["#ffd54f", "#ff8c2b"]))
    elif kind == "tones":
        for i in range(4):
            x = 168 + i * 34
            tone_mark(d, x + 6, 92, i + 1)
            cv = Canvas()
            pumpkin_small(cv, 0)
            blit(d, cv, x, GROUND_Y - 16)
    elif kind == "map":
        house(d, 60, GROUND_Y - 30)
        for i in range(4):
            x = 300 + i * 40
            d.rectangle([x, GROUND_Y - 10, x + 1, GROUND_Y - 1], fill="#6b4a2a")
            d.rectangle([x - 1, GROUND_Y - 12, x + 2, GROUND_Y - 11], fill="#4f9a28")
        d.rectangle([100, GROUND_Y + 8, 340, GROUND_Y + 9], fill="#514e73")
        cv = Canvas()
        candles(cv, 0)
        blit(d, cv, 210, GROUND_Y - 34)
    elif kind == "quiz":
        f = font(96)
        for (dx, dy) in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
            d.text((240 + dx, 72 + dy), "?", font=f, fill="#a3271f", anchor="mm")
        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            d.text((240 + dx, 72 + dy), "?", font=f, fill="#e64533", anchor="mm")
        d.text((240, 72), "?", font=f, fill="#ffd54f", anchor="mm")
        for x in (150, 306):
            cv = Canvas()
            pumpkin_small(cv, 0)
            blit(d, cv, x, GROUND_Y - 16)
    elif kind == "finale":
        cv = Canvas()
        t_big(cv, 0)
        blit(d, cv, 216, GROUND_Y - 34, sx=2)
        for _ in range(14):
            x, y = rng.randrange(140, 340), rng.randrange(24, 110)
            d.rectangle([x, y, x + 1, y + 1], fill=rng.choice(PARTY))
    elif kind == "bonus":
        house(d, 214, GROUND_Y - 30)
        for (x, y) in [(120, 70), (170, 46), (330, 56)]:
            cv = Canvas()
            pumpkin_small(cv, 0)
            blit(d, cv, x, y)
            d.rectangle([x + 4, y + 14, x + 5, y + 15], fill="#e64533")
        for (x, y) in [(108, 62), (158, 38), (318, 48)]:
            d.rectangle([x, y, x + 1, y + 1], fill="#ffd54f")


def render(title, kind, target, num):
    rng = random.Random("cover:" + title)
    img = Image.new("RGB", (LW, LH))
    d = ImageDraw.Draw(img)
    sky(img, d, rng)
    moon(d, 404, 34, 24)
    for (bx, by) in [(60, 22), (150, 58), (352, 74), (280, 30)]:
        bat(d, bx, by)
    ground(d, rng)
    if kind in ("glyph", "word"):
        glyph_center(d, target)
        d.text((10, 10), "%d/25" % num, font=font(13), fill="#b3a8d4", anchor="lm")
    else:
        emblem(d, rng, kind)
    return img.resize((LW * SCALE, LH * SCALE), Image.NEAREST)


def main():
    model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    man = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    by_title = {}
    for sec in model["sections"]:
        for l in sec["lessons"]:
            by_title[l["title"]] = l
    made = 0
    pos = 0
    for sname, s in man["sections"].items():
        for ltitle, le in s["lessons"].items():
            lid = le.get("lesson_id")
            if not lid:
                continue
            l = by_title.get(ltitle)
            if l and l["kind"] in ("glyph", "word"):
                d = l["data"]
                kind = l["kind"]
                target = d.get("char") or d.get("word")
                num = l["num"]
            else:
                kind = SPECIAL_KINDS.get(ltitle)
                target, num = None, None
            if not kind:
                print("ПРОПУСК (нет темы):", ltitle)
                continue
            pos += 1
            img = render(ltitle, kind, target, num)
            name = "%02d %s.png" % (pos, human_name(ltitle, kind, target))
            out = OUT / name
            img.save(out, "PNG", optimize=True)
            made += 1
            print(name, "| lesson", lid, "|", ltitle)
    print("ИТОГО обложек:", made)


if __name__ == "__main__":
    main()
