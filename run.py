from collections import OrderedDict

import simpy
import random
from process import source
from models import Place
import matplotlib.pyplot as plt
import numpy as np
from random import uniform
from constants import *
import process

random.seed(RANDOM_SEED)
env = simpy.Environment()


class Uniform:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, *args, **kwargs):
        return uniform(self.a, self.b)

process.places = OrderedDict()
process.places[PlaceName.HOT] = \
        Place(env, PlaceName.HOT, Uniform(50, 120), Uniform(20, 40), speed=1)
process.places[PlaceName.COLD] = \
        Place(env, PlaceName.COLD, Uniform(60, 180), Uniform(5, 15), speed=1)
process.places[PlaceName.DRINK] = \
        Place(env, PlaceName.DRINK, Uniform(5, 20), Uniform(5, 10), speed=1)
process.places[PlaceName.CASH_DESK] = \
        Place(env, PlaceName.CASH_DESK, None, None, speed=1)


env.process(source(env))
env.run(until=SIMULATION_DURATION)

for i, (key, place) in enumerate(process.places.items()):

    x, y = np.array(place.data).transpose()

    plt.subplot(2, 2, i+1)
    plt.title(place.name)
    plt.plot(x, y)

plt.show()