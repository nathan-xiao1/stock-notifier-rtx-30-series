from .StoreABC import Store, Product
import time
import json
import os.path

SCRAPE_DELAY = 0.3
STORE_NAME = "Umart"


class Umart(Store):

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
            # Only URLs for a result search or product list is supported
            product_list = driver.find_element_by_css_selector("#goods_sty")
            for product_detail in product_list.find_elements_by_class_name("goods_info"):
                name = product_detail.find_element_by_css_selector(
                    "div div.goods_name > a").text
                link = product_detail.find_element_by_css_selector(
                    "div div.goods_name > a").get_attribute("href")
                price = "$" + product_detail.find_element_by_css_selector(
                    "div span.goods_price.graphik-bold > span.goods-price").text
                image = product_detail.find_element_by_css_selector(
                    "div div.goods_img > a > img").get_attribute("src")
                in_stock = product_detail.find_element_by_css_selector(
                    "div  span.goods_stock > font > b").text != "Out Of Stock"
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
