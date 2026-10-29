# -*- coding: utf-8 -*-
"""Подземный слой катакомб 360x150 (вывод 1440x600) -> shared/frame/underground.svg.

Скелет, зомби, крипта с монстром, гроб, сундук конфет, призрак, тыква, черви,
кости, корни — всё в единственном экземпляре."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W, H = 360, 150

C = {
    "soil2": "#0e0a1d", "gate": "#070510", "pebble": "#1c1533",
    "stone": "#514e73", "stone2": "#3a3757",
    "bone": "#c9c2a4", "skull": "#e8e2c4",
    "pump": "#ff8c2b", "stem": "#4f9a28",
    "zskin": "#86c232", "zskin2": "#4f7a1e", "zdark": "#0e0a1d", "shirt": "#4a3a5e",
    "gold": "#ffd54f", "blood": "#e64533", "eyes": "#e64533",
    "wood": "#6b4a2a", "wood2": "#4e351f",
    "chest": "#8a5fd6", "chest2": "#6a48ab",
    "root": "#2c5a14", "worm": "#e88fb0", "line": "#2e2240",
    "ghostC": "#bfe8e0",
}

R = []


def px(x, y, w, h, c):
    R.append((x, y, w, h, C[c]))


def skull(x, y):
    px(x, y, 8, 5, "skull")
    px(x + 1, y + 5, 6, 2, "skull")
    px(x + 1, y + 2, 1, 1, "gate")
    px(x + 6, y + 2, 1, 1, "gate")
    px(x + 2, y + 5, 1, 1, "gate")
    px(x + 5, y + 5, 1, 1, "gate")


def worm(x, y):
    px(x, y, 3, 1, "worm")
    px(x + 3, y + 1, 2, 1, "worm")
    px(x + 5, y, 3, 1, "worm")
    px(x + 8, y + 1, 2, 1, "worm")


def bone(x, y):
    px(x, y, 8, 2, "bone")
    px(x - 1, y - 1, 2, 2, "bone")
    px(x - 1, y + 1, 2, 2, "bone")
    px(x + 7, y - 1, 2, 2, "bone")
    px(x + 7, y + 1, 2, 2, "bone")


def root_top(x, ln):
    px(x, 0, 2, ln, "root")
    if ln >= 8:
        px(x - 2, ln - 4, 2, 2, "root")


# корни, спускающиеся от поверхности
root_top(28, 16)
root_top(92, 9)
root_top(176, 12)
root_top(215, 12)
root_top(295, 25)
root_top(338, 10)

# скелет, лежащий в земле (слева)
skull(18, 30)
for i in range(8):
    px(28 + i * 4, 34, 3, 2, "bone")
for i in range(6):
    px(31 + i * 5, 27, 2, 14, "bone")
px(60, 31, 9, 7, "bone")
px(63, 34, 3, 2, "gate")
px(69, 32, 22, 2, "bone")
px(69, 36, 22, 2, "bone")
px(92, 38, 5, 3, "bone")
px(92, 42, 5, 3, "bone")
px(30, 36, 2, 16, "bone")
px(29, 52, 1, 3, "bone")
px(32, 52, 1, 3, "bone")

# зомби, тянущийся вверх из земли (центр)
px(146, 8, 12, 10, "zskin")
px(146, 7, 12, 2, "zdark")
px(148, 11, 3, 3, "gate")
px(155, 11, 3, 3, "gate")
px(151, 16, 6, 2, "gate")
px(152, 16, 1, 1, "bone")
px(155, 16, 1, 1, "bone")
px(150, 18, 4, 3, "zskin")
px(144, 21, 16, 22, "zskin2")
px(146, 24, 12, 8, "shirt")
px(144, 30, 4, 4, "shirt")
px(138, 4, 3, 20, "zskin")
px(137, 1, 1, 3, "zskin")
px(140, 0, 1, 4, "zskin")
px(165, 8, 3, 18, "zskin")
px(164, 5, 1, 3, "zskin")
px(167, 4, 1, 4, "zskin")
px(145, 43, 5, 16, "zskin2")
px(154, 43, 5, 16, "zskin2")

# крипта с монстром (справа)
px(246, 24, 4, 14, "stone2")
px(242, 28, 12, 4, "stone2")
px(215, 38, 70, 6, "stone")
px(209, 44, 82, 6, "stone")
px(205, 50, 90, 6, "stone")
px(215, 43, 70, 1, "stone2")
px(209, 49, 82, 1, "stone2")
for x in range(215, 285, 14):
    px(x, 40, 1, 3, "stone2")
for x in range(209, 291, 14):
    px(x, 46, 1, 3, "stone2")
px(205, 56, 12, 56, "stone")
px(283, 56, 12, 56, "stone")
for y in range(60, 112, 8):
    px(205, y, 12, 1, "stone2")
    px(283, y, 12, 1, "stone2")
px(209, 56, 1, 56, "stone2")
px(287, 56, 1, 56, "stone2")
px(217, 60, 66, 52, "gate")
px(240, 84, 5, 5, "eyes")
px(256, 84, 5, 5, "eyes")
px(242, 86, 1, 2, "gate")
px(258, 86, 1, 2, "gate")
for i in range(6):
    px(242 + i * 3, 94, 2, 4, "bone")
px(250, 62, 1, 10, "line")
px(248, 72, 5, 4, "line")
px(249, 73, 1, 1, "eyes")
skull(220, 116)
px(218, 124, 12, 3, "stone2")

# призрак, выглядывающий из земли
px(181, 86, 8, 2, "ghostC")
px(180, 88, 10, 8, "ghostC")
px(182, 91, 2, 2, "gate")
px(186, 91, 2, 2, "gate")
px(180, 96, 2, 3, "ghostC")
px(184, 96, 2, 3, "ghostC")
px(188, 96, 2, 3, "ghostC")

# полу-засыпанная тыква
px(115, 44, 14, 8, "pump")
px(119, 47, 2, 2, "gate")
px(124, 47, 2, 2, "gate")
px(117, 51, 10, 1, "gate")
px(113, 52, 18, 3, "soil2")
px(120, 42, 2, 2, "stem")

# гроб в глубине (слева-снизу)
px(46, 100, 54, 6, "wood2")
px(48, 106, 50, 16, "wood")
px(48, 120, 50, 4, "wood2")
px(69, 102, 2, 8, "bone")
px(66, 104, 8, 2, "bone")
px(50, 108, 2, 2, "bone")
px(94, 108, 2, 2, "bone")

# сундук с конфетами (справа-снизу)
px(304, 74, 40, 10, "chest2")
px(308, 84, 32, 18, "chest")
px(318, 84, 4, 18, "gold")
px(317, 90, 6, 6, "gold")
px(296, 102, 3, 4, "pump")
px(299, 106, 5, 4, "blood")
px(305, 106, 5, 4, "gold")
px(313, 104, 5, 4, "pump")
px(322, 103, 5, 4, "gold")

# россыпь: черви, кости, камешки, корни
worm(126, 110)
worm(240, 132)
worm(70, 88)
bone(115, 120)
bone(196, 140)
bone(260, 132)
for x, y, w in [(12, 70, 2), (38, 64, 1), (105, 95, 2), (132, 70, 1), (168, 60, 2),
                (204, 74, 1), (232, 70, 2), (262, 120, 1), (306, 60, 2), (330, 68, 1),
                (24, 100, 1), (170, 118, 2), (280, 128, 1), (348, 90, 2)]:
    R.append((x, y, w, 1, C["pebble"]))
R.append((30, 138, 30, 2, C["root"]))
R.append((200, 140, 26, 2, C["root"]))

out = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 150" width="1440" height="600" '
    'shape-rendering="crispEdges">',
    '<defs><linearGradient id="ug" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#120d26"/><stop offset="1" stop-color="#0a0714"/>'
    "</linearGradient></defs>",
    '<rect x="0" y="0" width="%d" height="%d" fill="url(#ug)"/>' % (W, H),
]
out += ['<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % r for r in R]
out.append("</svg>")
(ROOT / "shared" / "frame" / "underground.svg").write_text("\n".join(out), encoding="utf-8")
print("underground.svg:", len(R), "rects |",
      (ROOT / "shared" / "frame" / "underground.svg").stat().st_size, "bytes")
