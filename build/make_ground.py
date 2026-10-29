# -*- coding: utf-8 -*-
"""Тайл «кладбищенская земля» 240x36 -> shared/frame/ground.svg (repeat-x внизу уроков)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W, H = 240, 36
GRASS = 16

P = {
    "g1": "#3f7a1e", "g2": "#2c5a14", "g3": "#4f9a28",
    "soil": "#141027", "dark": "#0b0716",
    "stone": "#514e73", "stone2": "#3a3757",
    "bone": "#c9c2a4", "skull": "#e8e2c4",
    "pump": "#ff8c2b", "pump2": "#d96a12",
    "hand": "#86c232", "hand2": "#4f7a1e",
    "flame": "#ffd54f", "candle": "#efe9dc",
}

R = []


def px(x, y, w, h, c):
    R.append((int(x), int(y), int(w), int(h), P[c]))


def hand(x, y):
    px(x + 1, y, 2, 3, "hand")
    px(x + 4, y - 1, 2, 4, "hand")
    px(x + 7, y + 1, 2, 2, "hand")
    px(x + 2, y + 3, 6, 3, "hand2")
    px(x + 3, y + 6, 4, 8, "hand2")


def skull(x, y):
    px(x, y, 8, 5, "skull")
    px(x + 1, y + 5, 6, 2, "skull")
    px(x + 1, y + 2, 1, 1, "dark")
    px(x + 6, y + 2, 1, 1, "dark")
    px(x + 2, y + 5, 1, 1, "dark")
    px(x + 5, y + 5, 1, 1, "dark")


def pumpkin(x, y):
    px(x + 3, y, 2, 2, "g3")
    px(x, y + 2, 10, 6, "pump")
    px(x + 2, y + 4, 1, 3, "pump2")
    px(x + 7, y + 4, 1, 3, "pump2")
    px(x + 2, y + 3, 2, 2, "dark")
    px(x + 6, y + 3, 2, 2, "dark")
    px(x + 3, y + 6, 4, 1, "dark")


def cross(x, y):
    px(x + 3, y, 2, 12, "stone")
    px(x, y + 3, 8, 2, "stone")
    px(x + 3, y, 1, 12, "stone2")


def slab(x, y):
    px(x + 2, y, 8, 2, "stone")
    px(x + 1, y + 2, 10, 1, "stone")
    px(x, y + 3, 12, 9, "stone")
    px(x + 3, y + 5, 6, 1, "stone2")
    px(x, y + 12, 14, 2, "stone2")


def candle(x, y):
    px(x + 2, y - 2, 1, 2, "flame")
    px(x + 1, y, 3, 6, "candle")
    px(x, y + 6, 5, 1, "stone2")


def bone(x, y):
    px(x, y, 8, 2, "bone")
    px(x - 1, y - 1, 2, 2, "bone")
    px(x - 1, y + 1, 2, 2, "bone")
    px(x + 7, y - 1, 2, 2, "bone")
    px(x + 7, y + 1, 2, 2, "bone")


px(0, GRASS, W, H - GRASS, "soil")
px(0, GRASS, W, 2, "g1")
px(0, GRASS + 2, W, 2, "g2")
for x in range(0, W, 4):
    if (x // 4) % 3:
        px(x, GRASS - 2, 2, 2, "g1")
    if (x // 4) % 4 == 1:
        px(x + 2, GRASS - 4, 2, 2, "g3")
for x in range(10, W - 10, 23):
    px(x, GRASS + 7 + x % 6, 2, 2, "g2")

cross(34, GRASS - 12)
slab(58, GRASS - 12)
skull(96, GRASS - 4)
bone(88, GRASS + 8)
pumpkin(118, GRASS - 7)
hand(148, GRASS - 4)
skull(176, GRASS - 2)
candle(196, GRASS - 6)
hand(212, GRASS - 6)

out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 36" width="960" height="144" shape-rendering="crispEdges">']
out += ['<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % r for r in R]
out.append("</svg>")
(ROOT / "shared" / "frame" / "ground.svg").write_text("\n".join(out), encoding="utf-8")
print("ground.svg rects:", len(R))
