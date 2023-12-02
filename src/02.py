# aoc 2023 day 2

# input paths
INP_PATH = 'data\\02'
TEST_PATH = 'data\\02_test'

from pprint import pprint

# read input function: get a dict of color: number for each round of a game
# [[{color: number, color: number, color: number}, {color:..}], [{..}, {..}], ..]
# yes, i am cheating as i don't parse the game id (ids are ascending, use range)
def read_input(path: str):
    with open(path) as file:
        return [[{li[1]: int(li[0]) for li in [x.split(' ') for x in lin.split(', ')]} for lin in line.split(': ')[1].split('; ')] for line in file.read().splitlines()]
    

# function to determine whether a game is possible
def possible(game):
    return all(map(lambda t: t.get('red', 0) <= 12 and t.get('green', 0) <= 13 and t.get('blue', 0) <= 14, (turn for turn in game)))
    

# part 1: run solution on test and full input
test_input = read_input(TEST_PATH)
pprint(sum(id for (val, id) in zip((possible(game) for game in test_input), range(1, len(test_input) + 1)) if val))
input = read_input(INP_PATH)
pprint(sum(id for (val, id) in zip((possible(game) for game in input), range(1, len(input) + 1)) if val))


# determine power of a game
# multiply the maximum of each color in a game (use 1 as default so we don't mess up multiplication)
def power(game):
    return max(turn.get('red', 1) for turn in game) * max(turn.get('green', 1) for turn in game) * max(turn.get('blue', 1) for turn in game)


# part 2: run solution on test and full input
pprint(sum(power(game) for game in test_input))
pprint(sum(power(game) for game in input))