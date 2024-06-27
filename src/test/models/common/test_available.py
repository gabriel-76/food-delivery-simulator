import unittest
from src.main.models.common.available import Available


class TestAvailable(unittest.TestCase):

    def setUp(self):
        self.available = Available(False)

    def test_available(self):
        self.assertFalse(self.available.available)

    def test_enable(self):
        self.available.enable()
        self.assertTrue(self.available.available)

    def test_disable(self):
        self.available.disable()
        self.assertFalse(self.available.available)


if __name__ == '__main__':
    unittest.main()
