from typing import List

from src.main.models.common.item import Item


class Catalog:
    def __init__(self, items: List[Item]):
        self.items = items

    @staticmethod
    def empty() -> 'Catalog':
        return Catalog([])
