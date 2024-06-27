from typing import List

from src.main.models.common.item import Item


class Catalog:
    def __init__(self, items: List[Item]):
        self._items = items

    @property
    def items(self) -> List[Item]:
        return self._items

    @staticmethod
    def empty() -> 'Catalog':
        return Catalog([])
