import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def create_feed(title, link, description, filename, articles):
    fg = FeedGenerator()
    fg.id(link)
    fg.title(title)
    fg.link(href=link, rel='alternate')
    fg.description(description)
    fg.language('id')

    for art in articles[:30]: # Limit 30 postingan per feed
        fe = fg.add_entry()
        fe.id(art['link'])
        fe.title(art['title'])
        fe.link(href=art['link'])
        fe.description(art['desc'])
        fe.pubDate(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
    
    fg.rss_file(filename)
    print(f"✅ Berhasil update {filename}")

def scrape_detik():
    url = "https://sport.detik.com/sepakbola/indeks"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    data = []
    for item in soup.select('article'):
        title_node = item.select_one('.media__title a')
        desc_node = item.select_one('.media__desc')
        if title_node:
            data.append({
                'title': title_node.get_text(strip=True),
                'link': title_node['href'],
                'desc': desc_node.get_text(strip=True) if desc_node else "Berita DetikSport"
            })
    return data

def scrape_bola_com():
    url = "https://www.bola.com/indonesia"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    data = []
    for item in soup.select('.articles--irregular-list--item'):
        title_node = item.select_one('.articles--irregular-list--title-link')
        if title_node:
            data.append({
                'title': title_node['title'],
                'link': title_node['href'],
                'desc': "Update berita terbaru dari Bola.com"
            })
    return data

def scrape_goal():
    url = "https://www.goal.com/id/berita/1"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    data = []
    for item in soup.select('li[data-testid="article-card"]'):
        title_node = item.select_one('h3')
        link_node = item.select_one('a')
        if title_node and link_node:
            data.append({
                'title': title_node.get_text(strip=True),
                'link': "https://www.goal.com" + link_node['href'],
                'desc': "Berita terbaru dari Goal.com"
            })
    return data

if __name__ == '__main__':
    # 1. Detik
    create_feed("Detik Sport Sepakbola", "https://sport.detik.com/sepakbola", "Info Bola Detik", "feed_detik.xml", scrape_detik())
    # 2. Bola.com
    create_feed("Bola.com", "https://www.bola.com", "Info Bola.com", "feed_bola.xml", scrape_bola_com())
    # 3. Goal.com
    create_feed("Goal.com Indonesia", "https://www.goal.com/id", "Info Goal.com", "feed_goal.xml", scrape_goal())
