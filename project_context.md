# AI News Digest Bot — Project Context

> Dit document bewaart de context van dit project voor toekomstige chats met Claude. Plak of upload dit aan het begin van een nieuwe sessie zodat je niet hoeft uit te leggen waar je staat.

## Wie ben ik

- **Naam:** Julian
- **Werkt aan:** memecoin trading bot met een vriend (Solana + Jupiter + Grafana, 2-3x per week samen)
- **Wil daarnaast:** dagelijks (~30-60 min) zelf met AI bouwen om voorop te lopen op de massa
- **Skill level:** sterke frontend (HTML/CSS/JS/Liquid/JSON), Python is nieuw maar pikt 't snel op
- **Aanpak:** klein beginnen, snel werkend product, daarna iteratief uitbouwen
- **Editor:** VSCodium op Windows
- **Werkmap:** `C:\AI projecten\`

## Wat we bouwen

**AI News Digest Bot** — dagelijkse gefilterde AI-nieuwsdigest om "AI Report fatigue" op te lossen en bij te blijven zonder overweldigd te worden.

### Huidige stack

- Python 3.14
- `feedparser` voor RSS feeds
- `anthropic` SDK + `python-dotenv` voor Claude API
- Model: `claude-haiku-4-5` (goedkoop, snel, prima voor samenvatting)
- API key staat in `.env` (gitignored)

### Bestanden in projectmap

- `news.py` — hoofdscript
- `digest.html` — gegenereerde output (per run overschreven)
- `.env` — API key (NOOIT committen)
- `.gitignore` — `.env`, `__pycache__/`, `*.pyc`
- `test.py` — eerste hello-world (kan weg)

### Wat het script doet

1. Haalt artikelen op uit RSS feeds (TechCrunch AI, The Verge AI — 5 per feed)
2. Stuurt naar Claude met assistant prefill `{` om JSON af te dwingen
3. Claude filtert op "relevant voor wie wil voorlopen, geen hype"
4. Output: `digest.html` met dark mode, oranje accent (#d97757), cards per artikel + "overgeslagen" sectie

## Status dag 1 (afgerond)

- ✅ Python werkend op Windows
- ✅ VSCodium ingericht
- ✅ Anthropic account + €5 startkrediet + API key
- ✅ RSS scraping
- ✅ AI-filtering met JSON output
- ✅ HTML digest met eigen styling

## Roadmap (in volgorde van prioriteit)

**Korte termijn (deze week):**
- [ ] Meer feeds toevoegen (HackerNews AI tag? AI Report zelf via RSS?)
- [ ] Deduplicatie als hetzelfde verhaal in meerdere bronnen staat
- [ ] Prompt finetunen op basis van wat ik mis/te veel zie
- [ ] Output naar timestamped bestanden (archief opbouwen)

**Middellange termijn:**
- [ ] Autonoom maken via Windows Task Scheduler — elke ochtend 7:30
- [ ] Notificatie / email / Telegram als digest klaar is
- [ ] Eenvoudige web-frontend om door oude digests te bladeren

**Lange termijn (afgeleid van memecoin-project):**
- [ ] Zelfde architectuur (data → AI oordeel → output) toepassen op coin signals
- [ ] Overstappen naar Claude Code voor grotere bouwprojecten

## Hoe ik met Claude wil werken

- **Dagelijks korte sessies** (30-60 min)
- **Concrete stappen**, niet te veel uitleg vooraf
- **Recht door zee** als ik iets onhandig doe — zeg het
- **Push me niet** als ik aangeef door te willen, ook al gaat 't snel
- **Memory aan** — context tussen sessies in claude.ai mag onthouden worden
- **Eventueel Claude Code** voor zwaardere bouwsessies (nog niet geïnstalleerd)

## Belangrijke principes uit dag 1

- API keys NOOIT in code zelf — altijd `.env` + `.gitignore`
- Voor JSON-output altijd assistant prefill `{` gebruiken
- Defensief parsen: zoek eerste `{` en laatste `}`, knip ertussen
- Haiku 4.5 voor lichte taken, Sonnet 4.6 als Haiku te zwak filtert

---

*Laatst bijgewerkt: dag 1 — eerste werkende versie. Update dit document zelf na elke sessie of vraag Claude het te doen.*
