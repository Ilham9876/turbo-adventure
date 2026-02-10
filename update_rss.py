import requests
import os

# 1. URL Sumber (Ganti dengan link XML dari RSS.app atau generator lo)
SOURCE_URL = "https://rss.app/feeds/4AnZaegv6Z4lgL1c.xml" 

# 2. Lokasi file di GitHub lo
FILE_PATH = "RSS Feed/detiksains.xml"

def main():
    try:
        print(f"Sedang mengambil data dari {SOURCE_URL}...")
        response = requests.get(SOURCE_URL, timeout=30)
        
        if response.status_code == 200:
            # Pastikan folder ada
            os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
            
            # Simpan data ke file xml lo
            with open(FILE_PATH, "wb") as f:
                f.write(response.content)
            print("✅ Berhasil memperbarui file XML!")
        else:
            print(f"❌ Gagal mengambil data. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Terjadi error: {e}")

if __name__ == "__main__":
    main()
