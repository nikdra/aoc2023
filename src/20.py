# aoc 2023 day 20

# input paths
INP_PATH = 'data\\20'
TEST_PATH = 'data\\20_test'

from pprint import pprint
from queue import Queue
import math
from functools import reduce

# read the input as maps/dicts of their inputs, outputs, and types
def read_input(path:str):
    inputs = {}
    outputs = {}
    types = {}
    with open(path) as file:
        for line in file.read().splitlines():
            module, out = line.replace(' ','').split('->')
            if '%' in module: 
                module = module[1:]
                types[module] = 'f' # flip-flop module
            elif '&' in module:
                module = module[1:]
                types[module] = 'c' # connection module
            else:
                types[module] = 'b' # broadcast
            outs = out.split(',')
            outputs[module] = outs
            for out in outs:
                inputs[out] = inputs.get(out, {})
                inputs[out][module] = -1
    return inputs, outputs, types


# least common multiple (thanks, wikipedia!)
def lcm(a,b):
    # define greatest common devisor (euclidean algorithm)
    def gcd(a,b):
        if b == 0:
            return a
        return gcd(b, a % b)
    # lcm = |ab| / gcd(a,b)
    return int(abs(a*b)/gcd(a,b))


# push the button a lot of times
# 1000 button presses for part1
# n button presses for part2 until we have seen each of the inputs for the last gate of rx light up
# the inputs for rx depend on your specific input
# return the number of sent low and high presses for part1
# return the number of button presses necessary to send a high pulse to rx for part2
def button(inputs, outputs, types, part2=False):
    # number of low and high pulses in the circuit
    low = 0
    high = 0
    # state initalization: all modules start with low states
    states = {module: -1 for module in outputs.keys()}
    # number of presses
    presses = 0
    # the inputs for the last connector gate before rx
    rx_inputs = [module for module in inputs['rx']] if 'rx' in inputs.keys() else []
    rx_inputs = {module: math.inf for in_module in rx_inputs for module in inputs[in_module]}
    while True:
        if presses == 1000 and not part2:
            # part1: return number of low pulses times number of high pulses
            return low*high
        if all(val != math.inf for val in rx_inputs.values()) and part2:
            # part2: assume n-partite graph for each of the inputs to rx (except button and broadcast)
            # return lcm of the number of times the button has to be pressed for each of the gates to send a high pulse
            return reduce(lambda a,b: lcm(a,b), rx_inputs.values())
        # press the button
        presses += 1
        # initialize queue of pulses
        st = Queue()
        st.put(('button', 'broadcaster', -1))
        while not st.empty(): # we just pray it terminates
            frommodule, module, pulse = st.get()
            # add up low and high pulses
            if pulse == 1:
                high += 1
            else:
                low += 1
            # module without output gates
            if module not in types.keys():
                continue
            # flip-flop module
            if types[module] == 'f':
                # if a low pulse is sent, the module switches states
                out = (-1) * states[module] if pulse == -1 else states[module]
                states[module] = out
                if pulse == -1: # flip-flops only send signals if they receive an off pulse!
                    for tomodule in outputs[module]:
                        st.put((module, tomodule, states[module]))
            # conjunction module
            elif types[module] == 'c':
                # update input from module for this module
                inputs[module][frommodule] = pulse
                # if all of the last pulses sent by each of the inputs were high, send high pulse
                out = -1 if all(inp == 1 for inp in inputs[module].values()) else 1
                # one of the modules we track for part 2
                if out == 1 and module in rx_inputs.keys():
                    # how many presses did it take to send a high pulse
                    rx_inputs[module] = min((presses, rx_inputs[module]))
                # this module always sends a pulse
                for tomodule in outputs[module]:
                    st.put((module, tomodule, out))
            # broadcaster module
            elif types[module] == 'b':
                out = pulse # just throughput the input
                for tomodule in outputs[module]:
                    st.put((module, tomodule, out))
            else: # hope we never get here
                raise Exception('unknown module')
    

# run solution on test and full input
test_inp = read_input(TEST_PATH)
pprint(button(*test_inp))
inp = read_input(INP_PATH)
pprint(button(*inp))

# run solution on full input
# no example provided here (for puzzle purposes, i suppose)
pprint(button(*inp, True))