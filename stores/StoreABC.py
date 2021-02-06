from abc import ABC, abstractmethod

class Store(ABC):

    @abstractmethod
    def scrape(self, options):
        pass