# -*- coding: utf-8 -*-
"""Персональные нижние фоны для каждого урока-иероглифа.

Для каждого знака генерирует:
  shared/frame/grounds/<знак>.svg       — срез поверхности 1440x144 (уникальная композиция)
  shared/frame/undergrounds/<знак>.svg  — подземелье 1440x600 с тематическим героем
Тема подбирается по смыслу знака; расстановка общих элементов — random.Random(знак)."""
import random
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from data import GLYPHS

OUT_G = ROOT / "shared" / "frame" / "grounds"
OUT_U = ROOT / "shared" / "frame" / "undergrounds"
OUT_G.mkdir(parents=True, exist_ok=True)
OUT_U.mkdir(parents=True, exist_ok=True)

W, H, G = 360, 36, 16
UH = 150

PAL = {
    "g1": "#3f7a1e", "g2": "#2c5a14", "g3": "#4f9a28", "g4": "#62b436",
    "soil2": "#0e0a1d", "dark": "#0b0716", "gate": "#070510", "pebble": "#1c1533",
    "stone": "#514e73", "stone2": "#3a3757", "stone3": "#5d5a80",
    "bone": "#c9c2a4", "bone2": "#a89f86", "skull": "#e8e2c4",
    "pump": "#ff8c2b", "pump2": "#d96a12", "stem": "#4f9a28",
    "hand": "#86c232", "hand2": "#4f7a1e",
    "flame": "#ffd54f", "candle": "#efe9dc",
    "wood": "#6b4a2a", "wood2": "#4e351f",
    "chest": "#8a5fd6", "chest2": "#6a48ab",
    "root": "#2c5a14", "worm": "#e88fb0", "line": "#2e2240",
    "ghostC": "#bfe8e0", "gold": "#ffd54f", "gold2": "#d9b44a",
    "blood": "#e64533", "blood2": "#a3271f", "eyes": "#e64533",
    "blue": "#29b6f6", "lblue": "#7fd8ff",
    "lava": "#ff5c1f", "iron": "#8a8ba8", "iron2": "#6e6f8c",
    "petal": "#ff9ec4", "teddy": "#8a5f3a", "teddy2": "#a87950",
    "rpost": "#b93126", "rpost2": "#8a1f18",
    "mouse": "#9b93b8", "mole": "#6b4a2a", "poison": "#86c232",
    "shirt": "#4a3a5e",
}


class Canvas:
    def __init__(self):
        self.r = []

    def px(self, x, y, w, h, c):
        self.r.append((int(x), int(y), int(w), int(h), PAL[c]))


# ---------------------------------------------------------------- общие элементы поверхности
def skull(cv, x, y):
    cv.px(x, y, 8, 5, "skull")
    cv.px(x + 1, y + 5, 6, 2, "skull")
    cv.px(x + 1, y + 2, 1, 1, "gate")
    cv.px(x + 6, y + 2, 1, 1, "gate")
    cv.px(x + 2, y + 5, 1, 1, "gate")
    cv.px(x + 5, y + 5, 1, 1, "gate")


def bone(cv, x, y):
    cv.px(x, y, 8, 2, "bone")
    cv.px(x - 1, y - 1, 2, 2, "bone")
    cv.px(x - 1, y + 1, 2, 2, "bone")
    cv.px(x + 7, y - 1, 2, 2, "bone")
    cv.px(x + 7, y + 1, 2, 2, "bone")


def cross(cv, x):
    cv.px(x + 3, 4, 2, 14, "stone")
    cv.px(x, 8, 8, 2, "stone")
    cv.px(x + 3, 4, 1, 14, "stone2")
    cv.px(x - 1, 18, 10, 2, "stone2")


def slab(cv, x):
    cv.px(x + 3, 3, 8, 2, "stone")
    cv.px(x + 1, 5, 12, 2, "stone")
    cv.px(x, 7, 14, 10, "stone")
    cv.px(x + 3, 9, 8, 2, "stone2")
    cv.px(x + 3, 12, 6, 2, "stone2")
    cv.px(x - 2, 17, 18, 3, "stone2")


def arch(cv, x):
    cv.px(x + 4, 2, 8, 2, "stone")
    cv.px(x + 2, 4, 12, 2, "stone")
    cv.px(x, 6, 16, 10, "stone")
    cv.px(x + 12, 6, 4, 10, "stone2")
    cv.px(x + 4, 8, 8, 2, "stone2")
    cv.px(x + 5, 11, 6, 2, "stone2")


def hand(cv, x):
    cv.px(x + 1, 9, 2, 3, "hand")
    cv.px(x + 4, 8, 2, 4, "hand")
    cv.px(x + 7, 10, 2, 2, "hand")
    cv.px(x + 2, 12, 6, 3, "hand2")
    cv.px(x + 3, 15, 4, 7, "hand2")


def pumpkin(cv, x):
    cv.px(x + 4, 6, 2, 2, "stem")
    cv.px(x + 8, 6, 4, 1, "stem")
    cv.px(x, 8, 16, 10, "pump")
    cv.px(x + 3, 10, 2, 6, "pump2")
    cv.px(x + 11, 10, 2, 6, "pump2")
    cv.px(x + 3, 11, 3, 3, "gate")
    cv.px(x + 10, 11, 3, 3, "gate")
    cv.px(x + 4, 16, 8, 1, "gate")


def pumpkin_small(cv, x):
    cv.px(x + 3, 10, 1, 1, "stem")
    cv.px(x, 11, 8, 5, "pump")
    cv.px(x + 3, 12, 1, 3, "pump2")
    cv.px(x + 1, 12, 2, 2, "gate")
    cv.px(x + 5, 12, 2, 2, "gate")


def candles(cv, x):
    cv.px(x + 2, 6, 1, 2, "flame")
    cv.px(x + 1, 8, 3, 6, "candle")
    cv.px(x, 14, 5, 1, "stone2")
    cv.px(x + 9, 4, 1, 2, "flame")
    cv.px(x + 8, 6, 3, 4, "candle")
    cv.px(x + 7, 10, 5, 1, "stone2")


def coffin(cv, x):
    cv.px(x + 2, 7, 10, 3, "wood2")
    cv.px(x + 1, 10, 12, 3, "wood")
    cv.px(x, 13, 14, 3, "wood")
    cv.px(x, 13, 14, 1, "wood2")
    cv.px(x + 3, 14, 1, 1, "bone")
    cv.px(x + 10, 14, 1, 1, "bone")
    cv.px(x - 2, 16, 18, 2, "dark")


def mound(cv, x):
    cv.px(x + 4, 11, 4, 1, "soil2")
    cv.px(x, 14, 3, 3, "soil2")
    cv.px(x + 3, 12, 6, 5, "soil2")
    cv.px(x + 9, 14, 3, 3, "soil2")


def spider(cv, x):
    cv.px(x + 4, 0, 1, 8, "line")
    cv.px(x + 3, 8, 3, 3, "line")
    cv.px(x + 4, 8, 1, 1, "stone2")
    cv.px(x + 1, 9, 2, 1, "line")
    cv.px(x + 6, 9, 2, 1, "line")
    cv.px(x + 2, 11, 1, 1, "line")
    cv.px(x + 5, 11, 1, 1, "line")


SURF_ELS = [
    ("cross", lambda cv, x: cross(cv, x), 11),
    ("slab", lambda cv, x: slab(cv, x), 19),
    ("arch", lambda cv, x: arch(cv, x), 17),
    ("hand", lambda cv, x: hand(cv, x), 10),
    ("pumpkin", lambda cv, x: pumpkin(cv, x), 17),
    ("skull", lambda cv, x: skull(cv, x, 11), 9),
    ("candles", lambda cv, x: candles(cv, x), 13),
    ("bone", lambda cv, x: bone(cv, x, 14), 11),
    ("coffin", lambda cv, x: coffin(cv, x), 19),
    ("mound", lambda cv, x: mound(cv, x), 13),
    ("pumpkin2", lambda cv, x: pumpkin_small(cv, x), 9),
    ("spider", lambda cv, x: spider(cv, x), 10),
]


# ---------------------------------------------------------------- тематические поверхности
def t_sky(cv, x):
    slab(cv, x)
    cx, cy = x + 7, 9
    cv.px(cx, cy - 2, 1, 5, "gold")
    cv.px(cx - 2, cy, 5, 1, "gold")
    cv.px(cx - 1, cy - 1, 1, 1, "gold")
    cv.px(cx + 1, cy - 1, 1, 1, "gold")
    cv.px(cx - 1, cy + 1, 1, 1, "gold")
    cv.px(cx + 1, cy + 1, 1, 1, "gold")


def t_center(cv, x):
    arch(cv, x)
    cv.px(x + 6, 9, 6, 6, "blood")
    cv.px(x + 7, 10, 4, 4, "skull")
    cv.px(x + 8, 11, 2, 2, "blood")


def t_up(cv, x):
    slab(cv, x)
    for i in range(3):
        yy = 5 + i * 3
        cv.px(x + 6, yy, 4, 1, "bone")
        cv.px(x + 5, yy + 1, 1, 1, "bone")
        cv.px(x + 10, yy + 1, 1, 1, "bone")


def t_down(cv, x):
    slab(cv, x)
    for i in range(3):
        yy = 6 + i * 3
        cv.px(x + 6, yy + 1, 4, 1, "bone")
        cv.px(x + 5, yy, 1, 1, "bone")
        cv.px(x + 10, yy, 1, 1, "bone")


def t_big(cv, x):
    cv.px(x + 8, G - 18, 3, 3, "stem")
    cv.px(x + 16, G - 17, 6, 1, "stem")
    cv.px(x, G - 15, 24, 15, "pump")
    cv.px(x + 5, G - 12, 3, 9, "pump2")
    cv.px(x + 16, G - 12, 3, 9, "pump2")
    cv.px(x + 5, G - 11, 4, 4, "gate")
    cv.px(x + 15, G - 11, 4, 4, "gate")
    cv.px(x + 7, G - 4, 10, 1, "gate")
    cv.px(x + 9, G - 6, 1, 1, "gate")
    cv.px(x + 13, G - 6, 1, 1, "gate")


def t_small(cv, x):
    for i in range(3):
        xx = x + i * 8
        cv.px(xx, G - 5, 6, 5, "stone")
        cv.px(xx + 1, G - 6, 4, 1, "stone")
        cv.px(xx + 2, G - 3, 2, 1, "stone2")


def t_mountain(cv, x):
    cv.px(x + 6, G - 9, 10, 9, "stone")
    cv.px(x, G - 5, 8, 5, "stone")
    cv.px(x + 14, G - 4, 8, 4, "stone")
    cv.px(x + 8, G - 11, 5, 2, "stone2")
    cv.px(x + 2, G - 6, 3, 2, "stone2")


def t_water(cv, x):
    cv.px(x, G + 2, 18, 2, "blue")
    cv.px(x + 2, G + 1, 14, 1, "lblue")
    cv.px(x + 4, G + 2, 2, 1, "lblue")
    cv.px(x + 19, G - 5, 1, 5, "g3")
    cv.px(x + 20, G - 7, 1, 2, "g4")


def t_fire(cv, x):
    cv.px(x, G + 3, 4, 1, "lava")
    cv.px(x + 4, G + 4, 3, 1, "lava")
    cv.px(x + 7, G + 3, 2, 1, "gold")
    cv.px(x + 9, G + 5, 4, 1, "lava")
    cv.px(x + 13, G + 4, 2, 1, "gold")
    cv.px(x + 2, G + 1, 1, 1, "lava")
    cv.px(x + 10, G + 1, 1, 1, "gold")


def t_earth(cv, x):
    cv.px(x + 2, G - 18, 2, 10, "wood")
    cv.px(x + 1, G - 20, 4, 2, "wood2")
    cv.px(x, G - 8, 6, 8, "iron")
    cv.px(x + 1, G - 2, 4, 2, "iron2")


def t_stone(cv, x):
    cv.px(x + 2, G - 10, 12, 10, "stone")
    cv.px(x, G - 6, 4, 6, "stone")
    cv.px(x + 12, G - 4, 4, 4, "stone")
    cv.px(x + 4, G - 9, 5, 2, "stone3")


def t_field(cv, x):
    for i in range(3):
        cv.px(x, G + 3 + i * 4, 24, 1, "pebble")
        cv.px(x, G + 4 + i * 4, 24, 1, "soil2")
    for i in range(4):
        cv.px(x + 2 + i * 6, G + 2, 1, 3, "g3")
        cv.px(x + 2 + i * 6, G + 1, 1, 1, "gold")


def t_female(cv, x):
    slab(cv, x)
    for dx, dy in [(-1, 1), (3, 0), (8, 0), (12, 1), (14, 4), (-2, 5)]:
        cv.px(x + dx, dy, 2, 2, "petal")


def t_child(cv, x):
    cv.px(x + 2, G - 9, 8, 9, "teddy")
    cv.px(x + 1, G - 11, 2, 2, "teddy")
    cv.px(x + 9, G - 11, 2, 2, "teddy")
    cv.px(x + 3, G - 7, 1, 1, "gate")
    cv.px(x + 8, G - 7, 1, 1, "gate")
    cv.px(x + 5, G - 5, 2, 1, "gate")
    cv.px(x + 4, G - 3, 4, 4, "teddy2")
    cv.px(x - 1, G - 6, 3, 2, "teddy")
    cv.px(x + 10, G - 6, 3, 2, "teddy")


def t_horse(cv, x):
    slab(cv, x)
    cv.px(x + 5, 7, 2, 7, "gold")
    cv.px(x + 10, 7, 2, 7, "gold")
    cv.px(x + 5, 5, 7, 2, "gold")
    cv.px(x + 7, 4, 3, 1, "gold")


def t_cart(cv, x):
    cv.px(x + 4, G - 12, 8, 1, "wood")
    cv.px(x + 2, G - 11, 2, 2, "wood")
    cv.px(x + 12, G - 11, 2, 2, "wood")
    cv.px(x, G - 9, 2, 4, "wood")
    cv.px(x + 14, G - 9, 2, 4, "wood")
    cv.px(x + 2, G - 5, 2, 2, "wood")
    cv.px(x + 12, G - 5, 2, 2, "wood")
    cv.px(x + 4, G - 3, 8, 1, "wood")
    cv.px(x + 7, G - 10, 1, 8, "wood2")
    cv.px(x + 3, G - 6, 9, 1, "wood2")


def t_gate(cv, x):
    cv.px(x, G - 14, 3, 14, "rpost")
    cv.px(x + 13, G - 14, 3, 14, "rpost")
    cv.px(x - 1, G - 16, 18, 3, "rpost2")
    cv.px(x + 5, G - 13, 6, 4, "gold")
    cv.px(x + 6, G - 12, 4, 2, "flame")


# ---------------------------------------------------------------- тематические подземелья
def u_meteor(cv, x, y):
    cv.px(x, y, 12, 10, "stone")
    cv.px(x + 2, y + 2, 8, 3, "stone3")
    cv.px(x + 5, y + 1, 1, 5, "gold")
    cv.px(x + 3, y + 3, 5, 1, "gold")
    cv.px(x + 8, y + 6, 3, 3, "stone2")
    cv.px(x + 14, y - 4, 2, 2, "lava")
    cv.px(x + 18, y - 8, 2, 2, "gold")
    cv.px(x + 22, y - 12, 1, 1, "gold")
    for dx, dy in [(30, 10), (36, 7), (42, 12), (38, 18)]:
        cv.px(x + dx, y + dy, 2, 2, "gold")


def u_well(cv, x, y):
    cv.px(x, y, 20, 2, "stone")
    cv.px(x, y + 12, 20, 2, "stone")
    cv.px(x, y + 2, 2, 10, "stone")
    cv.px(x + 18, y + 2, 2, 10, "stone")
    cv.px(x + 4, y + 2, 12, 10, "gate")
    cv.px(x + 9, y - 12, 1, 14, "line")
    cv.px(x + 7, y + 4, 5, 4, "wood")
    cv.px(x + 7, y + 3, 5, 1, "wood2")


def u_pedestal(cv, x, y):
    cv.px(x + 2, y, 10, 3, "stone2")
    cv.px(x + 3, y - 18, 8, 18, "stone")
    cv.px(x + 2, y - 20, 10, 2, "stone3")
    cv.px(x + 4, y - 26, 6, 6, "chest")
    cv.px(x + 5, y - 28, 4, 2, "gold")
    cv.px(x + 6, y - 29, 2, 1, "pump")


def u_shaft(cv, x, y):
    cv.px(x, y, 10, 70, "gate")
    cv.px(x - 2, y, 2, 70, "stone2")
    cv.px(x + 10, y, 2, 70, "stone2")
    cv.px(x + 3, y + 18, 4, 2, "bone")
    cv.px(x + 2, y + 34, 5, 2, "bone")
    skull(cv, x + 1, y + 52)
    cv.px(x + 2, y + 66, 6, 2, "pebble")


def u_ribs(cv, x, y):
    cv.px(x, y + 2, 40, 2, "bone")
    for i in range(6):
        cv.px(x + 2 + i * 7, y + 4, 3, 22, "bone")
    cv.px(x, y + 4, 2, 22, "bone")
    cv.px(x + 44, y + 6, 12, 8, "skull")
    cv.px(x + 45, y + 14, 10, 3, "skull")
    cv.px(x + 47, y + 9, 3, 3, "gate")
    cv.px(x + 53, y + 9, 3, 3, "gate")
    cv.px(x + 48, y + 14, 4, 2, "gate")


def u_mouse(cv, x, y):
    cv.px(x, y + 8, 16, 12, "gate")
    cv.px(x + 2, y + 6, 12, 2, "gate")
    cv.px(x + 4, y + 2, 9, 6, "mouse")
    cv.px(x + 12, y + 3, 4, 3, "mouse")
    cv.px(x + 15, y + 4, 1, 1, "petal")
    cv.px(x + 3, y, 2, 2, "mouse")
    cv.px(x + 7, y, 2, 2, "mouse")
    cv.px(x + 1, y + 5, 1, 1, "gate")
    cv.px(x + 16, y + 7, 8, 1, "petal")


def u_strata(cv, x, y):
    for i in range(3):
        cv.px(x, y + i * 10, 80, 3, "stone")
        cv.px(x, y + i * 10 + 3, 80, 7, "soil2")
    cv.px(x + 12, y + 4, 10, 6, "stone2")
    cv.px(x + 40, y + 14, 12, 6, "stone2")
    cv.px(x + 62, y + 24, 8, 5, "stone2")


def u_river(cv, x, y):
    cv.px(x, y, 70, 8, "blue")
    cv.px(x + 2, y + 1, 66, 2, "lblue")
    for i in range(5):
        cv.px(x + 4 + i * 12, y + 4, 5, 1, "lblue")
    cv.px(x + 20, y + 3, 8, 1, "bone")
    cv.px(x + 22, y + 2, 1, 3, "bone")
    cv.px(x + 17, y + 2, 1, 3, "bone")
    cv.px(x + 40, y - 3, 2, 2, "lblue")
    cv.px(x + 52, y - 6, 1, 1, "lblue")


def u_lava(cv, x, y):
    cv.px(x, y, 76, 6, "lava")
    cv.px(x + 4, y + 6, 68, 4, "blood2")
    for i in range(6):
        cv.px(x + 6 + i * 12, y - 2, 3, 2, "gold")
    cv.px(x + 20, y - 6, 2, 2, "lava")
    cv.px(x + 48, y - 7, 1, 1, "gold")
    cv.px(x + 30, y - 10, 1, 3, "lava")
    cv.px(x + 56, y - 11, 1, 3, "lava")


def u_roots(cv, x, y):
    cv.px(x + 16, y, 4, 40, "root")
    for i, dx in enumerate([-14, -8, 10, 16]):
        cv.px(x + 16 + min(dx, 0), y + 8 + i * 6, abs(dx) + 4, 2, "root")
    cv.px(x + 36, y + 30, 10, 7, "mole")
    cv.px(x + 44, y + 32, 3, 3, "mole")
    cv.px(x + 46, y + 33, 1, 1, "petal")
    cv.px(x + 38, y + 32, 1, 1, "gate")


def u_golem(cv, x, y):
    cv.px(x, y, 22, 18, "stone")
    cv.px(x + 2, y - 3, 18, 3, "stone2")
    cv.px(x + 4, y + 5, 4, 4, "poison")
    cv.px(x + 14, y + 5, 4, 4, "poison")
    cv.px(x + 8, y + 13, 6, 2, "gate")
    cv.px(x + 6, y + 2, 1, 3, "stone2")
    cv.px(x + 16, y + 10, 1, 4, "stone2")


def u_rice(cv, x, y):
    for i in range(3):
        cv.px(x, y + i * 12, 70, 2, "pebble")
    cv.px(x + 24, y + 30, 20, 12, "wood")
    cv.px(x + 24, y + 30, 20, 2, "wood2")
    cv.px(x + 27, y + 26, 14, 4, "gold")
    cv.px(x + 30, y + 24, 8, 2, "gold")
    cv.px(x + 20, y + 44, 2, 1, "gold")
    cv.px(x + 46, y + 42, 2, 1, "gold")
    cv.px(x + 34, y + 46, 2, 1, "gold")


def u_mirror(cv, x, y):
    cv.px(x, y, 12, 12, "gold")
    cv.px(x + 2, y + 2, 8, 8, "lblue")
    cv.px(x + 3, y + 3, 2, 2, "skull")
    cv.px(x + 5, y + 12, 2, 8, "gold")
    for i in range(6):
        cv.px(x + 18 + (i % 3) * 4, y + 4 + (i // 3) * 4, 2, 2, "gold")
    cv.px(x - 8, y + 20, 10, 2, "petal")
    cv.px(x - 10, y + 18, 2, 2, "petal")
    cv.px(x - 10, y + 22, 2, 2, "petal")


def u_toys(cv, x, y):
    cv.px(x, y, 8, 8, "chest")
    cv.px(x + 2, y + 2, 4, 4, "gate")
    cv.px(x + 10, y + 2, 8, 8, "pump")
    cv.px(x + 12, y + 4, 4, 4, "gate")
    cv.px(x + 20, y, 8, 8, "poison")
    cv.px(x + 22, y + 2, 4, 4, "gate")
    cv.px(x + 32, y + 3, 8, 8, "blood")
    cv.px(x + 34, y + 5, 4, 4, "skull")
    cv.px(x + 44, y + 6, 3, 4, "gold")
    cv.px(x + 48, y + 5, 3, 4, "pump")
    cv.px(x + 52, y + 7, 3, 4, "petal")


def u_horse(cv, x, y):
    cv.px(x, y, 10, 8, "skull")
    cv.px(x + 10, y + 3, 14, 5, "skull")
    cv.px(x + 2, y + 2, 3, 3, "gate")
    cv.px(x + 8, y + 2, 3, 3, "gate")
    for i in range(4):
        cv.px(x + 12 + i * 3, y + 6, 2, 2, "gate")
    cv.px(x + 2, y + 14, 2, 6, "gold")
    cv.px(x + 7, y + 14, 2, 6, "gold")
    cv.px(x + 2, y + 12, 7, 2, "gold")
    cv.px(x + 14, y + 14, 2, 6, "gold")
    cv.px(x + 19, y + 14, 2, 6, "gold")
    cv.px(x + 14, y + 12, 7, 2, "gold")
    cv.px(x - 7, y + 12, 5, 1, "gold2")
    cv.px(x - 6, y + 14, 3, 1, "gold2")


def u_cart(cv, x, y):
    cv.px(x + 8, y, 12, 2, "wood")
    cv.px(x + 2, y + 2, 4, 4, "wood")
    cv.px(x + 22, y + 2, 4, 4, "wood")
    cv.px(x, y + 6, 2, 8, "wood")
    cv.px(x + 26, y + 6, 2, 8, "wood")
    cv.px(x + 2, y + 14, 4, 4, "wood")
    cv.px(x + 22, y + 14, 4, 4, "wood")
    cv.px(x + 8, y + 18, 12, 2, "wood")
    cv.px(x + 13, y + 2, 2, 16, "wood2")
    cv.px(x + 4, y + 8, 20, 2, "wood2")
    cv.px(x + 30, y + 9, 26, 3, "wood2")
    cv.px(x + 56, y + 7, 8, 8, "iron")
    cv.px(x + 40, y + 24, 12, 2, "wood")
    cv.px(x + 38, y + 22, 2, 2, "wood")
    cv.px(x + 52, y + 22, 2, 2, "wood")


def u_gate(cv, x, y):
    cv.px(x, y + 14, 3, 40, "stone2")
    cv.px(x + 27, y + 14, 3, 40, "stone2")
    cv.px(x + 3, y + 4, 24, 4, "stone")
    cv.px(x + 5, y, 20, 4, "stone")
    cv.px(x + 3, y + 18, 24, 36, "wood")
    for i in range(4):
        cv.px(x + 3, y + 20 + i * 9, 24, 1, "wood2")
    cv.px(x + 14, y + 30, 2, 20, "gold")
    cv.px(x + 13, y + 8, 4, 6, "pump")
    cv.px(x + 14, y + 9, 2, 3, "flame")


THEMES = {
    "天": {"s": (t_sky, 19), "u": (u_meteor, 70), "dots": [("gold", 4)]},
    "中": {"s": (t_center, 17), "u": (u_well, 24), "dots": [("blood", 3)]},
    "上": {"s": (t_up, 19), "u": (u_pedestal, 16), "dots": [("bone", 3)]},
    "下": {"s": (t_down, 19), "u": (u_shaft, 16), "dots": [("bone", 3)]},
    "大": {"s": (t_big, 25), "u": (u_ribs, 60), "dots": [("pump", 5)]},
    "小": {"s": (t_small, 23), "u": (u_mouse, 28), "dots": [("gold", 3)]},
    "山": {"s": (t_mountain, 23), "u": (u_strata, 82), "dots": [("stone3", 5)]},
    "水": {"s": (t_water, 21), "u": (u_river, 72), "dots": [("blue", 6), ("lblue", 4)]},
    "火": {"s": (t_fire, 16), "u": (u_lava, 78), "dots": [("lava", 6), ("gold", 4)]},
    "土": {"s": (t_earth, 7), "u": (u_roots, 50), "dots": [("g3", 5)]},
    "石": {"s": (t_stone, 17), "u": (u_golem, 24), "dots": [("stone3", 5)]},
    "田": {"s": (t_field, 25), "u": (u_rice, 72), "dots": [("gold", 6)]},
    "女": {"s": (t_female, 19), "u": (u_mirror, 34), "dots": [("petal", 6)]},
    "子": {"s": (t_child, 14), "u": (u_toys, 57), "dots": [("petal", 4), ("gold", 3), ("pump", 3)]},
    "马": {"s": (t_horse, 19), "u": (u_horse, 26), "dots": [("gold2", 4)]},
    "车": {"s": (t_cart, 17), "u": (u_cart, 66), "dots": [("wood2", 4)]},
    "门": {"s": (t_gate, 18), "u": (u_gate, 32), "dots": [("blood", 3), ("gold", 3)]},
}

# ---------------------------------------------------------------- крупные объекты подземелья
def m_skeleton(cv, x, y):
    skull(cv, x, y)
    for i in range(8):
        cv.px(x + 10 + i * 4, y + 4, 3, 2, "bone")
    for i in range(6):
        cv.px(x + 13 + i * 5, y - 3, 2, 14, "bone")
    cv.px(x + 42, y + 1, 9, 7, "bone")
    cv.px(x + 45, y + 4, 3, 2, "gate")
    cv.px(x + 51, y + 2, 22, 2, "bone")
    cv.px(x + 51, y + 6, 22, 2, "bone")
    cv.px(x + 74, y + 8, 5, 3, "bone")
    cv.px(x + 74, y + 12, 5, 3, "bone")
    cv.px(x + 12, y + 6, 2, 16, "bone")
    cv.px(x + 11, y + 22, 1, 3, "bone")
    cv.px(x + 14, y + 22, 1, 3, "bone")


def m_crypt(cv, x, y):
    cv.px(x + 41, y, 4, 14, "stone2")
    cv.px(x + 37, y + 4, 12, 4, "stone2")
    cv.px(x + 10, y + 14, 70, 6, "stone")
    cv.px(x + 4, y + 20, 82, 6, "stone")
    cv.px(x, y + 26, 90, 6, "stone")
    cv.px(x + 10, y + 19, 70, 1, "stone2")
    cv.px(x + 4, y + 25, 82, 1, "stone2")
    cv.px(x, y + 32, 12, 56, "stone")
    cv.px(x + 78, y + 32, 12, 56, "stone")
    for yy in range(y + 36, y + 88, 8):
        cv.px(x, yy, 12, 1, "stone2")
        cv.px(x + 78, yy, 12, 1, "stone2")
    cv.px(x + 4, y + 32, 1, 56, "stone2")
    cv.px(x + 86, y + 32, 1, 56, "stone2")
    cv.px(x + 12, y + 36, 66, 52, "gate")
    cv.px(x + 35, y + 60, 5, 5, "eyes")
    cv.px(x + 51, y + 60, 5, 5, "eyes")
    for i in range(6):
        cv.px(x + 37 + i * 3, y + 70, 2, 4, "bone")
    cv.px(x + 45, y + 38, 1, 10, "line")
    cv.px(x + 43, y + 48, 5, 4, "line")
    cv.px(x + 44, y + 49, 1, 1, "eyes")
    skull(cv, x + 15, y + 92)
    cv.px(x + 13, y + 100, 12, 3, "stone2")


def m_coffin(cv, x, y):
    cv.px(x, y, 54, 6, "wood2")
    cv.px(x + 2, y + 6, 50, 16, "wood")
    cv.px(x + 2, y + 20, 50, 4, "wood2")
    cv.px(x + 23, y + 2, 2, 8, "bone")
    cv.px(x + 20, y + 4, 8, 2, "bone")
    cv.px(x + 4, y + 8, 2, 2, "bone")
    cv.px(x + 48, y + 8, 2, 2, "bone")


def m_chest(cv, x, y):
    cv.px(x, y, 40, 10, "chest2")
    cv.px(x + 4, y + 10, 32, 18, "chest")
    cv.px(x + 14, y + 10, 4, 18, "gold")
    cv.px(x + 13, y + 16, 6, 6, "gold")
    cv.px(x - 8, y + 28, 3, 4, "pump")
    cv.px(x - 5, y + 32, 5, 4, "blood")
    cv.px(x + 1, y + 32, 5, 4, "gold")
    cv.px(x + 9, y + 30, 5, 4, "pump")
    cv.px(x + 18, y + 29, 5, 4, "gold")


def m_zombie(cv, x, y):
    cv.px(x + 9, y + 8, 12, 10, "hand")
    cv.px(x + 9, y + 7, 12, 2, "soil2")
    cv.px(x + 11, y + 11, 3, 3, "gate")
    cv.px(x + 18, y + 11, 3, 3, "gate")
    cv.px(x + 14, y + 16, 6, 2, "gate")
    cv.px(x + 15, y + 16, 1, 1, "bone")
    cv.px(x + 18, y + 16, 1, 1, "bone")
    cv.px(x + 13, y + 18, 4, 3, "hand")
    cv.px(x + 7, y + 21, 16, 22, "hand2")
    cv.px(x + 9, y + 24, 12, 8, "shirt")
    cv.px(x + 7, y + 30, 4, 4, "shirt")
    cv.px(x + 1, y + 4, 3, 20, "hand")
    cv.px(x, y + 1, 1, 3, "hand")
    cv.px(x + 3, y, 1, 4, "hand")
    cv.px(x + 28, y + 8, 3, 18, "hand")
    cv.px(x + 27, y + 5, 1, 3, "hand")
    cv.px(x + 30, y + 4, 1, 4, "hand")
    cv.px(x + 8, y + 43, 5, 16, "hand2")
    cv.px(x + 17, y + 43, 5, 16, "hand2")


def m_ghost(cv, x, y):
    cv.px(x + 1, y, 8, 2, "ghostC")
    cv.px(x, y + 2, 10, 8, "ghostC")
    cv.px(x + 2, y + 5, 2, 2, "gate")
    cv.px(x + 6, y + 5, 2, 2, "gate")
    cv.px(x, y + 10, 2, 3, "ghostC")
    cv.px(x + 4, y + 10, 2, 3, "ghostC")
    cv.px(x + 8, y + 10, 2, 3, "ghostC")


def m_pumpkin_half(cv, x, y):
    cv.px(x + 5, y, 2, 2, "stem")
    cv.px(x, y + 2, 14, 8, "pump")
    cv.px(x + 4, y + 5, 2, 2, "gate")
    cv.px(x + 9, y + 5, 2, 2, "gate")
    cv.px(x + 2, y + 9, 10, 1, "gate")
    cv.px(x - 2, y + 10, 18, 3, "soil2")


MAJORS = {
    "skeleton": (m_skeleton, 87, 35),
    "crypt": (m_crypt, 92, 24),
    "coffin": (m_coffin, 56, 100),
    "chest": (m_chest, 50, 78),
    "zombie": (m_zombie, 34, 6),
}


def svg_out(cv, w, h, vw, vh, grad_id, c1, c2, grad_y, grad_h):
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
        "shape-rendering=\"crispEdges\">" % (w, h, vw, vh),
        '<defs><linearGradient id="%s" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
        "</linearGradient></defs>" % (grad_id, c1, c2),
        '<rect x="0" y="%d" width="%d" height="%d" fill="url(#%s)"/>' % (grad_y, w, grad_h, grad_id),
    ]
    parts += ['<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % r for r in cv.r]
    parts.append("</svg>")
    return "\n".join(parts)


def compose_surface(ch, theme):
    cv = Canvas()
    rng = random.Random("s" + ch)
    els = SURF_ELS[:]
    rng.shuffle(els)
    theme_fn, theme_w = theme["s"]
    order = [(theme_fn, theme_w)]
    for name, fn, w in els:
        order.append((fn, w))
        if len(order) >= 8:
            break
    start = rng.randrange(0, 3)
    order = order[start:] + order[:start]
    x = 12
    for fn, w in order:
        if x + w > 348:
            break
        fn(cv, x)
        x += w + rng.randint(4, 8)
    for tx in range(2, W, 7):
        r = (tx * 13 + ord(ch[0])) % 7
        if r < 2:
            cv.px(tx, G - 2, 2, 2, "g3" if r == 0 else "g1")
        elif r == 3:
            cv.px(tx + 1, G - 3, 1, 1, "g4")
    for color, n in theme["dots"]:
        for _ in range(n):
            cv.px(rng.randrange(8, 340), rng.randrange(G + 5, 33), 2, 1, color)
    for _ in range(6):
        cv.px(rng.randrange(10, 340), rng.randrange(G + 6, 33), 2, 1, "pebble")
    cv.r[0:0] = [(0, G, W, 2, PAL["g1"]), (0, G + 2, W, 2, PAL["g2"])]
    out = svg_out(cv, W, H, 1440, 144, "sg", "#141027", "#120d26", G + 4, H - G - 4)
    (OUT_G / (ch + ".svg")).write_text(out, encoding="utf-8")
    return len(cv.r)


def compose_underground(ch, theme):
    cv = Canvas()
    rng = random.Random("u" + ch)
    hero_fn, hero_w = theme["u"]
    hero_x = 130 + rng.randint(0, max(1, 95 - hero_w))
    hero_y = rng.choice([38, 44, 50])
    picks = rng.sample(list(MAJORS), 2)
    for i, name in enumerate(picks):
        fn, w, y = MAJORS[name]
        x = 14 if i == 0 else 346 - w
        fn(cv, x, y)
    ghost_x = 108 + rng.randint(0, 8)
    m_ghost(cv, ghost_x, 86 + rng.randint(0, 10))
    m_pumpkin_half(cv, 228 + rng.randint(0, 8), 44 + rng.randint(0, 6))
    for _ in range(rng.randint(2, 3)):
        wx = rng.randrange(20, 330)
        wy = rng.randrange(118, 140)
        cv.px(wx, wy, 3, 1, "worm")
        cv.px(wx + 3, wy + 1, 2, 1, "worm")
        cv.px(wx + 5, wy, 3, 1, "worm")
    for _ in range(rng.randint(1, 2)):
        bone(cv, rng.randrange(30, 300), rng.randrange(122, 140))
    for rx in rng.sample([20, 55, 90, 175, 210, 300, 335], 5):
        ln = rng.randint(8, 22)
        cv.px(rx, 0, 2, ln, "root")
        if ln >= 12:
            cv.px(rx - 2, ln - 5, 2, 2, "root")
    for _ in range(rng.randint(8, 12)):
        cv.px(rng.randrange(8, 348), rng.randrange(20, 144), rng.choice([1, 2]), 1, "pebble")
    hero_fn(cv, hero_x, hero_y)
    out = svg_out(cv, W, UH, 1440, 600, "ug", "#120d26", "#0a0714", 0, UH)
    (OUT_U / (ch + ".svg")).write_text(out, encoding="utf-8")
    return len(cv.r)


def main():
    total = 0
    for g in GLYPHS:
        ch = g["char"]
        theme = THEMES.get(ch)
        if not theme:
            print("нет темы:", ch)
            continue
        n1 = compose_surface(ch, theme)
        n2 = compose_underground(ch, theme)
        total += 1
        print(ch, g["meaning"], "| поверхность:", n1, "rect | подземелье:", n2, "rect")
    print("ИТОГО уроков:", total, "| файлов:", total * 2)


if __name__ == "__main__":
    main()
