import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import time
import uuid

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36'
}

def create_feed(title, link, description, filename, articles):
    fg = FeedGenerator()
    fg.id(link)
    fg.title(title)
    fg.link(href=link, rel='alternate')
    fg.description(description)
    fg.language('id')
    fg.lastBuildDate(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))

    if not articles:
        print(f"⚠️ Peringatan: Data artikel untuk {filename} kosong!")
        return

    for art in articles[:30]:
        fe = fg.add_entry()
        fe.id(art.get('link', str(uuid.uuid4()))) # Pake UUID kalo link bermasalah
        fe.title(art['title'])
        fe.link(href=art['link'])
        fe.description(art['desc'])
        # Format tanggal harus bener-bener standar RFC 822
        fe.pubDate(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
    
    fg.rss_file(filename)
    print(f"✅ Berhasil update {filename} dengan {len(articles)} berita.")

def scrape_detik():
    url = "https://sport.detik.com/sepakbola/indeks"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        data = []
        for item in soup.select('article'):
            t = item.select_one('.media__title a')
            d = item.select_one('.media__desc')
            if t:
                data.append({'title': t.get_text(strip=True), 'link': t['href'], 'desc': d.get_text(strip=True) if d else "Update Berita Detik"})
        return data
    except: return []

def scrape_bola_com():
    # Pake URL berita terbaru biar selector-nya lebih gampang ditembus
    url = "https://www.bola.com/indonesia"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        data = []
        # Update selector khusus Bola.com
        for item in soup.find_all('article', class_='articles--irreguler-list--item', limit=30):
            t = item.find('a', class_='articles--irreguler-list--title-link')
            if t:
                data.append({'title': t['title'], 'link': t['href'], 'desc': "Update liga indonesia dan dunia dari Bola.com"})
        return data
    except: return []

def scrape_goal():
    url = "https://www.goal.com/id/berita/1"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        data = []
        for item in soup.select('li[data-testid="article-card"]'):
            t = item.select_one('h3')
            l = item.select_one('a')
            if t and l:
                full_link = l['href'] if l['href'].startswith('http') else "https://www.goal.com" + l['href']
                data.append({'title': t.get_text(strip=True), 'link': full_link, 'desc': "Berita Sepakbola Internasional Goal.com"})
        return data
    except: return []

if __name__ == '__main__':
    create_feed("Detik Sport Sepakbola", "https://sport.detik.com/sepakbola", "Info Bola Terupdate", "feed_detik.xml", scrape_detik())
    create_feed("Bola.com", "https://www.bola.com", "Portal Berita Bola.com", "feed_bola.xml", scrape_bola_com())
    create_feed("Goal.com Indonesia", "https://www.goal.com/id", "Berita Dunia Goal.com", "feed_goal.xml", scrape_goal())
