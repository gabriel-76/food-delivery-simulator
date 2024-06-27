import unittest

from src.main.models.common.localizable import Localizable


class TestLocalizable(unittest.TestCase):

    def setUp(self):
        self.coordinate = (1, 1)
        self.localizable = Localizable(self.coordinate)

    def test_coordinate(self):
        self.assertEqual(self.localizable.coordinate, self.coordinate)


if __name__ == '__main__':
    unittest.main()
