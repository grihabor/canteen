from canteen import Canteen
import random
from process import source, Client
import matplotlib.pyplot as plt
import numpy as np
import os
from constants import *


def max_and_mean_time(time_list):
    return max(time_list), sum(time_list) / len(time_list)


def get_cumulative_proportional_time(client_list):
    client_time_list = [sum(client.time_list) * client.way.value[0]
                        for client in client_list]

    return sum(client_time_list) / len(client_time_list)


def run(random_seed=None):
    """Runs the simulation and returns plot data and metrics

    :param random_seed:
    :return:
    """
    if random_seed:
        random.seed(random_seed)

    metrics = {}
    plot_data = {}

    env = Canteen()

    env.process(source(env))
    env.run(until=SIMULATION_DURATION)

    places = [env.places[PlaceName.HOT], env.places[PlaceName.COLD]]
    cash_desks = env.cash_desks

    height = 3
    width = max(2, len(cash_desks))
    plot_data['size'] = [height, width]

    plot_data['data'] = []
    for i, place in enumerate(places + cash_desks):

        if not place.data:
            continue

        x, y = np.array(place.data).transpose()
        plot_data['data'].append([
            i+1 if i < 2 else width+i-1,
            repr(place).strip('<>'),
            x, y
        ])

    for place in places[:2] + cash_desks:
        max_time, mean_time = max_and_mean_time(place.time_list)

        data = np.array(place.data)
        mean_clients = sum(data[:, 1])/len(data[:, 1])
        max_clients = max(data[:, 1])

        metrics[place] = [mean_time, max_time, mean_clients, max_clients]

    cumulative = get_cumulative_proportional_time(Client.client_list)
    metrics['Cumulative proportional time'] = cumulative

    x, y = np.array(env.client_count_list).transpose()
    plot_data['data'].append([
        width * 2 + 1,
        'Total client count',
        x, y
    ])

    return plot_data, metrics


plt.figure(figsize=(16, 12))
for random_seed in range(10):
    plot_data, metrics = run(random_seed)

    for index, title, x, y in plot_data['data']:
        plt.subplot(plot_data['size'][0], plot_data['size'][1], index)
        plt.title(title)
        if max(y) < 2:
            plt.ylim(0, 10)
        plt.plot(x, y)

    for key, value in metrics.items():
        print(key)
        print('    {}'.format(value))
    print()

output_dir = 'output'
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

plt.savefig('{}/img_{}.png'.format(output_dir, 0))

plt.show()