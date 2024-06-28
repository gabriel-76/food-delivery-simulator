import unittest
import uuid
from src.main.models.commons.localizable import Localizable


class TestLocalizable(unittest.TestCase):
    def setUp(self):
        self.id1 = uuid.uuid4()
        self.coord1 = (1, 1)
        self.localizable1 = Localizable(self.id1, True, self.coord1)

    def test_properties(self):
        self.assertEqual(self.localizable1.identifier, self.id1)
        self.assertEqual(self.localizable1.coordinate, self.coord1)
        self.assertTrue(self.localizable1.available)

    def test_enable_disable(self):
        self.localizable1.disable()
        self.assertFalse(self.localizable1.available)
        self.localizable1.enable()
        self.assertTrue(self.localizable1.available)


if __name__ == '__main__':
    unittest.main()
