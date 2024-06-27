import unittest
from src.main.models.common.types import Number, Coordinate


class TestTypes(unittest.TestCase):
    def test_number(self):
        self.assertIsInstance(1, Number)
        self.assertIsInstance(1.0, Number)
        self.assertNotIsInstance("1", Number)

    # def test_coordinate(self):
    #     self.assertIsInstance((1, 1), Coordinate)
    #     self.assertIsInstance((1.0, 1.0), Coordinate)
    #     self.assertNotIsInstance((1, "1"), Coordinate)
    #     self.assertNotIsInstance((1, 1, 1), Coordinate)


if __name__ == '__main__':
    unittest.main()
