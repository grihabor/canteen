from simpy import Resource
from enum import Enum
from random import random

class Place:
    HOT = 1
    COLD = 2
    DRINK = 3
    CASH_DESK = 4

    @staticmethod
    def set_resourses(env):
        Place.HOT = [Place.HOT, Resource(env, capacity=1)]
        Place.COLD = [Place.COLD, Resource(env, capacity=1)]
        Place.DRINK = [Place.DRINK, Resource(env, capacity=1)]
        Place.CASH_DESK = [Place.CASH_DESK, Resource(env, capacity=1)]

    @staticmethod
    def get(index):
        places = [place for key, place in Place.__dict__.items() if key == key.upper()]
        for i, way in places:
            if i == index:
                return way


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