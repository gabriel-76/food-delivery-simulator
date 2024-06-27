import unittest

from src.main.models.customer.customer import Customer


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.coordinate = (1, 1)
        self.available = True
        self.customer = Customer(self.coordinate, self.available)

    def test_coordinate(self):
        self.assertEqual(self.customer.coordinate, self.coordinate)

    def test_available(self):
        self.assertEqual(self.customer.available, self.available)


if __name__ == '__main__':
    unittest.main()
