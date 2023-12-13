# aoc 2023 day 11

# input paths
INP_PATH = 'data\\11'
TEST_PATH = 'data\\11_test'

from pprint import pprint


# read input as lines of strings
def read_input(path: str):
    with open(path) as file:
        return file.read().splitlines()


# return the expanded universe by multiplying the empty rows and columns by a ratio
def expanded_universe(image, ratio = 2):
    # how many rows do we have to add for each row?
    row_index = [0 if '#' in line else ratio-1 for line in image]
    # add up the rows we have to add for each row
    row_index = [sum(row_index[:i]) for i in range(len(row_index))]
    # same for columns
    col_index = [0 if '#' in ''.join(ln[i] for ln in image) else ratio-1 for i in range(len(image[0]))]
    col_index = [sum(col_index[:i]) for i in range(len(col_index))]
    # get the coordinates of the galaxies in the expanded univers
    return [(xc[0]+xd, yline[0]+yd) for yline, yd in zip(enumerate(image), row_index) for xc, xd in zip(enumerate(yline[1]), col_index) if xc[1] == '#']
    

# sum of pairwise distances
def pairwise_distances(points):
    # distance between two points (x1,y1) and (x2,y2) going only up, down, left, right
    def distance(x1, y1, x2, y2):
        # manhattan distance
        return abs(x1-x2) + abs(y1-y2)
    return sum(distance(*points[i], *points[j]) for i in range(len(points)) for j in range(i+1, len(points)))


# run solution on test and full input
test_inp = read_input(TEST_PATH)
pprint(pairwise_distances(expanded_universe(test_inp)))
inp = read_input(INP_PATH)
pprint(pairwise_distances(expanded_universe(inp)))

# run solution on test and full input
pprint(pairwise_distances(expanded_universe(test_inp, 100)))
pprint(pairwise_distances(expanded_universe(inp, 10**6)))