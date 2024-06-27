import unittest
from src.main.models.common.dimensions import Dimensions


class TestDimensions(unittest.TestCase):

    def setUp(self):
        self.dim1 = Dimensions(2, 2, 2, 2)
        self.dim2 = Dimensions(3, 3, 3, 3)

    def test_properties(self):
        self.assertEqual(self.dim1.length, 2)
        self.assertEqual(self.dim1.height, 2)
        self.assertEqual(self.dim1.width, 2)
        self.assertEqual(self.dim1.weight, 2)

    def test_volume(self):
        self.assertEqual(self.dim1.volume, 8)
        self.assertEqual(self.dim2.volume, 27)

    def test_comparison(self):
        self.assertTrue(self.dim1 < self.dim2)
        self.assertFalse(self.dim1 > self.dim2)
        self.assertFalse(self.dim1 == self.dim2)

    def test_addition(self):
        result = self.dim1 + self.dim2
        self.assertEqual(result.length, 5)
        self.assertEqual(result.height, 5)
        self.assertEqual(result.width, 5)
        self.assertEqual(result.weight, 5)


if __name__ == '__main__':
    unittest.main()
