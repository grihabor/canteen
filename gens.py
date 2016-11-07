from enum import Enum
from random import random, randint


class Place(Enum):
    HOT = 1
    COLD = 2
    DRINK = 3
    CASH_DESK = 4


class Way(Enum):
    HOT_AND_DRINK = [0.8, [Place.HOT, Place.DRINK, Place.CASH_DESK]]
    COLD_AND_DRINK = [0.15, [Place.COLD, Place.DRINK, Place.CASH_DESK]]
    ONLY_DRINK = [0.05, [Place.DRINK, Place.CASH_DESK]]


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
    for way in model:
        if not type(way.value) is list:
            raise TypeError('type({}.value) must be list, got: {}'\
                .format(way, type(way.value)))
        if not type(way.value[0]) is float:
            raise TypeError('type({}.value[0]) must be float, got: {}'\
                .format(way, type(way.value[0])))
        elif way.value[0] < 0. or way.value[0] > 1.:
            raise ValueError('{}.value[0] must be between 0. and 1., got: {}'
                             .format(way, way.value[0]))

        if way.value[0] > x:
            return way
        else:
            x -= way.value[0]


def source(env):
    while True:
        group(env, get(Group).value[1])
        yield env.timeout(1)


def group(env, number):
    for i in range(number):
        c = client_proc(env, Client(get(Way)))
        env.process(c)
    print('group came!')


class Client:
    count = 0

    def __init__(self, way):
        self.way = way
        self.id = Client.count
        Client.count += 1
        print('Client {:>3} going to {}'.format(self.id, self.way))


def client_proc(env, c):
    print('Client {} at {}'.format(c.id, env.now))
    yield env.timeout(3)