# -*- coding: utf-8 -*-
"""Обложки уроков для Stepik (cover в «Настройках урока»).

Генерирует build/covers/NN <имя>.png — квадрат 720x720, пиксель-арт в стиле курса:
модель рисуется 240x240 и увеличивается x3 (nearest). На каждой обложке — крупная
тыква с вырезанным светящимся номером урока в формате Stepik «раздел.урок» (1.1…6.3).
Детерминизм: random.Random("cover:"+title)."""
import json
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_grounds import PAL, Canvas, pumpkin_small

MODEL_PATH = ROOT / "build" / "course_model.json"
MANIFEST_PATH = ROOT / "build" / "stepik_manifest.json"
OUT = ROOT / "build" / "covers"
OUT.mkdir(parents=True, exist_ok=True)

SIDE, SCALE = 240, 3
GROUND_Y = 208
SKY_BANDS = [(0, 44, "#0a0714"), (44, 88, "#110c26"), (88, 132, "#171030"),
             (132, 176, "#1f153d"), (176, GROUND_Y, "#261a49")]

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

DIGITS = {
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
}


def human_name(title, kind, target):
    if kind in ("glyph", "word"):
        tail = title.split("—", 1)[1].strip() if "—" in title else ""
        tail = tail.split(";")[0].split(".")[0].strip()
        return "%s %s" % (target, tail)
    return SPECIAL_NAMES.get(title, title)


def blit(d, cv, dx, dy, sx=1):
    for (x, y, w, h, c) in cv.r:
        d.rectangle([dx + x * sx, dy + y * sx,
                     dx + (x + w) * sx - 1, dy + (y + h) * sx - 1], fill=c)


def sky(d, rng):
    for (y0, y1, c) in SKY_BANDS:
        d.rectangle([0, y0, SIDE, y1 - 1], fill=c)
    for _ in range(26):
        x, y = rng.randrange(4, SIDE - 4), rng.randrange(3, 180)
        d.point((x, y), fill=rng.choice(["#7a6f8a", "#b3a8d4", "#7fd8ff"]))
    for _ in range(5):
        x, y = rng.randrange(8, SIDE - 10), rng.randrange(6, 150)
        d.rectangle([x, y, x + 1, y + 1], fill="#ffd54f")


def ground(d):
    d.rectangle([0, GROUND_Y, SIDE, GROUND_Y + 1], fill="#3f7a1e")
    d.rectangle([0, GROUND_Y + 2, SIDE, GROUND_Y + 3], fill="#2c5a14")
    d.rectangle([0, GROUND_Y + 4, SIDE, SIDE - 5], fill="#141027")
    d.rectangle([0, SIDE - 4, SIDE, SIDE - 1], fill="#0e0a1d")


def big_pumpkin(d):
    cx = SIDE // 2
    top, height, half = 92, 112, 78
    for yy in range(height + 4):
        t = (yy - (height + 4) / 2) / ((height + 4) / 2)
        hw = int(half * max(0.0, 1 - t * t) ** 0.5) + 2
        d.rectangle([cx - hw, top + yy - 2, cx + hw, top + yy - 2], fill="#5e2306")
    for yy in range(height):
        t = (yy - height / 2) / (height / 2)
        hw = int(half * max(0.0, 1 - t * t) ** 0.5)
        d.rectangle([cx - hw, top + yy, cx + hw, top + yy], fill=PAL["pump"])
    for rx, rw in [(cx - 46, 14), (cx + 32, 14)]:
        for yy in range(10, height - 14):
            t = (yy - height / 2) / (height / 2)
            hw = int(half * max(0.0, 1 - t * t) ** 0.5)
            if cx - rx <= hw - 2 and rx + rw - cx <= hw - 2:
                d.rectangle([rx, top + yy, rx + rw, top + yy + 3], fill=PAL["pump2"])
    for yy in range(height - 10, height):
        t = (yy - height / 2) / (height / 2)
        hw = int(half * max(0.0, 1 - t * t) ** 0.5)
        d.rectangle([cx - hw + 2, top + yy, cx + hw - 2, top + yy], fill=PAL["pump2"])
    d.rectangle([cx - 9, 76, cx - 3, 91], fill=PAL["stem"])
    d.rectangle([cx - 2, 74, cx + 9, 80], fill=PAL["stem"])
    d.rectangle([cx + 1, 74, cx + 8, 75], fill="#2c5a14")


def number(d, label):
    text = str(label)
    s = 11 if len(text) == 1 else 7
    cols = 5 * len(text) + (len(text) - 1)
    x0 = (SIDE - cols * s) // 2
    y0 = 92 + (112 - 7 * s) // 2
    for i, ch in enumerate(text):
        rows = DIGITS[ch]
        bx = x0 + i * 6 * s
        for ry, row in enumerate(rows):
            for rx, bit in enumerate(row):
                if bit == "1":
                    px, py = bx + rx * s, y0 + ry * s
                    d.rectangle([px - 2, py - 2, px + s + 1, py + s + 1], fill="#4a1c06")
    for i, ch in enumerate(text):
        rows = DIGITS[ch]
        bx = x0 + i * 6 * s
        for ry, row in enumerate(rows):
            for rx, bit in enumerate(row):
                if bit == "1":
                    px, py = bx + rx * s, y0 + ry * s
                    d.rectangle([px, py, px + s - 1, py + s - 1], fill="#ffd54f")
                    d.rectangle([px, py, px + s - 1, py + 2], fill="#fff3b0")


def render(title, pos, label):
    rng = random.Random("cover:" + title)
    img = Image.new("RGB", (SIDE, SIDE))
    d = ImageDraw.Draw(img)
    sky(d, rng)
    ground(d)
    big_pumpkin(d)
    number(d, label)
    for x in (14, SIDE - 14 - 16):
        cv = Canvas()
        pumpkin_small(cv, 0)
        blit(d, cv, x, 174, sx=2)
    return img.resize((SIDE * SCALE, SIDE * SCALE), Image.NEAREST)


def main():
    model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    man = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    by_title = {}
    for sec in model["sections"]:
        for l in sec["lessons"]:
            by_title[l["title"]] = l
    made = 0
    pos = 0
    for snum, (sname, s) in enumerate(man["sections"].items(), start=1):
        lpos = 0
        for ltitle, le in s["lessons"].items():
            lid = le.get("lesson_id")
            if not lid:
                continue
            l = by_title.get(ltitle)
            if l and l["kind"] in ("glyph", "word"):
                kind = l["kind"]
                target = (l["data"].get("char") or l["data"].get("word"))
            else:
                kind = SPECIAL_KINDS.get(ltitle)
                target = None
            if not kind:
                print("ПРОПУСК (нет темы):", ltitle)
                continue
            lpos += 1
            pos += 1
            label = "%d.%d" % (snum, lpos)
            img = render(ltitle, pos, label)
            name = "%02d %s.png" % (pos, human_name(ltitle, kind, target))
            img.save(OUT / name, "PNG", optimize=True)
            made += 1
            print(name, "| lesson", lid, "| номер", label, "|", ltitle)
    print("ИТОГО обложек:", made)


if __name__ == "__main__":
    main()
