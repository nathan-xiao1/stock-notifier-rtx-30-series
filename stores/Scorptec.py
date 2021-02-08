from .StoreABC import Store, Product
import time
import json
import os.path

SCRAPE_DELAY = 0.3
STORE_NAME = "Scorptec"


class Scorptec(Store):

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
            if url.startswith("https://www.scorptec.com.au/product/"):
                # URL is for a product page
                name = driver.find_element_by_css_selector("#product_name").text
                price = driver.find_element_by_css_selector("#price-price").text
                image = driver.find_element_by_css_selector("#large_image").get_attribute("src")
                in_stock = (driver.find_element_by_css_selector("#delivery-wrapper > div.product-stock-text > span").text != "SOLD OUT" or
                            driver.find_element_by_css_selector("#collect-wrapper > div.product-stock-text > a").text != "SOLD OUT")
                # Handle in stock or out of stock
                if in_stock and name not in self.in_stock_items:
                    changed = True
                    self.in_stock_items.add(name)
                    new_in_stock.append(
                        Product(name, price, image, self.store_name(), url))
                elif not in_stock and name in self.in_stock_items:
                    changed = True
                    self.in_stock_items.remove(name)
                    new_out_of_stock.append(
                        Product(name, price, image, self.store_name(), url))
            else:
                # URL is for a product list
                # Loop over each product item in the product list
                product_list = driver.find_element_by_id("product_list")
                for product_detail in product_list.find_elements_by_class_name("inner-detail"):
                    # Get necessary infomation
                    name = product_detail.find_element_by_css_selector(
                        "div > div.desc > a > div > h3").text
                    link = product_detail.find_element_by_css_selector(
                        "div > div.desc > a").get_attribute("href")
                    price = product_detail.find_element_by_css_selector(
                        "div > div.price > div.price-inner > div").text
                    image = product_detail.find_element_by_css_selector(
                        "div.image.hidden-xs > div.image-inner > div > a > img").get_attribute("src")
                    stock_levels = product_detail.find_elements_by_class_name(
                        "stock-status-text")
                    # Check if in stock for delivery or pickup
                    in_stock = False
                    for stock_level in stock_levels:
                        in_stock = in_stock or stock_level.find_element_by_tag_name(
                            "span").text != "SOLD OUT"
                    # Handle in stock or out of stock
                    if in_stock and name not in self.in_stock_items:
                        changed = True
                        self.in_stock_items.add(name)
                        new_in_stock.append(
                            Product(name, price, image, self.store_name(), link))
                    elif not in_stock and name in self.in_stock_items:
                        changed = True
                        self.in_stock_items.remove(name)
                        new_out_of_stock.append(
                            Product(name, price, image, self.store_name(), link))

            # Delay to avoid overloading server
            time.sleep(SCRAPE_DELAY)
        return changed, new_in_stock, new_out_of_stock
