# AI News Digest Bot

Een autonome bot die dagelijks AI-nieuws ophaalt, filtert via Claude, en als digest naar Telegram stuurt.

## Wat het doet

1. Haalt artikelen op uit RSS-feeds (TechCrunch AI, The Verge AI)
2. Stuurt naar Claude Haiku 4.5 voor filtering op relevantie
3. Genereert een gestylede `digest.html`
4. Pusht notificatie naar Telegram

Kosten: ~€0,001 per run. Draait dagelijks via Windows Task Scheduler.

## Stack

- Python 3.14
- `feedparser`, `anthropic`, `python-dotenv`, `requests`
- Claude Haiku 4.5 met JSON output (assistant prefill techniek)
- Telegram Bot API

## Setup

### 1. Clone

```bash
git clone https://github.com/JulianDavelaar/news-digest-bot.git
cd news-digest-bot
```

### 2. Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment variables

Maak een `.env` bestand in de root:
ANTHROPIC_API_KEY=sk-ant-...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...

- **Anthropic key**: maak aan op https://console.anthropic.com
- **Telegram bot**: chat met @BotFather → `/newbot`
- **Chat ID**: open `https://api.telegram.org/bot<TOKEN>/getUpdates` na een bericht naar je bot te sturen

### 4. Test

```bash
python news.py
```

## Autonoom draaien (Windows)

1. Pas paden in `run_bot.bat` aan naar jouw lokale locatie
2. Open Task Scheduler → Create Basic Task
3. Trigger: Daily, gewenste tijd
4. Action: Start program → wijs naar `run_bot.bat`
5. Start in: projectmap-pad

## Bestanden

- `news.py` — hoofdscript
- `run_bot.bat` — Windows batch wrapper voor Task Scheduler
- `digest.html` — gegenereerde output (per run overschreven)
- `log.txt` — output van scheduled runs
- `.env` — secrets (niet in git)