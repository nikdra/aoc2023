# aoc 2023 day 7

# input paths
INP_PATH = 'data\\07'
TEST_PATH = 'data\\07_test'

from pprint import pprint
from functools import cmp_to_key
from collections import Counter

# read input as hand, bid
def read_input(path:str):
    with open(path) as file:
        return [(line[0], int(line[1])) for line in [li.split(' ') for li in file.read().splitlines()]]
    

# determine type of hand (with jokers)
def hand_type(cards, joker=False):
    counts = Counter(cards)
    num_jokers = 0
    if joker:
        num_jokers = counts.get('J', 0)
    counts = Counter(filter(lambda x: x != 'J', cards)).values() if joker else counts.values()
    if num_jokers == 5 or max(counts) + num_jokers == 5:
        return 6
    if max(counts) + num_jokers == 4:
        return 5
    if (num_jokers == 1 and Counter(counts).get(2,0) == 2) or (3 in counts and 2 in counts): # "pure" full house or XXYYJ
        return 4
    if max(counts) + num_jokers == 3:
        return 3
    if Counter(counts).get(2,0) == 2:
        return 2
    if max(counts) + num_jokers == 2:
        return 1
    return 0
    

# compare hands function: return 1 if a bigger than b else -1
def compare_hands(a, b, joker=False):
    # comparison function
    a_cards, _ = a
    b_cards, _ = b
    a_hand = hand_type(a_cards, joker)
    b_hand = hand_type(b_cards, joker)
    if a_hand != b_hand: # first tiebreaker: hand strength
        return 1 if a_hand > b_hand else -1
    card_strength = '23456789TJQKA' if not joker else 'J23456789TQKA'
    # map hands to values for each card
    a_hand = list(map(lambda x: [card_strength.index(x)], a_cards))
    b_hand = list(map(lambda x: [card_strength.index(x)], b_cards))
    if a_hand > b_hand:
        return 1
    return -1 # assume no ties


# run solution on test and full input
test_inp = read_input(TEST_PATH)
pprint(sum(i*v for i,v in enumerate(map(lambda hv: hv[1], sorted(test_inp,key=cmp_to_key(compare_hands))), 1)))
inp = read_input(INP_PATH)
pprint(sum(i*v for i,v in enumerate(map(lambda hv: hv[1], sorted(inp,key=cmp_to_key(compare_hands))), 1)))


# run solution on test and full input (with jokers)
pprint(sum(i*v for i,v in enumerate(map(lambda hv: hv[1], sorted(test_inp,key=cmp_to_key(lambda a,b: compare_hands(a,b,True)))), 1)))
pprint(sum(i*v for i,v in enumerate(map(lambda hv: hv[1], sorted(inp,key=cmp_to_key(lambda a,b: compare_hands(a,b,True)))), 1)))