import requests
from feedgen.feed import FeedGenerator

def generate_rss():
    fg = FeedGenerator()
    fg.id('https://github.com/lo/repo')
    fg.title('My Personal Feed')
    fg.author({'name': 'Gen Z Innovator'})
    fg.link(href='https://github.com/lo/repo', rel='alternate')
    fg.description('RSS Feed hasil ngulik gratisan via GitHub Actions')

    # CONTOH: Ambil data (lo bisa ganti pake API atau scraping)
    # Di sini lo tambahin logika buat nambahin entry
    fe = fg.add_entry()
    fe.id('http://link-berita.com/1')
    fe.title('Update Skor Liga Inggris Terkini!')
    fe.link(href='http://link-berita.com/1')
    fe.description('Cek update terbaru Premier League biar gak ketinggalan info.')

    fg.rss_file('feed.xml')

if __name__ == '__main__':
    generate_rss()
