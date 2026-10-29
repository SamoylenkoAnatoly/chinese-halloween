# -*- coding: utf-8 -*-
"""Пиксельные хэллоуинские ВОРОТА для iframe-шагов Stepik.

top.svg (240x44 -> 960x176): каменные столбы с тыквами-фонарями,
кованая арка с шипами, серп луны, летучие мыши, призрак, фонарь.
bottom.svg (240x20 -> 960x80): постаменты столбов, земля, надгробия, конфеты.
Боковые створки ворот — border-left/right 32px цвета L в frame_step
(publish_stepik.py), клетка = 4px.
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "shared" / "frame"
OUT.mkdir(parents=True, exist_ok=True)

PALETTE = {
    "N": "#120b24",  # ночь
    "P": "#241744",  # панели / камень-тень
    "L": "#3a2a5e",  # камень / контуры
    "K": "#8a5fd6",  # фиолет Коко (ковка)
    "O": "#ff8c2b",  # тыква
    "G": "#ffd54f",  # золото
    "I": "#efe9dc",  # светлая кость
    "D": "#b3a8d4",  # туман
    "W": "#bfe8e0",  # призрак
    "E": "#86c232",  # трава
    "e": "#4f7a1e",  # трава тень
    "R": "#e64533",  # конфета
}


class Grid:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.c = [[None] * w for _ in range(h)]

    def px(self, x, y, col):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.c[y][x] = col

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
        # 5x3: крылья вверх
        self.px(x - 2, y, col); self.px(x - 1, y - 1, col)
        self.px(x, y, col); self.px(x, y + 1, col)
        self.px(x + 1, y - 1, col); self.px(x + 2, y, col)

    def render(self, name, desc):
        paths = []
        for key, hexcol in PALETTE.items():
            cells = []
            for j in range(self.h):
                run = None
                for i in range(self.w + 1):
                    cur = key if i < self.w and self.c[j][i] == key else None
                    if cur != run:
                        if run:
                            cells.append("M{0} {1}h{2}v1h-{2}z".format(run, j, i - run))
                        run = i if cur else None
            if cells:
                paths.append('<path fill="{0}" d="{1}"/>'.format(hexcol, "".join(cells)))
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {0} {1}" '
            'width="{2}" height="{3}" shape-rendering="crispEdges" role="img" '
            'aria-label="{4}">\n{5}\n</svg>\n'
        ).format(self.w, self.h, self.w * 4, self.h * 4, desc, "\n".join(paths))
        (OUT / name).write_text(svg, encoding="utf-8")
        print(name, "OK", self.w, "x", self.h, len(svg), "bytes")


def pumpkin(g, cx, top_y=5):
    g.px(cx, top_y - 2, "E"); g.px(cx, top_y - 1, "E")          # хвостик
    g.hline(cx - 1, top_y, 3, "O")
    g.hline(cx - 3, top_y + 1, 7, "O")
    g.hline(cx - 3, top_y + 2, 7, "O")
    g.hline(cx - 2, top_y + 3, 5, "O")
    g.hline(cx - 1, top_y + 4, 3, "O")
    g.px(cx - 2, top_y + 1, "G"); g.px(cx + 2, top_y + 1, "G")  # глаза
    g.hline(cx - 2, top_y + 2, 5, "G")                          # ухмылка
    g.px(cx - 3, top_y + 1, "R"); g.px(cx + 3, top_y + 2, "R")  # бока


def brick(g, x0, y0, w, h):
    # каменная кладка: горизонтальные швы P каждые 6 рядов, вертикальные вразбежку
    for y in range(y0 + 5, y0 + h, 6):
        g.hline(x0, y, w, "P")
    c = 0
    for y0c in range(y0, y0 + h, 6):
        yend = min(y0c + 5, y0 + h)
        off = 5 if c % 2 == 0 else 2
        for x in range(x0 + off, x0 + w, 6):
            if x0 < x < x0 + w - 1:
                for y in range(y0c, yend):
                    g.px(x, y, "P")
        c += 1


def pillar(g, x0, w=10):
    pumpkin(g, x0 + w // 2, top_y=2)      # тыква-фонарь на макушке
    g.hline(x0, 7, w, "L")                # капитель
    g.hline(x0, 8, w, "P")
    g.rect(x0, 9, w, 35, "L")             # ствол до низа баннера
    brick(g, x0, 9, w, 35)


def arch_ring(g, cx, cy, rx, ry, col="K"):
    # кольцо-арка толщиной ~3 клетки
    for j in range(g.h):
        for i in range(g.w):
            o = ((i - cx) / rx) ** 2 + ((j - cy) / ry) ** 2
            inn = ((i - cx) / (rx - 3)) ** 2 + ((j - cy) / (ry - 3)) ** 2
            if o <= 1.0 and inn >= 1.0:
                g.px(i, j, col)


def spikes(g, cx, cy, rx, ry, col="K", n=9):
    # шипы по нормали к арке
    for k in range(n):
        th = math.pi * (k + 0.5) / n
        ex, ey = rx * math.cos(th), -ry * math.sin(th)
        x, y = cx + ex, cy + ey
        nx, ny = ex / rx ** 2, ey / ry ** 2
        ln = math.hypot(nx, ny) or 1.0
        nx, ny = nx / ln, ny / ln
        for s in (1, 2):
            g.px(int(round(x + nx * s)), int(round(y + ny * s)), col)


def make_top():
    g = Grid(240, 44)
    g.rect(0, 0, 240, 44, "N")
    # серп луны (слева от арки, над ней)
    g.ellipse(40, 7, 3.6, 3.6, "G")
    g.ellipse(42, 7, 2.6, 2.6, "N")
    # звёзды
    for x, y, c in [(26, 3, "I"), (70, 3, "D"), (95, 2, "I"), (140, 2, "G"),
                    (165, 4, "D"), (205, 3, "I"), (120, 3, "D"), (85, 4, "D"),
                    (175, 8, "D"), (60, 10, "D"), (200, 16, "I"), (150, 20, "D"),
                    (100, 22, "D"), (30, 30, "D"), (210, 28, "D")]:
        g.px(x, y, c)
    # летучие мыши в проёме и у арки
    g.bat(100, 13, "K"); g.bat(150, 17, "K"); g.bat(75, 21, "K")
    # кованая арка-полукруг с шипами между столбами
    arch_ring(g, 120, 44, 110, 38, "K")
    spikes(g, 120, 44, 110, 38, "K", 9)
    # фонарь на нити из вершины арки
    for y in range(10, 14):
        g.px(120, y, "D")
    g.hline(118, 14, 5, "O")
    g.hline(118, 15, 5, "O")
    g.hline(119, 16, 3, "O")
    g.px(120, 15, "G")
    # паук на нити из арки
    for y in range(11, 16):
        g.px(90, y, "D")
    g.px(90, 16, "P"); g.px(89, 17, "P"); g.px(91, 17, "P")
    g.px(90, 17, "P"); g.px(90, 18, "P")
    # призрак выглядывает в проёме
    g.hline(18, 37, 2, "W")
    g.hline(17, 38, 4, "W")
    g.hline(17, 39, 4, "W")
    g.hline(17, 40, 4, "W")
    g.px(18, 38, "K"); g.px(20, 38, "K")
    # каменные столбы с тыквами
    pillar(g, 0)
    pillar(g, 230)
    g.render("top.svg", "Хэллоуинские ворота: каменные столбы, тыквы-фонари, кованая арка с шипами")


def make_bottom():
    g = Grid(240, 20)
    g.rect(0, 0, 240, 20, "N")
    # звёзды/туман вверху
    for x, y, c in [(40, 1, "D"), (95, 2, "I"), (170, 1, "D"), (220, 2, "D"), (60, 3, "D")]:
        g.px(x, y, c)
    g.bat(125, 2)
    # земля
    g.hline(0, 12, 240, "E")
    g.hline(0, 13, 240, "E")
    for y in range(14, 20):
        g.hline(0, y, 240, "e" if y >= 16 else "E")
    for x in range(4, 230, 13):
        g.px(x, 13 + (x // 13) % 4, "e")
        g.px(x + 5, 15 + (x // 13) % 3, "e")
    # постаменты столбов
    for x0 in (0, 230):
        g.rect(x0, 0, 10, 3, "L")            # низ ствола
        g.hline(x0, 1, 10, "P")
        g.rect(x0, 3, 10, 9, "L")            # постамент до земли
        g.hline(x0, 3, 10, "P")
        g.vline(x0, 4, 7, "P")
        g.vline(x0 + 9, 4, 7, "P")
        g.hline(x0, 11, 10, "P")
    # надгробие 1
    g.hline(29, 5, 3, "L")
    for y in range(6, 10):
        g.hline(27, y, 7, "P")
    g.px(27, 6, "L"); g.px(33, 6, "L")
    for y in range(7, 10):
        g.px(27, y, "L"); g.px(33, y, "L")
    g.px(30, 6, "L"); g.hline(29, 7, 3, "L")
    g.hline(26, 10, 9, "L")
    # надгробие 2 (шире)
    g.hline(148, 5, 5, "L")
    for y in range(6, 10):
        g.hline(146, y, 9, "P")
    g.px(150, 4, "L"); g.px(148, 5, "L"); g.px(152, 5, "L")
    for y in range(6, 10):
        g.px(146, y, "L"); g.px(154, y, "L")
    g.px(149, 7, "L"); g.px(151, 7, "L")
    g.hline(145, 10, 11, "L")
    # конфеты на земле
    g.px(68, 10, "I"); g.hline(69, 10, 3, "R"); g.px(70, 10, "G"); g.px(72, 10, "I")
    g.hline(69, 11, 3, "R")
    g.px(183, 10, "I"); g.hline(184, 10, 3, "O"); g.px(185, 10, "G"); g.px(187, 10, "I")
    # чупа-чупс
    g.hline(109, 7, 3, "R"); g.hline(109, 8, 3, "R"); g.px(110, 8, "G")
    g.vline(110, 9, 3, "I")
    # косточка
    g.hline(128, 10, 5, "I")
    g.px(127, 9, "I"); g.px(133, 9, "I"); g.px(127, 11, "I"); g.px(133, 11, "I")
    # тыквочка
    pumpkin(g, 215, top_y=8)
    # травинки
    for x in (45, 90, 120, 165, 200):
        g.px(x, 11, "E"); g.px(x + 1, 11, "E"); g.px(x, 10, "E")
    # туман у земли
    for x in range(50, 56):
        g.px(x, 11, "D")
    for x in range(96, 102):
        g.px(x, 11, "D")
    for x in range(172, 178):
        g.px(x, 11, "D")
    g.render("bottom.svg", "Основания ворот, кладбищенская земля с надгробиями и конфетами")


if __name__ == "__main__":
    make_top()
    make_bottom()
