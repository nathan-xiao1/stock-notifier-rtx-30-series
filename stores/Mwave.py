from .StoreABC import Store
import time

SCRAPE_DELAY = 1

class Mwave(Store):

	def scrape(self, driver, options, urls):
		in_stock = []
		for url in urls:
			driver.get(url)
			ul = driver.find_element_by_class_name("stockAndDelivery")
			dd = ul.find_element_by_tag_name("dd")
			if dd.text != "Currently No Stock":
				basic_info = driver.find_element_by_class_name("basicInfos")
				item_name = basic_info.find_element_by_xpath("//span[@itemprop='name']").text
				in_stock.append({item_name: url})
			time.sleep(SCRAPE_DELAY)
		return in_stock

	def scrapeAIO(self, driver, options, url):
		in_stocks = []
		driver.get(url)
		result_li = driver.find_element_by_xpath("//div[@id='ProductResults']/ul[@class='productList']")
		items_li = result_li.find_elements_by_tag_name("li")
		for item in items_li:
			button = item.find_element_by_class_name("button")
			if "normalButton" in button.get_attribute("class"):
				link = item.find_element_by_xpath("./div[@class='name']/a")
				in_stocks.append({link.text: link.get_attribute("href")})
		return in_stocks

