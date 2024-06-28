import unittest
import uuid

from src.main.models.commons.dimension import Dimension
from src.main.models.commons.item import Item
from src.main.models.customer.customer import Customer
from src.main.models.establishment.establishment import Establishment
from src.main.models.order.order import Order


class TestEstablishment(unittest.TestCase):
    def setUp(self):
        self.establishment = Establishment()
        self.customer = Customer(uuid.uuid4(), True, (1, 1))
        self.items = [Item(Dimension(2, 3, 4, 5), 10)]
        self.order = Order(self.customer, self.establishment, self.items, 10)

    def test_request(self):
        self.establishment.request(self.order)
        self.assertIn(self.order, self.establishment._requests)

    def test_accept(self):
        time = 10
        estimated_time = 20
        self.establishment.accept(self.order, time, estimated_time)
        self.assertIn(self.order, self.establishment._accepted)

    def test_reject(self):
        time = 10
        self.assertEqual(len(self.order._rejections), 0)
        self.establishment.reject(self.order, time)
        self.assertIn(self.order, self.establishment._rejected)
        self.assertEqual(len(self.order._rejections), 1)


if __name__ == '__main__':
    unittest.main()
