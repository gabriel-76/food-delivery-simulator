import uuid
from typing import Optional, Union, List, Dict

from simpy import Environment, Event
from simpy.core import SimTime
from simpy.events import ProcessGenerator

from src.main.environment.actors.customer_actor import CustomerActor
from src.main.environment.actors.driver_actor import DriverActor
from src.main.environment.actors.establishment_actor import EstablishmentActor
from src.main.models.customer.customer import Customer
from src.main.environment.state import State
from src.main.models.driver.driver import Driver
from src.main.models.establishment.establishment import Establishment
from src.main.map.map import Map
from src.main.models.order.order import Order
from src.main.models.route.route import Route
from src.main.view.food_delivery_view import FoodDeliveryView


class DeliveryEnvironment(Environment):
    def __init__(self, map: Map, generators, optimizer, view: FoodDeliveryView = None):
        super().__init__()
        self.map = map
        self.generators = generators
        self.optimizer = optimizer
        self.view = view
        self._state = State()
        self._actors: Dict[uuid, Union[CustomerActor, EstablishmentActor, DriverActor]] = {}
        self.init()

    @property
    def events(self):
        return self._state.events

    @property
    def state(self):
        return self._state

    @property
    def actors(self):
        return self._actors

    def place(self, order: Order, customer: Customer, establishment: Establishment):
        self._state.add_orders([order])
        if customer.identifier not in self._actors:
            customer_actor = CustomerActor(self, customer)
            self._state.add_customers([customer])
            self._actors[customer.identifier] = customer_actor
            customer_actor.place(order, establishment)
        else:
            self._actors[customer.identifier].place(order, establishment)

        if establishment.identifier not in self._actors:
            establishment_actor = EstablishmentActor(self, establishment)
            self._actors[establishment.identifier] = establishment_actor
            self._state.add_establishments([establishment])

    def deliver(self, route: Route, driver: Driver):
        if driver.identifier not in self._actors:
            driver_actor = DriverActor(self, driver)
            self._actors[driver.identifier] = driver_actor
            # self._state.add_drivers([driver])
            driver_actor.request(route)
        else:
            self._actors[driver.identifier].request(route)

    def receive(self, order: Order, customer: Customer, driver: Driver) -> ProcessGenerator:
        customer_actor = self._actors[customer.identifier]
        yield self.process(customer_actor.receive(order, driver))

    def delivered(self, route: Order, driver: Driver):
        if driver.identifier not in self._actors:
            driver_actor = DriverActor(self, driver)
            self._actors[driver.identifier] = driver_actor
            driver_actor.delivered(route)
        else:
            self._actors[driver.identifier].delivered(route)

    def get_actor(self, actor_id):
        return self._actors.get(actor_id)

    def add_actor(self, actor_id, actor):
        self._actors[actor_id] = actor

    def add_customers(self, customers: List[Customer]):
        self._state.add_customers(customers)

    def add_establishments(self, establishments: List[Establishment]):
        self._state.add_establishments(establishments)

    def add_drivers(self, drivers: List[Driver]):
        self._state.add_drivers(drivers)

    def available_drivers(self, route):
        return [driver for driver in self._state.drivers if driver.check_availability(route)]

    def add_ready_order(self, order):
        self._state.orders_awaiting_delivery.append(order)

    def get_ready_orders(self):
        read_orders = []
        while len(self._state.orders_awaiting_delivery) > 0:
            read_orders = self._state.orders_awaiting_delivery
            self._state.orders_awaiting_delivery = []
        return read_orders

    def count_ready_orders(self):
        return len(self._state.orders_awaiting_delivery)

    def add_rejected_delivery(self, order, delivery_rejection):
        order.add_delivery_rejection(delivery_rejection)
        self._state.orders_awaiting_delivery.append(order)

    def get_rejected_deliveries(self):
        rejected_orders = []
        while len(self._state.rejected_deliveries) > 0:
            rejected_orders = self._state.rejected_deliveries
            self._state.rejected_deliveries = []
        return rejected_orders

    def add_event(self, event):
        self._state.add_event(event)

    def init(self):
        for generator in self.generators:
            self.process(generator.generate(self))

        if self.optimizer:
            self.process(self.optimizer.generate(self))

    def log_events(self):
        self._state.log_events()

    def run(self, until: Optional[Union[SimTime, Event]] = None, render_mode=None):
        if render_mode == "human" and self.view is not None:
            if not isinstance(until, Event):
                until = until if isinstance(until, int) else float(until)
                while self.now < until and not self.view.quited:
                    self.view.render(self)
                    super().run(until=self.now + 1)
                if self.view.quited:
                    self.view.quit()
        else:
            super().run(until=until)

        if self.view is not None and self.view.quited:
            self.view.quit()

    def render(self):
        if self.view is not None and not self.view.quited:
            self.view.render(self)

    def close(self):
        if self.view is not None and not self.view.quited:
            self.view.quit()
