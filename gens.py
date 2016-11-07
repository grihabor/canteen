from models import Place, Group, get, Way


def source(env):
    Place.set_resourses(env)
    while True:
        group(env, get(Group).value[1])
        yield env.timeout(1)


def group(env, number):
    for i in range(number):
        c = client_proc(env, Client(get(Way)))
        env.process(c)
    print('group came!')


class Client:
    count = 0

    def __init__(self, way):
        self.way = way
        self.id = Client.count
        Client.count += 1
        print('Client {:>3} going to {}'.format(self.id, self.way))


def client_proc(env, c):
    print('Client {} at {}'.format(c.id, env.now))
    yield env.timeout(3)