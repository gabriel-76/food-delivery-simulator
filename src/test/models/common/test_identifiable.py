import unittest
from src.main.models.common.identifiable import Identifiable
import uuid


class TestIdentifiable(unittest.TestCase):

    def setUp(self):
        self.id = uuid.uuid4()
        self.identifiable = Identifiable(self.id)

    def test_id(self):
        self.assertEqual(self.identifiable.id, self.id)


if __name__ == '__main__':
    unittest.main()
