# aoc 2023 day 5

# input paths
INP_PATH = 'data\\05'
TEST_PATH = 'data\\05_test'

from pprint import pprint

# read input as seeds, list of maps
# each map is of the form [dest_start, [lower_bound, upper_bound]]
def read_input(path: str):
    with open(path) as file:
        inps = file.read().split('\n\n')
        seeds = [int(x) for x in inps[0].split(': ')[1].split(' ')]
        ranges = [[[m[0], [m[1], m[1] + m[2] - 1]] for m in map(lambda x: list(map(lambda i: int(i), x.split(' '))), maps.split('\n')[1:])] for maps in inps[1:]]
        return seeds, ranges
    

# for a range of seeds, find the minimum location
def seed_destination(seed_ranges, maps):
    for m in maps: # for each of our transformation maps (in the correct order)
        new_seeds = [] # container for new seeds
        for seed_range in seed_ranges: # for each of our seed ranges
            mapped_ranges = [] # container for mapped ranges of our current seed range
            for r in m: # for each map instruction of our current map group
                # find overlap
                dest, src = r[0], r[1]
                start, end = max(src[0], seed_range[0]), min(src[1], seed_range[1])
                if start <= end: 
                    # overlap found, add new mapped ranges to our container
                    new_seeds.append([dest +  start - src[0], dest + end - src[0]])
                    mapped_ranges.append([start, end]) # keep track of mapped range
            if mapped_ranges != []: # if we have mappings
                mapped_ranges = sorted(mapped_ranges, key=lambda x: x[0]) # for the rest of unmapped: fill the gaps by sorting
                for i, range in enumerate(mapped_ranges):
                    if i == 0: # first
                        if seed_range[0] != range[0]: # gap at start
                            new_seeds.append([seed_range[0], range[0]-1])
                    elif i < len(mapped_ranges) - 1: # gap inbetween mapped ranges
                        if range[1] != mapped_ranges[i+1][0]: # gap
                            new_seeds.append([range[1]+1, mapped_ranges[i][0]-1])
                    else: # last
                        if seed_range[1] != range[1]: # gap at end
                            new_seeds.append([range[1]+1, seed_range[1]])
            else: 
                # no mappings at all, add the old range as a new range
                new_seeds.append(seed_range)
        seed_ranges = new_seeds # take over the mapped seed ranges in the next iteration
    # return the minimum number in our intervals
    return min(s[0] for s in seed_ranges)

# run solution on test and full input
test_inp = read_input(TEST_PATH)
pprint(min(seed_destination([[seed, seed]], test_inp[1]) for seed in test_inp[0]))
inp = read_input(INP_PATH)
pprint(min(seed_destination([[seed, seed]], inp[1]) for seed in inp[0]))

# run solution on test and full input (this time, as pairs of ranges)
pprint(min(seed_destination([[test_inp[0][i],test_inp[0][i] + test_inp[0][i+1] - 1]], test_inp[1]) for i in range(0, len(test_inp[0]), 2)))
pprint(min(seed_destination([[inp[0][i], inp[0][i] + inp[0][i+1] - 1]], inp[1]) for i in range(0, len(inp[0]), 2)))