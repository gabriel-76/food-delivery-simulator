import unittest
import uuid

from src.main.models.customer.customer import Customer


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.id1 = uuid.uuid4()
        self.coord1 = (1, 1)
        self.customer1 = Customer(self.id1, True, self.coord1)

    def test_properties(self):
        self.assertEqual(self.customer1.identifier, self.id1)
        self.assertEqual(self.customer1.coordinate, self.coord1)
        self.assertTrue(self.customer1.available)

    def test_enable_disable(self):
        self.customer1.disable()
        self.assertFalse(self.customer1.available)
        self.customer1.enable()
        self.assertTrue(self.customer1.available)


if __name__ == '__main__':
    unittest.main()
