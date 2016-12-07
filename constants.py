from enum import Enum
from random import expovariate

SIMULATION_DURATION = 60*90
CASH_DESK_COUNT = 2


class PlaceName:
    HOT = 'hot'
    COLD = 'cold'
    DRINK = 'drink'
    CASH_DESK = 'cash desk'


class Group(Enum):
    ONE = [0.5, 1]
    TWO = [0.3, 2]
    THREE = [0.1, 3]
    FOUR = [0.1, 4]


class Way(Enum):
    HOT_AND_DRINK = [0.8, [PlaceName.HOT, PlaceName.DRINK]]
    COLD_AND_DRINK = [0.15, [PlaceName.COLD, PlaceName.DRINK]]
    ONLY_DRINK = [0.05, [PlaceName.DRINK]]

# interval between group arrivals
def groups_interval():
    return expovariate(1 / 30)