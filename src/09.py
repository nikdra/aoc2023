# aoc 2023 day 9

# input paths
INP_PATH = 'data\\09'
TEST_PATH = 'data\\09_test'

from pprint import pprint


# read input as list of numbers
def read_input(path: str):
    with open(path) as file:
        return [list(map(int, line.split())) for line in file.read().splitlines()]
    

# extrapolate: always add the last value in the series to the total
def extrapolate(history):
    if any(history): # while not all 0
        # add last element and extrapolate further
        return history[-1] + extrapolate([history[i] - history[i-1] for i in range(1, len(history))]) 
    # all zero, return
    return 0
    

# run solution on test and full input
test_inp = read_input(TEST_PATH)
inp = read_input(INP_PATH)
pprint(sum(extrapolate(h) for h in test_inp))
pprint(sum(extrapolate(h) for h in inp))

# run solution on test and full input
# extrapolate to front = extrapolate to back, but in reverse
pprint(sum(extrapolate(h[::-1]) for h in test_inp))
pprint(sum(extrapolate(h[::-1]) for h in inp))