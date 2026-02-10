import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import time
import uuid

# Headers biar gak diblokir sama website berita
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
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
        print(f"⚠️ Waduh, artikel {filename} kosong bro!")
        return

    for art in articles[:30]: # Limit 30 berita biar gak kepenuhan
        fe = fg.add_entry()
        fe.id(art.get('link', str(uuid.uuid4())))
        fe.title(art['title'])
        fe.link(href=art['link'])
        fe.description(art['desc'])
        fe.pubDate(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
    
    fg.rss_file(filename)
    print(f"✅ Mantap! {filename} beres dengan {len(articles)} berita.")

def scrape_detik():
    url = "https://sport.detik.com/sepakbola/indeks"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        data = []
        for item in soup.select('article'):
            t = item.select_one('.media__title a')
            d = item.select_one('.media__desc')
            if t:
                data.append({
                    'title': t.get_text(strip=True), 
                    'link': t['href'], 
                    'desc': d.get_text(strip=True) if d else "Berita Sepakbola DetikSport"
                })
        return data
    except: return []

def scrape_bola_com():
    url = "https://www.bola.com/indonesia"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        data = []
        # Menggunakan class 'irreguler' sesuai struktur web aslinya
        articles = soup.find_all('article', class_='articles--irreguler-list--item')
        for item in articles:
            t_node = item.find('a', class_='articles--irreguler-list--title-link')
            d_node = item.find('div', class_='articles--irreguler-list--summary')
            if t_node:
                data.append({
                    'title': t_node.get('title') or t_node.get_text(strip=True),
                    'link': t_node.get('href'),
                    'desc': d_node.get_text(strip=True) if d_node else "Update terbaru dari Bola.com"
                })
        return data
    except: return []

def scrape_goal():
    url = "https://www.goal.com/id/berita/1"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        data = []
        for item in soup.select('li[data-testid="article-card"]'):
            t = item.select_one('h3')
            l = item.select_one('a')
            if t and l:
                full_link = l['href'] if l['href'].startswith('http') else "https://www.goal.com" + l['href']
                data.append({
                    'title': t.get_text(strip=True), 
                    'link': full_link, 
                    'desc': "Update Goal.com Indonesia"
                })
        return data
    except: return []

if __name__ == '__main__':
    # Eksekusi semua sumber
    create_feed("Detik Sport Sepakbola", "https://sport.detik.com/sepakbola", "Info Bola Detik", "feed_detik.xml", scrape_detik())
    create_feed("Bola.com", "https://www.bola.com", "Portal Berita Bola.com", "feed_bola.xml", scrape_bola_com())
    create_feed("Goal.com Indonesia", "https://www.goal.com/id", "Berita Dunia Goal.com", "feed_goal.xml", scrape_goal())
