# aoc 2023 day 17

# input paths
INP_PATH = 'data\\17'
TEST_PATH = 'data\\17_test'
TEST_PATH2 = 'data\\17_2_test'

from pprint import pprint
from heapq import heappush, heappop

# read input as points of heat loss
def read_input(path:str):
    with open(path) as file:
        return {(x,y):int(c) for y, line in enumerate(file.read().splitlines()) for x,c in enumerate(line) if c != '.'}


# dijkstra with some extra states
def dijkstra(grid:dict, mindist = 1, maxdist = 3):
    seen = set() # important so we don't infa-loop
    xmax, ymax = map(max, zip(*grid.keys())) # end position

    q = [] # our state queue
    # (x, y) = point
    # (dx, dy) = velocity
    # state = cost, x, y, dx, dy, distance travelled
    heappush(q, (0,0,0,1,0,1)) # add move right
    heappush(q, (0,0,0,0,1,1)) # add move down

    while True:
        # get the next state
        (cost, x, y, dx, dy, distance) = heappop(q)

        # calculate new point
        newx, newy = x + dx, y + dy

        # skip, we've already been here before
        if (newx, newy, dx, dy, distance) in seen:
            continue
        
        # bound checking
        if (newx, newy) not in grid.keys():
            continue
        
        # calculate cost to get here
        newcost = cost + grid[(newx, newy)]

        # are we done? - we have to travel at least mindist squares to get to a valid end state
        if (newx, newy) == (xmax, ymax) and distance >= mindist:
            return newcost
        
        # add new state to set of seen states
        newstate = (newx, newy, dx, dy, distance)
        seen.add(newstate)
        # print(seen)

        # turn left and right if we can - we must travel the minimum distance
        if distance >= mindist:
            heappush(q, (newcost, newx, newy, -dy, dx, 1))
            heappush(q, (newcost, newx, newy, dy, -dx, 1))

        # go straight if we can - no more than the maximum distance
        if distance < maxdist:
            heappush(q, (newcost, newx, newy, dx, dy, distance + 1))


# test solution on test and full input
test_inp = read_input(TEST_PATH)
print(dijkstra(test_inp))
inp = read_input(INP_PATH)
print(dijkstra(inp))

# test solution on test and full input
print(dijkstra(test_inp, 4, 10))
test_inp = read_input(TEST_PATH2)
print(dijkstra(test_inp, 4, 10))
print(dijkstra(inp, 4, 10))