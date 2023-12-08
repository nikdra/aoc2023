# aoc 2023 day 8

# input paths
INP_PATH = 'data\\08'
TEST_PATH = 'data\\08_test'
TEST2_PATH = 'data\\08_2_test'

from pprint import pprint
from functools import reduce

# read input as map of node: (left_node, right_node)
def read_input(path: str):
    with open(path) as file:
        inst, nodes = file.read().split('\n\n')
        return inst, {node.split(' = ')[0]: (node.split(' = ')[1].split(',')[0][1:], node.split(' = ')[1].split(',')[1][1:-1]) for node in nodes.split('\n')}
    

# determine how many steps from start to end with the instrucitons we have
def steps(inst, network, start, end=None):
    c = 0
    while not (start == 'ZZZ' if end is not None else start[-1] == 'Z'):
        start = network[start][0] if inst[c % len(inst)] == 'L' else network[start][1]
        c += 1
    return c    


# run solution on test and full input
test_inp = read_input(TEST_PATH)
pprint(steps(*test_inp, 'AAA', 'ZZZ'))
inp = read_input(INP_PATH)
pprint(steps(*inp, 'AAA', 'ZZZ'))


# least common multiple (thanks, wikipedia!)
def lcm(a,b):
    # define greatest common devisor (euclidean algorithm)
    def gcd(a,b):
        if b == 0:
            return a
        return gcd(b, a % b)
    # lcm = |ab| / gcd(a,b)
    return int(abs(a*b)/gcd(a,b))


# determine the number of steps we need from every start node to every end node
def ghost_steps(inst, network):
    # get the start nodes
    starts = filter(lambda n: n[-1] == 'A', network.keys())
    # peculiarity of the input: the paths cycle from each start to each end node with a certain period
    cycles = map(lambda s: steps(inst, network, s), starts)
    # return the lcm of the cycles
    return reduce(lambda a,b: lcm(a,b), cycles)


# run solution on test and full input
test_inp = read_input(TEST2_PATH)
pprint(ghost_steps(*test_inp))
pprint(ghost_steps(*inp))
