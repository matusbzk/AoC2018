import re
from collections import defaultdict


regex = re.compile(r'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>')
MAX_SIZE = 100  # if size of the picture is bigger than this, it is too large to consider as an option
MAX_NUMBER = 999999999  # Not sure what to use instead
MIN_NUMBER = -MAX_NUMBER


class Point:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def position_after(self, seconds):
        return self.x + seconds * self.dx, self.y + seconds * self.dy


class PointSet:
    def __init__(self):
        self.points = []
        self.seconds = 0

    def add_point(self, point: Point):
        self.points.append(point)

    def min_x(self):
        return min(self.points, key=lambda p: p.x).x

    def max_x(self):
        return max(self.points, key=lambda p: p.x).x

    def min_y(self):
        return min(self.points, key=lambda p: p.y).y

    def max_y(self):
        return max(self.points, key=lambda p: p.y).y

    def pretty_print(self):
        drawing = defaultdict(bool)
        # using methods min_x, max_x, etc. here did not work for some reason
        min_x = MAX_NUMBER
        max_x = MIN_NUMBER
        min_y = MAX_NUMBER
        max_y = MIN_NUMBER

        for point in self.points:
            drawing[point.x, point.y] = True
            if min_x > point.x:
                min_x = point.x
            if max_x < point.x:
                max_x = point.x
            if min_y > point.y:
                min_y = point.y
            if max_y < point.y:
                max_y = point.y
        min_x -= 1
        min_y -= 1
        max_x += 2
        max_y += 2

        print("-" * (max_x - min_x))
        print("After %d seconds." % self.seconds)
        for y in range(min_y, max_y):
            line = ""
            for x in range(min_x, max_x):
                if drawing[x, y]:
                    line += "#"
                else:
                    line += "."
            print(line)
        print("-" * (max_x - min_x))

    def next_second(self):
        for point in self.points:
            point.x += point.dx
            point.y += point.dy
        self.seconds += 1

    def is_small_enough_to_consider(self):
        size_x = self.max_x() - self.min_x()
        size_y = self.max_y() - self.min_y()
        return size_x < MAX_SIZE and size_y < MAX_SIZE


def load_input():
    result = PointSet()
    with open("input.txt", "r") as puzzle_input:
        for line in puzzle_input:
            matched = regex.match(line)
            x = int(matched.group(1))
            y = int(matched.group(2))
            dx = int(matched.group(3))
            dy = int(matched.group(4))
            result.add_point(Point(x, y, dx, dy))
    return result


def main():
    points = load_input()
    while True:
        if points.is_small_enough_to_consider():
            points.pretty_print()
            cmd = input()
            if cmd == "exit":
                break
        points.next_second()


main()
