import re
from collections import defaultdict
import itertools


class Claim:
    regex = re.compile("#(\\d+) @ (\\d+),(\\d+): (\\d+)x(\\d+)")

    def __init__(self, input_line):
        matched = self.regex.match(input_line)
        self.claim_id = int(matched.group(1))
        self.x = int(matched.group(2))
        self.y = int(matched.group(3))
        self.width = int(matched.group(4))
        self.height = int(matched.group(5))

    def add_squares_to_dict(self, dictionary):
        for i, j in itertools.product(range(self.width), range(self.height)):
            dictionary[i + self.x, j + self.y] += 1

    def is_overlapping(self, dictionary):
        for i, j in itertools.product(range(self.width), range(self.height)):
            if dictionary[i + self.x, j + self.y] != 1:
                return True
        return False


def get_nonoverlapping(claims_list, squares_dict):
    for claim_item in claims_list:
        if not claim_item.is_overlapping(squares_dict):
            return claim_item


squares = defaultdict(int)
claims = []

with open("input.txt", "r") as puzzle_input:
    for line in puzzle_input:
        claim = Claim(line)
        claims.append(claim)
        claim.add_squares_to_dict(squares)

count = 0
for i in squares.values():
    if i > 1:
        count += 1

print(count)  # part 1

nonoverlapping = get_nonoverlapping(claims, squares)

print(nonoverlapping.claim_id)  # part 2
