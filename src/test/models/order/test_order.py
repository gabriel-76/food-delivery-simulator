import unittest
import uuid
from src.main.models.establishment.establishment import Establishment
from src.main.models.customer.customer import Customer
from src.main.models.order.order import Order, OrderStatus
from src.main.models.order.rejection import RejectionType, Rejection
from src.main.models.commons.item import Item
from src.main.models.commons.dimension import Dimension


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.customer = Customer(uuid.uuid4(), True, (1, 1))
        self.establishment = Establishment(uuid.uuid4(), True, (2, 2))
        self.items = [Item(Dimension(2, 3, 4, 5), 10)]
        self.order = Order(self.customer, self.establishment, self.items, 10)

    def test_properties(self):
        self.assertEqual(self.order.customer, self.customer)
        self.assertEqual(self.order.establishment, self.establishment)

    def test_methods(self):
        self.order.accept_preparation(10, 20)
        self.assertEqual(self.order._status, OrderStatus.ESTABLISHMENT_ACCEPTED)
        self.order.start_preparation(15)
        self.assertEqual(self.order._status, OrderStatus.PREPARING)
        self.order.finish_preparation(25)
        self.assertEqual(self.order._status, OrderStatus.READY)
        self.order.accept_pickup(30, 40)
        self.assertEqual(self.order._status, OrderStatus.DRIVER_ACCEPTED)
        self.order.start_pickup(35)
        self.assertEqual(self.order._status, OrderStatus.PICKING_UP)
        self.order.finish_pickup(45)
        self.assertEqual(self.order._status, OrderStatus.PICKED_UP)
        self.order.accept_delivery(50, 60)
        self.assertEqual(self.order._status, OrderStatus.PICKED_UP)
        self.order.start_delivery(55)
        self.assertEqual(self.order._status, OrderStatus.DELIVERING)
        self.order.finish_delivery(65)
        self.assertEqual(self.order._status, OrderStatus.DELIVERED)
        self.order.reject(Rejection(70, RejectionType.ESTABLISHMENT_REJECTED))
        self.assertEqual(self.order._status, OrderStatus.ESTABLISHMENT_REJECTED)


if __name__ == '__main__':
    unittest.main()
