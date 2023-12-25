# aoc 2023 day 19

# input paths
INP_PATH = 'data\\19'
TEST_PATH = 'data\\19_test'

from pprint import pprint
from functools import reduce

# read input as maps of workflows and parts
def read_input(path: str):
    with open(path) as file:
        workflows, parts = file.read().split('\n\n')
        parts = [{kv[0]:int(kv[1]) for kv in [x.split('=') for x in part[1:-1].split(',')]} for part in parts.split('\n')]
        workflows = {k:v[:-1].split(',') for k,v in [part.split('{') for part in workflows.split('\n')]}
        return workflows, parts
    

# determine if a part is accepted by the workflow
# basically the same as below, but simpler
# this is just a quick solution, literally no thought went into this
def accept(part, workflows) -> bool:
    # starting workflow
    workflow = workflows['in']
    while True:
        for step in workflow:
            if ':' in step: # branching
                cond, nxt = step.split(':')
                cat, op, val = cond[0], cond[1], int(cond[2:])
                if op == '<':
                    op = lambda x,y: x < y
                else:
                    op = lambda x,y: x > y
                if op(part[cat], val):
                    if nxt == 'R':
                        return False
                    if nxt == 'A':
                        return True
                    workflow = workflows[nxt]
                    break
            else: # continue
                if step == 'R': # rejecting leaf
                    return False
                if step == 'A': # accepting leaf
                    return True
                # more workflows to process
                workflow = workflows[step]


# determine the number of combinations accepted by the workflow
def combinations(workflows, ranges, current='in') -> int:
    # get the workflow/space partition
    if current == 'A': # we are in an accepting leaf
        return reduce(lambda a,b: a*b, map(lambda r: r[1] - r[0] + 1, ranges.values()))
    if current == 'R': # we are in a rejecting leaf
        return 0
    # workflow
    workflow = workflows[current]
    # current volume
    volume = 0
    # for each step in the workflow, determine how many accepting combinations there are by partition
    for step in workflow[:-1]:
        cond, nxt = step.split(':')
        # get the splitting condition
        cat, op, val = cond[0], cond[1], int(cond[2:])
        if op == '<' and ranges[cat][1] > val: # split
            # make new range for split
            upper = ranges[cat][1]
            ranges[cat] = [ranges[cat][0], val-1]
            # determine accepted volume of partition
            volume += combinations(workflows, ranges.copy(), nxt)
            # continue with the rest
            ranges[cat] = [val, upper]
        elif op == '>' and ranges[cat][0] < val: # split
            # make new range for split
            lower = ranges[cat][0]
            ranges[cat] = [val+1, ranges[cat][1]]
            # determine accepted volume of partition
            volume += combinations(workflows, ranges.copy(), nxt)
            # continue with the rest
            ranges[cat] = [lower, val]
    # continue with the rest
    return volume + combinations(workflows, ranges.copy(), workflow[-1])


# run solution on test and full input
test_inp = read_input(TEST_PATH)
pprint(sum(sum(part.values()) for part in test_inp[1] if accept(part, test_inp[0])))
inp = read_input(INP_PATH)
pprint(sum(sum(part.values()) for part in inp[1] if accept(part, inp[0])))

# run solution on test and full input
pprint(combinations(test_inp[0], {'x':[1,4000], 'm':[1,4000], 'a':[1,4000], 's':[1,4000]}))
pprint(combinations(inp[0], {'x':[1,4000], 'm':[1,4000], 'a':[1,4000], 's':[1,4000]}))