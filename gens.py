from models import Place, Group, get, Way
from random import expovariate


# interval between group arrivals
def groups_interval():
    return expovariate(1/30)


def source(env):
    Place.set_resourses(env)
    while True:
        group(env, get(Group).value[1])
        yield env.timeout(groups_interval())


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

    def __repr__(self):
        return '<Client [id={:0>2}]>'.format(self.id)

def client_proc(env, c):
    way = [(index, Place.get(index)) for index in c.way.value[1]]
    for i, place in way:
        with place.request() as req:
            yield req
            print('{} locked {} at {}'.format(c, i, env.now))
            yield env.timeout(30)
            print('{}  freed {} at {}'.format(c, i, env.now))
    yield env.timeout(3)