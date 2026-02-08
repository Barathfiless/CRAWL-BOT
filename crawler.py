import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse
import os
import time

class GodLevelMediaBeast:
    def __init__(self, seeds, max_pages=20, download_folder="downloaded_images"):
        self.seeds = seeds
        self.max_pages = max_pages
        self.visited = set()
        self.results = []
        self.queue = asyncio.Queue()
        
        # Image Storage Setup
        self.download_path = download_folder
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    async def fetch(self, session, url):
        """Page HTML-ah fetch panna (With Headers)"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
        try:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
        except Exception:
            return None
        return None

    async def download_image(self, session, img_url):
        """Images-ah folder-la download panni save panna"""
        # Wikipedia-la images often '//' nu start aagum, adha fix panrom
        if img_url.startswith('//'):
            img_url = 'https:' + img_url

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
        try:
            async with session.get(img_url, headers=headers, timeout=15) as response:
                if response.status == 200:
                    parsed_path = urlparse(img_url).path
                    base_name = os.path.basename(parsed_path)
                    
                    # Valid image format-ah nu check panrom
                    if not base_name or not base_name.lower().endswith(('.jpg', '.png', '.jpeg', '.gif', '.svg', '.webp')):
                        return None
                    
                    filename = os.path.join(self.download_path, base_name)
                    content = await response.read()
                    
                    with open(filename, 'wb') as f:
                        f.write(content)
                    return filename
        except Exception:
            return None

    async def scrape_page(self, session, url):
        """Title extract panna, Images download panna, and pudhu links theda"""
        if url in self.visited or len(self.visited) >= self.max_pages:
            return

        html = await self.fetch(session, url)
        if not html:
            return

        self.visited.add(url)
        # 'lxml' is super fast for God-level speed
        soup = BeautifulSoup(html, 'lxml') 
        
        # 1. Extract Title (Old Part-1 logic)
        title = soup.title.string.strip() if soup.title else "No Title"
        
        # 2. Media Extraction & Download
        img_tags = soup.find_all('img')
        downloaded_count = 0
        
        # First 10 images per page download panrom
        for img in img_tags[:10]:
            img_src = img.get('src') or img.get('data-src')
            if img_src:
                img_url = urljoin(url, img_src)
                saved_path = await self.download_image(session, img_url)
                if saved_path:
                    downloaded_count += 1

        # 3. Store Results for CSV
        self.results.append({
            'url': url,
            'title': title,
            'total_images_on_page': len(img_tags),
            'downloaded_now': downloaded_count
        })
        
        print(f"[{len(self.visited)}] Captured: {title} | Images Downloaded: {downloaded_count}")

        # 4. Link Discovery (Deep Crawling)
        for a in soup.find_all('a', href=True):
            link = urljoin(url, a['href'])
            # Wikipedia-kulla mattum crawl panna lock (Optional but faster)
            if link.startswith('http') and link not in self.visited:
                if "wikipedia.org" in link:
                    await self.queue.put(link)

    async def run(self):
        """Async Session-ah manage panna"""
        for url in self.seeds:
            await self.queue.put(url)

        # SSL=False added to bypass certificate errors
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            while not self.queue.empty() and len(self.visited) < self.max_pages:
                current_url = await self.queue.get()
                await self.scrape_page(session, current_url)
                self.queue.task_done()

async def main():
    # --- CONFIGURATION ---
    seeds = ["https://en.wikipedia.org/wiki/Main_Page"]
    max_pages = 20 # Neenga limit-ah 200 kooda ethikalaam
    
    crawler = GodLevelMediaBeast(seeds, max_pages=max_pages)
    
    print(f"Beast Mode Online: Crawling {max_pages} pages and downloading media...\n")
    start_time = time.time()
    
    await crawler.run()
    
    # --- SAVE TO CSV (PANDAS) ---
    if crawler.results:
        df = pd.DataFrame(crawler.results)
        df.drop_duplicates(subset='url', inplace=True)
        
        csv_filename = 'beast_media_final_results.csv'
        df.to_csv(csv_filename, index=False)
        
        print(f"\n{'='*40}")
        print(f"Total Time: {time.time() - start_time:.2f} seconds")
        print(f"Results saved: {csv_filename}")
        print(f"Images saved in folder: {crawler.download_path}")
        print(f"{'='*40}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping Beast...")
