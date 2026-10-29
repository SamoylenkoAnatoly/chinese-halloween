# -*- coding: utf-8 -*-
"""Широкий уникальный срез кладбищенской земли 360x36 (вывод 1440x144) -> shared/frame/ground.svg.

Один проход на 1440px: все объекты уникальны, без повторяющейся сетки.
Поверхность: трава y16-19, грунт y20-35 с градиентом в темноту."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W, H = 360, 36
GRASS = 16

C = {
    "g1": "#3f7a1e", "g2": "#2c5a14", "g3": "#4f9a28", "g4": "#62b436",
    "soil2": "#0e0a1d", "dark": "#0b0716", "pebble": "#1c1533",
    "stone": "#514e73", "stone2": "#3a3757",
    "bone": "#c9c2a4", "skull": "#e8e2c4",
    "pump": "#ff8c2b", "pump2": "#d96a12", "stem": "#4f9a28",
    "hand": "#86c232", "hand2": "#4f7a1e",
    "flame": "#ffd54f", "candle": "#efe9dc",
    "wood": "#6b4a2a", "wood2": "#4e351f",
    "root": "#2c5a14", "worm": "#e88fb0", "line": "#2e2240",
}

R = []


def px(x, y, w, h, c):
    R.append((x, y, w, h, C[c]))


def cross(x, y):
    px(x + 3, y, 2, 14, "stone")
    px(x, y + 4, 8, 2, "stone")
    px(x + 3, y, 1, 14, "stone2")
    px(x - 1, y + 14, 10, 2, "stone2")


def slab(x, y):
    px(x + 3, y, 8, 2, "stone")
    px(x + 1, y + 2, 12, 2, "stone")
    px(x, y + 4, 14, 10, "stone")
    px(x + 3, y + 6, 8, 2, "stone2")
    px(x + 3, y + 9, 6, 2, "stone2")
    px(x + 10, y + 5, 1, 4, "stone2")
    px(x - 2, y + 14, 18, 3, "stone2")


def arch(x, y):
    px(x + 4, y, 8, 2, "stone")
    px(x + 2, y + 2, 12, 2, "stone")
    px(x, y + 4, 16, 10, "stone")
    px(x + 12, y + 4, 4, 10, "stone2")
    px(x + 4, y + 6, 8, 2, "stone2")
    px(x + 5, y + 9, 6, 2, "stone2")


def mound(x, y):
    px(x + 4, y + 1, 4, 1, "soil2")
    px(x, y + 4, 3, 3, "soil2")
    px(x + 3, y + 2, 6, 5, "soil2")
    px(x + 9, y + 4, 3, 3, "soil2")


def pumpkin(x, y):
    px(x + 4, y, 2, 2, "stem")
    px(x + 8, y, 4, 1, "stem")
    px(x, y + 2, 16, 10, "pump")
    px(x + 3, y + 4, 2, 6, "pump2")
    px(x + 11, y + 4, 2, 6, "pump2")
    px(x + 3, y + 5, 3, 3, "dark")
    px(x + 10, y + 5, 3, 3, "dark")
    px(x + 4, y + 10, 8, 1, "dark")
    px(x + 5, y + 9, 1, 1, "dark")
    px(x + 9, y + 9, 1, 1, "dark")


def pumpkin_small(x, y):
    px(x + 3, y, 1, 1, "stem")
    px(x, y + 1, 8, 5, "pump")
    px(x + 3, y + 2, 1, 3, "pump2")
    px(x + 1, y + 2, 2, 2, "dark")
    px(x + 5, y + 2, 2, 2, "dark")
    px(x + 2, y + 4, 4, 1, "dark")


def hand(x, y):
    px(x + 1, y, 2, 3, "hand")
    px(x + 4, y - 1, 2, 4, "hand")
    px(x + 7, y + 1, 2, 2, "hand")
    px(x + 2, y + 3, 6, 3, "hand2")
    px(x + 3, y + 6, 4, 7, "hand2")


def skull(x, y):
    px(x, y, 8, 5, "skull")
    px(x + 1, y + 5, 6, 2, "skull")
    px(x + 1, y + 2, 1, 1, "dark")
    px(x + 6, y + 2, 1, 1, "dark")
    px(x + 2, y + 5, 1, 1, "dark")
    px(x + 5, y + 5, 1, 1, "dark")


def candle(x, y, h=6):
    px(x + 2, y - 2, 1, 2, "flame")
    px(x + 1, y, 3, h, "candle")
    px(x, y + h, 5, 1, "stone2")


def bone(x, y):
    px(x, y, 8, 2, "bone")
    px(x - 1, y - 1, 2, 2, "bone")
    px(x - 1, y + 1, 2, 2, "bone")
    px(x + 7, y - 1, 2, 2, "bone")
    px(x + 7, y + 1, 2, 2, "bone")


def coffin(x, y):
    px(x + 2, y, 10, 3, "wood2")
    px(x + 1, y + 3, 12, 3, "wood")
    px(x, y + 6, 14, 3, "wood")
    px(x, y + 6, 14, 1, "wood2")
    px(x + 3, y + 7, 1, 1, "bone")
    px(x + 10, y + 7, 1, 1, "bone")
    px(x - 2, y + 9, 18, 2, "dark")


def spider(x):
    px(x + 4, 0, 1, 8, "line")
    px(x + 3, 8, 3, 3, "line")
    px(x + 4, 8, 1, 1, "stone2")
    px(x + 1, 9, 2, 1, "line")
    px(x + 6, 9, 2, 1, "line")
    px(x + 2, 11, 1, 1, "line")
    px(x + 5, 11, 1, 1, "line")


def roots(x, y):
    px(x, y, 2, 6, "root")
    px(x + 4, y + 3, 2, 6, "root")
    px(x + 8, y, 2, 4, "root")


def worm(x, y):
    px(x, y, 3, 1, "worm")
    px(x + 3, y + 1, 2, 1, "worm")
    px(x + 5, y, 3, 1, "worm")
    px(x + 8, y + 1, 2, 1, "worm")


# трава
for x in range(2, W, 7):
    r = (x * 13) % 7
    if r < 2:
        px(x, GRASS - 2, 2, 2, "g3" if r == 0 else "g1")
    elif r == 3:
        px(x + 1, GRASS - 3, 1, 1, "g4")

# объекты поверхности (уникальные, слева направо)
cross(14, 4)
mound(40, 10)
candle(45, 9)
slab(74, 3)
hand(108, 9)
pumpkin(134, 6)
skull(162, 11)
arch(186, 2)
candle(214, 8)
candle(221, 6, 4)
bone(240, 14)
coffin(262, 7)
hand(292, 10)
skull(302, 12)
pumpkin_small(318, 10)
spider(336)

# глубина: корни, кости, черви, камешки — тоже уникальные
bone(70, 26)
skull(150, 27)
roots(78, 20)
roots(190, 20)
roots(300, 21)
worm(250, 30)
worm(120, 32)
for x, y, w in [(30, 24, 2), (56, 30, 1), (102, 27, 2), (140, 22, 1), (205, 26, 2),
                (230, 31, 1), (268, 24, 2), (310, 29, 2), (345, 25, 1), (96, 33, 2), (285, 33, 1)]:
    R.append((x, y, w, 1, C["pebble"]))
R.append((160, 32, 14, 2, C["root"]))
R.append((174, 31, 12, 2, C["root"]))
R.append((186, 32, 16, 2, C["root"]))

out = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 36" width="1440" height="144" '
    'shape-rendering="crispEdges">',
    '<defs><linearGradient id="soilg" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#141027"/><stop offset="1" stop-color="#0b0716"/>'
    "</linearGradient></defs>",
    '<rect x="0" y="%d" width="%d" height="%d" fill="url(#soilg)"/>' % (GRASS + 4, W, H - GRASS - 4),
    '<rect x="0" y="%d" width="%d" height="2" fill="%s"/>' % (GRASS, W, C["g1"]),
    '<rect x="0" y="%d" width="%d" height="2" fill="%s"/>' % (GRASS + 2, W, C["g2"]),
]
out += ['<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % r for r in R]
out.append("</svg>")
(ROOT / "shared" / "frame" / "ground.svg").write_text("\n".join(out), encoding="utf-8")
print("ground.svg:", len(R), "rects |", (ROOT / "shared" / "frame" / "ground.svg").stat().st_size, "bytes")
