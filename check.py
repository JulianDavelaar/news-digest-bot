import feedparser

url = "https://techcrunch.com/category/artificial-intelligence/feed/"   # pak 'm uit je feed_urls lijst
feed = feedparser.parse(url)

print("Aantal artikelen:", len(feed.entries))
print("HTTP-status:", feed.get("status"))
print("Parse-fout?:", feed.bozo)
if feed.bozo:
    print("Foutmelding:", feed.bozo_exception)
if feed.entries:
    entry = feed.entries[0]
    print("Velden:", list(entry.keys()))
    print("Lengte summary:", len(entry.get("summary", "")))
    if "content" in entry:
        print("Lengte content:", len(entry.content[0].value))