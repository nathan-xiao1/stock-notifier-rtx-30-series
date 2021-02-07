from abc import ABC, abstractmethod
from collections import namedtuple

Product = namedtuple("Product", ["name", "price", "image", "store", "link"])

class Store(ABC):

    @abstractmethod
    def scrape(self, driver, url):
        raise NotImplementedError