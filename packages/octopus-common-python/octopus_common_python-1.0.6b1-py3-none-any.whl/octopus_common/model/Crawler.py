from abc import abstractmethod

from octopus_common.model import ResultDetail


class Crawler:
    @abstractmethod
    def crawl(self, task) -> ResultDetail:
        pass
