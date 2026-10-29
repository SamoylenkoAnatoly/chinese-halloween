/* Двор Тихой Луны — общий движок */
(function () {
  "use strict";

  var QM = (window.QM = {});

  QM.TONE_COLORS = { 1: "#e64533", 2: "#ff8c2b", 3: "#29b6f6", 4: "#86c232", 0: "#bfe8e0" };
  QM.TONE_NAMES = { 1: "1-й тон", 2: "2-й тон", 3: "3-й тон", 4: "4-й тон", 0: "нейтральный" };
  QM.BASE = (function () {
    var el = document.querySelector("meta[name=qm-base]");
    var fromMeta = el ? el.getAttribute("content") : "";
    var css = document.querySelector('link[href$="spooky.css"]');
    if (css) {
      var href = css.getAttribute("href");
      return href.replace(/shared\/spooky\.css.*$/, "");
    }
    return fromMeta;
  })();

  /* ---------- прогресс ---------- */
  var KEY = "quiet-moon-progress";
  var state = null;
  function load() {
    if (state) return state;
    try { state = JSON.parse(localStorage.getItem(KEY) || "{}"); }
    catch (e) { state = {}; }
    state.lit = state.lit || {};
    state.words = state.words || {};
    state.tones = !!state.tones;
    state.story = !!state.story;
    return state;
  }
  QM.progress = {
    lit: function (ch) { return !!load().lit[ch]; },
    light: function (ch) { var s = load(); s.lit[ch] = true; save(s); },
    word: function (w) { return !!load().words[w]; },
    lightWord: function (w) { var s = load(); s.words[w] = true; save(s); },
    tones: function () { return load().tones; },
    markTones: function () { var s = load(); s.tones = true; save(s); },
    story: function () { return load().story; },
    markStory: function () { var s = load(); s.story = true; save(s); },
    litCount: function () {
      var s = load(), n = 0;
      Object.keys(s.lit).forEach(function (k) { if (s.lit[k]) n++; });
      Object.keys(s.words).forEach(function (k) { if (s.words[k]) n++; });
      return n;
    },
    reset: function () { localStorage.removeItem(KEY); state = null; },
  };
  function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {} }

  /* ---------- SFX (WebAudio) ---------- */
  var actx = null;
  function ctx() {
    if (!actx) {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return null;
      actx = new AC();
    }
    if (actx.state === "suspended") { actx.resume(); }
    return actx;
  }
  function tone(freq, dur, type, vol, delay, slide) {
    var c = ctx(); if (!c) return;
    var t0 = c.currentTime + (delay || 0);
    var o = c.createOscillator(), g = c.createGain();
    o.type = type || "square";
    o.frequency.setValueAtTime(freq, t0);
    if (slide) o.frequency.exponentialRampToValueAtTime(slide, t0 + dur);
    g.gain.setValueAtTime(vol || 0.12, t0);
    g.gain.exponentialRampToValueAtTime(0.001, t0 + dur);
    o.connect(g); g.connect(c.destination);
    o.start(t0); o.stop(t0 + dur + 0.02);
  }
  QM.sfx = {
    click: function () { tone(520, 0.06, "square", 0.08); },
    good: function () { tone(392, 0.1, "square", 0.1); tone(523, 0.1, "square", 0.1, 0.09); tone(659, 0.16, "square", 0.1, 0.18); },
    bad: function () { tone(196, 0.22, "sawtooth", 0.1, 0, 130); },
    flame: function () { tone(180, 0.5, "triangle", 0.12, 0, 720); tone(1200, 0.3, "sine", 0.05, 0.15); },
    ghost: function () { tone(660, 0.7, "sine", 0.05, 0, 330); },
    finish: function () {
      [523, 659, 784, 1046].forEach(function (f, i) { tone(f, 0.16, "square", 0.1, i * 0.11); });
    },
  };

  /* ---------- аудио mp3 ---------- */
  var currentAudio = null;
  QM.playAudio = function (file, slow) {
    if (currentAudio) { currentAudio.pause(); currentAudio = null; }
    var a = new Audio(QM.BASE + "audio/" + file);
    if (slow) a.playbackRate = 0.65;
    currentAudio = a;
    return a.play().catch(function () {
      console.warn("Не удалось загрузить аудио: " + file);
    });
  };

  /* ---------- компаньон ---------- */
  var AVATARS = {
    kostik: "shared/characters/kostik-portrait.svg",
    koko: "shared/characters/wizard.svg",
    lumi: "shared/characters/lumi-portrait.svg",
    echo: "shared/characters/echo-portrait.svg",
  };
  var NAMES = { kostik: "Костик", koko: "Коко", lumi: "Люми", echo: "Эхо" };
  QM.say = function (who, lines, done) {
    var bar = document.getElementById("companion");
    if (!bar) return;
    bar.innerHTML =
      '<img class="ava" alt="" src="' + QM.BASE + AVATARS[who] + '">' +
      '<div class="bubble"><span class="who">' + NAMES[who] + ':</span><span id="comp-line"></span></div>';
    var el = document.getElementById("comp-line");
    var arr = Array.isArray(lines) ? lines : [lines];
    var i = 0;
    function showNext() {
      if (i >= arr.length) {
        if (done) done();
        return;
      }
      el.innerHTML = arr[i];
      i++;
    }
    showNext();
    bar.onclick = function () { QM.sfx.click(); showNext(); };
    bar.style.pointerEvents = "auto";
    bar.title = "Клик — дальше";
  };
  QM.clearSay = function () {
    var bar = document.getElementById("companion");
    if (bar) { bar.innerHTML = ""; bar.onclick = null; }
  };

  /* ---------- искры ---------- */
  QM.sparks = function (x, y, colors, count) {
    colors = colors || ["#ffd54f", "#ff8c2b", "#bfe8e0"];
    count = count || 26;
    for (var i = 0; i < count; i++) {
      var s = document.createElement("div");
      s.className = "spark";
      s.style.left = x + (Math.random() * 80 - 40) + "px";
      s.style.top = y + (Math.random() * 30 - 10) + "px";
      s.style.background = colors[i % colors.length];
      s.style.animationDelay = Math.random() * 0.4 + "s";
      document.body.appendChild(s);
      (function (el) { setTimeout(function () { el.remove(); }, 2200); })(s);
    }
  };

  /* ---------- тональный контур ---------- */
  var CONTOURS = {
    1: "M 20 32 L 180 32",
    2: "M 20 92 Q 70 88 100 62 T 180 30",
    3: "M 30 56 Q 55 78 75 92 T 130 78 Q 160 62 180 52",
    4: "M 25 28 Q 100 55 175 96",
    0: "M 20 62 Q 100 58 180 62",
  };
  QM.drawTone = function (container, toneN, animate) {
    var box = typeof container === "string" ? document.querySelector(container) : container;
    if (!box) return;
    var col = QM.TONE_COLORS[toneN];
    var d = CONTOURS[toneN] || CONTOURS[0];
    var anim = animate === false ? "" :
      '<animate attributeName="stroke-dashoffset" from="400" to="0" dur="0.8s" fill="freeze"/>';
    box.innerHTML =
      '<svg viewBox="0 0 200 120" preserveAspectRatio="none">' +
      '<path d="M 0 0 H 200 M 0 60 H 200 M 0 120 H 200" stroke="#241744" stroke-width="1" stroke-dasharray="3 5"/>' +
      '<path d="' + d + '" fill="none" stroke="' + col + '" stroke-width="7" stroke-linecap="round" ' +
      'stroke-dasharray="400" stroke-dashoffset="0">' + anim + "</path></svg>";
  };

  /* ---------- типовая кнопка звука ---------- */
  QM.bindPlay = function (btn, file, slow) {
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      QM.sfx.click();
      QM.playAudio(file, slow);
    });
  };

  QM.esc = function (s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  };
})();
