from .StoreABC import Store, Product
import time
import json
import os.path

SCRAPE_DELAY = 0.3
STORE_NAME = "PC Case Gear"


class PCCG(Store):

    def __init__(self):
        # Set of items that are in stock
        self.in_stock_items = self.load()

    def store_name(self):
        return STORE_NAME

    def scrape(self, driver, urls):
        changed = False
        new_in_stock = []
        new_out_of_stock = []
        # Scrape each URL
        for url in urls:
            print(f"Processing: {url}")
            driver.get(url)
            # URL is for a result search or product list
            product_list = driver.find_element_by_css_selector(
                "#CategoryView > div > div.cat-container.list-container")
            for product_detail in product_list.find_elements_by_class_name("product-container"):
                # Get necessary infomation
                name = product_detail.find_element_by_css_selector(
                    "div.product-desc > div > a").text
                link = product_detail.find_element_by_css_selector(
                    "div.product-desc > div > a").get_attribute("href")
                price = product_detail.find_element_by_css_selector(
                    "div.price-box > div.price").text
                try:
                    image = product_detail.find_element_by_css_selector(
                        "a > img").get_attribute("src")
                except Exception:
                    image = "https://files.pccasegear.com/images/pccg_logo.png"
                in_stock = product_detail.find_element_by_css_selector(
                    "div.price-box > button > span.full-text-add-to-cart").text != "SOLD OUT"
                if "3080" in name:
                    model = "RTX 3080"
                elif "3070" in name:
                    model = "RTX 3070"
                else:
                    model = "N/A"
                # Handle in stock or out of stock
                if in_stock and name not in self.in_stock_items:
                    changed = True
                    self.in_stock_items.add(name)
                    new_in_stock.append(
                        Product(name, model, price, image, self.store_name(), link))
                elif not in_stock and name in self.in_stock_items:
                    changed = True
                    self.in_stock_items.remove(name)
                    new_out_of_stock.append(
                        Product(name, model, price, image, self.store_name(), link))
                        
            # Delay to avoid overloading server
            time.sleep(SCRAPE_DELAY)
        return changed, new_in_stock, new_out_of_stock
