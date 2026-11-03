#!/usr/bin/env python3
"""Vytvoří zkrácenou verzi prezentace v kratka/ z plné verze v assets/data.js.

Použití:  python3 tools/build-kratka.py

Vynechá slajdy uvedené v VYNECHAT (čísla podle plné verze), zbylé přečísluje
a zapíše kratka/data.js. Do kratka/index.html doplní počet slajdů a verzi assetů
z hlavního index.html. Plnou verzi nemění. Spouštějte po každé úpravě assets/data.js.
"""
import hashlib, json, re
from pathlib import Path

VYNECHAT = {7, 9, 12, 13, 14, 47, 51, 84, 90, 91, 92, 93, 102, 115, 118, 120, 124, 131, 132}

# úpravy jen pro zkrácenou verzi, podle čísla slajdu plné verze; None pole odstraní
UPRAVY = {
    99: {"title": "Modlitební knihy", "kind": "text", "images": None},  # bez ukázky Kancionálu 1659
}

# náhrady textu v odstavcích jen pro zkrácenou verzi: {slajd plné verze: [(původní, nový), …]}
NAHRADIT = {
    94: [(  # slajd se Zimmermannem (93) ve zkrácené verzi chybí
        "přičemž hájí stávající monarchistický řád panující v německých zemích. Podobně jako Zimmermann "
        "v předešlém případě pak varuje před vlivem Francie uplatňovaným prostřednictvím tajných jakobínů, "
        "republikánů a vůbec protistátních buřičů",
        "přičemž hájí stávající monarchistický řád panující v německých zemích a varuje před vlivem Francie "
        "uplatňovaným prostřednictvím tajných jakobínů, republikánů a vůbec protistátních buřičů",
    )],
}

root = Path(__file__).resolve().parent.parent
src = (root / "assets" / "data.js").read_text(encoding="utf-8")
slides = json.loads(src[src.index("["):src.rstrip().rindex("]") + 1])

out = []
for s in slides:
    if s["id"] in VYNECHAT:
        continue
    for k, v in UPRAVY.get(s["id"], {}).items():
        if v is None:
            s.pop(k, None)
        else:
            s[k] = v
    for old, new in NAHRADIT.get(s["id"], []):
        paras = s.get("paragraphs", [])
        hits = [i for i, p in enumerate(paras) if old in p]
        if len(hits) != 1:
            raise SystemExit(f"slajd {s['id']}: nahrazovaný text nenalezen ({len(hits)}×) — zkontrolujte NAHRADIT")
        paras[hits[0]] = paras[hits[0]].replace(old, new)
    s = dict(s, id=len(out) + 1)
    for im in s.get("images", []):
        im["src"] = "../" + im["src"]
    out.append(s)

body = json.dumps(out, ensure_ascii=False, indent=2)
data_ver = hashlib.sha1(body.encode("utf-8")).hexdigest()[:10]  # nová adresa při každé změně dat → žádná stará cache
head = ("// Zkrácená verze prezentace „Příběh písma“ — vygenerováno z assets/data.js\n"
        "// skriptem tools/build-kratka.py; neupravujte ručně, změny dělejte v plné verzi.\n"
        "// Vynechané slajdy plné verze: " + ", ".join(map(str, sorted(VYNECHAT))) + "\n")
(root / "kratka" / "data.js").write_text(
    head + "window.SLIDES = " + body + ";\n",
    encoding="utf-8", newline="\n")

# stránka: stejná jako hlavní index.html, jen s cestami o úroveň výš a vlastními daty
page = (root / "index.html").read_text(encoding="utf-8")
page = page.replace('href="assets/', 'href="../assets/').replace('src="assets/app.js', 'src="../assets/app.js')
page = re.sub(r'src="assets/data\.js\?v=[^"]*"', 'src="data.js?v=%s"' % data_ver, page)
page = re.sub(r'(<span id="countTotal">)\d+(</span>)', r"\g<1>%d\g<2>" % len(out), page)
(root / "kratka" / "index.html").write_text(page, encoding="utf-8", newline="\n")

print(f"kratka/: {len(out)} slajdů (vynecháno {len(slides) - len(out)} z {len(slides)})")
