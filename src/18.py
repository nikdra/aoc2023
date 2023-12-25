# aoc 2023 day 18

# input paths
INP_PATH = 'data\\18'
TEST_PATH = 'data\\18_test'

from pprint import pprint
from itertools import accumulate

# get instructions as list of direction, length, color
def read_input(path:str):
    with open(path) as file:
        return [line.split() for line in file.read().splitlines()]
    

# directions as dx, dy instructions
DIRECTIONS = {
    'R': (1, 0),
    'L': (-1,0),
    'U': (0,-1),
    'D': (0,1)
}

# convert digits 1..4 to directions
INTDIR = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U'
}
    

# calculate area to dig
def dig(instructions, part2=False):
    if part2:
        # part 2: last digit is direction, four digits before that are the number in hexadecimal
        instructions = [[INTDIR[color[-2]], int(color[2:-2], 16), color] for _,_,color in instructions]

    # generate a list of edges starting from (0,0) and adding up all the directions in the instructions
    edges = list(accumulate([(DIRECTIONS[dir][0] * int(l), DIRECTIONS[dir][1] * int(l)) for dir, l, _ in instructions], lambda a,b: (a[0] + b[0], a[1] + b[1]), initial= (0,0)))

    def shoelace(vertices):
        #The Shoelace Algorithm - www.101computing.net/the-shoelace-algorithm
        numberOfVertices = len(vertices)
        sum1 = 0
        sum2 = 0
        
        for i in range(0,numberOfVertices-1):
            sum1 = sum1 + vertices[i][0] *  vertices[i+1][1]
            sum2 = sum2 + vertices[i][1] *  vertices[i+1][0]
        
        #Add xn.y1
        sum1 = sum1 + vertices[numberOfVertices-1][0]*vertices[0][1]   
        #Add x1.yn
        sum2 = sum2 + vertices[0][0]*vertices[numberOfVertices-1][1]   
        
        # we also have to add the edge as an area of a cubic meter
        area = (abs(sum1 - sum2) + sum(map(int, (length for _,length,_ in instructions)))) / 2 + 1
        return int(area)
    
    # shoelace for area defined by the edges
    return shoelace(edges)
    

# run solution on test and full input
test_inp = read_input(TEST_PATH)
pprint(dig(test_inp))
inp = read_input(INP_PATH)
pprint(dig(inp))

# run solution on test and full input
pprint(dig(test_inp, True))
pprint(dig(inp, True))