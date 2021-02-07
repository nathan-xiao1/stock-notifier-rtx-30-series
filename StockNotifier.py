from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from stores.Mwave import Mwave
import os, json, asyncio

# Time between scrapes (seconds)
SCRAPE_INTERVAL = 30
DRIVER_PATH = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"

class StockNotifier:

    def __init__(self):
        self.running = True
        self.callbacks = []
        self.stores = [Mwave()]
        with open("urls.json") as json_file:
            self.urls = json.load(json_file)

        # Webdriver options
        options = Options()
        options.headless = True
        options.add_argument('--log-level=3')
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--disable-gpu")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36")

        # Create a Chrome webdriver
        self.driver = webdriver.Chrome(options=options, service_log_path=os.devnull, executable_path=DRIVER_PATH)
        
    async def start(self):
        print("StockNotifier: Started")
        while self.running:
            for store in self.stores:
                changed, in_stock, out_stock = store.scrape(self.driver, self.urls["mwave"])
                if changed:
                    for callback in self.callbacks:
                        await callback(in_stock, out_stock)
                print("StockNotifier: Sleeping")
                await asyncio.sleep(SCRAPE_INTERVAL)

    def stop(self):
        self.running = False

    def registerCallback(self, callback):
        self.callbacks.append(callback)

    def save(self):
        for store in self.stores:
            store.save()

if __name__ == "__main__":
    stock_notifier = StockNotifier()
    stock_notifier.start()
    stock_notifier.registerCallback(print)
