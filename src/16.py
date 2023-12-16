# aoc 2023 day 16

# input paths
INP_PATH = 'data\\16'
TEST_PATH = 'data\\16_test'

from pprint import pprint

# read input as points of mirrors
def read_input(path:str):
    with open(path) as file:
        return {(x,y):c for y, line in enumerate(file.read().splitlines()) for x,c in enumerate(line) if c != '.'}
    

# possible reflections given beam direction and mirrors
REFLECTIONS = {
    ('>', '|'): lambda x, y: [(x,y-1,'^'), (x,y+1,'v')],
    ('<', '|'): lambda x, y: [(x,y-1,'^'), (x,y+1,'v')],
    ('^', '|'): lambda x, y: [(x,y-1,'^')],
    ('v', '|'): lambda x, y: [(x,y+1,'v')],
    ('>', '-'): lambda x, y: [(x+1,y,'>')],
    ('<', '-'): lambda x, y: [(x-1,y,'<')],
    ('^', '-'): lambda x, y: [(x+1,y,'>'), (x-1,y,'<')],
    ('v', '-'): lambda x, y: [(x+1,y,'>'), (x-1,y,'<')],
    ('>', '/'): lambda x, y: [(x,y-1,'^')],
    ('<', '/'): lambda x, y: [(x,y+1,'v')],
    ('^', '/'): lambda x, y: [(x+1,y,'>')],
    ('v', '/'): lambda x, y: [(x-1,y,'<')],
    ('>', '\\'): lambda x, y: [(x,y+1,'v')],
    ('<', '\\'): lambda x, y: [(x,y-1,'^')],
    ('^', '\\'): lambda x, y: [(x-1,y,'<')],
    ('v', '\\'): lambda x, y: [(x+1,y,'>')],
    ('>', '.'): lambda x, y: [(x+1,y,'>')],
    ('<', '.'): lambda x, y: [(x-1,y,'<')],
    ('^', '.'): lambda x, y: [(x,y-1,'^')],
    ('v', '.'): lambda x, y: [(x,y+1,'v')],
}
    

# energize the grid with mirrors and a starting beam
def energize(mirrors, beams=None):
    if beams is None: # part 1: start with beam facing right at top left corner
        beams = [(0, 0, '>')]
    tiles = set() # set of tiles we've visited with the direction of the beam
    xmax, ymax = map(max, zip(*mirrors.keys()))
    while len(beams) > 0: # while we have beams to process
        beam = beams.pop() # get beam
        if beam in tiles: # processed before, skip
            continue
        tiles.add(beam) # add beam to processed tiles
        x,y,c = beam
        # add reflected beam with new direction to beams to consider
        beams.extend(filter(lambda xy: 0 <= xy[0] <= xmax and 0 <= xy[1] <= ymax, REFLECTIONS[(c, mirrors.get((x,y), '.'))](x,y)))
    # return the number of distinct tiles that we've visited
    return len(set((x,y) for (x,y,_) in tiles))


# get the possible starting beams
def get_beams(mirrors):
    xmax, ymax = map(max, zip(*mirrors.keys()))
    # corners are submitted twice (depending on direction)
    # beam can start from any top or bottom edge
    for x in range(0,xmax+1):
        yield [(x,0,'v')]
        yield [(x,ymax,'^')]
    # beam can start from any left or right edge    
    for y in range(0,ymax+1):
        yield [(0,y,'>')]
        yield [(xmax,y,'<')]


# run solution on test and full input
test_inp = read_input(TEST_PATH)
pprint(energize(test_inp))
inp = read_input(INP_PATH)
pprint(energize(inp))

# run solution on test and full input
# brute force of xmax*ymax+4 input beams...takes a bit
pprint(max(energize(test_inp, beams) for beams in get_beams(test_inp)))
pprint(max(energize(inp, beams) for beams in get_beams(inp)))