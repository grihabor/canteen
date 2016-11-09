from simpy import Resource
from enum import Enum
from random import random
from constants import PlaceName


class Place(Resource):
    def __init__(self, env, name, service_time, cum_service_time, speed):
        super().__init__(env)
        self.name = name
        self.data = []
        self.service_time = service_time
        self.cum_service_time = cum_service_time
        self.cum = 0

    def get_service_time(self):
        time = self.service_time(self.cum)
        self.cum += self.service_time(self.cum)
        return time

    def request(self, *args, **kwargs):
        ret = super().request(*args, **kwargs)
        self.data.append([self._env.now, len(self.queue)])
        return ret

    def release(self, *args, **kwargs):
        ret = super().release(*args, **kwargs)
        self.data.append([self._env.now, len(self.queue)])
        return ret

    def __repr__(self):
        return '<Place \'{}\'>'.format(self.name)


class Way(Enum):
    HOT_AND_DRINK = [0.8, [PlaceName.HOT, PlaceName.DRINK, PlaceName.CASH_DESK]]
    COLD_AND_DRINK = [0.15, [PlaceName.COLD, PlaceName.DRINK, PlaceName.CASH_DESK]]
    ONLY_DRINK = [0.05, [PlaceName.DRINK, PlaceName.CASH_DESK]]


class Group(Enum):
    ONE = [0.5, 1]
    TWO = [0.3, 2]
    THREE = [0.1, 3]
    FOUR = [0.1, 4]


def get(model):
    """Generates enum item based on probability information

    member.value[0] must be the probabilty of getting the member
    :param model: Enum class
    :return: Enum member
    """
    x = random()
    for item in model:
        if not type(item.value) is list:
            raise TypeError('type({}.value) must be list, got: {}'\
                .format(item, type(item.value)))
        if not type(item.value[0]) is float:
            raise TypeError('type({}.value[0]) must be float, got: {}'\
                .format(item, type(item.value[0])))
        elif item.value[0] < 0. or item.value[0] > 1.:
            raise ValueError('{}.value[0] must be between 0. and 1., got: {}'
                             .format(item, item.value[0]))

        if item.value[0] > x:
            return item
        else:
            x -= item.value[0]