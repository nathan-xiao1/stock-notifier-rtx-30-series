from .StoreABC import Store, Product
import time, json, os.path

SCRAPE_DELAY = 0.3
STORE_NAME = "Mwave"

class Mwave(Store):

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
            if url.startswith("https://www.mwave.com.au/product/"):
                # URL is for a product page
                product_container = driver.find_element_by_class_name(
                    "productCommon")
                # Get necessary infomation
                name = product_container.find_element_by_xpath(
                    "./div[@class='basicInfos']/h1/span[@itemprop='name']")
                price = product_container.find_element_by_xpath(
                    "./div[@class='divAddCart']//div[@class='divPriceNormal']/div[1]").text
                image = product_container.find_element_by_xpath(
                    "./div[@class='packshotAndReviews']//div[@class='medium']/a[1]/img"
                ).get_attribute("src")
                stock_level = product_container.find_element_by_xpath(
                    "./div[@class='basicInfos']/ul[@class='stockAndDelivery']//dd").text
                # Handle in stock or out of stock
                if stock_level != "Currently No Stock" and name not in self.in_stock_items:
                    changed = True
                    self.in_stock_items.add(name)
                    new_in_stock.append(Product(name, price, STORE_NAME, url))
                elif stock_level == "Currently No Stock" and name in self.in_stock_items:
                    changed = True
                    self.in_stock_items.remove(name)
                    new_out_of_stock.append(
                        Product(name, price, image, STORE_NAME, url))
            else:
                # URL is for a result search or product list
                result_li = driver.find_element_by_xpath(
                    "//div[@id='ProductResults']/ul[@class='productList']")
                # Loop over each product item inside the li tag
                for item in result_li.find_elements_by_tag_name("li"):
                    # Get necessary infomation
                    name = item.find_element_by_xpath(
                        "./div[@class='name']/a").text
                    link = item.find_element_by_xpath(
                        "./div[@class='name']/a").get_attribute("href")
                    price = item.find_element_by_xpath(
                        "./div[@class='price']/div[@class='current'][1]").text
                    image = item.find_element_by_xpath(
                        "./div[@class='imageProd']/a/img"
                    ).get_attribute("src")
                    in_stock = "normalButton" in item.find_element_by_class_name(
                        "button").get_attribute("class")
                    # Handle in stock or out of stock
                    if in_stock and name not in self.in_stock_items:
                        changed = True
                        self.in_stock_items.add(name)
                        new_in_stock.append(
                            Product(name, price, image, STORE_NAME, link))
                    elif not in_stock and name in self.in_stock_items:
                        changed = True
                        self.in_stock_items.remove(name)
                        new_out_of_stock.append(
                            Product(name, price, image, STORE_NAME, link))
                        # Delay to avoid overloading server
            time.sleep(SCRAPE_DELAY)
        return changed, new_in_stock, new_out_of_stock