import feedparser
import os
import json
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
]

def fetch_articles(feed_urls, per_feed=5):
    articles = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        source = feed.feed.title
        for entry in feed.entries[:per_feed]:
            articles.append({
                "source": source,
                "title": entry.title,
                "summary": entry.get("summary", ""),
                "link": entry.link,
                "published": entry.get("published", ""),
            })
    return articles

def summarize_with_claude(articles):
    articles_text = "\n\n".join([
        f"[{a['source']}] {a['title']}\n{a['summary']}\nLink: {a['link']}"
        for a in articles
    ])

    prompt = f"""Filter deze AI-nieuws artikelen voor iemand die:
- Wil voorlopen op de rest, niet de hype volgen
- Geen tijd heeft voor fluff of marketing-praat
- Interesse heeft in praktische ontwikkelingen, nieuwe tools, concrete capabilities

Geef terug in dit JSON formaat:
{{
  "relevant": [
    {{"title": "korte titel", "why": "2-3 zinnen waarom relevant", "link": "url", "source": "bron"}}
  ],
  "skipped": [
    {{"title": "titel", "reason": "kort waarom overgeslagen"}}
  ]
}}

Beter 3 relevante dan 10 middelmatige.

Artikelen:
{articles_text}

Geef alleen het JSON-object terug, geen tekst eromheen."""

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "{"}
        ],
    )

    raw = "{" + response.content[0].text

    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1:
        print("DEBUG - Claude gaf terug:")
        print(raw)
        raise ValueError("Geen geldig JSON gevonden in response")

    json_str = raw[start:end+1]

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print("DEBUG - JSON parsing faalde. Claude gaf terug:")
        print(json_str)
        raise e

def build_html(digest):
    now = datetime.now().strftime("%d %B %Y — %H:%M")
    
    relevant_html = ""
    for item in digest.get("relevant", []):
        relevant_html += f"""
        <article class="card">
          <div class="source">{item['source']}</div>
          <h2>{item['title']}</h2>
          <p>{item['why']}</p>
          <a href="{item['link']}" target="_blank">Lees origineel →</a>
        </article>
        """
    
    skipped_html = ""
    for item in digest.get("skipped", []):
        skipped_html += f"""
        <li><strong>{item['title']}</strong> <span class="reason">— {item['reason']}</span></li>
        """
    
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Digest — {now}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #0f0f0f;
    color: #e5e5e5;
    line-height: 1.6;
    padding: 40px 20px;
  }}
  .container {{ max-width: 720px; margin: 0 auto; }}
  header {{ margin-bottom: 40px; border-bottom: 1px solid #2a2a2a; padding-bottom: 24px; }}
  h1 {{ font-size: 32px; font-weight: 700; letter-spacing: -0.5px; }}
  .date {{ color: #888; font-size: 14px; margin-top: 8px; }}
  .card {{
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
    transition: border-color 0.15s ease;
  }}
  .card:hover {{ border-color: #d97757; }}
  .source {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #d97757;
    margin-bottom: 8px;
    font-weight: 600;
  }}
  .card h2 {{ font-size: 20px; font-weight: 600; margin-bottom: 12px; }}
  .card p {{ color: #b8b8b8; margin-bottom: 16px; }}
  .card a {{ color: #d97757; text-decoration: none; font-size: 14px; font-weight: 500; }}
  .card a:hover {{ text-decoration: underline; }}
  .skipped-section {{
    margin-top: 48px;
    padding-top: 24px;
    border-top: 1px solid #2a2a2a;
  }}
  .skipped-section h3 {{
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #666;
    margin-bottom: 16px;
  }}
  .skipped-section ul {{ list-style: none; }}
  .skipped-section li {{ color: #888; font-size: 14px; margin-bottom: 8px; }}
  .reason {{ color: #555; }}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>AI Digest</h1>
    <div class="date">{now}</div>
  </header>
  <main>
    {relevant_html}
  </main>
  <section class="skipped-section">
    <h3>Overgeslagen</h3>
    <ul>{skipped_html}</ul>
  </section>
</div>
</body>
</html>"""

def send_to_telegram(digest):
    import requests
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("⚠️ Telegram niet geconfigureerd, sla over")
        return
    
    lines = [f"*🤖 AI Digest — {datetime.now().strftime('%d %b %H:%M')}*\n"]
    
    for i, item in enumerate(digest.get("relevant", []), 1):
        lines.append(f"*{i}. {item['title']}*")
        lines.append(f"{item['why']}")
        lines.append(f"[Lees origineel]({item['link']})\n")
    
    skipped = digest.get("skipped", [])
    if skipped:
        lines.append(f"_Overgeslagen: {len(skipped)} artikelen_")
    
    message = "\n".join(lines)
    
    if len(message) > 4000:
        message = message[:4000] + "\n\n_(ingekort)_"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(url, json={
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    })
    
    if response.ok:
        print("✅ Verstuurd naar Telegram")
    else:
        print(f"❌ Telegram error: {response.text}")

if __name__ == "__main__":
    print("Nieuws ophalen...")
    articles = fetch_articles(FEEDS)
    print(f"{len(articles)} artikelen opgehaald. Claude filtert...")
    
    digest = summarize_with_claude(articles)
    print(f"Relevant: {len(digest.get('relevant', []))} | Overgeslagen: {len(digest.get('skipped', []))}")
    
    html = build_html(digest)
    
    with open("digest.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("\n✅ digest.html aangemaakt. Open 'm in je browser.")

    send_to_telegram(digest)   # ← deze regel moet erbij staan