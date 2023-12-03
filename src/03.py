# aoc 2023 day 3

# input paths
INP_PATH = 'data\\03'
TEST_PATH = 'data\\03_test'

from pprint import pprint
from functools import reduce

# read input
# get a map of all inputs plus the array
# use the array for iteration, and the map for neighbor search
# we carry the newline symbol because then we have an extra character for when there is a number at the end of a line and one on the start of the next one
def read_input(path: str):
    with open(path) as file:
        lines = file.readlines()
        return {(x,y): c for x, line in enumerate(lines) for y, c in enumerate(line)}, lines
    

# find all neighbors of a position that are a symbol (not number, dot or newline)
def symbol_neighbors(x: int, y: int, schematic: dict) -> bool:
    return filter(lambda c: not c[1].isdigit() and c[1] not in ['.', '\n'], (((xs, ys), schematic.get((xs, ys), '.')) for xs in range(x-1,x+2) for ys in range(y-1,y+2)))


# find all part numbers i.e., numbers adjacent to a symbol
# we go line by line, character for character
def part_numbers(schematic: dict, lines: list):
    num = ''
    for x, line in enumerate(lines):
        for y, c in enumerate(line):
            if c.isdigit():
                num += c
            else:
                if num != '':
                    # double any because we have neighbors for each digit in our number (could be done better)
                    if any(any(symbol_neighbors(x,ys,schematic)) for ys in range(y-len(num), y)):
                        yield int(num)
                    num = ''


# test solution on test and full input
test_input = read_input(TEST_PATH)
pprint(sum(part_numbers(*test_input)))
input = read_input(INP_PATH)
pprint(sum(part_numbers(*input)))


# find all the gears and return their sum
def gear_ratios(schematic: dict, lines: list):
    gears = {}
    num = ''
    for x, line in enumerate(lines):
        for y, c in enumerate(line):
            if c.isdigit():
                num += c
            else:
                if num != '':
                    stars = set(star_pos for ys in range(y-len(num), y) for star_pos, c in symbol_neighbors(x, ys, schematic) if c == '*')
                    for star in stars:
                        gears[star] = gears.get(star,[]) + [int(num)]
                    num = ''
    # a gear is any '*' which has exactly two numbers adjacent to it
    return sum((reduce(lambda a,b: a*b, lst) for lst in map(lambda g: g[1], filter(lambda k: len(k[1]) == 2, gears.items()))))


# test solution on test and full input
pprint(gear_ratios(*test_input))
pprint(gear_ratios(*input))