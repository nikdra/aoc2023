# aoc 2023 day 6
from math import sqrt, ceil, floor
from functools import reduce

# input paths
INP_PATH = 'data\\06'
TEST_PATH = 'data\\06_test'

from pprint import pprint

def read_input(path: str):
    with open(path) as file:
        return [[int(c) for c in line.split(':')[1].split()] for line in file.read().splitlines()]
    

def num_wins(time, distance):
    # distance travelled = x * (t-x) = -x^2 + xt
    # win if -x^2 + xt - d > 0
    # or x^2 - xt + d < 0
    # equals to all numbers between t/2 - sqrt(t^2/4 - d) and t/2 + sqrt(t^2/4 - d)
    sq = sqrt(time**2/4-distance)
    # edge case: perfect squares, therefore cap
    x2= ceil(0.5*time + sq) # button press must be capped 
    x1 = floor(0.5*time - sq) # button press must be capped
    return x2 - x1 - 1


# run solution on test and full input
test_inp = read_input(TEST_PATH)
pprint(reduce(lambda a,b: a*b, (num_wins(*x) for x in zip(*test_inp))))
inp = read_input(INP_PATH)
pprint(reduce(lambda a,b: a*b, (num_wins(*x) for x in zip(*inp))))


# part 2: time numbers are all joined
# run solution on test and full input
pprint(num_wins(int(''.join(map(lambda i: str(i), test_inp[0]))), int(''.join(map(lambda i: str(i), test_inp[1])))))
pprint(num_wins(int(''.join(map(lambda i: str(i), inp[0]))), int(''.join(map(lambda i: str(i), inp[1])))))
