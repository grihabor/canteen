import simpy
import random
from gens import source

RANDOM_SEED = 42


random.seed(RANDOM_SEED)
env = simpy.Environment()
env.process(source(env))
env.run(until=200)
