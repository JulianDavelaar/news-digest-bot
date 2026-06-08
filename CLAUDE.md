# CLAUDE.md — AI News Digest Bot

Context voor Claude (en mezelf) bij het werken aan dit project. Lees dit eerst.

## Wat het is

Autonome bot die dagelijks AI-nieuws ophaalt uit RSS-feeds, met Claude filtert op
relevantie, per relevant artikel de volledige tekst ophaalt en samenvat in bullets,
en het resultaat als `digest.html` wegschrijft + naar Telegram pusht.

Doel: "AI Report fatigue" oplossen — bijblijven zonder overweldigd te worden.
Kosten: ~€0,001–0,01 per run (Haiku 4.5).

## Stack

- **Python 3.14** (Windows)
- **feedparser** — RSS ophalen
- **trafilatura** — volledige artikeltekst van de pagina extraheren
- **anthropic** SDK — Claude `claude-haiku-4-5`
- **python-dotenv** — secrets uit `.env`
- **requests** — Telegram Bot API
- Pinned versies in `requirements.txt`.

## Mappenstructuur

```
news-digest-bot/
├── news.py            # hoofdscript (alle logica)
├── requirements.txt   # gepinde dependencies
├── run_bot.bat        # Windows-wrapper voor Task Scheduler
├── digest.html        # gegenereerde output (per run overschreven, gitignored)
├── log.txt            # output van scheduled runs (gitignored)
├── .env               # secrets — NOOIT committen (gitignored)
├── .gitignore         # .env, __pycache__/, *.pyc, log.txt, digest.html
├── README.md          # publieke setup-uitleg
├── project_context.md # achtergrond/roadmap van het project
└── CLAUDE.md          # dit bestand
```

`test.py` en `check.py` zijn losse scratch-/testbestanden, geen onderdeel van de pipeline.

## Pipeline (news.py)

1. `fetch_articles(feeds, per_feed=5)` — RSS → lijst artikelen (source, title, summary/teaser, link, published)
2. `summarize_with_claude(articles)` — Haiku filtert → `{"relevant": [...], "skipped": [...]}`
3. `enrich_with_bullets(digest, articles)` — alleen voor **relevante** artikelen:
   - `fetch_full_text(url, max_chars=3000)` — trafilatura haalt + truncet de paginatekst
   - `summarize_article_bullets(title, text)` — Haiku → 2-3 bullets met kerninfo
   - Graceful fallback op de RSS-teaser als tekst < ~200 tekens of ophalen faalt
4. `build_html(digest)` — dark-mode HTML met bullets onder de titel → `digest.html`
5. `send_to_telegram(digest)` — Markdown-melding met bullets (overgeslagen in `--test`)

## Draaien

```bash
# normale run (beide feeds + Telegram)
set PYTHONIOENCODING=utf-8
python news.py

# test-modus: alleen eerste feed, GEEN Telegram-melding
python news.py --test
```

Autonoom: `run_bot.bat` (zet `PYTHONIOENCODING=utf-8`, draait `news.py`, logt naar
`log.txt`) via Windows Task Scheduler — dagelijks ~7:30. Pas het pad in de `.bat`
aan je lokale locatie aan.

Dependencies installeren: `pip install -r requirements.txt`.

## Conventies (belangrijk — niet breken)

- **Secrets alleen in `.env`**, nooit hardcoden. Keys: `ANTHROPIC_API_KEY`,
  `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`. `.env` staat in `.gitignore`.
- **`PYTHONIOENCODING=utf-8`** vóór elke run (emoji + accenten in output op Windows-console).
  Staat al in `run_bot.bat`; bij handmatig draaien zelf zetten.
- **Assistant-prefill voor JSON**: elke Claude-call eindigt op
  `{"role": "assistant", "content": "{"}` om schone JSON af te dwingen. De response
  wordt voorafgegaan door `"{"` (`raw = "{" + response.content[0].text`).
- **Defensieve JSON-parsing**: knip van de eerste `{` tot de laatste `}` voordat je
  `json.loads` draait. Filterstap raist bij mislukking; bullet-stap valt stil terug
  op een lege lijst.
- **Kosten/tokens laag houden**: volledige tekst alleen voor gefilterde artikelen,
  getrunceerd tot ~3000 tekens vóór verzending naar Haiku.
- **Graceful fallback overal**: de bot mag nooit crashen op een losse feed/pagina —
  bij te weinig tekst terugvallen op de RSS-teaser.
- **Model**: `claude-haiku-4-5` voor alle calls (goedkoop/snel). Sonnet alleen als
  Haiku merkbaar te zwak filtert.

## Bij wijzigen

- Nieuwe dependency? Pin 'm in `requirements.txt`.
- Test eerst met `python news.py --test` (één feed, geen Telegram-spam) voordat je
  een volledige run doet.
- Laat bestaande RSS-, filter-, prefill-, HTML- en Telegram-logica intact tenzij de
  taak er expliciet om vraagt.
