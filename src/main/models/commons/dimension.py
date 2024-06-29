from typing import Tuple

from src.main.commons.types import Number


class Dimension:
    def __init__(self, length: Number, height: Number, width: Number, weight: Number) -> None:
        self._length = length
        self._height = height
        self._width = width
        self._weight = weight

    @property
    def length(self) -> Number:
        return self._length

    @property
    def height(self) -> Number:
        return self._height

    @property
    def width(self) -> Number:
        return self._width

    @property
    def weight(self) -> Number:
        return self._weight

    @property
    def volume(self) -> Number:
        return self._length * self._height * self._width

    @staticmethod
    def empty() -> 'Dimension':
        return Dimension(0, 0, 0, 0)

    def _to_tuple(self) -> Tuple[Number, Number, Number, Number]:
        return self.length, self.height, self.width, self.weight

    def __lt__(self, other: 'Dimension'):
        return self._to_tuple() < other._to_tuple()

    def __le__(self, other: 'Dimension'):
        return self._to_tuple() <= other._to_tuple()

    def __gt__(self, other: 'Dimension'):
        return self._to_tuple() > other._to_tuple()

    def __ge__(self, other: 'Dimension'):
        return self._to_tuple() >= other._to_tuple()

    def __eq__(self, other: 'Dimension'):
        return self._to_tuple() == other._to_tuple()

    def __add__(self, other: 'Dimension'):
        summed_tuples = tuple(s + o for s, o in zip(self._to_tuple(), other._to_tuple()))
        return Dimension(summed_tuples[0], summed_tuples[1], summed_tuples[2], summed_tuples[3])
