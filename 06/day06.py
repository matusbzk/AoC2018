import re
import itertools


MAX_NUMBER = 999999999  # Not sure what to use instead
MIN_NUMBER = -MAX_NUMBER
regex = re.compile(r'(\d+), (\d+)')
DISTANCE_SUM_MAX = 10000


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.can_have_infinite_area = False
        self.area = 0

    def distance_from(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def closest(self, points):
        closest_dist = 999999999
        closest = None
        for other in points.points:
            dist = self.distance_from(other)
            if dist == closest_dist:
                closest = None
            if dist < closest_dist:
                closest_dist = dist
                closest = other
        return closest

    def distance_sum(self, points):
        result = 0
        for other in points.points:
            result += self.distance_from(other)
        return result


def load_point(line):
    matched = regex.match(line)
    return Point(int(matched.group(1)), int(matched.group(2)))


class PointList:
    def __init__(self, points, min_x, max_x, min_y, max_y):
        self.points = points
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y


def load_points_from_input():
    points = []
    min_x = MAX_NUMBER
    max_x = MIN_NUMBER
    min_y = MAX_NUMBER
    max_y = MIN_NUMBER

    with open("input.txt", "r") as puzzle_input:
        for line in puzzle_input:
            point = load_point(line)
            points.append(point)
            if point.x < min_x:
                min_x = point.x
            if point.x > max_x:
                max_x = point.x
            if point.y < min_y:
                min_y = point.y
            if point.y > max_y:
                max_y = point.y

    return PointList(points, min_x, max_x, min_y, max_y)


def compute_areas(points: PointList):
    """For a set of points, computes area of each of them and whether they are (can be?) finite"""
    for x, y in itertools.product(range(points.min_x, points.max_x + 1), range(points.min_y, points.max_y + 1)):
        other = Point(x, y)
        closest = other.closest(points)
        if closest is not None:
            closest.area += 1
            if x == points.min_x or x == points.max_x or y == points.min_y or y == points.max_y:
                closest.can_have_infinite_area = True
    return points


def biggest_finite_area(points: PointList):
    """From a set of points, returns the biggest finite area

    The set of points need to have computed areas before!"""
    biggest_finite = 0
    for point in points.points:
        if not point.can_have_infinite_area and point.area > biggest_finite:
            biggest_finite = point.area
    return biggest_finite


def number_of_safe_points(points: PointList):
    can_be_more = False  # is it possible there is some safe point which is not in a given rectangle?
    result = 0
    for x, y in itertools.product(range(points.min_x, points.max_x + 1), range(points.min_y, points.max_y + 1)):
        other = Point(x, y)
        if other.distance_sum(points) < DISTANCE_SUM_MAX:
            result += 1
            if x == points.min_x or x == points.max_x or y == points.min_y or y == points.max_y:
                can_be_more = True
    if can_be_more:  # in my case it was not possible
        print("The result of number_of_safe_points may be underestimated.")
    return result


points_list = load_points_from_input()
points_list = compute_areas(points_list)

print(biggest_finite_area(points_list))  # part 1

print(number_of_safe_points(points_list))  # part 2
