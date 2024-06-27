import uuid
from abc import ABC


class Identifiable(ABC):
    def __init__(self, id: uuid = uuid.uuid4()) -> None:
        self._id = id

    @property
    def id(self):
        return self._id
