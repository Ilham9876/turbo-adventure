import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import time

def scrape_kompas_bola():
    # Pake URL terpopuler biasanya lebih stabil strukturnya
    url = "https://bola.kompas.com/search" 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []

        # Mencari semua link yang ada di dalam h3 dengan class common
        # Ini struktur yang lebih umum di Kompas
        for item in soup.select('.article__list'):
            title_node = item.select_one('.article__title a')
            desc_node = item.select_one('.article__excerpt')
            
            if title_node:
                title = title_node.get_text(strip=True)
                link = title_node['href']
                desc = desc_node.get_text(strip=True) if desc_node else "Berita terbaru dari Kompas Bola."
                
                articles.append({
                    'title': title,
                    'link': link,
                    'desc': desc
                })
        
        print(f"Berhasil dapet {len(articles)} berita!")
        return articles
    except Exception as e:
        print(f"Waduh, error pas scraping: {e}")
        return []

def generate_rss():
    articles = scrape_kompas_bola()
    
    if not articles:
        print("Yah, list beritanya kosong. Coba cek strukturnya lagi.")
        return

    fg = FeedGenerator()
    fg.id('https://github.com/lo/repo-rss')
    fg.title('Kompas Bola - Live Update')
    fg.author({'name': 'Gen Z Innovator'})
    fg.link(href='https://bola.kompas.com/', rel='alternate')
    fg.description('Update otomatis berita bola biar gak ketinggalan jaman.')
    fg.language('id')

    for berita in articles:
        fe = fg.add_entry()
        fe.id(berita['link'])
        fe.title(berita['title'])
        fe.link(href=berita['link'])
        fe.description(berita['desc'])
        fe.pubDate(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))

    fg.rss_file('feed.xml')

if __name__ == '__main__':
    generate_rss()
