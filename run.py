
from canteen import Canteen
import random
from process import source
import matplotlib.pyplot as plt
import numpy as np
from constants import *
import process

random.seed(RANDOM_SEED)


env = Canteen()

env.process(source(env))
env.run(until=SIMULATION_DURATION)

places = [env.places[PlaceName.HOT], env.places[PlaceName.COLD]]
cash_desks = env.cash_desks
print(places)
for i, place in enumerate(places + cash_desks):

    if not place.data:
        continue

    x, y = np.array(place.data).transpose()

    height = 2
    width = max(2, len(cash_desks))

    plt.subplot(height, width, i+1 if i < 2 else width+i-1)
    plt.title(place.name)
    plt.plot(x, y)

plt.show()