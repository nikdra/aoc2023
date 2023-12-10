# aoc 2023 day 10

# input paths
INP_PATH = 'data\\10'
TEST_PATH = 'data\\10_test'
TEST2_PATH = 'data\\10_2_test'

from pprint import pprint


def read_input(path:str):
    with open(path) as file:
        return {(x, y): c for y, line in enumerate(file.read().splitlines()) for x, c in enumerate(line)}
    


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


def fill(grid):
    lp = loop(grid)
    pprint(lp)
    grid = {xy: (grid[xy] if xy in lp else '.') for xy in grid}
    new_grid = [''.join([grid[(ys,xs)] for ys in range(max(map(lambda xy: xy[0], grid.keys()))+1)]) for xs in range(max(map(lambda xy: xy[1], grid.keys()))+1)]
    print('\n'.join(new_grid))
    

    # filled = {xy[0]: 'X' for xy in grid.items() if xy[1] != '.'}
    # candidates = [xy[0] for xy in grid.items() if xy[1] == '.']
    # dirs = [(0,1), (0,-1), (1,0), (-1, 0)]
    # 
    # # perpendicular = NOT a neighbor
    # while (len(candidates) != 0):
    #     curr_region = []
    #     currx, curry = candidates.pop()
    #     for dir in dirs:
    #         dx, dy = dir
    #         newxy = (currx + dx, curry + dy)
    #         if (newxy) not in filled.keys() and grid.get(newxy, '') == '.':
    #             curr_region.append(newxy)
    #         elif grid.get(newxy, '') not in ['.', ''] and (currx, curry) not in neighbors(newxy):
    #             newxy
    #             while newxy != '.' or newxy not in :     

test_inp = read_input(TEST2_PATH)
#pprint(test_inp)
fill(test_inp)
pprint(int((len(loop(test_inp)))/2))
# inp = read_input(INP_PATH)
# pprint(int((len(loop(inp)) + 1)/2))