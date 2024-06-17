from abc import abstractmethod

from src.main.statistic.metric import Metric


class Board:

    def __init__(self, metrics: [Metric]):
        self.metrics = metrics

    @abstractmethod
    def view(self) -> None:
        pass
