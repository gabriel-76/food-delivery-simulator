from abc import abstractmethod
from typing import List

from src.main.statistic.metric import Metric


class Board:

    def __init__(self, metrics: List[Metric]):
        self.metrics = metrics

    @abstractmethod
    def view(self) -> None:
        pass
