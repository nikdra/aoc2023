# aoc 2023 day 15

# input paths
INP_PATH = 'data\\15'
TEST_PATH = 'data\\15_test'

from pprint import pprint

# read the input as a list of instructions
def read_input(path:str):
    with open(path) as file:
        return file.read().strip('\n').split(',')
    

# calculate hash of a string
def hash(string: str):
    if string == '':
        return 0
    return ((hash(string[:-1]) + ord(string[-1])) * 17) % 256


# run solution on test and full input
test_inp = read_input(TEST_PATH)
pprint(sum(hash(s) for s in test_inp))
inp = read_input(INP_PATH)
pprint(sum(hash(s) for s in inp))


# get the instructions for each element in the sequence
# return the label, the box instruction, and the focal length if applicable
def get_instructions(sequence:list):
    for inst in sequence:
        if inst[-1] == '-':
            label = inst[:-1]
            # label, remove label from box, None
            yield label, lambda box: [l for l in box if l != label], None
        else:
            # label, add to end of box if not there yet, label value
            label, fl = inst.split('=')
            yield label, lambda box: box + [label] if label not in box else box, int(fl)


# initialize the sequence
# peculiarity of the input:
# each label can only fit into exactly one box because we hash labels!
# therefore, we only keep the labels as a map and the boxes as a list
def initialize(sequence:list):
    boxes = [[] for _ in range(256)]
    values = {}
    for label, bi, v in get_instructions(sequence):
        # act according to instruction
        boxes[hash(label)] = bi(boxes[hash(label)])
        if v is not None:
            # update label
            values[label] = v 
    return boxes, values


# calculate the sum of focusing power of each lens 
# focusing power = (1+box label) * (1+label index) * (label value)
def focusing_power(boxes:list, values:dict):
    return sum(id * ind * values[label] for id, box in enumerate(boxes, 1) for ind, label in enumerate(box, 1))


# run solution on test and full input
pprint(focusing_power(*initialize(test_inp)))
pprint(focusing_power(*initialize(inp)))