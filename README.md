# Příběh písma — interaktivní prezentace (Prezi styl)

Statická webová aplikace bez závislostí (vanilla HTML/CSS/JS), vytvořená z obsahu
PowerPointové prezentace k 550. výročí českého knihtisku (35 slajdů). Texty a obrázky
jsou beze změny, pořadí slajdů odpovídá originální prezentaci. Místo klasického
"slide vpřed/vzad" kamera plynule panoramuje a přibližuje/oddaluje mezi jednotlivými
"rámy" rozmístěnými na velkém plátně — efekt podobný Prezi.

## Struktura

```
prezi-vyroci-knihtisku/
├── index.html          # kostra stránky + HUD ovládání
├── assets/
│   ├── style.css        # veškerý vizuální styl
│   ├── app.js           # render slajdů, rozložení plátna, kamera, ovládání
│   ├── data.js           # obsahová data (texty, obrázky, tabulka) — zdroj pravdy
│   └── img/              # exportované obrázky z .pptx
└── README.md
```

## Ovládání

- šipky ← → / ↑ ↓, mezerník, Backspace — pohyb mezi slajdy (v pevném pořadí)
- kolečko myši / trackpad, swipe na dotykových zařízeních
- tlačítka prev/next v dolní liště
- `Home` / `End` — skok na první/poslední slajd
- `F` nebo tlačítko vpravo nahoře — fullscreen
- kliknutí na tmavé pozadí — přehled všech slajdů, kliknutím na slajd se do něj přiblížíte
- `Esc` — opuštění přehledu / fullscreenu

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
- Aplikace je plně responzivní — kamera se při změně velikosti okna přepočítá.
- Žádné externí závislosti kromě webfontu Google Fonts (Fraunces + Inter); pro plně
  offline nasazení lze fonty stáhnout a odkaz v `assets/style.css` nahradit lokálním.

## Úprava obsahu

Veškerý text a přiřazení obrázků je v `assets/data.js` — jde o pole objektů, jedno
na slajd. Pole `kind` určuje rozložení (`cover`, `quote`, `agenda`, `text`,
`specimen`, `figure`, `table`, `gallery`, `closing`), dále se používají `eyebrow`,
`title`, `paragraphs`, `images`, `groups`, `table`; `columns: true` rozdělí dlouhý
text do dvou sloupců a `width` určuje šířku rámu (volte tak, aby měl poměr stran
zhruba 16:9 — kamera se pak přiblíží nejvíc). Rozložení "plátna" (pozice jednotlivých
rámů) se počítá automaticky v `app.js` (`computeLayout`).

Při výměně obrázku pod stejným názvem zvyšte verzi v `ASSET_VERSION` (`app.js`) a
v odkazech `?v=` v `index.html`, ať prohlížeče nezobrazují starou cache.
