from simpy import Resource
from random import random


class Place(Resource):
    def __init__(self, env, name, service_time=None, cum_service_time=None,
                 speed=1, capacity=1, index=None):
        super().__init__(env, capacity=capacity)
        self.name = name
        self.data = []
        self.service_time = service_time
        self.cum_service_time = cum_service_time
        self.speed = speed
        self.index = index

    def get_service_time(self):
        time = self.service_time() / self.speed
        if self.cum_service_time:
            return time, self.cum_service_time()
        else:
            return time, None

    def request(self, *args, **kwargs):
        ret = super().request(*args, **kwargs)
        self.data.append([self._env.now, len(self.queue)])
        return ret

    def release(self, *args, **kwargs):
        ret = super().release(*args, **kwargs)
        self.data.append([self._env.now, len(self.queue)])
        return ret

    def __repr__(self):
        return '<Place \'{:<5}{}\'>'.format(
            self.name, '_{}'.format(self.index) if self.index else ''
        )


def get(model):
    """Generates enum item based on probability information

    member.value[0] must be the probabilty of getting the member
    :param model: Enum class
    :return: Enum member
    """
    x = random()
    for item in model:
        if not type(item.value) is list:
            raise TypeError('type({}.value) must be list, got: {}'\
                .format(item, type(item.value)))
        if not type(item.value[0]) is float:
            raise TypeError('type({}.value[0]) must be float, got: {}'\
                .format(item, type(item.value[0])))
        elif item.value[0] < 0. or item.value[0] > 1.:
            raise ValueError('{}.value[0] must be between 0. and 1., got: {}'
                             .format(item, item.value[0]))

        if item.value[0] > x:
            return item
        else:
            x -= item.value[0]