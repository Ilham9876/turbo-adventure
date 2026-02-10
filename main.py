import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import time
import uuid

# Headers lengkap biar gak diblokir web berita
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
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
        print(f"⚠️ {filename} Gagal narik berita, cek koneksi/selector!")
        return

    for art in articles[:30]:
        fe = fg.add_entry()
        fe.id(art['link'])
        fe.title(art['title'])
        fe.link(href=art['link'])
        fe.description(art['desc'])
        # Tambahan biar muncul gambar di RSS Reader
        if art.get('img'):
            fe.enclosure(art['img'], 0, 'image/jpeg')
        fe.pubDate(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
    
    fg.rss_file(filename)
    print(f"✅ {filename} sukses di-update!")

def scrape_bola_com():
    url = "https://www.bola.com/"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        data = []
        
        # Pake CSS Selector hasil riset lo yang tajam itu!
        selectors = '.article-video-section__list-text-title, .article-snippet__title-text, .article-snippet_headline .article-snippet__title-link'
        items = soup.select(selectors)
        
        for item in items:
            # Ambil link dari parent atau elemen itu sendiri
            parent_a = item if item.name == 'a' else item.find_parent('a')
            
            if parent_a and parent_a.get('href'):
                title = item.get_text(strip=True)
                link = parent_a['href']
                
                # Coba cari gambar biar feed lo gak ngebosenin
                img_tag = parent_a.find_parent().find('img') if parent_a.find_parent() else None
                img_url = ""
                if img_tag:
                    img_url = img_tag.get('data-src') or img_tag.get('src') or ""

                data.append({
                    'title': title,
                    'link': link,
                    'desc': f"Berita Bola.com: {title}",
                    'img': img_url
                })
        return data
    except Exception as e:
        print(f"Error Bola.com: {e}")
        return []

def scrape_detik():
    url = "https://sport.detik.com/sepakbola/indeks"
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        data = []
        for item in soup.select('article'):
            t = item.select_one('.media__title a')
            if t:
                data.append({'title': t.get_text(strip=True), 'link': t['href'], 'desc': "Update DetikSport"})
        return data
    except: return []

def scrape_goal():
    url = "https://www.goal.com/id/berita/1"
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        data = []
        for item in soup.select('li[data-testid="article-card"]'):
            t, l = item.select_one('h3'), item.select_one('a')
            if t and l:
                full_link = l['href'] if l['href'].startswith('http') else "https://www.goal.com" + l['href']
                data.append({'title': t.get_text(strip=True), 'link': full_link, 'desc': "Update Goal.com"})
        return data
    except: return []

if __name__ == '__main__':
    create_feed("Bola.com", "https://www.bola.com", "Info Bola Terkini", "feed_bola.xml", scrape_bola_com())
    create_feed("Detik Sport", "https://sport.detik.com/sepakbola", "News Detik", "feed_detik.xml", scrape_detik())
    create_feed("Goal.com", "https://www.goal.com/id", "News Goal", "feed_goal.xml", scrape_goal())
