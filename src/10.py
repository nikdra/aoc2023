# aoc 2023 day 10

# input paths
INP_PATH = 'data\\10'
TEST_PATH = 'data\\10_test'
TEST2_PATH = 'data\\10_2_test'

from pprint import pprint


# read input as (x,y): character
def read_input(path:str):
    with open(path) as file:
        return {(x, y): c for y, line in enumerate(file.read().splitlines()) for x, c in enumerate(line)}
    

# dict of pipe neighbors
CONNECTIONS = {
    '|' : lambda x,y: ((x, y-1), (x, y+1)),
    '-' : lambda x,y: ((x-1, y), (x+1, y)),
    'L' : lambda x,y: ((x, y-1), (x+1, y)),
    'J' : lambda x,y: ((x-1, y), (x, y-1)),
    '7' : lambda x,y: ((x-1, y), (x, y+1)),
    'F' : lambda x,y: ((x+1, y), (x, y+1)),
    '.' : lambda x,y: (),
    'S' : lambda x,y: ((x-1,y), (x+1,y), (x,y+1),(x,y-1))
}


def neighbors(x, y, grid):
    return (c for c in CONNECTIONS[grid[x,y]](x,y) if c in grid.keys() and (x,y) in CONNECTIONS[grid[c]](*c))


# find the loop from the starting character
def loop(grid): # assumes perfect loop at start
    discovered = []
    start = next(filter(lambda kv: kv[1] == 'S', grid.items()))[0]
    neigh = list(neighbors(*start, grid))
    while not all(map(lambda xy: xy in discovered, neigh)):
        discovered.append(start)
        start = next(filter(lambda xy: xy not in discovered, neigh))
        neigh = list(neighbors(*start, grid))
    discovered.append(start)
    return discovered


# transform our map representation to an array like in the input
def map_to_array(grid):
    return [[grid[(xs,ys)] for xs in range(max(map(lambda xy: xy[0], grid.keys()))+1)] for ys in range(max(map(lambda xy: xy[1], grid.keys()))+1)]


# replace the S character with a "pipe"
def replace_S(grid):
    sx, sy = next(filter(lambda kv: kv[1] == 'S', grid.items()))[0]
    d_neighbors = [[x-sx,y-sy] for (x,y) in neighbors(sx, sy, grid)]
    if d_neighbors == [[0,1], [0,-1]]:
        return '|'
    if d_neighbors == [[1,0], [-1,0]]:
        return '-'
    if d_neighbors == [[-1,0], [0,1]]:
        return '7'
    if d_neighbors == [[1,0], [0,-1]]:
        return 'L'
    if d_neighbors == [[1,0],[0,1]]:
        return 'F'
    if d_neighbors == [[-1,0],[0,-1]]:
        return 'J'
    raise Exception('bad')


# count the number of tiles inside the loop
def count_inside(grid):
    # find the loop
    lp = loop(grid)
    # print the number of steps to be from the furthest point in the starting position (part 1)
    pprint(len(lp)//2)
    # remove tiles not on the loop, replace S with pipe
    grid = {xy: (grid[xy] if xy in lp else '.') for xy in grid}
    s = next(filter(lambda kv: kv[1] == 'S', grid.items()))[0]
    grid[s] = replace_S(grid)
    grid = map_to_array(grid) # back to array form for looping
    count = 0
    for line in grid:
        inside = False # inside
        for char in line:
            if char == '.': # free tile
                if inside:
                    count += 1
            else: 
                if char == '-': # along the axis we are reading - continue
                    continue
                if char in ['|', 'F', '7']: # choose either F and 7 or L and J to change in-out perception 
                    inside = not inside
    return count
    

# run soltion on test and full output
test_inp = read_input(TEST2_PATH)
pprint(count_inside(test_inp))
inp = read_input(INP_PATH)
pprint(count_inside(inp))