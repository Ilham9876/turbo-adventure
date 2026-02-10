import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import os

def scrape_kompas_bola():
    url = "https://bola.kompas.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = []
    # Mencari elemen berita di struktur HTML Kompas
    for item in soup.find_all('div', class_='article__list', limit=10):
        try:
            title_elem = item.find('h3', class_='article__title').find('a')
            title = title_elem.text.strip()
            link = title_elem['href']
            
            desc_elem = item.find('div', class_='article__excerpt')
            desc = desc_elem.text.strip() if desc_elem else "Klik untuk baca selengkapnya."
            
            articles.append({
                'title': title,
                'link': link,
                'desc': desc
            })
        except AttributeError:
            continue
    return articles

def generate_rss():
    fg = FeedGenerator()
    fg.id('https://github.com/lo/repo')
    fg.title('Kompas Bola - Latest News')
    fg.author({'name': 'Gen Z Innovator'})
    fg.link(href='https://bola.kompas.com/', rel='alternate')
    fg.description('Update berita bola harian dari Kompas via GitHub Actions')
    fg.language('id')

    berita_bola = scrape_kompas_bola()

    for berita in berita_bola:
        fe = fg.add_entry()
        fe.id(berita['link'])
        fe.title(berita['title'])
        fe.link(href=berita['link'])
        fe.description(berita['desc'])

    fg.rss_file('feed.xml')
    print("Mantap! RSS Feed berhasil di-update.")

if __name__ == '__main__':
    generate_rss()
