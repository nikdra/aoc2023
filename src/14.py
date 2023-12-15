# aoc 2023 day 14

# input paths
INP_PATH = 'data\\14'
TEST_PATH = 'data\\14_test'

from pprint import pprint

def read_input(path:str):
    with open(path) as file:
        return {(x,y): c for y, line in enumerate(file.read().splitlines(),1) for x,c in enumerate(line,1) if c != '.'} 
    
def map_to_array(grid:dict):
    return [[grid.get((xs,ys), '.') for xs in range(1,max(map(lambda xy: xy[0], grid.keys()))+1)] for ys in range(1,max(map(lambda xy: xy[1], grid.keys()))+1)]


def tilt_north(grid: dict):
    grid = grid.copy()
    for (x,y), c in grid.copy().items():
        del grid[(x,y)]
        if c == 'O':
            while True:
                yn = y-1
                while grid.get((x,yn), '.') == 'O' and yn >= 1:
                    yn = yn-1
                if grid.get((x,yn), 'O') == '#' or yn < 1:
                    break
                y = yn
        grid[(x,y)] = c
    # print('\n'.join(''.join(l) for l in map_to_array(grid)))
    # print('')
    return grid
    

def total_load(grid: dict):
    ymax = max(map(lambda kv: kv[1], grid.keys()))
    return sum(ymax-y+1 for (x,y),c in grid.items() if c == 'O')


def tilt_west(grid:dict):
    grid = grid.copy()
    for (x,y), c in grid.copy().items():
        del grid[(x,y)]
        if c == 'O':
            while True:
                xn = x-1
                while grid.get((xn,y), '.') == 'O' and xn >= 1:
                    xn = xn-1
                if grid.get((xn,y), 'O') == '#' or xn < 1:
                    break
                x = xn
        grid[(x,y)] = c
    #print('\n'.join(''.join(l) for l in map_to_array(grid)))
    #print('')
    return grid


def tilt_south(grid:dict):
    grid = grid.copy()
    ymax = max(map(lambda kv: kv[1], grid.keys())) + 1
    for (x,y), c in grid.copy().items():
        del grid[(x,y)]
        if c == 'O':
            while True:
                yn = y+1
                while grid.get((x,yn), '.') == 'O' and yn < ymax:
                    yn = yn+1
                if grid.get((x,yn), 'O') == '#' or yn == ymax:
                    break
                y = yn
        grid[(x,y)] = c
    #print('\n'.join(''.join(l) for l in map_to_array(grid)))
    #print('')
    return grid


def tilt_east(grid:dict):
    grid = grid.copy()
    xmax = max(map(lambda kv: kv[0], grid.keys())) + 1
    for (x,y), c in grid.copy().items():
        del grid[(x,y)]
        if c == 'O':
            while True:
                xn = x+1
                while grid.get((xn,y), '.') == 'O' and xn < xmax:
                    xn = xn+1
                if grid.get((xn,y), 'O') == '#' or xn == xmax:
                    break
                x = xn
        grid[(x,y)] = c
    #print('\n'.join(''.join(l) for l in map_to_array(grid)))
    #print('')
    return grid


test_inp = read_input(TEST_PATH)
# pprint(total_load(tilt_north(test_inp)))
# # 
inp = read_input(INP_PATH)
pprint(total_load(tilt_north(inp)))



def cycle(grid:dict, cycles=1000000000):
    cache = []
    while cycles > 0:
        cycles -= 1
        if grid in cache: # have we been here before?
            break
        cache.append(grid) # index tells us the modulo
        grid = tilt_east(tilt_south(tilt_west(tilt_north(grid))))
        # print('\n'.join(''.join(l) for l in map_to_array(grid)))

    if cycles == 0:
        return total_load(grid)

    # where does the cycle start?
    cycle_start = cache.index(grid)
    # extract cycle
    cycle = cache[cycle_start:]
    # get the result of rotating the rest of the cycles by virtue of modulo
    return total_load(cycle[(cycles + 1) % len(cycle)])


# print('\n'.join(''.join(l) for l in map_to_array(test_inp)))
# print('')
pprint(cycle(test_inp))
pprint(cycle(inp))