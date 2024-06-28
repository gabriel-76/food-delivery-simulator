import unittest
from src.main.models.commons.capacity import Capacity
from src.main.models.commons.dimension import Dimension


class TestCapacity(unittest.TestCase):
    def setUp(self):
        self.dim1 = Dimension(2, 3, 4, 5)
        self.dim2 = Dimension(1, 1, 1, 1)
        self.cap1 = Capacity(self.dim1)
        self.cap2 = Capacity(self.dim2)

    def test_properties(self):
        self.assertEqual(self.cap1.dimension, self.dim1)
        self.assertEqual(self.cap2.dimension, self.dim2)

    def test_value(self):
        self.assertEqual(self.cap1.value, self.dim1.volume * self.dim1.weight)
        self.assertEqual(self.cap2.value, self.dim2.volume * self.dim2.weight)

    def test_fits(self):
        self.assertTrue(self.cap1.fits(self.dim2))
        self.assertFalse(self.cap2.fits(self.dim1))


if __name__ == '__main__':
    unittest.main()
