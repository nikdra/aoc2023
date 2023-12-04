# aoc 2023 day 4

# input paths
INP_PATH = 'data\\04'
TEST_PATH = 'data\\04_test'

from pprint import pprint

# read input as pairs of lists, winning numbers and the numbers you have
def read_input(path: str):
    with open(path) as file:
        return [[list(filter(lambda a: a != '', z.split(' '))) for z in y.split(' | ')] for y in [x.split(': ')[1] for x in file.read().splitlines()]]
    

# number of points
def points(winning, draw):
    return int(2 ** (matches(winning, draw) - 1))


# number of matches between winning numbers and ours
def matches(winning, draw):
    return sum(map(lambda _: True, filter(lambda x: x in winning, draw)))


# run solution on test and full input
test_input = read_input(TEST_PATH)
input = read_input(INP_PATH)
pprint(sum(points(*pair) for pair in test_input))
pprint(sum(points(*pair) for pair in input))


# scratches: add 1 of the following card for each match in the current card
# return the number of cards we end up with
def scratches(pairs):
    factors = [1] * len(pairs)
    for i, pair in enumerate(pairs, 1):
        for m in range(matches(*pair)):
            factors[i+m] += factors[i-1]
    return(sum(factors))


# run solution on test and full input
pprint(scratches(test_input))
pprint(scratches(input))