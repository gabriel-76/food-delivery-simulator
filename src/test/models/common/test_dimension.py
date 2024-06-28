import unittest
from src.main.models.commons.dimension import Dimension


class TestDimension(unittest.TestCase):
    def setUp(self):
        self.dim1 = Dimension(2, 3, 4, 5)
        self.dim2 = Dimension(1, 1, 1, 1)

    def test_properties(self):
        self.assertEqual(self.dim1.length, 2)
        self.assertEqual(self.dim1.height, 3)
        self.assertEqual(self.dim1.width, 4)
        self.assertEqual(self.dim1.weight, 5)

    def test_volume(self):
        self.assertEqual(self.dim1.volume, 2 * 3 * 4)
        self.assertEqual(self.dim2.volume, 1)

    def test_comparison(self):
        self.assertTrue(self.dim1 > self.dim2)
        self.assertFalse(self.dim1 < self.dim2)
        self.assertFalse(self.dim1 == self.dim2)

    def test_addition(self):
        result = self.dim1 + self.dim2
        self.assertEqual(result.length, 3)
        self.assertEqual(result.height, 4)
        self.assertEqual(result.width, 5)
        self.assertEqual(result.weight, 6)


if __name__ == '__main__':
    unittest.main()
