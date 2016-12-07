from simpy import Environment
from collections import OrderedDict
from random import uniform, randint

import constants
from constants import PlaceName
from models import Place


class Uniform:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, *args, **kwargs):
        return uniform(self.a, self.b)


class Canteen(Environment):
    def __init__(self, workers_count, verbose=False, initial_time=0):

        super().__init__(initial_time=initial_time)

        self.workers_count = {
            PlaceName.HOT: workers_count[0],
            PlaceName.COLD: workers_count[1],
            PlaceName.CASH_DESK: workers_count[2]
        }

        self.cash_desk_count = len(self.workers_count[PlaceName.CASH_DESK])

        self.verbose = verbose

        self.places = OrderedDict()
        self.places[PlaceName.HOT] = Place(
            self, PlaceName.HOT, Uniform(50, 120), Uniform(20, 40),
            speed=self.workers_count[PlaceName.HOT]
        )
        self.places[PlaceName.COLD] = Place(
            self, PlaceName.COLD, Uniform(60, 180), Uniform(5, 15),
            speed=self.workers_count[PlaceName.COLD]
        )

        self.places[PlaceName.DRINK] = Place(
            self, PlaceName.DRINK, Uniform(5, 20), Uniform(5, 10), capacity=100
        )

        self.cash_desks = []
        for i in range(self.cash_desk_count):
            self.cash_desks.append(
                Place(self, PlaceName.CASH_DESK, index=1+i)
            )

        self.client_count = 0
        # list of pairs [timestamp, client_count]
        self.client_count_list = []

    def get_small_queue_cash_desk(self):
        queues_len = [len(cash_desk.queue) for cash_desk in self.cash_desks]
        min_queue_len = min(queues_len)

        # get list of cash_desks with minimum queue
        cdl = [cash_desk for cash_desk in self.cash_desks
                if len(cash_desk.queue) == min_queue_len]
        # get a random cash_desk from the list
        cdl = cdl[randint(0, -1+len(cdl))]
        return cdl