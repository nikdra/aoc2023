# aoc 2023 day 22

from pprint import pprint
import copy

# input paths
INP_PATH = 'data\\22'
TEST_PATH = 'data\\22_test'


class Brick(object):
    def __init__(self, pos1, pos2, id):
        self.pos1 = pos1
        self.pos2 = pos2
        self.id = id

    @property
    def lowest_z(self):
        return min(self.pos1[2], self.pos2[2])
    
    @property
    def highest_z(self):
        return max(self.pos1[2], self.pos2[2])
    
    def fall_by_distance(self, distance):
        self.pos1[2] -= distance
        self.pos2[2] -= distance

    def intersects(self, other):
        x_axis = max(self.pos1[0], other.pos1[0]) - min(self.pos2[0], other.pos2[0]) <= 0
        y_axis = max(self.pos1[1], other.pos1[1]) - min(self.pos2[1], other.pos2[1]) <= 0
        z_axis = max(self.pos1[2], other.pos1[2]) - min(self.pos2[2], other.pos2[2]) <= 0
        
        return (x_axis, y_axis, z_axis)
    
    def __str__(self) -> str:
        return f"id: {id}, pos1: {self.pos1}, pos2: {self.pos2}"
    
    def raise_by_one(self):
        return Brick(pos1=self.pos1, pos2=self.pos2[0:2]+[self.pos2[2]+1], id=self.id)


def read_input(path:str) -> list[Brick]:
    with open(path) as file:
        return [Brick(*[list(map(int, point.split(','))) for point in line.split('~')], i) for i, line in enumerate(file.read().splitlines())]


def fall(bricks: list[Brick]):
    # sort bricks by lowest z-axis
    sorted_bricks = sorted(copy.deepcopy(bricks), key=lambda x: x.lowest_z)
    # for each sorted brick: let it fall 
    fallen_bricks : list[Brick] = []
    for brick in sorted_bricks:
        intersecting_bricks : list[Brick] = [b for b in fallen_bricks if all(brick.intersects(b)[0:2])]
        distance = brick.lowest_z - max((b.highest_z for b in intersecting_bricks), default=0) - 1
        brick.fall_by_distance(distance=distance)
        fallen_bricks.append(brick)

    return fallen_bricks


def supported_by(bricks: list[Brick]):
    raised_bricks = [b.raise_by_one() for b in copy.deepcopy(bricks)]
    return [[b.id for b in raised_bricks if all(br.intersects(b)) and br.id != b.id] for br in bricks]


def part1(bricks: list[Brick]):
    fallen_bricks = fall(bricks)
    # find all supporters of all blocks
    supps = supported_by(fallen_bricks) 
    # a block is unsafe to remove if it is the _only_ supporter of a block
    # a block can be the only supporter of multiple blocks
    unsafe_remove = set(a for b in supps for a in b if len(b) == 1)
    # return number of blocks that can be safely removed (all blocks - unsafe blocks)
    return len(fallen_bricks) - len(unsafe_remove)


def chain(brick, supportedBy):
    q = [brick]
    fallen = set()
    while len(q) != 0:
        b = q.pop()
        fallen.add(b)
        supportedBy = {i:[v for v in val if v != b] for i,val in supportedBy.items()}
        q.extend(i for i,v in supportedBy.items() if v == [])
        supportedBy = {i:v for i,v in supportedBy.items() if v != []}
    # print(f"brick {brick} let {len(fallen)-1} bricks fall")
    return len(fallen) - 1


def part2(bricks: list[Brick]):
    fallen_bricks = fall(bricks)
    # we already know this one
    supportedBy = {b.id:v for b,v in zip(fallen_bricks, supported_by(fallen_bricks)) if v != []}
    unsafe = set(val[0] for val in supportedBy.values() if len(val) == 1)
    # speedup: only consider unsafe releases
    return sum(chain(brick, supportedBy=copy.deepcopy(supportedBy)) for brick in unsafe)


test_inp = read_input(TEST_PATH)
pprint(part1(test_inp))
pprint(part2(test_inp))

inp = read_input(INP_PATH)
pprint(part1(inp))
pprint(part2(inp))