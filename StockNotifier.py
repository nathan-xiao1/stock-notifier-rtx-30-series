from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from stores.Mwave import Mwave
from stores.Scorptec import Scorptec
from stores.Umart import Umart
import os, sys
import json
import asyncio

# Time between scrapes (seconds)
SCRAPE_INTERVAL = 60

class StockNotifier:

    def __init__(self):
        self.running = True
        self.callbacks = []
        self.stores = [Mwave(), Scorptec(), Umart()]
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
        driver_path = "chromedriver/chromedriver.exe" if sys.platform == "Windows" else "chromedriver/chromedriver"
        self.driver = webdriver.Chrome(
            options=options, service_log_path=os.devnull, executable_path=driver_path)

    async def start(self):
        print("StockNotifier: Started")
        while self.running:
            for store in self.stores:
                changed, in_stock, out_stock = store.scrape(
                    self.driver, self.urls[store.store_name()])
                if changed:
                    for callback in self.callbacks:
                        await callback(in_stock, out_stock)
                print("StockNotifier:", in_stock)
            self.save()
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
    try:
        stock_notifier = StockNotifier()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(stock_notifier.start())
    except KeyboardInterrupt:
        print("Exiting")