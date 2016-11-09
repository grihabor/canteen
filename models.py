from simpy import Resource
from enum import Enum
from random import random


class PlaceType:
    HOT = 1
    COLD = 2
    DRINK = 3
    CASH_DESK = 4

    @staticmethod
    def set_resources(env):
        PlaceType.HOT = [PlaceType.HOT, Place(env, capacity=1)]
        PlaceType.COLD = [PlaceType.COLD, Place(env, capacity=1)]
        PlaceType.DRINK = [PlaceType.DRINK, Place(env, capacity=1)]
        PlaceType.CASH_DESK = [PlaceType.CASH_DESK, Place(env, capacity=1)]

    @staticmethod
    def get(index):
        places = [place for key, place in PlaceType.__dict__.items() if key == key.upper()]
        for i, way in places:
            if i == index:
                return way


class Place(Resource):
    def __init__(self, env, capacity=1):
        super().__init__(env, capacity)


class Way(Enum):
    HOT_AND_DRINK = [0.8, [PlaceType.HOT, PlaceType.DRINK, PlaceType.CASH_DESK]]
    COLD_AND_DRINK = [0.15, [PlaceType.COLD, PlaceType.DRINK, PlaceType.CASH_DESK]]
    ONLY_DRINK = [0.05, [PlaceType.DRINK, PlaceType.CASH_DESK]]


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