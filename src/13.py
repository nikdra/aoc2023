# aoc 2023 day 13

# input paths
INP_PATH = 'data\\13'
TEST_PATH = 'data\\13_test'

from pprint import pprint

# read the input as a list of points for each grid in the input
def read_input(path: str):
    with open(path) as file:
        return [{(x, y): c for y, line in enumerate(grid.split('\n'), 1) for x, c in enumerate(line, 1)} for grid in file.read().split("\n\n")]
    

# reflect a point along the y-axis
def reflect_x(x, y, dx):
    return 2*dx-x+1, y


# reflect a point along the x-axis
def reflect_y(x, y, dy):
    return x, 2*dy-y+1
    

# find the reflection axis 
# return the y-axis if it exists, otherwise the x-axis * 100
# smudge: if no smudge, return perfect reflection axis
# if smudge, return reflection axis with exactly one imperfection
def reflection_axis(points: dict, smudge = False):
    # brute force?
    maxx, maxy = map(max, zip(*points.keys()))
    for xa in range(1,maxx):
        reflected = {reflect_x(*point,xa):c for point, c in points.items() if 2*xa+1-maxx <= point[0] <= xa}
        diff = len(set(reflected.items()) - set(points.items()))
        if diff - (1 if smudge else 0) == 0:
            return xa
    for ya in range(1,maxy):
        reflected = {reflect_y(*point,ya):c for point, c in points.items() if 2*ya+1-maxy <= point[1] <= ya}
        diff = len(set(reflected.items()) - set(points.items()))
        if diff - (1 if smudge else 0) == 0:
            return ya * 100
    raise Exception('oh no')


# run solution on test and full input
test_inp = read_input(TEST_PATH)
pprint([reflection_axis(pts) for pts in test_inp])
inp = read_input(INP_PATH)
pprint(sum([reflection_axis(pts) for pts in inp]))

# run soluton on test and full input
pprint([reflection_axis(pts, True) for pts in test_inp])
pprint(sum([reflection_axis(pts, True) for pts in inp]))