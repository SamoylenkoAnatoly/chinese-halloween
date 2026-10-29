# -*- coding: utf-8 -*-
"""Детальные пиксельные картинки-значения иероглифов для фазы «Туман».

40x40, клетка = 1 единица viewBox, рендер в shared/meanings/<char>.svg
(стиль make_characters: crispEdges, каждая группа цвета — path из квадратов).
"""
from pathlib import Path

import make_characters as mc
from make_characters import Grid

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "shared" / "meanings"
OUT.mkdir(parents=True, exist_ok=True)
mc.OUT = OUT  # Grid.render_svg пишет в mc.OUT — целим в shared/meanings

P = dict(
    N="#120b24", V="#241744", U="#3a2a5e",
    E="#2a1c4e", e="#1c1338",
    S="#f4efe2", s="#d8d1bd",
    G="#86c232", t="#5f9420",
    O="#ff8c2b", o="#c5640d",
    Y="#ffd54f", F="#ffb347",
    K="#0b0716", I="#fdfaf1",
    D="#b3a8d4",
    W="#4a7fd4", w="#35609e",
    R="#8a6a4a", r="#6e5238",
    M="#94886a", m="#6e6552",
    A="#e8709a",
)


def night(g):
    g.rect(0, 0, 40, 40, "N")
    g.rect(0, 27, 40, 13, "V")


def stars(g, pts):
    for x, y in pts:
        g.px(x, y, "I")


def moon(g, cx, cy, r=4):
    g.ellipse(cx, cy, r + 2, r + 2, "V")
    g.ellipse(cx, cy, r, r, "S")
    g.px(cx - 1, cy - 1, "s")
    g.px(cx + 1, cy + 1, "s")


def ground(g, y=35):
    g.rect(0, y, 40, 40 - y, "E")
    g.hline(0, y, 40, "e")
    for x in range(3, 38, 7):
        g.px(x, y + 2 + (x // 7) % 2, "e")


def fir(g, x, base, h=6):
    for i in range(h):
        w = min(1 + i, 7)
        g.hline(x - w // 2, base - h + i, w, "U")
    g.px(x, base - h - 1, "G")


def tri(g, cx, apex, base, col, s=2):
    for i in range(base - apex + 1):
        w = max(1, (i * s) // 2)
        g.hline(cx - w, apex + i, 2 * w + 1, col)


# ------------------------------------------------------------------ 天 небо
def art_sky():
    g = Grid(40, 40)
    g.rect(0, 0, 40, 40, "N")
    stars(g, [(4, 4), (9, 7), (14, 3), (20, 6), (25, 4), (37, 6),
              (2, 12), (17, 11), (38, 20), (7, 16), (12, 20)])
    moon(g, 31, 9, 4)
    g.hline(3, 18, 8, "U")
    g.hline(2, 19, 10, "D")
    g.hline(3, 20, 7, "U")
    g.hline(20, 23, 6, "U")
    g.hline(19, 24, 8, "D")
    g.hline(21, 25, 5, "U")
    g.rect(0, 34, 40, 6, "E")
    g.rect(2, 30, 12, 4, "V")
    g.hline(1, 29, 14, "U")
    g.px(5, 31, "Y")
    g.px(6, 31, "Y")
    g.rect(18, 31, 9, 3, "V")
    g.hline(17, 30, 11, "U")
    g.px(21, 32, "Y")
    g.rect(31, 29, 8, 5, "V")
    g.hline(30, 28, 10, "U")
    g.px(34, 31, "Y")
    ground(g, 34)
    return g, P, "Небо над двором"


# ------------------------------------------------------------------ 中 середина
def art_center():
    g = Grid(40, 40)
    night(g)
    stars(g, [(6, 5), (14, 3), (25, 6), (33, 4), (10, 10), (30, 12)])
    ground(g, 34)
    for x0 in (4, 29):
        g.rect(x0, 12, 7, 22, "R")
        g.vline(x0, 13, 21, "r")
        g.rect(x0 - 2, 9, 11, 3, "r")
        g.hline(x0 - 2, 9, 11, "R")
    for y in range(8, 33, 3):
        g.px(20, y, "U")
    g.ellipse(20, 19, 5, 5, "V")
    g.ellipse(20, 19, 3, 3, "F")
    g.px(20, 19, "Y")
    g.px(20, 15, "Y")
    g.px(20, 23, "Y")
    g.px(16, 19, "Y")
    g.px(24, 19, "Y")
    return g, P, "Звезда точно посередине"


# ------------------------------------------------------------------ 上 верх
def art_up():
    g = Grid(40, 40)
    night(g)
    stars(g, [(5, 4), (12, 7), (28, 4), (35, 8), (9, 13), (33, 15), (3, 22), (37, 21)])
    moon(g, 8, 8, 3)
    ground(g, 35)
    fir(g, 6, 35, 7)
    fir(g, 13, 35, 5)
    fir(g, 24, 35, 4)
    fir(g, 31, 35, 7)
    fir(g, 37, 35, 5)
    g.ellipse(21, 12, 5, 5, "D")
    g.rect(16, 12, 10, 5, "D")
    g.px(17, 17, "D")
    g.px(20, 17, "D")
    g.px(23, 17, "D")
    g.px(19, 11, "K")
    g.px(22, 11, "K")
    g.px(21, 3, "Y")
    g.px(21, 5, "I")
    g.px(21, 7, "I")
    g.px(20, 4, "I")
    g.px(22, 4, "I")
    return g, P, "Призрак взлетел наверх"


# ------------------------------------------------------------------ 下 низ
def art_down():
    g = Grid(40, 40)
    night(g)
    stars(g, [(5, 6), (13, 4), (27, 6), (35, 10), (9, 14), (31, 16)])
    g.rect(0, 2, 40, 3, "r")
    g.hline(0, 2, 40, "R")
    g.vline(20, 5, 15, "I")
    g.rect(18, 20, 5, 4, "K")
    g.px(19, 19, "K")
    g.px(21, 19, "K")
    for dx, dy in ((-2, -1), (-3, 1), (-2, 2), (2, -1), (3, 1), (2, 2)):
        g.px(20 + dx, 22 + dy, "K")
    g.px(20, 22, "A")
    g.rect(12, 32, 16, 6, "D")
    g.rect(13, 38, 14, 1, "K")
    g.hline(10, 32, 3, "D")
    g.hline(27, 32, 3, "D")
    g.px(14, 30, "G")
    g.px(25, 29, "G")
    g.px(20, 28, "G")
    return g, P, "Паук спускается вниз, в котёл"


# ------------------------------------------------------------------ 大 большой
def art_big():
    g = Grid(40, 40)
    night(g)
    stars(g, [(4, 4), (10, 8), (34, 5), (37, 12), (2, 16), (38, 22)])
    ground(g, 35)
    g.ellipse(20, 24, 15, 11, "o")
    g.ellipse(19, 23, 14, 10, "O")
    g.vline(13, 16, 14, "o")
    g.vline(26, 16, 14, "o")
    g.rect(19, 8, 3, 4, "R")
    g.px(18, 8, "G")
    g.rect(13, 19, 3, 2, "F")
    g.px(14, 21, "F")
    g.rect(24, 19, 3, 2, "F")
    g.px(25, 21, "F")
    g.px(14, 19, "Y")
    g.px(25, 19, "Y")
    g.hline(13, 26, 14, "F")
    g.hline(14, 27, 12, "Y")
    g.px(15, 28, "K")
    g.px(18, 28, "K")
    g.px(21, 28, "K")
    g.px(24, 28, "K")
    g.ellipse(35, 33, 3, 2, "O")
    g.px(35, 30, "R")
    return g, P, "Огромная тыква"


# ------------------------------------------------------------------ 小 маленький
def art_small():
    g = Grid(40, 40)
    night(g)
    stars(g, [(4, 4), (11, 6), (28, 4), (35, 9), (7, 14), (32, 15), (2, 22), (37, 24)])
    moon(g, 33, 7, 2)
    ground(g, 35)
    g.ellipse(18, 33, 3, 2, "O")
    g.px(18, 30, "R")
    g.px(17, 32, "o")
    g.px(26, 34, "s")
    g.px(27, 34, "s")
    g.px(27, 33, "s")
    g.px(28, 34, "K")
    g.hline(24, 35, 2, "s")
    g.px(13, 29, "G")
    g.px(23, 28, "G")
    return g, P, "Крошечная тыковка и мышка"


# ------------------------------------------------------------------ 山 гора
def art_mountain():
    g = Grid(40, 40)
    night(g)
    stars(g, [(6, 4), (14, 6), (30, 3), (36, 7), (3, 12), (22, 5), (37, 14)])
    moon(g, 32, 9, 3)
    ground(g, 35)
    tri(g, 13, 9, 35, "M")
    tri(g, 26, 16, 35, "m")
    for i in range(5):
        w = max(1, (i * 2) // 2)
        g.hline(13 - w, 9 + i, 2 * w + 1, "S")
    for i in range(4):
        w = max(1, (i * 2) // 2)
        g.hline(26 - w, 16 + i, 2 * w + 1, "S")
    for x in range(2, 38, 4):
        g.px(x, 31 + (x // 4) % 2, "D")
    fir(g, 5, 35, 6)
    fir(g, 35, 35, 6)
    fir(g, 20, 35, 4)
    return g, P, "Гора со снежной шапкой"


# ------------------------------------------------------------------ 水 вода
def art_water():
    g = Grid(40, 40)
    g.rect(0, 0, 40, 24, "N")
    stars(g, [(5, 4), (12, 7), (22, 3), (37, 6), (3, 14), (37, 16), (28, 13)])
    moon(g, 30, 8, 3)
    g.rect(0, 22, 6, 4, "E")
    g.rect(34, 22, 6, 4, "E")
    g.hline(0, 22, 6, "t")
    g.hline(34, 22, 6, "t")
    g.vline(2, 12, 10, "t")
    g.px(2, 11, "G")
    g.vline(4, 14, 8, "t")
    g.px(4, 13, "G")
    g.rect(0, 26, 40, 14, "W")
    g.hline(0, 26, 40, "w")
    for y, off in ((28, 0), (31, 3), (34, 1), (37, 4)):
        for x in range(off, 40, 6):
            g.hline(x, y, 3, "w")
    for y in range(27, 34, 2):
        g.hline(28, y, 5, "S")
        g.hline(29, y + 1, 3, "Y")
    g.px(10, 18, "G")
    g.px(18, 20, "G")
    return g, P, "Река под луной"


# ------------------------------------------------------------------ 火 огонь
def art_fire():
    g = Grid(40, 40)
    night(g)
    stars(g, [(4, 4), (11, 6), (28, 4), (36, 8), (7, 13), (33, 13)])
    ground(g, 34)
    g.rect(9, 31, 22, 3, "R")
    g.vline(9, 31, 3, "r")
    g.vline(30, 31, 3, "r")
    g.hline(11, 30, 6, "r")
    g.rect(16, 26, 9, 5, "O")
    g.rect(17, 21, 7, 5, "O")
    g.rect(18, 17, 5, 4, "O")
    g.px(20, 14, "O")
    g.px(19, 15, "O")
    g.px(21, 15, "O")
    g.rect(18, 24, 5, 5, "F")
    g.rect(19, 20, 3, 4, "F")
    g.rect(19, 25, 3, 3, "Y")
    g.px(13, 18, "Y")
    g.px(27, 16, "Y")
    g.px(24, 12, "F")
    g.px(16, 11, "F")
    g.rect(4, 31, 4, 3, "S")
    g.px(5, 32, "K")
    g.px(6, 32, "K")
    g.rect(33, 31, 3, 3, "S")
    g.px(34, 32, "K")
    return g, P, "Костёр с искрами"


# ------------------------------------------------------------------ 土 земля
def art_earth():
    g = Grid(40, 40)
    night(g)
    stars(g, [(5, 4), (13, 5), (27, 4), (35, 7), (9, 12), (31, 12)])
    ground(g, 36)
    g.ellipse(20, 36, 13, 7, "M")
    g.ellipse(20, 37, 13, 6, "m")
    g.px(10, 35, "s")
    g.px(29, 34, "s")
    g.px(24, 37, "S")
    g.vline(20, 26, 6, "t")
    g.px(18, 26, "G")
    g.px(19, 25, "G")
    g.px(21, 25, "G")
    g.px(22, 26, "G")
    g.px(13, 31, "A")
    g.px(14, 32, "A")
    g.px(15, 31, "A")
    g.px(32, 24, "G")
    return g, P, "Земляной холм с ростком"


# ------------------------------------------------------------------ 石 камень
def art_stone():
    g = Grid(40, 40)
    night(g)
    stars(g, [(6, 4), (15, 6), (24, 3), (33, 6), (3, 13), (37, 12)])
    moon(g, 7, 8, 3)
    ground(g, 34)
    g.ellipse(16, 30, 9, 6, "M")
    g.hline(11, 26, 9, "s")
    g.vline(10, 28, 3, "s")
    g.px(18, 29, "K")
    g.px(19, 30, "K")
    g.px(18, 31, "K")
    g.px(11, 25, "G")
    g.px(12, 25, "G")
    g.px(20, 25, "G")
    g.px(21, 26, "t")
    g.ellipse(30, 32, 5, 3, "m")
    g.hline(27, 31, 4, "s")
    g.px(28, 29, "G")
    g.rect(4, 32, 3, 2, "S")
    g.px(5, 32, "K")
    return g, P, "Валун с мхом"


# ------------------------------------------------------------------ 田 поле
def art_field():
    g = Grid(40, 40)
    g.rect(0, 0, 40, 10, "N")
    stars(g, [(4, 3), (12, 5), (22, 2), (31, 4)])
    moon(g, 34, 5, 2)
    for y in (10, 17, 24, 31):
        g.hline(0, y, 40, "R")
    g.vline(13, 10, 29, "R")
    g.vline(26, 10, 29, "R")
    g.rect(0, 32, 40, 6, "E")
    for x0, x1 in ((0, 13), (14, 26), (27, 40)):
        for y0 in (11, 18, 25):
            g.rect(x0 + 1, y0, x1 - x0 - 2, 6, "W")
    for px_, py_ in ((3, 13), (7, 14), (10, 12), (17, 13), (21, 14), (24, 12),
                     (30, 13), (34, 14), (37, 12), (4, 20), (8, 19), (11, 21),
                     (17, 20), (22, 19), (24, 21), (30, 20), (35, 21), (38, 19),
                     (4, 27), (8, 28), (11, 26), (18, 27), (22, 28), (31, 27), (36, 26)):
        g.px(px_, py_, "G")
    return g, P, "Рисовое поле с делянками"


# ------------------------------------------------------------------ 女 женщина
def art_woman():
    g = Grid(40, 40)
    night(g)
    stars(g, [(5, 4), (12, 6), (27, 4), (35, 8), (8, 14), (33, 15), (3, 22), (37, 24)])
    ground(g, 35)
    g.px(20, 6, "E")
    g.px(21, 6, "E")
    g.px(20, 7, "K")
    g.rect(17, 8, 7, 4, "K")
    g.rect(18, 10, 5, 3, "S")
    g.px(19, 11, "K")
    g.px(21, 11, "K")
    g.px(20, 12, "s")
    g.px(18, 12, "A")
    g.px(22, 12, "A")
    g.px(16, 8, "A")
    g.px(15, 8, "G")
    g.rect(16, 14, 9, 12, "D")
    g.rect(15, 26, 11, 8, "D")
    g.vline(20, 15, 24, "U")
    g.hline(16, 17, 9, "U")
    g.hline(15, 33, 11, "U")
    g.vline(14, 15, 7, "S")
    g.vline(25, 15, 7, "S")
    g.px(14, 22, "S")
    g.px(25, 22, "S")
    g.rect(24, 23, 3, 3, "O")
    g.px(25, 24, "Y")
    g.px(18, 34, "S")
    g.px(22, 34, "S")
    return g, P, "Женщина с фонариком"


# ------------------------------------------------------------------ 子 ребёнок
def art_child():
    g = Grid(40, 40)
    night(g)
    stars(g, [(5, 3), (12, 5), (33, 3), (37, 9), (8, 12), (35, 14), (3, 20)])
    ground(g, 35)
    g.rect(16, 10, 8, 7, "S")
    g.rect(17, 9, 6, 1, "E")
    g.px(18, 13, "K")
    g.px(22, 13, "K")
    g.px(20, 15, "s")
    g.px(17, 14, "A")
    g.px(23, 14, "A")
    g.rect(16, 18, 8, 8, "F")
    g.hline(16, 20, 8, "o")
    g.rect(17, 26, 3, 3, "U")
    g.rect(21, 26, 3, 3, "U")
    g.vline(18, 29, 5, "S")
    g.vline(22, 29, 5, "S")
    g.rect(17, 34, 3, 1, "K")
    g.rect(21, 34, 3, 1, "K")
    g.vline(25, 19, 5, "S")
    g.px(26, 20, "Y")
    g.px(27, 19, "Y")
    g.vline(27, 8, 11, "Y")
    g.ellipse(27, 6, 3, 3, "O")
    g.px(27, 3, "R")
    return g, P, "Ребёнок с шариком"


# ------------------------------------------------------------------ 马 лошадь
def art_horse():
    g = Grid(40, 40)
    night(g)
    stars(g, [(5, 4), (12, 6), (28, 4), (36, 7), (3, 14), (8, 10), (33, 12)])
    moon(g, 20, 7, 3)
    ground(g, 34)
    g.rect(7, 19, 19, 9, "R")
    g.rect(13, 19, 6, 3, "D")
    g.px(13, 22, "G")
    g.px(18, 22, "G")
    g.rect(24, 12, 5, 8, "R")
    g.rect(27, 10, 8, 5, "R")
    g.rect(33, 12, 3, 3, "S")
    g.px(28, 9, "R")
    g.px(30, 9, "R")
    g.px(30, 12, "K")
    g.px(24, 12, "K")
    g.px(24, 14, "K")
    g.px(25, 16, "K")
    g.px(24, 18, "K")
    g.px(28, 9, "K")
    g.vline(6, 20, 4, "K")
    g.px(5, 24, "K")
    g.px(5, 26, "K")
    for x0 in (9, 13, 19, 23):
        g.vline(x0, 28, 5, "R")
        g.px(x0, 33, "K")
        g.px(x0 + 1, 33, "K")
    return g, P, "Лошадь в ночи"


# ------------------------------------------------------------------ 车 повозка
def art_cart():
    g = Grid(40, 40)
    night(g)
    stars(g, [(6, 4), (14, 5), (26, 3), (34, 6), (4, 12), (36, 13)])
    ground(g, 34)
    g.ellipse(12, 30, 5, 5, "M")
    g.ellipse(12, 30, 3, 3, "N")
    g.vline(12, 26, 9, "K")
    g.hline(7, 30, 11, "K")
    g.px(12, 30, "S")
    g.ellipse(28, 30, 5, 5, "M")
    g.ellipse(28, 30, 3, 3, "N")
    g.vline(28, 26, 9, "K")
    g.hline(23, 30, 11, "K")
    g.px(28, 30, "S")
    g.rect(5, 18, 30, 8, "R")
    g.hline(5, 18, 30, "r")
    for x0 in (8, 13, 18, 23, 28, 33):
        g.vline(x0, 19, 6, "r")
    g.ellipse(12, 16, 3, 2, "O")
    g.ellipse(20, 15, 3, 2, "O")
    g.ellipse(27, 16, 2, 2, "O")
    g.rect(34, 22, 5, 2, "r")
    g.px(38, 21, "r")
    return g, P, "Повозка с тыквами"


# ------------------------------------------------------------------ 门 ворота
def art_gate():
    g = Grid(40, 40)
    night(g)
    stars(g, [(5, 3), (14, 3), (25, 3), (35, 4), (3, 9), (37, 10)])
    g.rect(2, 36, 36, 3, "E")
    g.hline(2, 36, 36, "e")
    for x0 in (7, 28):
        g.rect(x0, 12, 5, 24, "R")
        g.vline(x0, 13, 23, "r")
    g.rect(13, 14, 14, 22, "D")
    g.rect(14, 15, 5, 20, "U")
    g.rect(21, 15, 5, 20, "U")
    g.vline(20, 14, 22, "K")
    g.px(19, 25, "Y")
    g.px(21, 25, "Y")
    g.hline(14, 9, 12, "r")
    g.hline(6, 10, 28, "R")
    g.hline(4, 11, 32, "r")
    g.hline(2, 12, 36, "R")
    g.px(1, 11, "r")
    g.px(38, 11, "r")
    g.px(19, 7, "Y")
    g.px(20, 7, "Y")
    g.px(21, 7, "Y")
    g.px(20, 6, "F")
    g.vline(15, 13, 2, "K")
    g.rect(14, 15, 3, 3, "O")
    g.px(15, 16, "Y")
    g.vline(25, 13, 2, "K")
    g.rect(24, 15, 3, 3, "O")
    g.px(25, 16, "Y")
    return g, P, "Ворота с фонариками"


ART = {
    "天": art_sky,
    "中": art_center,
    "上": art_up,
    "下": art_down,
    "大": art_big,
    "小": art_small,
    "山": art_mountain,
    "水": art_water,
    "火": art_fire,
    "土": art_earth,
    "石": art_stone,
    "田": art_field,
    "女": art_woman,
    "子": art_child,
    "马": art_horse,
    "车": art_cart,
    "门": art_gate,
}

if __name__ == "__main__":
    for ch, fn in ART.items():
        g, p, desc = fn()
        g.render_svg(p, ch + ".svg", desc)
    print("done:", len(ART), "meaning arts")
