from random import expovariate
from models import PlaceName, Group, get, Way

places = {}


# interval between group arrivals
def groups_interval():
    return expovariate(1/30)


def source(env):
    while True:
        group(env, get(Group).value[1])
        yield env.timeout(groups_interval())


def client_proc(env, client):
    way = [(index, places[index]) for index in client.way.value[1]]
    for i, place in way:
        with place.request() as req:
            yield req
            print('{} locked {} at {}'.format(client, place, env.now))
            yield env.timeout(client.service_time(place))
            print('{}  freed {} at {}'.format(client, place, env.now))
    yield env.timeout(3)


def group(env, number):
    for i in range(number):
        c = client_proc(env, Client(get(Way)))
        env.process(c)
    Client.group_count += 1
    print('Group {:>4} at {}'.format(Client.group_count, env.now))


class Client:
    group_count = 0
    count = 0

    def __init__(self, way):
        self.way = way
        self.id = Client.count
        Client.count += 1
        print('{} going to {}'.format(self, self.way))

    def service_time(self, place):
        return 30

    def __repr__(self):
        return '<Client [id={:0>2}]>'.format(self.id)
