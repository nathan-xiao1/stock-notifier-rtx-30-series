from abc import ABC, abstractmethod
from collections import namedtuple
import os.path
import json

Product = namedtuple("Product", ["name", "price", "image", "store", "link"])
DIRECTORY = "data/"

class Store(ABC):

    @property
    @abstractmethod
    def store_name(self):
        ...

    @property
    def filename(self):
        return f"{DIRECTORY}{self.store_name()}.json"

    @abstractmethod
    def scrape(self, driver, url):
        ...

    def load(self):
        os.makedirs(DIRECTORY, exist_ok=True)
        if not os.path.isfile(self.filename):
            return set()
        with open(self.filename, "r") as json_file:
            return set(json.load(json_file))

    def save(self):
        with open(self.filename, "w") as json_file:
            json.dump(list(self.in_stock_items), json_file)
