# -*- coding: utf-8 -*-
"""Генератор сайта «Двор Тихой Луны».

Запуск: python build/build.py
Создаёт:
  lesson/<знак>/index.html   — уроки (4 фазы) для 17 знаков и 8 слов
  shared/lesson-data.js      — данные для карты, бонуса, финала
  build/course_model.json    — модель курса для publish_stepik.py
"""
import json
import random
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from data import (COURSE, GLYPHS, WORDS, SECTIONS, SPECIAL_LESSONS, SPECIAL_POINTS,
                  CHARACTERS, WING_TITLES, STORY_PANELS, FINALE, TONES)

TOTAL_LESSONS = len(GLYPHS) + len(WORDS)
MAP_LESSON_URL = "https://stepik.org/lesson/2666960/step/1"

# ---------------------------------------------------------------- тоны
MARKS = {
    "a": "āáǎà", "o": "ōóǒò", "e": "ēéěè", "i": "īíǐì",
    "u": "ūúǔù", "ü": "ǖǘǚǜ", "v": "ǖǘǚǜ",
}


def strip_tone(syl):
    for v, seq in MARKS.items():
        for m in seq:
            syl = syl.replace(m, v)
    return syl


def tone_mark(syl, tone):
    syl = strip_tone(syl)
    vowels = [c for c in syl if c in "aoeiuvü"]
    if not vowels:
        return syl
    if "iu" in syl:
        target = "u"
    elif "ui" in syl:
        target = "i"
    else:
        target = None
        for cand in "aoe":
            if cand in syl:
                target = cand
                break
        if target is None:
            target = vowels[-1]
    idx = syl.index(target)
    return syl[:idx] + MARKS[target][tone - 1] + syl[idx + 1:]


def pinyin_variants(pinyin):
    """[правильный пиньинь, + 3 варианта того же слога с другими тонами]."""
    tone = 1
    syl = pinyin
    for t in (1, 2, 3, 4):
        if tone_mark(strip_tone(pinyin), t) == pinyin:
            tone, syl = t, pinyin
            break
    base = strip_tone(pinyin)
    out = []
    for t in (1, 2, 3, 4):
        v = tone_mark(base, t)
        if v == pinyin:
            out.insert(0, v)
        else:
            out.append(v)
    return out, tone


def color_pinyin(pinyin, tone):
    return '<span style="color:{0}">{1}</span>'.format(
        {1: "#e64533", 2: "#ff8c2b", 3: "#29b6f6", 4: "#86c232", 0: "#bfe8e0"}[tone], pinyin)


# ---------------------------------------------------------------- игровые раунды
def pick_glyph_distractors(answer, n, offset):
    chars = [g["char"] for g in GLYPHS]
    idx = chars.index(answer)
    out = []
    k = offset
    while len(out) < n:
        cand = chars[(idx + k) % len(chars)]
        if cand != answer:
            out.append(cand)
        k += 1
    return out


def pick_word_distractors(answer, n, offset):
    ws = [w["word"] for w in WORDS]
    idx = ws.index(answer)
    out = []
    k = offset
    while len(out) < n:
        cand = ws[(idx + k) % len(ws)]
        if cand != answer:
            out.append(cand)
        k += 1
    return out


def shuffled(items, seed):
    r = random.Random(seed)
    out = list(items)
    r.shuffle(out)
    return out


def glyph_game(g, glyph_index):
    ch = g["char"]
    variants, _ = pinyin_variants(g["pinyin"])
    d1 = pick_glyph_distractors(ch, 3, 1)
    d2 = pick_glyph_distractors(ch, 3, 4)
    seed = g["char"] + str(glyph_index)
    return [
        {"kind": "audio2glyph", "opts": shuffled([ch] + d1, seed + "a"), "ans": ch,
         "prompt": "audio", "audio": g["audio"]},
        {"kind": "meaning2glyph", "opts": shuffled([ch] + d2, seed + "b"), "ans": ch,
         "prompt": g["meaning"]},
        {"kind": "glyph2pinyin", "opts": shuffled(variants, seed + "c"), "ans": g["pinyin"],
         "prompt": ch},
        {"kind": "pinyin2glyph", "opts": shuffled([ch] + d1, seed + "d"), "ans": ch,
         "prompt": g["pinyin"]},
        {"kind": "audio2pinyin", "opts": shuffled(variants, seed + "e"), "ans": g["pinyin"],
         "prompt": "audio", "audio": g["audio"]},
    ]


def word_game(w, word_index):
    word = w["word"]
    py_variants, _ = pinyin_variants(w["pinyin"])
    other_py = []
    for cand in pick_word_distractors(word, 5, 1):
        p = next(x for x in WORDS if x["word"] == cand)["pinyin"]
        if p != w["pinyin"] and p not in other_py:
            other_py.append(p)
        if len(other_py) == 3:
            break
    d1 = pick_word_distractors(word, 3, 1)
    d2 = pick_word_distractors(word, 3, 4)
    meaning_opts = []
    for cand in d1:
        meaning_opts.append(next(x for x in WORDS if x["word"] == cand)["meaning"])
    seed = w["word"] + str(word_index)
    return [
        {"kind": "audio2word", "opts": shuffled([word] + d1, seed + "a"), "ans": word,
         "prompt": "audio", "audio": w["audio"]},
        {"kind": "meaning2word", "opts": shuffled([word] + d2, seed + "b"), "ans": word,
         "prompt": w["meaning"]},
        {"kind": "word2pinyin", "opts": shuffled([w["pinyin"]] + other_py, seed + "c"),
         "ans": w["pinyin"], "prompt": word},
        {"kind": "meaning2word", "opts": shuffled([word] + d1, seed + "d"), "ans": word,
         "prompt": w["meaning"]},
        {"kind": "audio2pinyin", "opts": shuffled([w["pinyin"]] + other_py, seed + "e"),
         "ans": w["pinyin"], "prompt": "audio", "audio": w["audio"]},
    ]


# ---------------------------------------------------------------- сборка данных
def build_lesson_data():
    glyphs_js, words_js = [], []
    for i, g in enumerate(GLYPHS):
        variants, tone = pinyin_variants(g["pinyin"])
        glyphs_js.append({
            "char": g["char"], "pinyin": g["pinyin"], "tone": tone,
            "meaning": g["meaning"], "audio": g["audio"], "wing": g["wing"],
            "key": g["key"], "strokes": g["strokes"],
            "map": list(g["map"]), "index": i, "total": TOTAL_LESSONS,
            "pinyinOpts": variants, "game": glyph_game(g, i), "tale": g["tale"],
        })
    for i, w in enumerate(WORDS):
        variants, tone = pinyin_variants(w["pinyin"])
        words_js.append({
            "word": w["word"], "pinyin": w["pinyin"], "tone": tone,
            "meaning": w["meaning"], "audio": w["audio"],
            "parts": w["parts"], "map": list(w["map"]),
            "index": len(GLYPHS) + i, "total": TOTAL_LESSONS,
            "pinyinOpts": variants, "game": word_game(w, i), "tale": w["tale"],
        })
    specials = {k: {"title": v.get("title", ""), "url": v.get("url", ""),
                    "map": list(SPECIAL_POINTS.get(k, (500, 560)))}
                for k, v in SPECIAL_LESSONS.items()}
    return {"glyphs": glyphs_js, "words": words_js, "special": specials}


# ---------------------------------------------------------------- шаблон урока
HEAD = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="qm-base" content="">
<title>{title} · Двор Тихой Луны</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}shared/spooky.css?v=14">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><text y='13' font-size='13'>🎃</text></svg>">
</head>
<body class="with-ground">
<header class="topbar">
  <div class="logo">Двор Тихой Луны <span class="hanzi">🌙</span></div>
  <div class="spacer"></div>
  <a class="back" href="{map_url}" target="_top">⟵ Карта двора</a>
</header>
<nav class="stepper" id="stepper">
  <div class="step active" data-ph="1"><span class="dot"></span>Туман</div>
  <div class="step" data-ph="2"><span class="dot"></span>Голос Коко</div>
  <div class="step" data-ph="3"><span class="dot"></span>Мел и камень</div>
  <div class="step" data-ph="4"><span class="dot"></span>Сладость или гадость</div>
</nav>
<div class="companion" id="companion"></div>
"""

BODY_HEAD = """
<div class="phase" id="p1">
  <h1>{h1}</h1>
  <div class="sub">{sub}</div>
  <div class="glyph-hero">
    <div class="big hanzi">{big}</div>
    <div>
      <div class="py">{py_colored}</div>
      <div class="mn">{meaning}</div>
      <div class="meta">
        <span class="badge" style="background:{tone_bg};color:{tone_fg}">{tone_name}</span>
        <span>черты: <b>{strokes}</b></span>
        <span>{key_html}</span>
        <span>фонарь <b>{num}</b> из {total}</span>
      </div>
      <div class="audio-row">
        <button class="play" id="audio-main"><span class="ico">🔊</span> Послушать</button>
        <button class="play slow" id="audio-slow">🐢 Медленно</button>
      </div>
    </div>
    <div class="meaning-art">{meaning_art}</div>
  </div>
  <div style="margin-top:22px;text-align:right"><button class="btn" id="go2">Дальше: голос Коко →</button></div>
</div>

<div class="phase" id="p2" style="display:none">
  <h1>Голос Коко</h1>
  <div class="sub">Магистр Коко отвечает за звуки. С неправильного тона всё и началось...</div>
  <div class="panel">
    <div class="audio-row" style="margin-top:0">
      <button class="play" id="audio-main2"><span class="ico">🔊</span> {big2} = {py2}</button>
      <button class="play slow" id="audio-slow2">🐢 Медленно</button>
      <button class="play" id="audio-echo"><span class="ico">🐭</span> Повторить за Эхо</button>
    </div>
    <div class="tone-line" id="tone-line"></div>
    <div class="tone-hint">Это слепок голоса: линия показывает движение тона. Жми кнопки тонов — слушай и сравнивай.</div>
    <div class="tone-btns" id="tone-btns"></div>
  </div>
  <div class="panel tale" style="margin-top:18px">
    <h2>Сказка-заклинание <span class="tag">рассказывает Коко</span></h2>
    {tale_html}
  </div>
  <div style="margin-top:22px;display:flex;justify-content:space-between">
    <button class="btn ghosty small" id="back1">⟵ Туман</button>
    <button class="btn" id="go3">Дальше: мел и камень →</button>
  </div>
</div>

<div class="phase" id="p3" style="display:none">
  <h1>Мел и камень</h1>
  <div class="sub">{writer_sub}</div>
  <div class="writer-wrap">
    <img class="bone-hand hand-l" src="{up}shared/characters/bone-hand-l.svg?v=13" alt="Костяная рука держит холст">
    <div class="writer-duo">
      <div id="hanzi-target"></div>
      <div id="hanzi-target2" style="display:none"></div>
    </div>
    <img class="bone-hand hand-r" src="{up}shared/characters/bone-hand-r.svg?v=13" alt="">
    <div class="writer-status" id="writer-status">Обведи черты по костям — я смотрю, Костик</div>
    <div class="skulls" id="skulls"></div>
    <div class="writer-ctrl">
      <button class="btn ghosty small" id="show-strokes">Показать черты</button>
      <button class="btn small" id="reset-writer">Заново</button>
    </div>
  </div>
  <div style="margin-top:22px;display:flex;justify-content:space-between">
    <button class="btn ghosty small" id="back2">⟵ Голос Коко</button>
    <button class="btn" id="go4" disabled>Дальше: сладость или гадость →</button>
  </div>
</div>

<div class="phase" id="p4" style="display:none">
  <h1>Сладость или гадость?</h1>
  <div class="sub">Гости двора приходят за знаками. Угости правильно — получишь конфету-фонарик.</div>
  <div class="game-scene">
    <div class="guest-row">
      <img class="lumi-host" src="{up}shared/characters/lumi.svg" alt="Люми — ведёт игру">
      <img class="sack-img" id="sack" src="{up}shared/characters/sack.svg" alt="Мешок вопросов">
      <img class="guest-img" id="guest-img" src="{up}shared/characters/ghost.svg" alt="">
      <div class="say"><span class="q" id="guest-say">Сладость или гадость?</span><div id="guest-note" style="color:#b3a8d4;font-size:13px;margin-top:4px"></div></div>
    </div>
    <div class="prompt" id="prompt"></div>
    <div class="candies" id="candies"></div>
    <div class="game-progress" id="game-progress"></div>
  </div>
  <div class="lantern-ceremony" id="ceremony" style="display:none">
    <div class="flame">🏮</div>
    <h2 id="cer-title"></h2>
    <p style="color:#b3a8d4;margin:10px 0 20px" id="cer-text"></p>
    <a class="btn poison" id="to-map" href="{map_url}" target="_top">На карту двора →</a>
  </div>
  <div style="margin-top:22px"><button class="btn ghosty small" id="back3">⟵ Мел и камень</button></div>
</div>

{ground_div}
"""

TAIL = """
<script src="https://cdn.jsdelivr.net/npm/hanzi-writer@3.5.0/dist/hanzi-writer.min.js"></script>
<script src="{up}shared/spooky.js?v=13"></script>
<script>/*PAYLOAD*/</script>
<script>/*LESSON_JS*/</script>
</body>
</html>
"""


def lesson_html(item, kind):
    up = "../../"
    is_glyph = kind == "glyph"
    num = item["index"] + 1
    title = item["char"] if is_glyph else item["word"]
    variants, tone = pinyin_variants(item["pinyin"])
    h1 = "Иероглиф {0} — {1}".format(title, item["meaning"]) if is_glyph \
        else "Слово {0} — {1}".format(title, item["meaning"])
    sub = "{0} · Фонарь {1} из {2}".format(
        WING_TITLES.get(item.get("wing", ""), "Слова-заклинания"), num, TOTAL_LESSONS)
    if is_glyph:
        key_html = "ключ: <b>{0}</b>".format(item["key"])
        writer_sub = "Пиши как Костик: черта за чертой, мел не жалеем. Три раунда — и фонарь наш."
    else:
        key_html = "состоит из: <b>{0}</b>".format(" + ".join(item["parts"]))
        writer_sub = "Оба знака уже на доске: веди мелом по контуру — сначала первый, потом второй."
    tale_html = "".join("<p>{0}</p>".format(t) for t in item["tale"])
    glyph_mean = {g["char"]: g["meaning"] for g in __import__("data").GLYPHS}
    chars = [title] if is_glyph else list(item["parts"])
    boxes = []
    for ch in chars:
        alt = glyph_mean.get(ch, "").split(";")[0].strip()
        boxes.append(
            '<div class="meaning-box"><img src="{0}shared/meanings/{1}.svg?v=12" '
            'alt="{2}"><span class="mb-cap">{3}</span></div>'.format(
                up, quote(ch), alt, ch))
    meaning_art = "".join(boxes)
    payload = {
        "type": kind, "target": title, "pinyin": item["pinyin"], "tone": tone,
        "meaning": item["meaning"], "audio": item["audio"], "game": item["game"],
        "parts": item.get("parts", []), "num": num, "total": TOTAL_LESSONS,
    }
    if kind == "glyph":
        g = quote(title)
        ground_div = ('<div class="ground-strip" style="background-image:'
                      "url('{up}shared/frame/grounds/{g}.svg?v=1'),"
                      "url('{up}shared/frame/undergrounds/{g}.svg?v=1')\"></div>"
                      ).format(up=up, g=g)
    else:
        ground_div = '<div class="ground-strip"></div>'
    body = BODY_HEAD.format(
        h1=h1, sub=sub, big=title, py_colored=color_pinyin(item["pinyin"], tone),
        meaning=item["meaning"], tone_bg=__import__("data").TONE_COLORS[tone],
        tone_fg="#120b24" if tone in (0, 2) else "#ffffff",
        tone_name=__import__("data").TONE_NAMES[tone],
        strokes=item.get("strokes", ""), key_html=key_html, num=num,
        total=TOTAL_LESSONS, big2=title, py2=item["pinyin"],
        tale_html=tale_html, writer_sub=writer_sub, up=up, map_url=MAP_LESSON_URL,
        ground_div=ground_div, meaning_art=meaning_art)
    tail = TAIL.format(up=up).replace("/*PAYLOAD*/",
        "window.LESSON = " + json.dumps(payload, ensure_ascii=False) + ";"
        ).replace("/*LESSON_JS*/", LESSON_JS)
    return HEAD.format(title=title, up=up, map_url=MAP_LESSON_URL) + body + tail


LESSON_JS = r"""
(function () {
  "use strict";
  var L = window.LESSON, QM = window.QM;
  var phases = { 1: document.getElementById("p1"), 2: document.getElementById("p2"),
                 3: document.getElementById("p3"), 4: document.getElementById("p4") };
  var cur = 1;

  function showPh(n) {
    Object.keys(phases).forEach(function (k) {
      phases[k].style.display = (+k === n) ? "" : "none";
    });
    document.querySelectorAll("#stepper .step").forEach(function (el) {
      var ph = +el.getAttribute("data-ph");
      el.classList.toggle("active", ph === n);
      el.classList.toggle("done", ph < n);
    });
    cur = n;
    if (n === 2) onPhase2();
    if (n === 3) onPhase3();
    if (n === 4) onPhase4();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
  document.getElementById("go2").onclick = function () { QM.sfx.click(); showPh(2); };
  document.getElementById("go3").onclick = function () { QM.sfx.click(); showPh(3); };
  document.getElementById("go4").onclick = function () { QM.sfx.click(); showPh(4); };
  document.getElementById("back1").onclick = function () { showPh(1); };
  document.getElementById("back2").onclick = function () { showPh(2); };
  document.getElementById("back3").onclick = function () { showPh(3); };

  QM.bindPlay(document.getElementById("audio-main"), L.audio);
  QM.bindPlay(document.getElementById("audio-slow"), L.audio, true);
  QM.bindPlay(document.getElementById("audio-main2"), L.audio);
  QM.bindPlay(document.getElementById("audio-slow2"), L.audio, true);
  document.getElementById("audio-echo").onclick = function () {
    var btn = this;
    QM.sfx.ghost();
    QM.playAudio(L.audio);
    btn.disabled = true;
    setTimeout(function () {
      QM.playAudio(L.audio, true);
      setTimeout(function () { btn.disabled = false; }, 2400);
    }, 1600);
  };

  /* ---- фаза 1 ---- */
  QM.say("kostik", [
    "Вот наш фонарь номер " + L.num + " из " + L.total + ". Сначала — туман: знак ещё не виден.",
    "Смотри внимательно: " + L.target + " = " + L.pinyin + ". Слышишь звук? Кликни меня, когда будешь готов.",
  ]);

  /* ---- фаза 2 ---- */
  var kokoLines = [
    "Хе-хе-е... Так вот как звучит «" + L.target + "». Послушай ещё раз — нормальным тоном и медленно.",
    "Слог «" + QM.esc(L.pinyin) + "» — " + QM.TONE_NAMES[L.tone].toLowerCase() + ". А теперь послушай все четыре тона полуночи — и запомни наш.",
  ];
  var tonesBox = document.getElementById("tone-btns");
  var toneNames = { 1: "рОВНО", 2: "ВВЕРХ", 3: "НЫРОК", 4: "ВНИЗ" };
  [1, 2, 3, 4].forEach(function (t) {
    var b = document.createElement("button");
    b.className = "tone-btn";
    b.style.background = QM.TONE_COLORS[t];
    b.innerHTML = '<span class="n">' + t + '-й тон · ' + toneNames[t] + '</span>mā ' + t;
    b.onclick = function () {
      QM.sfx.click();
      QM.playAudio("ma" + t + ".mp3");
      QM.drawTone("tone-line", t);
    };
    tonesBox.appendChild(b);
  });
  function onPhase2() {
    QM.say("koko", kokoLines, function () {
      QM.say("koko", "Кликай «Повторить за Эхо» и тоны ниже. Потом — tale-сказка. Читай! Она работает лучше запоминания.");
    });
    QM.drawTone("tone-line", L.tone);
  }

  /* ---- фаза 3: hanzi-writer ---- */
  var writer = null, buddy = null, curW = null, curId = "hanzi-target",
      round = 1, rounds = L.type === "word" ? 2 : 3;
  var statusEl = document.getElementById("writer-status");
  var skullsEl = document.getElementById("skulls");
  var go4 = document.getElementById("go4");
  var chars = L.type === "word" ? L.parts : [L.target, L.target, L.target];

  function updateSkulls() {
    var s = "";
    for (var i = 1; i <= rounds; i++) s += i < round ? "☠️" : "💀";
    skullsEl.textContent = s;
  }
  function makeCfg() {
    return {
      width: 300, height: 300, padding: 10,
      strokeColor: "#4a3560", radicalColor: "#7a4310",
      outlineColor: "#b7aa8a", drawingColor: "#3a2a5e",
      highlightColor: "#a3560d", leniency: 1.4,
      charDataLoader: function (ch, onComplete) {
        var src = "https://cdn.jsdelivr.net/npm/hanzi-writer-data@2.0/" + ch + ".json";
        fetch(src).then(function (r) { return r.json(); }).then(onComplete);
      },
    };
  }
  function initWriter() {
    writer = HanziWriter.create("hanzi-target", chars[0], makeCfg());
    if (L.type === "word") {
      document.getElementById("hanzi-target2").style.display = "";
      buddy = HanziWriter.create("hanzi-target2", chars[1], makeCfg());
    }
    startRound();
  }
  function startRound() {
    updateSkulls();
    var duo = !!buddy;
    if (duo) {
      writer.showOutline();
      buddy.showOutline();
      writer.setCharacter(chars[0]);
      buddy.setCharacter(chars[1]);
    } else if (round > 1) { writer.hideOutline(); } else { writer.showOutline(); }
    curW = duo && round === 2 ? buddy : writer;
    curId = duo && round === 2 ? "hanzi-target2" : "hanzi-target";
    statusEl.textContent = "Раунд " + round + " из " + rounds +
      (duo ? " — оба знака на доске, обводи «" + chars[round - 1] + "»."
        : round === 1 ? " — контур виден, просто веди мелом."
        : round === 2 ? " — теперь по памяти! Контур скрыт." : " — финальный раунд, ты почти Костик!");
    curW.quiz({
      onMistake: function (data) {
        statusEl.textContent = "Черта №" + (data.strokeNum + 1) + " уехала. Попробуй ещё раз — мел прощает.";
      },
      onCorrect: function () {
        QM.sfx.good();
      },
      onComplete: function () {
        round++;
        if (round > rounds) {
          updateSkulls();
          statusEl.textContent = "Плита выбита! Костик аплодирует костяшками.";
          go4.disabled = false;
          document.querySelectorAll(".bone-hand").forEach(function (h) {
            h.classList.remove("joy"); void h.offsetWidth; h.classList.add("joy");
          });
          var rect = document.getElementById(curId).getBoundingClientRect();
          QM.halloweenBurst(rect.left + rect.width / 2, rect.top + rect.height / 2);
          QM.sfx.flame();
          setTimeout(function () { QM.sfx.finish(); }, 450);
          QM.say("kostik", duo ? "Ха! Оба знака выбиты в камне — вот это рука мастера! Жми «сладость или гадость»!" : "Ха! Три раунда — и ни одной кривой черты! Вот это рука мастера, я аж подпрыгнул. Жми «сладость или гадость»!");
        } else {
          setTimeout(startRound, 700);
        }
      },
    });
  }
  function onPhase3() {
    if (!writer) { initWriter(); }
    QM.say("kostik", "Правило костяной руки: черта слева направо, сверху вниз. Горизонталь первой, вертикаль следом.");
  }
  document.getElementById("show-strokes").onclick = function () {
    QM.sfx.click(); curW.animateCharacter();
  };
  document.getElementById("reset-writer").onclick = function () {
    QM.sfx.click(); startRound();
  };

  /* ---- фаза 4: игра ---- */
  var guests = ["ghost", "pumpkin", "bat"];
  var guestSay = {
    ghost: "У-у-у... сладости передумал. Принеси знак!",
    pumpkin: "Тыква-джек слушает внимательно. Ну же!",
    bat: "Пи-и! Эхо на связи. Повтори звук — и получишь конфету.",
  };
  var rIdx = 0, tries = 0, solved = 0;
  var roundsTotal = L.game.length;

  function renderProgress() {
    var s = "";
    for (var i = 0; i < roundsTotal; i++) s += i < solved ? "🍬" : i === rIdx ? "🔸" : "▫️";
    document.getElementById("game-progress").textContent = s;
  }
  function renderRound() {
    renderProgress();
    if (rIdx >= roundsTotal) { ceremony(); return; }
    var r = L.game[rIdx];
    var guest = guests[rIdx % guests.length];
    var img = document.getElementById("guest-img");
    img.src = QM.BASE + "shared/characters/" + guest + ".svg";
    img.className = "guest-img";
    document.getElementById("guest-say").textContent = guestSay[guest];
    var sack = document.getElementById("sack");
    if (sack) { sack.classList.remove("pull"); void sack.offsetWidth; sack.classList.add("pull"); }
    document.getElementById("guest-note").textContent = "Люми достаёт из мешка вопрос " + (rIdx + 1) + " из " + roundsTotal;
    var p = document.getElementById("prompt");
    var isAudio = r.prompt === "audio";
    if (isAudio) {
      p.innerHTML = '<button class="play" id="rprompt"><span class="ico">🔊</span> Послушай</button>' +
        (r.kind === "audio2pinyin" || r.kind === "audio2word" ? '<div style="color:#b3a8d4;font-size:14px;margin-top:6px">выбери написание звука</div>'
          : '<div style="color:#b3a8d4;font-size:14px;margin-top:6px">выбери знак этого звука</div>');
      p.querySelector("#rprompt").onclick = function () { QM.playAudio(r.audio); };
      QM.playAudio(r.audio);
    } else if (r.kind === "glyph2pinyin" || r.kind === "word2pinyin") {
      p.innerHTML = '<span class="hanzi">' + r.prompt + "</span>";
    } else if (r.kind === "pinyin2glyph") {
      p.innerHTML = '<span class="py">' + r.prompt + "</span>";
    } else {
      p.innerHTML = "<span>" + r.prompt + "</span>";
    }
    var box = document.getElementById("candies");
    box.innerHTML = "";
    r.opts.forEach(function (opt) {
      var c = document.createElement("div");
      c.className = "candy";
      var isGlyphOpt = !/[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜüa-z]/i.test(opt) || /[\u4e00-\u9fff]/.test(opt);
      c.innerHTML = isGlyphOpt ? '<span class="hanzi">' + opt + "</span>" : opt;
      c.onclick = function () {
        tries++;
        if (opt === r.ans) {
          c.classList.add("good");
          img.classList.add("happy");
          QM.sfx.good();
          solved++;
          document.getElementById("guest-note").textContent = "Сладость! 🍬 Конфета летит в твой мешок.";
          setTimeout(function () { rIdx++; renderRound(); }, 850);
        } else {
          c.classList.add("bad");
          img.classList.add("angry");
          QM.sfx.bad();
          document.getElementById("guest-note").textContent = "Гадость! 👻 Гость швыряет паутину — пробуй ещё.";
          setTimeout(function () { c.classList.remove("bad"); img.classList.remove("angry"); }, 500);
        }
      };
      box.appendChild(c);
    });
  }
  function ceremony() {
    document.querySelector(".game-scene").style.display = "none";
    var cer = document.getElementById("ceremony");
    cer.style.display = "";
    var rect = cer.getBoundingClientRect();
    QM.sparks(window.innerWidth / 2, window.innerHeight / 2);
    QM.sfx.flame();
    setTimeout(function () { QM.sfx.finish(); }, 500);
    document.getElementById("cer-title").innerHTML =
      "Фонарь <span class='hanzi' style='font-size:40px;color:#ffd54f'>" + L.target + "</span> зажжён!";
    document.getElementById("cer-text").textContent =
      L.target + " = " + L.pinyin + " · " + L.meaning + ". Люми повесил его на крюк памяти. Фонарь " +
      L.num + " из " + L.total + " горит!";
    if (L.type === "glyph") QM.progress.light(L.target); else QM.progress.lightWord(L.target);
    QM.say("kostik", "Фонарь горит — значит, знак твой навсегда. Пойдём на карту, там ещё столько света нужно!");
  }
  function onPhase4() {
    QM.say("lumi", "Я Люми, и вот мой мешок вопросов! Гость за гостем, знак за знаком: отвечаешь верно — сладость, ошибаешься — гадость. Тяну первый вопрос...");
    renderRound();
  }

  showPh(1);
})();
"""


# ---------------------------------------------------------------- генерация
def main():
    data = build_lesson_data()
    ok = True
    audio_dir = ROOT / "audio"
    for item in data["glyphs"] + data["words"]:
        f = audio_dir / item["audio"]
        if not f.exists():
            print("НЕТ АУДИО:", item["audio"]); ok = False
    for t in (1, 2, 3, 4):
        if not (audio_dir / ("ma%d.mp3" % t)).exists():
            print("НЕТ АУДИО тона:", t); ok = False
    chars_dir = ROOT / "shared" / "characters"
    for f in ["wizard.svg", "kostik.svg", "lumi.svg", "echo.svg", "ghost.svg",
              "pumpkin.svg", "bat.svg", "kostik-portrait.svg", "lumi-portrait.svg",
              "echo-portrait.svg", "bone-hand-l.svg", "bone-hand-r.svg", "sack.svg"]:
        if not (chars_dir / f).exists():
            print("НЕТ SVG:", f); ok = False

    (ROOT / "shared" / "lesson-data.js").write_text(
        "window.QM_LESSONS = " + json.dumps(data, ensure_ascii=False) + ";\n",
        encoding="utf-8")

    for g in GLYPHS:
        d = ROOT / "lesson" / g["char"]
        d.mkdir(parents=True, exist_ok=True)
        item = next(x for x in data["glyphs"] if x["char"] == g["char"])
        (d / "index.html").write_text(lesson_html(item, "glyph"), encoding="utf-8")
    for w in WORDS:
        d = ROOT / "lesson" / w["word"]
        d.mkdir(parents=True, exist_ok=True)
        item = next(x for x in data["words"] if x["word"] == w["word"])
        (d / "index.html").write_text(lesson_html(item, "word"), encoding="utf-8")

    # модель курса для Stepik
    model = {
        "course_id": COURSE["id"], "course_title": COURSE["title"],
        "base_url": COURSE["base_url"],
        "summary": COURSE["summary"],
        "sections": [],
    }
    for sec in SECTIONS:
        lessons = []
        for les in sec["lessons"]:
            kind = les["kind"]
            if kind in ("glyph", "word"):
                src = next(x for x in (data["glyphs"] if kind == "glyph" else data["words"])
                           if x.get("char", x.get("word")) == les["ref"])
                title = "{0} [{1}] — {2}".format(les["ref"], src["pinyin"], src["meaning"])
                rel = "lesson/{0}/".format(les["ref"])
                lessons.append({"kind": kind, "title": title, "url": rel,
                                "data": src, "num": src["index"] + 1,
                                "total": TOTAL_LESSONS})
            else:
                info = SPECIAL_LESSONS[kind]
                lessons.append({"kind": kind, "title": info["title"],
                                "url": info.get("url", "")})
        model["sections"].append({"title": sec["title"], "lessons": lessons})
    model["story"] = STORY_PANELS
    model["finale"] = FINALE
    model["tones"] = TONES
    (ROOT / "build" / "course_model.json").write_text(
        json.dumps(model, ensure_ascii=False, indent=1), encoding="utf-8")

    pages = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "lesson").glob("*/index.html"))
    print("OK" if ok else "ЕСТЬ ОШИБКИ", "|", len(pages), "уроков |",
          "model:", len(model["sections"]), "секций")


if __name__ == "__main__":
    main()
