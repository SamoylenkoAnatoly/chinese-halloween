# -*- coding: utf-8 -*-
"""Пиксельные баннеры хэллоуин-рамки для iframe-шагов Stepik.

Рисует top.svg (забор с тыквами, небо, летучие мыши) и bottom.svg
(кладбищенская земля, надгробия, конфеты) в технике персонажей:
shape-rendering="crispEdges", <path> из квадратов сетки.
Сетка 240x16, показ 960x64 (клетка = 4px).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "shared" / "frame"
OUT.mkdir(parents=True, exist_ok=True)

PALETTE = {
    "N": "#120b24",  # ночь
    "P": "#241744",  # панели / тыквенные столбики
    "L": "#3a2a5e",  # контуры / перекладины
    "K": "#8a5fd6",  # фиолет Коко
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
            'width="960" height="64" shape-rendering="crispEdges" role="img" '
            'aria-label="{2}">\n{3}\n</svg>\n'
        ).format(self.w, self.h, desc, "\n".join(paths))
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


def make_top():
    g = Grid(240, 16)
    g.rect(0, 0, 240, 16, "N")
    # луна-серп
    g.ellipse(12, 5, 3.6, 3.6, "G")
    g.ellipse(14, 5, 2.6, 2.6, "N")
    # звёзды
    for x, y, c in [(30, 2, "I"), (55, 1, "D"), (90, 3, "I"), (122, 1, "G"),
                    (150, 3, "D"), (178, 2, "I"), (212, 6, "D"), (60, 6, "D"),
                    (100, 6, "D"), (140, 6, "D")]:
        g.px(x, y, c)
    # паутина в правом верхнем углу
    for i in range(8):
        g.px(239 - i, i, "D")
        g.px(239, i, "D")
        g.px(239 - i, 0, "D")
    for i in range(8):
        g.px(239 - i, 2 if i in (2, 5) else (4 if i in (4, 6) else i), "D")
    # летучие мыши
    g.bat(70, 3, "K"); g.bat(110, 2, "K"); g.bat(160, 4, "K")
    # штакетник
    for x0 in range(2, 238, 9):
        g.px(x0 + 2, 7, "K")
        g.hline(x0 + 1, 8, 3, "P")
        for y in range(9, 16):
            g.hline(x0, y, 5, "P")
    g.hline(0, 11, 240, "L"); g.hline(0, 12, 240, "L")
    g.hline(0, 14, 240, "L"); g.hline(0, 15, 240, "L")
    # тыквы на заборе
    pumpkin(g, 35); pumpkin(g, 205)
    # призрак выглядывает
    g.hline(149, 7, 2, "W"); g.hline(148, 8, 4, "W"); g.hline(148, 9, 4, "W")
    g.px(148, 8, "K"); g.px(151, 8, "K")
    g.render("top.svg", "Хэллоуинский забор с тыквами и летучими мышами")


def make_bottom():
    g = Grid(240, 16)
    g.rect(0, 0, 240, 16, "N")
    # звёзды/туман вверху
    for x, y, c in [(40, 1, "D"), (95, 2, "I"), (170, 1, "D"), (220, 2, "D")]:
        g.px(x, y, c)
    g.bat(125, 2)
    # земля
    g.hline(0, 8, 240, "E")
    g.hline(0, 9, 240, "E")
    for y in range(10, 16):
        g.hline(0, y, 240, "e" if y >= 12 else "E")
    for x in range(4, 238, 13):
        g.px(x, 9 + (x // 13) % 4, "e")
        g.px(x + 5, 11 + (x // 13) % 3, "e")
    # надгробие 1
    g.hline(29, 3, 3, "L")
    for y in range(4, 8):
        g.hline(27, y, 7, "P")
    g.hline(29, 3, 3, "L")
    g.px(27, 4, "L"); g.px(33, 4, "L")
    for y in range(5, 8):
        g.px(27, y, "L"); g.px(33, y, "L")
    g.px(30, 4, "L"); g.hline(29, 5, 3, "L")
    g.hline(26, 8, 9, "L")
    # надгробие 2 (шире)
    g.hline(148, 3, 5, "L")
    for y in range(4, 8):
        g.hline(146, y, 9, "P")
    g.px(150, 2, "L"); g.px(148, 3, "L"); g.px(152, 3, "L")
    for y in range(4, 8):
        g.px(146, y, "L"); g.px(154, y, "L")
    g.px(149, 5, "L"); g.px(151, 5, "L")
    g.hline(145, 8, 11, "L")
    # конфеты на земле
    g.px(68, 6, "I"); g.hline(69, 6, 3, "R"); g.px(70, 6, "G"); g.px(72, 6, "I")
    g.hline(69, 7, 3, "R")
    g.px(183, 6, "I"); g.hline(184, 6, 3, "O"); g.px(185, 6, "G"); g.px(187, 6, "I")
    # чупа-чупс
    g.vline(110, 6, 2, "I")
    g.hline(109, 4, 3, "R"); g.hline(109, 5, 3, "R"); g.px(110, 5, "G")
    # косточка
    g.hline(128, 6, 5, "I")
    g.px(127, 5, "I"); g.px(133, 5, "I"); g.px(127, 7, "I"); g.px(133, 7, "I")
    # тыквочка
    pumpkin(g, 215, top_y=4)
    # травинки
    for x in (45, 90, 120, 165, 200):
        g.px(x, 7, "E"); g.px(x + 1, 7, "E"); g.px(x, 6, "E")
    # туман у земли
    for x in range(50, 56):
        g.px(x, 7, "D")
    for x in range(96, 102):
        g.px(x, 7, "D")
    for x in range(172, 178):
        g.px(x, 7, "D")
    g.render("bottom.svg", "Кладбищенская земля с надгробиями и конфетами")


if __name__ == "__main__":
    make_top()
    make_bottom()
