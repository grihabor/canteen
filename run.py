
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

height = 3
width = max(3, len(cash_desks))

for i, place in enumerate(places + cash_desks):

    if not place.data:
        continue

    x, y = np.array(place.data).transpose()

    plt.subplot(height, width, i+1 if i < 2 else width+i-1)
    plt.title(place.name)
    plt.plot(x, y)

plt.subplot(height, width, 2*width+1)
plt.plot(np.array(places[0].time_list))

#plt.subplot(height, width, 2*width+2)
plt.plot(np.array(places[1].time_list))

plt.plot(np.array(cash_desks[0].time_list))
plt.plot(np.array(cash_desks[1].time_list))

plt.show()
