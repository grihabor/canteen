
from canteen import Canteen
import random
from process import source, Client
import matplotlib.pyplot as plt
import numpy as np
from constants import *

random.seed(RANDOM_SEED)


env = Canteen()

env.process(source(env))
env.run(until=SIMULATION_DURATION)

places = [env.places[PlaceName.HOT], env.places[PlaceName.COLD]]
cash_desks = env.cash_desks

height = 3
width = max(2, len(cash_desks))

for i, place in enumerate(places + cash_desks):

    if not place.data:
        continue

    x, y = np.array(place.data).transpose()

    plt.subplot(height, width, i+1 if i < 2 else width+i-1)
    plt.title(place.name)
    plt.plot(x, y)


def max_and_mean_time(time_list):
    return max(time_list), sum(time_list)/len(time_list)

for place in places[:2] + cash_desks:
    max_time, mean_time = max_and_mean_time(place.time_list)
    print()
    print("{}".format(place))
    print("Mean time: {}".format(mean_time))
    print("Max time : {}".format(max_time))

    data = np.array(place.data)

    print("Mean clients: {}".format(sum(data[:, 1])/len(data[:, 1])))
    print("Max clients : {}".format(max(data[:, 1])))


client_time_list = [sum(client.time_list)*client.way.value[0]
                    for client in Client.client_list]

print()
print("Cumulative {}".format(sum(client_time_list)/len(client_time_list)))

print()
x, y = np.array(env.client_count_list).transpose()
plt.subplot(height, width, width*2+1)
plt.plot(x, y)

plt.show()
