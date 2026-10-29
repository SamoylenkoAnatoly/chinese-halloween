# -*- coding: utf-8 -*-
"""Детальные пиксельные сцены истории «Чих Магистра Коко».

scene1..6.svg (240x90 -> 960x360, клетка 4px): окружение рисуется вручную,
персонажи блитятся из shared/characters/*.svg (парсинг пиксельных путей).
"""
import re
from pathlib import Path

import make_frame
from make_frame import Grid, spider_on_thread

ROOT = Path(__file__).resolve().parent.parent
CHAR_DIR = ROOT / "shared" / "characters"
OUT = ROOT / "shared" / "story"
OUT.mkdir(parents=True, exist_ok=True)
make_frame.OUT = OUT  # Grid.render пишет в make_frame.OUT — целим в shared/story

INK = "#efe9dc"
POT = "#0d081a"
WOOD = "#5c3a80"
WOOD_D = "#4a2f66"
PATH_RE = re.compile(r'<path fill="(#[0-9A-Fa-f]+)" d="([^"]+)"')
PX_RE = re.compile(r"M(\d+) (\d+)h1v1h-1z")
SPRITES = {}


def load_sprite(name):
    if name not in SPRITES:
        txt = (CHAR_DIR / name).read_text(encoding="utf-8")
        px = []
        for m in PATH_RE.finditer(txt):
            col = m.group(1).lower()
            for pm in PX_RE.finditer(m.group(2)):
                px.append((int(pm.group(1)), int(pm.group(2)), col))
        SPRITES[name] = px
    return SPRITES[name]


def blit(g, name, x0, y0, s=3):
    g.blit(load_sprite(name), x0, y0, s)


def stars(g, pts):
    for x, y, c in pts:
        g.px(x, y, c)


def fog(g, y, spans):
    for x0, x1 in spans:
        for x in range(x0, x1, 4):
            g.px(x, y + (x // 4) % 2, "D")


def grave(g, cx, base, w, tilt=0):
    h = w // 2 + 6
    top = base - h
    g.hline(cx - w // 4 + tilt, top, w // 2, "P")
    g.hline(cx - w // 2 + 1 + tilt, top + 1, w - 2, "P")
    g.hline(cx - w // 2 + tilt, top + 2, w, "P")
    for y in range(top + 3, base):
        g.hline(cx - w // 2 + tilt, y, w, "P")
    g.vline(cx - w // 2 + tilt, top + 2, h - 2, "L")
    g.vline(cx + w // 2 - 1 + tilt, top + 2, h - 2, "L")
    g.hline(cx - w // 2 + tilt, base - 1, w, "L")
    g.px(cx - 2, top + 5, "K"); g.px(cx + 1, top + 5, "K")
    g.hline(cx - 3, top + 8, 6, "K")
    g.hline(cx - w // 2 - 2, base, w + 4, "e")
    g.hline(cx - w // 2 - 2, base + 1, w + 4, "e")


def ground(g, y0=66):
    g.rect(0, y0, 240, 90 - y0, "E")
    g.hline(0, y0, 240, "E")
    g.hline(0, 90 - 3, 240, "e")
    g.hline(0, 90 - 1, 240, "e")
    for x in range(6, 234, 11):
        g.px(x, y0 + 2 + (x // 11) % 3, "e")
        g.px(x + 5, y0 + 5 + (x // 13) % 3, "e")


def lantern(g, cx, top, lit=True):
    body = "R" if lit else "L"
    g.hline(cx - 2, top, 5, "L")
    for y in range(top + 1, top + 7):
        g.hline(cx - 4, y, 9, body)
    g.px(cx - 3, top + 1, "K"); g.px(cx + 3, top + 5, "K")
    g.px(cx + 3, top + 1, "K"); g.px(cx - 3, top + 5, "K")
    if lit:
        g.rect(cx - 1, top + 3, 3, 2, "G")
    g.hline(cx - 1, top + 7, 3, "L")
    g.vline(cx, top + 8, 2, "G")


def flame(g, cx, y):
    g.px(cx, y - 2, "G")
    g.hline(cx - 1, y - 1, 3, "O")
    g.hline(cx - 2, y, 5, "O")
    g.hline(cx - 1, y + 1, 3, "R")


def cauldron(g, cx, ytop, splash=False):
    g.hline(cx - 20, ytop, 41, "L")
    g.hline(cx - 19, ytop + 1, 39, "E")
    g.rect(cx - 18, ytop + 2, 37, 14, POT)
    g.rect(cx - 19, ytop + 4, 39, 10, POT)
    g.hline(cx - 18, ytop + 16, 37, "L")
    g.hline(cx - 16, ytop + 17, 33, "L")
    for k, dx in enumerate((-12, 0, 12)):
        flame(g, cx + dx, ytop + 19)
    g.hline(cx - 15, ytop + 20, 31, "e")
    if splash:
        for x, y, c in [(-22, -6, "E"), (-26, -12, "E"), (-18, -14, "G"),
                        (-10, -18, "E"), (-2, -22, "E"), (6, -16, "G"),
                        (14, -12, "E"), (20, -8, "E"), (-14, -9, "E"), (10, -20, "E")]:
            g.px(cx + x, ytop + y, c)
    else:
        for x, y in ((-10, -4), (-3, -7), (4, -5), (11, -3)):
            g.px(cx + x, ytop + y, "E")
            g.px(cx + x + 1, ytop + y - 1, "D")


def shelf(g, x0, y):
    g.hline(x0, y, 48, "L")
    g.hline(x0, y + 1, 48, "P")
    for k, (bx, c) in enumerate(((2, "G"), (8, "R"), (14, "E"), (21, "K"), (27, "O"), (34, "D"))):
        bw = 4 if k % 2 == 0 else 3
        g.rect(x0 + bx, y - 6, bw, 6, c)
        g.px(x0 + bx + bw // 2, y - 7, "D")
    g.hline(x0, y + 12, 32, "L")
    g.hline(x0, y + 13, 32, "P")
    for bx, bw, c in ((2, 10, "I"), (13, 8, "K"), (22, 9, "P")):
        g.rect(x0 + bx, y + 6, bw, 6, c)
        g.hline(x0 + bx, y + 8, bw, "L")


def web(g, x0, y0, n=9):
    for k in range(n):
        g.px(x0 + k, y0 + k, "D")
        g.px(x0 + k // 2, y0 + k, "D")
        g.px(x0 + k, y0 + k // 2, "D")
    for k in range(3, n, 3):
        g.px(x0 + k, y0 + k - 1, "D")
        g.px(x0 + k - 1, y0 + k, "D")


def window(g, x0, y0, w=40, h=22, open_shutter=True):
    g.rect(x0 - 2, y0 - 2, w + 4, h + 4, "L")
    g.rect(x0, y0, w, h, "N")
    g.vline(x0 + w // 2, y0, h, "L")
    g.hline(x0, y0 + h // 2, w, "L")
    if open_shutter:
        g.rect(x0 + w + 2, y0 - 2, 6, h + 4, "P")
        for y in range(y0, y0 + h, 4):
            g.px(x0 + w + 4, y, "L")
    else:
        g.rect(x0 - 8, y0 - 2, 6, h + 4, "P")
    stars(g, [(x0 + 6, y0 + 4, "I"), (x0 + 30, y0 + 6, "D"), (x0 + 16, y0 + 12, "I")])


def book_stand(g, x0, y):
    g.rect(x0, y, 24, 3, "L")
    g.vline(x0 + 3, y + 3, 8, "L")
    g.vline(x0 + 20, y + 3, 8, "L")
    g.rect(x0 + 2, y - 7, 20, 7, "I")
    g.vline(x0 + 12, y - 7, 7, "L")
    for yy in (y - 5, y - 3):
        g.hline(x0 + 4, yy, 6, "K")
        g.hline(x0 + 14, yy, 6, "K")


def waves(g, x, y, col="K"):
    for r, ln in ((0, 3), (3, 5), (6, 7)):
        for k in range(ln):
            g.px(x - r, y - ln // 2 + k, col)
    for r in (2, 5, 8):
        g.px(x - r, y, col)


def scene1():
    g = Grid(240, 90)
    g.rect(0, 0, 240, 68, "P")
    for y in (12, 24, 36, 48, 60):
        g.hline(0, y, 240, "L")
        for x in range(30 if (y // 12) % 2 else 60, 240, 60):
            g.vline(x, y - 12, 12, "L")
    g.rect(0, 68, 240, 22, WOOD)
    g.hline(0, 68, 240, WOOD_D)
    g.hline(0, 76, 240, WOOD_D)
    g.hline(0, 84, 240, WOOD_D)
    for x in range(20, 240, 40):
        g.px(x, 72, WOOD_D); g.px(x + 20, 80, WOOD_D)
    web(g, 1, 1, 12)
    web(g, 228, 1, 9)
    shelf(g, 16, 26)
    window(g, 168, 14, 52, 22, open_shutter=True)
    g.ellipse(180, 24, 3, 3, "G")
    g.ellipse(182, 24, 2.2, 2.2, "N")
    blit(g, "bat.svg", 184, 20, 1)
    g.hline(166, 37, 60, "L")
    g.hline(166, 38, 60, "P")
    spider_on_thread(g, 84, 1, 12, "K")
    cauldron(g, 118, 48, splash=False)
    book_stand(g, 58, 60)
    blit(g, "wizard.svg", 142, 46, 1)
    blit(g, "pumpkin.svg", 8, 56, 1)
    fog(g, 66, [(96, 112), (150, 162)])
    g.render("scene1.svg", "Магистр Коко варит зелье «Тыквенная улыбка» в хижине")


def scene2():
    g = Grid(240, 90)
    g.rect(0, 0, 240, 68, "P")
    for y in (12, 24, 36, 48, 60):
        g.hline(0, y, 240, "L")
    g.rect(0, 68, 240, 22, WOOD)
    g.hline(0, 68, 240, WOOD_D)
    g.hline(0, 78, 240, WOOD_D)
    web(g, 1, 1, 10)
    window(g, 172, 12, 52, 22, open_shutter=True)
    blit(g, "bat.svg", 188, 18, 1)
    for k, (px_, py) in enumerate(((204, 6), (210, 2), (215, 0))):
        g.rect(px_, py, 6, 4, INK)
        g.hline(px_ + 1, py + 1, 4, "L")
        g.hline(px_ + 1, py + 2, 3, "K")
        g.px(px_ + 5, py - 1, "D")
    for x, y in ((146, 28), (156, 24), (166, 20)):
        g.px(x, y, "D")
    cauldron(g, 40, 52, splash=True)
    cx, cy = 128, 34
    g.ellipse(cx, cy, 3, 3, "G")
    g.ellipse(cx, cy, 5.5, 5.5, "O")
    for dx, dy, c in ((0, -9, "G"), (0, 9, "R"), (-9, 0, "G"), (9, 0, "R"),
                      (-7, -7, "O"), (7, -7, "R"), (-7, 7, "R"), (7, 7, "G")):
        for s in range(1, 5):
            g.px(cx + dx * s // 4, cy + dy * s // 4, c)
    blit(g, "wizard.svg", 116, 46, 1)
    for x in (96, 100, 104):
        g.px(x, 52, INK); g.px(x - 2, 56, INK)
    for y in (44, 48, 52):
        g.px(110, y, INK)
    spider_on_thread(g, 84, 1, 10, "K")
    g.render("scene2.svg", "Чих Коко с неправильным тоном: страница гримуара улетает в окно")


def scene3():
    g = Grid(240, 90)
    g.rect(0, 0, 240, 90, "N")
    stars(g, [(20, 6, "I"), (52, 12, "D"), (84, 4, "G"), (120, 8, "I"), (150, 3, "D"),
              (185, 9, "I"), (215, 5, "D"), (70, 18, "D"), (140, 16, "I"), (200, 20, "D"),
              (35, 24, "D"), (170, 26, "D")])
    g.ellipse(36, 14, 5, 5, "G")
    g.ellipse(39, 13, 3.6, 3.6, "N")
    g.bat(96, 12, "K"); g.bat(210, 14, "P"); g.bat(150, 8, "K")
    for x in range(8, 236, 14):
        g.vline(x, 52, 14, "L")
    g.hline(0, 56, 240, "L")
    ground(g, 66)
    blit(g, "ghost.svg", 30, 36, 1)
    blit(g, "ghost.svg", 106, 28, 1)
    blit(g, "ghost.svg", 178, 38, 1)
    grave(g, 52, 76, 30, tilt=-1)
    grave(g, 122, 78, 36, tilt=1)
    grave(g, 190, 76, 26, tilt=0)
    for cx, y in ((70, 72), (142, 74), (208, 72)):
        g.ellipse(cx, y, 6, 2, "e")
    blit(g, "pumpkin.svg", 10, 58, 1)
    fog(g, 64, [(20, 44), (90, 120), (170, 200)])
    g.render("scene3.svg", "Двор просыпается: добрые призраки встают из-за надгробий")


def scene4():
    g = Grid(240, 90)
    g.rect(0, 0, 240, 90, "N")
    stars(g, [(30, 8, "D"), (70, 5, "D"), (110, 9, "D"), (160, 6, "D"), (205, 10, "D"),
              (50, 16, "D"), (185, 18, "D")])
    for x0, y, w in ((24, 12, 34), (90, 8, 44), (150, 14, 38), (200, 6, 30)):
        g.rect(x0, y, w, 3, "P")
        g.rect(x0 + 4, y + 3, w - 8, 1, "P")
    ground(g, 70)
    grave(g, 36, 78, 20, tilt=-1)
    grave(g, 208, 78, 18, tilt=1)
    for x in range(60, 190, 16):
        g.hline(x, 76, 9, "I")
    for x in range(66, 190, 16):
        g.px(x + 4, 77, "D")
    blit(g, "kostik.svg", 104, 46, 1)
    g.px(137, 58, "I"); g.px(138, 57, "I"); g.px(139, 56, "I")
    g.rect(146, 28, 56, 32, "L")
    g.rect(148, 30, 52, 28, "P")
    for yy in (36, 42, 48):
        g.hline(152, yy, 26 + (48 - yy) // 3, INK)
    g.px(192, 34, "G"); g.px(193, 33, "G"); g.px(194, 34, "G"); g.px(193, 35, "G")
    g.vline(152, 60, 10, "L")
    g.vline(196, 60, 10, "L")
    fog(g, 68, [(10, 60), (100, 150), (190, 235)])
    g.render("scene4.svg", "Костик, учитель каллиграфии, чертит план мелом")


def scene5():
    g = Grid(240, 90)
    g.rect(0, 0, 240, 90, "N")
    stars(g, [(24, 6, "I"), (66, 10, "D"), (108, 5, "I"), (170, 8, "D"), (205, 4, "I"),
              (140, 14, "D"), (44, 20, "D")])
    g.hline(20, 13, 200, "D")
    for x in (70, 120, 170):
        g.px(x, 14, "D")
    for x, y, lit in ((30, 14, True), (78, 18, False), (126, 14, True), (174, 18, True)):
        lantern(g, x, y, lit)
    g.vline(212, 26, 52, "L")
    g.hline(212, 30, 8, "L")
    g.rect(200, 22, 13, 10, "R")
    g.hline(202, 21, 9, "L")
    g.rect(204, 26, 5, 3, "G")
    g.vline(206, 32, 3, "G")
    g.px(198, 24, "K"); g.px(213, 30, "K")
    ground(g, 68)
    g.rect(24, 52, 18, 4, "L")
    g.rect(28, 44, 10, 8, "P")
    g.rect(30, 40, 6, 4, "L")
    g.px(33, 41, "E")
    g.rect(30, 56, 6, 12, "L")
    blit(g, "lumi.svg", 104, 44, 1)
    g.px(100, 54, "W"); g.px(98, 58, "W")
    g.bat(64, 26, "K")
    fog(g, 66, [(16, 70), (150, 200)])
    g.render("scene5.svg", "Люми зажигает Фонарики Памяти: каждый — от китайского знака")


def scene6():
    g = Grid(240, 90)
    g.rect(0, 0, 240, 90, "N")
    stars(g, [(60, 6, "I"), (100, 12, "D"), (140, 4, "I"), (185, 9, "D"), (30, 18, "D")])
    g.ellipse(34, 12, 4, 4, "G")
    g.ellipse(36, 11, 2.8, 2.8, "N")
    g.rect(206, 10, 26, 54, "P")
    g.vline(206, 10, 54, "L")
    g.vline(231, 10, 54, "L")
    g.rect(210, 16, 18, 14, "N")
    g.rect(214, 20, 10, 8, "G")
    g.hline(212, 19, 14, "L")
    g.px(218, 21, "K"); g.px(219, 22, "K")
    for k, w in enumerate((8, 14, 20, 26)):
        g.hline(219 - w // 2, 9 - k, w, "L")
    g.px(219, 2, "G"); g.px(219, 3, "G")
    for y in (34, 46):
        g.hline(206, y, 26, "L")
    ground(g, 64)
    grave(g, 26, 72, 20, tilt=0)
    waves(g, 58, 42)
    blit(g, "echo.svg", 66, 30, 1)
    blit(g, "wizard.svg", 96, 42, 1)
    blit(g, "kostik.svg", 150, 40, 1)
    blit(g, "bat.svg", 140, 8, 1)
    fog(g, 62, [(20, 80), (120, 170), (200, 240)])
    g.render("scene6.svg", "Эхо, Коко и Костик договариваются: идём зажигать фонари")


if __name__ == "__main__":
    scene1()
    scene2()
    scene3()
    scene4()
    scene5()
    scene6()
