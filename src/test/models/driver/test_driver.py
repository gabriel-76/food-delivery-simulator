import unittest
import uuid
from src.main.models.driver.driver import Driver
from src.main.models.order.order import Order, OrderStatus
from src.main.models.customer.customer import Customer
from src.main.models.establishment.establishment import Establishment
from src.main.models.commons.item import Item
from src.main.models.commons.dimension import Dimension


class TestDriver(unittest.TestCase):
    def setUp(self):
        self.driver = Driver()
        self.customer = Customer(uuid.uuid4(), True, (1, 1))
        self.establishment = Establishment(uuid.uuid4(), True, (2, 2))
        self.items = [Item(Dimension(2, 3, 4, 5), 10)]
        self.order = Order(self.customer, self.establishment, self.items, 10)

    def test_deliver(self):
        time = 10
        self.driver.deliver(self.order, time)
        self.assertEqual(self.order._status, OrderStatus.DELIVERED)


if __name__ == '__main__':
    unittest.main()
