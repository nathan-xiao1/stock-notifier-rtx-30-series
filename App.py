from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from stores.Mwave import Mwave
import os, time

# Time between scrapes (seconds)
SCRAPE_INTERVAL = 30
DRIVER_PATH = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Connection': 'keep-alive'
}

# Options
options = Options()
options.headless = True
options.add_argument('--log-level=3')
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-gpu")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36")

# Create a Chrome webdriver
driver = webdriver.Chrome(options=options, service_log_path=os.devnull, executable_path=DRIVER_PATH)

# URLs to scrape
mwaveUrls = [
    "https://www.mwave.com.au/graphics-cards/geforce-rtx-3070",
    "https://www.mwave.com.au/product/evga-geforce-rtx-3080-ftw3-ultra-gaming-10gb-video-card-ac38322"
]


stores = [
    Mwave()
]

while True:
    for store in stores:
        print(store.scrape(driver, options, mwaveUrls))
    time.sleep(SCRAPE_INTERVAL)