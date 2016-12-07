import constants
from simulation import run

params = [
    # 4 workers
    [1, 1, [1, 1]],

    # 5 workers
    [1, 1, [1, 1, 1]],
    [2, 1, [1, 1]],
    [1, 2, [1, 1]],

    # 6 workers
    [2, 2, [1, 1]],
    [2, 1, [1, 1, 1]],
    [1, 2, [1, 1, 1]],

    # 7 workers
    [2, 2, [1, 1, 1]],

    # almost good
    [4, 1, [1, 1]],
    # good
    [5, 2, [1, 1, 1]]
]

if __name__ == '__main__':

    for i, workers_count in enumerate(params):
        run(i+1, workers_count)
