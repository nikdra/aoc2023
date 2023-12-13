# aoc 2023 day 12

# input paths
INP_PATH = 'data\\12'
TEST_PATH = 'data\\12_test'

from pprint import pprint
import functools


# return tuple of spring list, groups
# groups are a tuple because lists are not hashable for caching
def read_input(path:str):
    with open(path) as file:
        return [(x[0], tuple(map(int, x[1].split(',')))) for line in file.read().splitlines() for x in [line.split()]] 
    

# recursion takes too long? slap a cache on there
# find the number of arrangements given a list of springs and groups of damaged springs
@functools.lru_cache(maxsize=None)
def arrangements(springs, groups):
    if springs == '': # recursion done
        return 1 if groups == () else 0
    if springs[0] == '.':
        return arrangements(springs[1:], groups)
    if springs[0] == '?':
        return arrangements(springs[1:], groups) + arrangements('#' + springs[1:], groups)
    # damaged spring. '#'
    if groups == () or len(springs) < groups[0] or any(c == '.' for c in springs[:groups[0]]):
        return 0 # no group assignment possible
    if len(springs) == groups[0] or springs[groups[0]] != '#': # can we make a contained group?
        return arrangements(springs[groups[0]+1:], groups[1:])
    # no
    return 0


# unfold the map, multiply every input by five (separate list of springs by '?')
def unfold(springs, groups):
    return '?'.join(springs for _ in range(5)), groups * 5


# run solution on test and full input
test_inp = read_input(TEST_PATH)
pprint(sum(arrangements(*sg) for sg in test_inp))
inp = read_input(INP_PATH)
pprint(sum(arrangements(*sg) for sg in inp))

# run solution on test and full input, but unfold first
pprint(sum(arrangements(*unfold(*sg)) for sg in test_inp))
pprint(sum(arrangements(*unfold(*sg)) for sg in inp))
