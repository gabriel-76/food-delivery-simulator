import unittest
from src.main.models.commons.item import Item
from src.main.models.commons.dimension import Dimension


class TestItem(unittest.TestCase):
    def setUp(self):
        self.dim1 = Dimension(2, 3, 4, 5)
        self.time1 = 10
        self.item1 = Item(self.dim1, self.time1)

    def test_properties(self):
        self.assertEqual(self.item1.dimension, self.dim1)
        self.assertEqual(self.item1.time, self.time1)


if __name__ == '__main__':
    unittest.main()
