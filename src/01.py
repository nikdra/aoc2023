# aoc 2023 day 1

# input paths
TEST_PATH = 'data\\01_test'
INP_PATH = 'data\\01'

import re

# read input function
def read_input(path: str) -> [str]:
    with open(path, 'r') as file:
        return [line for line in file.read().splitlines()]

# get the first and last digit in string using regex
def first_last_digit_value(string: str) -> int:
    matches = re.findall("(1|2|3|4|5|6|7|8|9)", string)
    return int(matches[0] + matches[-1])

# part 1: run solution on test and full input
test_input = read_input(TEST_PATH)
input = read_input(INP_PATH)
print(sum(first_last_digit_value(line) for line in test_input))
print(sum(first_last_digit_value(line) for line in input))

# part 2: new test input
TEST_PATH = 'data\\01_2_test'
test_input = read_input(TEST_PATH)

# find all digits in a string, regardless if as word or digit
def first_last_digit_string_value(string: str):
    value_map = {
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        '6': '6',
        '7': '7',
        '8': '8',
        '9': '9',
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }
    matches = re.findall(r'(?=(1|2|3|4|5|6|7|8|9|one|two|three|four|five|six|seven|eight|nine))', string)
    return int(value_map[matches[0]] + value_map[matches[-1]])

# part 2: run solution on test and full input
print(sum(first_last_digit_string_value(line) for line in test_input))
print(sum(first_last_digit_string_value(line) for line in input))