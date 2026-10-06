# Příběh písma — interaktivní prezentace

Statická webová aplikace bez závislostí (vanilla HTML/CSS/JS), vytvořená z obsahu
PowerPointové prezentace k 550. výročí českého knihtisku (34 slajdů). Texty a obrázky
jsou beze změny, pořadí slajdů odpovídá originální prezentaci.

## Vizuální systém „Rubrika“

Papír, inkoust a jediná rumělková červená — odkaz na rubrikaci rukopisů a raných tisků.
Designová filozofie je v [`design/RUBRIKA-design-philosophy.md`](design/RUBRIKA-design-philosophy.md),
key visual v `design/rubrika-key-visual.png`.

- **Paleta:** titulní slajd inkoust `#17150F`; ostatní slajdy černé pozadí `#000000`, bílé písmo, akcent rumělka `#E4513A`, grafit `#A3A3A3`
- **Písma** (self-hosted, SIL OFL 1.1, `assets/fonts/`): Instrument Serif (titulky),
  Instrument Sans (text), IBM Plex Mono (inventární čísla, pagina)
- **Scéna 1920 × 1080** se celá škáluje do okna/iframu — rozvržení je na každé obrazovce stejné.
- **Automatická sazba obrázků:** `app.js` pro každý slajd vyzkouší šířky textového sloupce,
  velikosti písma a rozložení obrázků do řádků/sloupců a vybere variantu s největšími
  obrázky při čitelném textu. Obrázky se nezvětšují nad 3,4× zdrojové velikosti.
- Kliknutím na obrázek se otevře zvětšený náhled s popiskem.

## Ovládání

- šipky ← → / ↑ ↓, mezerník, PageUp/PageDown — pohyb mezi slajdy
- kolečko myši / trackpad, swipe na dotykových zařízeních
- `Home` / `End` — první/poslední slajd
- `G` nebo tlačítko mřížky — přehled všech slajdů
- `F` nebo tlačítko vpravo dole — celá obrazovka, `Esc` — zavření přehledu/náhledu
- přímý odkaz na slajd: `index.html#14`

## Embedování do jiného webu

```html
<iframe
  src="https://vaše-doména.cz/prezi-vyroci-knihtisku/"
  style="width:100%; aspect-ratio:16/9; border:0;"
  allow="fullscreen"
  allowfullscreen
  title="Příběh písma — 550. výročí českého knihtisku">
</iframe>
```

- `allowfullscreen` (a `allow="fullscreen"`) je nutné pro funkční tlačítko fullscreen uvnitř iframe.
- Scéna drží poměr 16:9; mimo něj se doplní barvou aktuálního slajdu. Nejlépe vypadá
  v iframu 16:9, na výšku orientovaném mobilu se zobrazí zmenšeně.
- Žádné externí závislosti — písma jsou součástí repozitáře.

## Úprava obsahu

Veškerý text a přiřazení obrázků je v `assets/data.js` — jde o pole objektů, jedno
na slajd, s poli `kind`, `eyebrow`, `title`, `paragraphs`, `images` (u obrázku `caption`),
případně `groupCaption`, `table`. Druhy slajdů: `cover` (obal, volitelně `org` a `intro`), `quote`
(citát s obrázkem), `agenda` (`items`), `text`, `figure`/`gallery` (text a obrázky),
`table`, `closing`. Rozložení každého slajdu se počítá automaticky v `app.js`
(`buildText`, `buildFigure`, `arrange`): dlouhý text se sám rozdělí do dvou sloupců
přes celou stránku, obrázky se uspořádají do největší možné plochy. Není třeba nic
ručně polohovat.

Při výměně obrázku pod stejným názvem zvyšte verzi v `ASSET_VERSION` (`app.js`) a v
odkazech `?v=` v `index.html`, ať prohlížeče nezobrazují starou cache.

## Sazba

Při vykreslení (`orphans()` v `app.js`) se do textu vkládají pevné mezery: za jednopísmennými
předložkami a spojkami (k, s, v, z, o, u, a, i), v tisícových skupinách („3 000“), mezi
číslem a měnou/jednotkou/slovem („3 000 Kč“, „52 barevných“, „15. století“), u zkratek
(IČ, č., sv., obr.), titulů (Mgr., Bc.) a iniciál („T. G. Masaryk“). Automatické dělení
slov je vypnuté.

## Kontrola textu proti PDF

`python3 tools/verify-text.py "prezentace.pdf"` (vyžaduje `pip install pymupdf`) porovná
text v `assets/data.js` s textovou vrstvou PDF v obou směrech a vypíše každou odchylku.
