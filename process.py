from models import get
from constants import Group, Way, groups_interval


def source(env):
    while True:
        group(env, get(Group).value[1])
        yield env.timeout(groups_interval())


def client_proc(env, client):
    way = [(index, env.places[index]) for index in client.way.value[1]]
    for i, place in way:
        with place.request() as req:
            yield req
            client.lock(place)
            yield env.timeout(client.get_service_time(place))
            client.unlock(place)

    cash_desk = env.get_small_queue_cash_desk()

    with cash_desk.request() as req:
        yield req
        client.lock(cash_desk)
        yield env.timeout(client.get_cash_desk_time())
        client.unlock(cash_desk)


def group(env, number):
    for i in range(number):
        c = client_proc(env, Client(env, get(Way)))
        env.process(c)
    Client.group_count += 1
    print('Group {:>4} at {}'.format(Client.group_count, env.now))


class Client:
    group_count = 0
    count = 0

    def lock(self, cash_desk):
        print('{} locked {} at {}'.format(self, cash_desk, self.env.now))
        self.lock_time = self.env.now

    def unlock(self, cash_desk):
        print('{}  freed {} at {}'.format(self, cash_desk, self.env.now))
        cash_desk.add_time(self.env.now - self.lock_time)

    def __init__(self, env, way):
        self.way = way
        self.id = Client.count
        self.cum = 0
        self.env = env
        Client.count += 1
        print('{} going to {}'.format(self, self.way))

    def get_service_time(self, place):
        time, cum = place.get_service_time()
        if cum:
            self.cum += cum
        return time

    def get_cash_desk_time(self):
        return self.cum

    def __repr__(self):
        return '<Client [id={:0>2}]>'.format(self.id)
