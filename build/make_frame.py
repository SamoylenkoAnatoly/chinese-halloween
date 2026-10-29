# -*- coding: utf-8 -*-
"""Хэллоуинские ВОРОТА для iframe-шагов Stepik (во всю ширину).

top.svg (240x28 -> 960x112): балка с кованым заборчиком, тотемы-тыквы
на тёмных столбах по краям, серп луны, звёзды, мыши, паук на нити.
bottom.svg (240x13 -> 960x52): балка с заборчиком вниз, трава, тыквы.
iframe во всю ширину между ними (см. frame_step в publish_stepik.py),
клетка = 4px.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "shared" / "frame"
OUT.mkdir(parents=True, exist_ok=True)

PALETTE = {
    "N": "#120b24",  # ночь
    "P": "#241744",  # панели / камень-тень
    "L": "#3a2a5e",  # камень / контуры
    "B": "#1a1033",  # тело столба (как в примере)
    "K": "#8a5fd6",  # фиолет Коко (ковка)
    "O": "#ff8c2b",  # тыква
    "G": "#ffd54f",  # золото
    "I": "#efe9dc",  # светлая кость
    "D": "#b3a8d4",  # туман
    "W": "#bfe8e0",  # призрак
    "E": "#86c232",  # трава
    "e": "#4f7a1e",  # трава тень
    "R": "#e64533",  # конфета / глаза паука
}


class Grid:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.c = [[None] * w for _ in range(h)]

    def px(self, x, y, col):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.c[y][x] = PALETTE.get(col, col)

    def get(self, x, y):
        return self.c[y][x]

    def rect(self, x, y, w, h, col):
        for j in range(y, y + h):
            for i in range(x, x + w):
                self.px(i, j, col)

    def hline(self, x, y, w, col):
        self.rect(x, y, w, 1, col)

    def vline(self, x, y, h, col):
        self.rect(x, y, 1, h, col)

    def ellipse(self, cx, cy, rx, ry, col):
        for j in range(self.h):
            for i in range(self.w):
                if ((i - cx) / rx) ** 2 + ((j - cy) / ry) ** 2 <= 1.05:
                    self.px(i, j, col)

    def bat(self, x, y, col="P"):
        self.px(x - 2, y, col); self.px(x - 1, y - 1, col)
        self.px(x, y, col); self.px(x, y + 1, col)
        self.px(x + 1, y - 1, col); self.px(x + 2, y, col)

    def blit(self, pixels, x0, y0, s=1):
        for (px, py, col) in pixels:
            if s == 1:
                self.px(x0 + px, y0 + py, col)
            else:
                self.rect(x0 + px * s, y0 + py * s, s, s, col)

    def render(self, name, desc):
        paths = []
        for hexcol in sorted({v for row in self.c for v in row if v}):
            cells = []
            for j in range(self.h):
                run = None
                for i in range(self.w + 1):
                    cur = i if i < self.w and self.c[j][i] == hexcol else None
                    if cur != run:
                        if run is not None:
                            cells.append("M{0} {1}h{2}v1h-{2}z".format(run, j, i - run))
                        run = cur
            if cells:
                paths.append('<path fill="{0}" d="{1}"/>'.format(hexcol, "".join(cells)))
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {0} {1}" '
            'width="{2}" height="{3}" shape-rendering="crispEdges" role="img" '
            'aria-label="{4}">\n{5}\n</svg>\n'
        ).format(self.w, self.h, self.w * 4, self.h * 4, desc, "\n".join(paths))
        (OUT / name).write_text(svg, encoding="utf-8")
        print(name, "OK", self.w, "x", self.h, "->", self.w * 4, "x", self.h * 4, len(svg), "bytes")


def pumpkin(g, cx, top_y=5):
    g.px(cx, top_y - 2, "E"); g.px(cx, top_y - 1, "E")
    g.hline(cx - 1, top_y, 3, "O")
    g.hline(cx - 3, top_y + 1, 7, "O")
    g.hline(cx - 3, top_y + 2, 7, "O")
    g.hline(cx - 2, top_y + 3, 5, "O")
    g.hline(cx - 1, top_y + 4, 3, "O")
    g.px(cx - 2, top_y + 1, "G"); g.px(cx + 2, top_y + 1, "G")
    g.hline(cx - 2, top_y + 2, 5, "G")
    g.px(cx - 3, top_y + 1, "R"); g.px(cx + 3, top_y + 2, "R")


def pumpkin_totem(g, cx, top=0):
    """Большая тыква-тотем (13 клеток шириной) для столбов и краёв балки."""
    g.px(cx, top, "E"); g.px(cx, top + 1, "E")
    g.hline(cx - 2, top + 2, 5, "O")
    g.hline(cx - 4, top + 3, 9, "O")
    for y in range(top + 4, top + 9):
        g.hline(cx - 6, y, 13, "O")
    g.hline(cx - 4, top + 9, 9, "O")
    g.hline(cx - 2, top + 10, 5, "O")
    g.px(cx - 6, top + 5, "R"); g.px(cx + 6, top + 6, "R")
    g.px(cx - 5, top + 7, "R"); g.px(cx + 5, top + 8, "R")
    g.px(cx - 4, top + 5, "G"); g.px(cx - 3, top + 5, "G")
    g.px(cx + 3, top + 5, "G"); g.px(cx + 4, top + 5, "G")
    g.px(cx, top + 6, "G")
    g.hline(cx - 4, top + 8, 9, "G")
    g.px(cx - 2, top + 8, "O"); g.px(cx + 2, top + 8, "O")


def brick(g, x0, y0, w, h, off=0):
    """Кладка: швы P каждые 6 рядов, вертикальные вразбежку."""
    for y in range(y0 + 5, y0 + h, 6):
        g.hline(x0, y, w, "P")
    c = 0
    for y0c in range(y0, y0 + h, 6):
        yend = min(y0c + 5, y0 + h)
        o = (5 if c % 2 == 0 else 2) + off
        for x in range(x0 + o, x0 + w, 6):
            if x0 < x < x0 + w - 1:
                for y in range(y0c, yend):
                    g.px(x, y, "P")
        c += 1


def fence_up(g, x0, x1, y_base):
    """Кованый заборчик: прутья с наконечниками вверх + перекладина."""
    for x in range(x0 + 3, x1 - 2, 6):
        g.vline(x, y_base - 5, 5, "K")
        g.px(x, y_base - 6, "K")
        g.px(x - 1, y_base - 5, "K"); g.px(x + 1, y_base - 5, "K")
    g.hline(x0, y_base - 3, x1 - x0, "K")


def fence_down(g, x0, x1, y_top):
    """Кованый заборчик остриём вниз (для bottom)."""
    for x in range(x0 + 3, x1 - 2, 6):
        g.vline(x, y_top, 5, "K")
        g.px(x, y_top + 5, "K")
        g.px(x - 1, y_top + 4, "K"); g.px(x + 1, y_top + 4, "K")
    g.hline(x0, y_top + 2, x1 - x0, "K")


def spider_on_thread(g, x, y0, ln, body="P"):
    for y in range(y0, y0 + ln):
        g.px(x, y, "D")
    y = y0 + ln
    g.hline(x - 1, y, 3, body)
    g.hline(x - 1, y + 1, 3, body)
    g.px(x, y + 2, body)
    g.px(x - 1, y, "R"); g.px(x + 1, y, "R")
    g.px(x - 2, y + 1, "D"); g.px(x + 2, y + 1, "D")


def make_top():
    g = Grid(240, 28)
    g.rect(0, 0, 240, 28, "N")
    for x, y, c in [(30, 2, "I"), (55, 5, "D"), (80, 2, "G"), (105, 4, "D"),
                    (130, 2, "I"), (155, 5, "D"), (180, 3, "I"), (60, 9, "D"),
                    (100, 8, "D"), (140, 9, "D"), (175, 8, "I"), (205, 9, "D")]:
        g.px(x, y, c)
    g.ellipse(200, 6, 3.2, 3.2, "G")
    g.ellipse(202, 6, 2.3, 2.3, "N")
    g.bat(58, 6, "K"); g.bat(168, 4, "K")
    g.rect(0, 0, 20, 28, "B")
    g.rect(220, 0, 20, 28, "B")
    brick(g, 0, 13, 20, 15, off=0)
    brick(g, 220, 13, 20, 15, off=2)
    g.vline(19, 13, 15, "L")
    g.vline(220, 13, 15, "L")
    g.hline(0, 13, 20, "L"); g.hline(220, 13, 20, "L")
    pumpkin_totem(g, 10, 0)
    pumpkin_totem(g, 230, 0)
    g.rect(20, 16, 200, 12, "L")
    brick(g, 20, 16, 200, 12)
    g.hline(20, 16, 200, "P")
    fence_up(g, 20, 220, 16)
    spider_on_thread(g, 120, 14, 8)
    g.render("top.svg", "Ворота двора: балка с кованой оградой, тотемы-тыквы, луна и паук")


def make_bottom():
    g = Grid(240, 13)
    g.rect(0, 0, 240, 13, "N")
    g.rect(0, 0, 240, 8, "L")
    brick(g, 0, 0, 240, 8)
    g.hline(0, 0, 240, "P")
    g.rect(0, 0, 20, 8, "B")
    g.rect(220, 0, 20, 8, "B")
    brick(g, 0, 0, 20, 8, off=1)
    brick(g, 220, 0, 20, 8, off=3)
    g.hline(0, 7, 240, "P")
    fence_down(g, 20, 220, 8)
    g.hline(0, 11, 240, "E")
    g.hline(0, 12, 240, "e")
    for x in range(24, 216, 9):
        g.px(x, 10, "E"); g.px(x + 1, 10, "E"); g.px(x, 11, "E")
        g.px(x + 4, 12, "e")
    pumpkin(g, 32, 5)
    pumpkin(g, 208, 5)
    g.px(70, 10, "I"); g.px(71, 10, "R"); g.px(72, 10, "I")
    g.px(170, 10, "I"); g.px(171, 10, "G"); g.px(172, 10, "I")
    for x in range(96, 102):
        g.px(x, 10, "D")
    for x in range(140, 146):
        g.px(x, 10, "D")
    g.render("bottom.svg", "Порог ворот: балка с оградой вниз, трава и тыквы")


if __name__ == "__main__":
    make_top()
    make_bottom()
