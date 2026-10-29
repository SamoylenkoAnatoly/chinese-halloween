# -*- coding: utf-8 -*-
"""Генерация mp3 произношения для новых знаков и слов через edge-tts.

Запуск: python build/make_audio.py
Создаёт audio/<имя>.mp3 для всех записей data.py, удаляет mp3,
которые больше не нужны (кроме тональных ma1..ma4).
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edge_tts

from data import GLYPHS, WORDS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(ROOT, "audio")
VOICE = "zh-CN-XiaoxiaoNeural"
KEEP_EXTRA = {"ma1.mp3", "ma2.mp3", "ma3.mp3", "ma4.mp3"}


def items():
    out = []
    for g in GLYPHS:
        out.append((g["audio"], g["char"]))
    for w in WORDS:
        out.append((w["audio"], w["word"]))
    return out


async def gen(text, out_path, sem):
    async with sem:
        for attempt in range(3):
            try:
                com = edge_tts.Communicate(text, VOICE)
                await com.save(out_path)
                return True
            except Exception as e:
                print("  retry %d for %s: %s" % (attempt + 1, out_path, e))
                await asyncio.sleep(2)
        return False


async def main():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    wanted = items()
    sem = asyncio.Semaphore(3)
    ok = fail = 0
    for fname, text in wanted:
        out_path = os.path.join(AUDIO_DIR, fname)
        good = await gen(text, out_path, sem)
        size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
        if good and size > 1000:
            ok += 1
            print("OK  %-16s %-4s %6d bytes" % (fname, text, size))
        else:
            fail += 1
            print("FAIL %-16s %-4s" % (fname, text))
    keep = {f for f, _ in wanted} | KEEP_EXTRA
    removed = 0
    if fail == 0:
        for f in sorted(os.listdir(AUDIO_DIR)):
            if f.endswith(".mp3") and f not in keep:
                os.remove(os.path.join(AUDIO_DIR, f))
                removed += 1
        print("old unused mp3 removed: %d" % removed)
    else:
        print("FAILURES: old mp3 NOT removed")
    print("done: ok=%d fail=%d total_in_dir=%d"
          % (ok, fail, len([f for f in os.listdir(AUDIO_DIR) if f.endswith('.mp3')])))
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
