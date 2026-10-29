# -*- coding: utf-8 -*-
"""Пиксельные интерьеры домика «Двора Тихой Луны» для описания курса.

Баннер-гостиная 96x40 + четыре комнаты 40x40 (по одной на обитателя),
рендер в shared/interior/<name>.svg (стиль make_meanings: Grid, crispEdges).
"""
from pathlib import Path

import make_characters as mc
from make_characters import Grid

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "shared" / "interior"
OUT.mkdir(parents=True, exist_ok=True)
mc.OUT = OUT

PI = dict(
    N="#120b24", V="#241744", U="#3a2a5e",
    E="#2a1c4e", e="#1c1338",
    S="#f4efe2", s="#d8d1bd",
    G="#86c232", t="#5f9420",
    O="#ff8c2b", o="#c5640d",
    Y="#ffd54f", F="#ffb347",
    K="#0b0716", I="#fdfaf1",
    D="#b3a8d4", P="#8a5fd6",
    W="#4a7fd4", w="#35609e",
    R="#8a6a4a", r="#6e5238",
    M="#94886a", m="#6e6552",
    A="#e8709a",
    B="#3a2a4e",
    x="#e64533", X="#b8402f",
    Q="#bfe8e0", q="#d9f5ee",
    C="#efe9dc", c="#c9c2ae",
)


def floor(g, y):
    g.rect(0, y, g.w, g.h - y, "E")
    g.hline(0, y, g.w, "e")
    for i, x in enumerate(range(6, g.w, 7)):
        g.vline(x, y + 1 + (i % 2), g.h - y - 1 - (i % 2), "e")


def bat(g, x, y):
    g.rect(x, y + 1, 2, 2, "B")
    g.px(x - 1, y, "B")
    g.px(x + 2, y, "B")
    g.px(x - 2, y + 1, "B")
    g.px(x + 3, y + 1, "B")
    g.px(x - 1, y + 2, "B")
    g.px(x + 2, y + 2, "B")
    g.px(x, y, "B")
    g.px(x + 1, y, "B")


def candle(g, x, y):
    g.rect(x, y, 2, 3, "C")
    g.px(x + 1, y, "c")
    g.px(x, y - 2, "F")
    g.px(x + 1, y - 2, "F")
    g.px(x, y - 1, "Y")


# ------------------------------------------------------------------ кабинет Коко
def art_koko_room():
    g = Grid(40, 40)
    g.rect(0, 0, 40, 30, "V")
    g.hline(0, 24, 40, "U")
    g.rect(0, 25, 40, 5, "E")
    floor(g, 30)
    # окно с луной
    g.rect(3, 4, 11, 11, "R")
    g.rect(5, 6, 7, 7, "K")
    g.vline(8, 6, 7, "R")
    g.hline(5, 9, 7, "R")
    g.ellipse(10, 8, 2, 2, "S")
    g.px(9, 8, "s")
    g.px(6, 7, "I")
    g.px(7, 11, "I")
    g.hline(2, 15, 13, "r")
    # полка с зельями
    g.hline(17, 13, 10, "R")
    g.px(18, 14, "r")
    g.px(25, 14, "r")
    g.rect(18, 11, 2, 2, "G")
    g.px(18, 10, "G")
    g.rect(21, 10, 2, 3, "D")
    g.px(21, 9, "D")
    g.rect(24, 11, 2, 2, "W")
    g.px(24, 10, "W")
    # письменный стол
    g.rect(8, 22, 16, 2, "R")
    g.vline(9, 24, 8, "r")
    g.vline(22, 24, 8, "r")
    # открытая книга заклинаний
    g.rect(12, 20, 7, 2, "S")
    g.vline(15, 20, 2, "K")
    g.px(13, 20, "D")
    g.px(17, 20, "D")
    g.px(14, 21, "D")
    g.px(16, 21, "D")
    # чернильница с пером
    g.rect(20, 20, 2, 2, "K")
    g.vline(20, 17, 3, "S")
    g.px(20, 16, "D")
    # свеча
    candle(g, 8, 19)
    # книжный шкаф
    g.rect(27, 8, 11, 20, "R")
    g.rect(28, 9, 9, 18, "K")
    g.hline(28, 14, 9, "r")
    g.hline(28, 19, 9, "r")
    g.hline(28, 24, 9, "r")
    g.rect(29, 11, 2, 3, "D")
    g.rect(31, 12, 2, 2, "G")
    g.rect(33, 11, 2, 3, "O")
    g.rect(35, 12, 2, 2, "A")
    g.px(37, 12, "S")
    g.px(37, 13, "S")
    g.rect(29, 16, 2, 3, "G")
    g.rect(31, 16, 2, 3, "A")
    g.rect(34, 17, 2, 2, "D")
    g.rect(35, 16, 2, 2, "S")
    g.px(35, 16, "K")
    g.px(36, 16, "K")
    g.rect(29, 21, 2, 3, "O")
    g.rect(31, 22, 2, 2, "S")
    g.rect(33, 21, 2, 3, "D")
    g.rect(35, 22, 2, 2, "G")
    g.rect(29, 26, 5, 1, "A")
    g.rect(30, 25, 3, 1, "D")
    # шляпа на шкафу
    g.hline(29, 7, 7, "D")
    g.hline(31, 5, 3, "D")
    g.px(32, 4, "D")
    g.hline(31, 6, 3, "O")
    # коврик и летучая мышь
    g.rect(11, 33, 18, 3, "A")
    g.hline(11, 33, 18, "D")
    g.hline(11, 35, 18, "D")
    g.hline(13, 34, 14, "D")
    bat(g, 22, 2)
    g.px(20, 8, "Y")
    g.px(21, 9, "Y")
    g.px(22, 8, "Y")
    return g, PI, "Кабинет Магистра Коко — книги заклинаний, зелья и свеча"


# ------------------------------------------------------------------ чердак Люми
def art_lumi_room():
    g = Grid(40, 40)
    g.rect(0, 0, 40, 29, "V")
    for i in range(6):
        g.px(i, 5 - i, "r")
        g.px(39 - i, 5 - i, "r")
        g.px(i, 6 - i, "R")
        g.px(39 - i, 6 - i, "R")
    g.vline(6, 2, 24, "R")
    g.vline(33, 2, 24, "R")
    g.hline(0, 26, 40, "R")
    floor(g, 29)
    # круглое окно с луной
    g.ellipse(20, 12, 7, 7, "R")
    g.ellipse(20, 12, 6, 6, "K")
    g.ellipse(20, 12, 4, 4, "S")
    g.px(19, 11, "s")
    g.px(21, 13, "s")
    g.vline(20, 7, 11, "R")
    g.hline(15, 12, 11, "R")
    g.px(9, 8, "I")
    g.px(31, 9, "I")
    # фонарики на верёвках
    g.vline(11, 4, 4, "r")
    g.hline(10, 8, 3, "r")
    g.rect(10, 9, 3, 3, "O")
    g.px(11, 10, "Y")
    g.ellipse(11, 31, 3, 1, "t")
    g.vline(28, 4, 4, "r")
    g.hline(27, 8, 3, "r")
    g.rect(27, 9, 3, 3, "G")
    g.px(28, 10, "I")
    g.ellipse(28, 31, 3, 1, "t")
    # паутина в углу
    for d in range(5):
        g.px(1 + d, 1 + d, "s")
        g.px(3 + d, 1 + d, "s")
    g.hline(1, 3, 5, "s")
    g.vline(3, 0, 5, "s")
    # сундук
    g.rect(6, 26, 10, 3, "r")
    g.rect(6, 29, 10, 5, "R")
    g.vline(8, 26, 8, "r")
    g.vline(14, 26, 8, "r")
    g.rect(10, 28, 2, 2, "Y")
    g.px(10, 28, "o")
    # Люми со свечой
    g.ellipse(31, 22, 5, 4, "q")
    g.rect(29, 19, 5, 6, "Q")
    g.rect(30, 18, 3, 1, "Q")
    g.px(29, 26, "Q")
    g.px(31, 26, "Q")
    g.px(33, 26, "Q")
    g.px(30, 22, "K")
    g.px(32, 22, "K")
    g.px(29, 23, "A")
    g.px(33, 23, "A")
    g.rect(31, 16, 1, 2, "C")
    g.px(31, 15, "F")
    # коробки
    g.rect(34, 27, 5, 3, "r")
    g.rect(35, 25, 3, 2, "R")
    return g, PI, "Чердак Люми — круглое окно с луной и фонарики"


# ------------------------------------------------------------------ кухонька Эхо
def art_echo_room():
    g = Grid(40, 40)
    g.rect(0, 0, 40, 15, "V")
    g.rect(0, 15, 40, 7, "e")
    g.hline(0, 15, 40, "U")
    g.hline(0, 18, 40, "U")
    g.hline(0, 21, 40, "U")
    for x in range(5, 40, 5):
        g.vline(x, 15, 6, "U")
    g.rect(0, 22, 40, 10, "V")
    floor(g, 32)
    # полка с сыром
    g.hline(4, 9, 12, "R")
    g.px(5, 10, "r")
    g.px(14, 10, "r")
    g.ellipse(7, 7, 3, 2, "Y")
    g.px(6, 7, "o")
    g.px(8, 6, "o")
    g.ellipse(12, 7, 2, 2, "F")
    g.px(12, 7, "o")
    # окно
    g.rect(30, 4, 8, 8, "R")
    g.rect(32, 6, 4, 4, "K")
    g.px(33, 7, "S")
    g.px(34, 8, "S")
    # колокольчик
    g.rect(25, 9, 5, 2, "Y")
    g.px(26, 8, "Y")
    g.px(27, 8, "Y")
    g.px(28, 8, "Y")
    g.hline(25, 11, 5, "o")
    g.px(27, 12, "K")
    # котёл
    g.rect(13, 20, 14, 2, "U")
    g.hline(15, 20, 10, "G")
    g.px(17, 19, "G")
    g.px(21, 19, "t")
    g.px(23, 19, "G")
    g.px(18, 17, "I")
    g.px(20, 16, "I")
    g.px(22, 17, "I")
    g.ellipse(20, 25, 7, 5, "K")
    g.px(14, 23, "U")
    g.px(15, 22, "U")
    g.px(14, 30, "K")
    g.px(26, 30, "K")
    g.rect(16, 29, 3, 2, "O")
    g.px(17, 28, "F")
    g.px(17, 29, "Y")
    g.rect(21, 29, 4, 2, "O")
    g.px(22, 28, "F")
    g.px(23, 29, "Y")
    g.rect(23, 13, 3, 2, "r")
    g.vline(24, 15, 5, "R")
    # метла
    g.vline(35, 20, 9, "R")
    g.rect(33, 29, 5, 3, "F")
    g.vline(34, 29, 3, "o")
    g.vline(36, 29, 3, "o")
    g.hline(33, 29, 5, "o")
    # травки и мышиная норка
    g.vline(4, 12, 3, "r")
    g.px(3, 15, "G")
    g.px(4, 15, "G")
    g.px(5, 15, "G")
    g.px(4, 16, "t")
    g.rect(3, 29, 4, 3, "K")
    g.px(4, 28, "K")
    # Эхо спит под потолочной балкой
    g.hline(0, 3, 40, "r")
    g.rect(9, 4, 5, 2, "B")
    g.px(7, 5, "B")
    g.px(8, 4, "B")
    g.px(14, 4, "B")
    g.px(15, 5, "B")
    g.px(10, 3, "B")
    g.px(12, 3, "B")
    g.px(10, 5, "Y")
    g.px(12, 5, "Y")
    return g, PI, "Кухонька Эхо — котёл с варевом и сырная полка"


# ------------------------------------------------------------------ гостиная Костика
def art_kostik_room():
    g = Grid(40, 40)
    g.rect(0, 0, 40, 23, "V")
    for x in range(4, 40, 6):
        g.vline(x, 0, 23, "U")
    g.hline(0, 23, 40, "U")
    g.rect(0, 24, 40, 5, "E")
    floor(g, 29)
    # портрет-череп
    g.rect(5, 5, 10, 9, "R")
    g.rect(6, 6, 8, 7, "K")
    g.rect(8, 8, 4, 3, "S")
    g.px(9, 11, "S")
    g.px(10, 11, "S")
    g.px(9, 9, "K")
    g.px(11, 9, "K")
    g.px(10, 10, "K")
    # кресло
    g.rect(5, 15, 9, 9, "x")
    g.rect(4, 19, 2, 7, "x")
    g.rect(13, 19, 2, 7, "x")
    g.rect(6, 22, 8, 3, "X")
    g.px(5, 29, "r")
    g.px(13, 29, "r")
    # столик с чайником
    g.hline(23, 22, 9, "R")
    g.vline(24, 23, 7, "r")
    g.vline(30, 23, 7, "r")
    g.hline(24, 26, 7, "r")
    g.rect(26, 18, 5, 4, "D")
    g.rect(27, 17, 3, 1, "U")
    g.px(28, 16, "Y")
    g.px(25, 19, "D")
    g.px(25, 18, "D")
    g.px(31, 18, "D")
    g.px(32, 19, "D")
    g.px(32, 20, "D")
    g.rect(21, 20, 2, 2, "S")
    g.px(20, 20, "S")
    g.rect(33, 20, 2, 2, "S")
    g.px(35, 20, "S")
    g.px(22, 18, "I")
    g.px(34, 18, "I")
    # канделябр
    g.hline(34, 24, 5, "r")
    g.vline(36, 15, 9, "R")
    candle(g, 35, 12)
    # коврик с косточкой
    g.ellipse(22, 33, 8, 2, "A")
    g.hline(16, 33, 12, "D")
    g.hline(26, 32, 3, "S")
    g.px(25, 31, "S")
    g.px(25, 33, "S")
    g.px(29, 31, "S")
    g.px(29, 33, "S")
    # стопка книг
    g.rect(2, 30, 4, 1, "A")
    g.rect(2, 31, 3, 1, "D")
    # гирлянда из мышек
    g.hline(4, 3, 32, "U")
    g.px(12, 4, "U")
    g.px(20, 4, "U")
    g.px(28, 4, "U")
    g.px(8, 4, "B")
    g.px(9, 4, "B")
    g.px(8, 5, "B")
    g.px(9, 5, "B")
    g.px(6, 4, "B")
    g.px(11, 4, "B")
    g.px(24, 4, "B")
    g.px(25, 4, "B")
    g.px(24, 5, "B")
    g.px(25, 5, "B")
    g.px(22, 4, "B")
    g.px(27, 4, "B")
    return g, PI, "Гостиная Костика — кресло, чай и портрет черепа"


# ------------------------------------------------------------------ баннер-гостиная
def art_banner():
    g = Grid(96, 40)
    g.rect(0, 0, 96, 28, "V")
    g.hline(0, 22, 96, "U")
    g.rect(0, 23, 96, 5, "E")
    floor(g, 28)
    # окно с луной и шторами
    g.rect(3, 3, 2, 14, "D")
    g.rect(21, 3, 2, 14, "D")
    g.hline(3, 2, 20, "D")
    g.rect(5, 4, 16, 14, "R")
    g.rect(7, 6, 12, 10, "K")
    g.vline(13, 6, 10, "R")
    g.hline(7, 11, 12, "R")
    g.ellipse(16, 9, 2, 2, "S")
    g.px(15, 9, "s")
    g.px(9, 8, "I")
    g.px(10, 13, "I")
    g.px(19, 14, "I")
    g.hline(4, 18, 18, "r")
    # камин
    g.hline(36, 13, 26, "R")
    g.hline(36, 14, 26, "r")
    g.rect(39, 15, 20, 12, "M")
    g.hline(40, 18, 18, "m")
    g.hline(40, 21, 18, "m")
    g.hline(40, 24, 18, "m")
    g.px(45, 16, "m")
    g.px(51, 16, "m")
    g.px(57, 16, "m")
    g.px(43, 19, "m")
    g.px(49, 19, "m")
    g.px(55, 19, "m")
    g.px(47, 22, "m")
    g.px(53, 22, "m")
    g.rect(44, 19, 10, 8, "K")
    g.rect(46, 24, 6, 3, "O")
    g.rect(47, 21, 2, 3, "F")
    g.rect(49, 22, 2, 2, "F")
    g.px(48, 20, "O")
    g.px(47, 23, "Y")
    g.px(48, 23, "Y")
    g.px(46, 20, "F")
    g.px(51, 20, "F")
    g.rect(37, 27, 24, 2, "m")
    # на каминной полке
    g.ellipse(38, 11, 2, 2, "O")
    g.px(38, 9, "G")
    g.px(37, 11, "K")
    g.px(39, 11, "K")
    g.rect(45, 9, 2, 3, "C")
    g.px(45, 8, "F")
    g.px(46, 8, "F")
    g.rect(58, 9, 2, 3, "C")
    g.px(58, 8, "F")
    g.px(59, 8, "F")
    g.rect(46, 6, 8, 6, "R")
    g.rect(47, 7, 6, 4, "K")
    g.rect(49, 8, 2, 2, "S")
    g.px(49, 8, "K")
    g.px(50, 8, "K")
    # книжный шкаф
    g.rect(64, 6, 16, 21, "R")
    g.rect(65, 7, 14, 19, "K")
    g.hline(65, 12, 14, "r")
    g.hline(65, 17, 14, "r")
    g.hline(65, 22, 14, "r")
    g.rect(66, 9, 2, 3, "D")
    g.rect(68, 10, 2, 2, "G")
    g.rect(70, 9, 2, 3, "O")
    g.rect(72, 10, 1, 2, "A")
    g.rect(74, 9, 2, 3, "S")
    g.rect(76, 10, 2, 2, "D")
    g.rect(66, 14, 2, 3, "G")
    g.rect(68, 14, 2, 3, "A")
    g.rect(71, 14, 2, 2, "W")
    g.px(71, 13, "W")
    g.rect(74, 13, 2, 4, "O")
    g.rect(76, 14, 2, 3, "G")
    g.rect(66, 18, 2, 4, "O")
    g.rect(68, 19, 2, 3, "S")
    g.rect(70, 18, 2, 4, "D")
    g.rect(72, 19, 2, 3, "G")
    g.rect(74, 18, 2, 4, "A")
    g.rect(66, 24, 6, 1, "D")
    g.rect(67, 23, 4, 1, "A")
    g.rect(73, 23, 5, 4, "R")
    g.hline(73, 23, 5, "r")
    # кресло
    g.rect(85, 15, 8, 9, "x")
    g.rect(84, 19, 2, 7, "x")
    g.rect(92, 19, 2, 7, "x")
    g.rect(86, 22, 6, 3, "X")
    g.px(85, 29, "r")
    g.px(92, 29, "r")
    # ковёр у камина
    g.ellipse(48, 34, 12, 3, "D")
    g.ellipse(48, 34, 9, 2, "A")
    g.hline(41, 34, 14, "x")
    g.px(44, 33, "Y")
    g.px(52, 35, "Y")
    # гирлянда фонариков
    g.hline(24, 2, 50, "U")
    g.px(30, 3, "U")
    g.px(36, 4, "U")
    g.px(42, 4, "U")
    g.px(48, 3, "U")
    g.vline(28, 2, 2, "r")
    g.rect(27, 4, 3, 3, "O")
    g.px(28, 5, "Y")
    g.vline(48, 3, 2, "r")
    g.rect(47, 5, 3, 3, "G")
    g.px(48, 6, "I")
    g.vline(68, 2, 2, "r")
    g.rect(67, 4, 3, 3, "O")
    g.px(68, 5, "Y")
    # летучие мыши и тыква на полу
    bat(g, 30, 7)
    bat(g, 61, 4)
    g.ellipse(26, 32, 3, 2, "O")
    g.px(26, 30, "G")
    g.px(25, 32, "K")
    g.px(27, 32, "K")
    g.px(26, 33, "K")
    return g, PI, "Гостиная двора Тихой Луны — камин, книжный шкаф и тыквы"


ART = [
    (art_banner, "banner.svg"),
    (art_koko_room, "koko-room.svg"),
    (art_lumi_room, "lumi-room.svg"),
    (art_echo_room, "echo-room.svg"),
    (art_kostik_room, "kostik-room.svg"),
]

if __name__ == "__main__":
    for fn, name in ART:
        g, p, desc = fn()
        g.render_svg(p, name, desc)
    print("done:", len(ART), "interior arts")
