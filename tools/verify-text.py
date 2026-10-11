#!/usr/bin/env python3
"""Porovná text v assets/data.js s textovou vrstvou PDF exportu prezentace.

Použití:  python3 tools/verify-text.py "cesta/k/prezentaci.pdf"
Vyžaduje: pip install pymupdf

Kontroluje v obou směrech:
  1. každý řádek textu na webu musí být souvislým úsekem textu na odpovídající straně PDF,
  2. každé slovo ze strany PDF musí být na webu.
Ignoruje velikost písmen, mezery, pevné mezery, druh pomlčky a uvozovek
(web používá typografické úpravy). Štítky z designu (eyebrow, „Část I“) se nekontrolují.
Konec s kódem 1, pokud se text liší.
"""
import json, re, sys
from collections import Counter
from pathlib import Path

import fitz

root = Path(__file__).resolve().parent.parent
t = (root / "assets" / "data.js").read_text(encoding="utf-8")
slides = json.loads(t[t.index("["):t.rindex("]") + 1])
pdf = fitz.open(sys.argv[1])
if len(slides) != len(pdf):
    sys.exit("Počet slajdů (%d) se liší od počtu stran PDF (%d)." % (len(slides), len(pdf)))


def norm(x):
    x = x.replace(" ", " ").lower()
    x = re.sub(r"[“”„\"‟«»]", "", x)
    x = re.sub(r"[–—−‑]", "-", x)
    return re.sub(r"\s+", "", x)


def fields(s):
    out = [s["title"]]
    out += s.get("paragraphs", []) + s.get("quote", [])
    out += [s[k] for k in ("quoteAuthor", "org", "intro") if s.get(k)]
    out += [i["text"] for i in s.get("items", [])]
    out += [im.get("caption", "") for im in s.get("images", [])]
    if s.get("groupCaption"):
        out.append(s["groupCaption"])
    if s.get("table"):
        out += s["table"]["headers"] + [c for r in s["table"]["rows"] for c in r]
    return out


# Text, který PDF ořezává na okraji strany (v prezentaci přesahuje mimo slajd):
# {číslo strany: [(úsek v PDF, skutečný text)]}
CLIPPED = {24: [("ve vývoj latinky", "ve vývoji latinky")]}


def split_words(x):
    # PDF zalamuje i na pomlčce („1477-“ / „1478“), proto se slova dělí i na pomlčkách
    return [norm(w) for w in re.split(r"[\s\-–—]+", x) if norm(w)]


problems = []
for i, s in enumerate(slides):
    words = sorted(pdf[i].get_text("words"), key=lambda w: (w[5], w[6], w[7]))
    stream = norm("".join(w[4] for w in words))
    for a, b in CLIPPED.get(i + 1, []):
        stream = stream.replace(norm(a), norm(b))
    for text in fields(s):
        for line in (l for l in text.split("\n") if l.strip()):
            if norm(line) and norm(line) not in stream:
                problems.append("slajd %d: na webu, ale ne v PDF: %s" % (i + 1, line[:90]))
    have = Counter(k for text in fields(s) for k in split_words(text))
    pdf_words = [w[4] for w in pdf[i].get_text("words")]
    clipped_fix = {a.split()[1]: b.split()[1] for a, b in CLIPPED.get(i + 1, [])}
    for w in pdf_words:
        for k in split_words(clipped_fix.get(w, w)):
            if have[k] > 0:
                have[k] -= 1
            elif i != 0:  # strana 1 má v PDF písmo s mezerami mezi písmeny
                problems.append("slajd %d: v PDF, ale ne na webu: %s" % (i + 1, w))

print("\n".join(problems) if problems else "OK: text na webu odpovídá PDF (%d slajdů)." % len(slides))
sys.exit(1 if problems else 0)
