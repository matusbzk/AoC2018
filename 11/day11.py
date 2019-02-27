# This works on example inputs, but my input does not pass with it.
# I am not able to find why is it wrong though.


from itertools import product
from collections import defaultdict
from math import ceil, floor


SERIAL_NUMBER = 18


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.power_level = (((((x+10) * y + SERIAL_NUMBER) * (x+10)) % 1000) // 100) - 5

    def power_level_of_3x3_square(self):
        result = 0
        for x, y in product(range(self.x, self.x+3), range(self.y, self.y + 3)):
            cell = Cell(x, y)
            result += cell.power_level()
        return result


class CellSquare:
    def __init__(self):
        self.cells = defaultdict(int)

    def add_cell(self, cell: Cell):
        self.cells[cell.x, cell.y] = cell.power_level
        self.cells[cell.x, cell.y, 1] = cell.power_level

    def power_level_of_3x3_square(self, x, y):
        return self.power_level_of_square(x, y, 3)

    def power_level_of_square(self, x, y, size):
        result = 0
        for a, b in product(range(x, x + size), range(y, y + size)):
            result += self.cells[a, b]
        return result

    def maximum_3x3_square(self):
        result = -999
        result_x = None
        result_y = None
        for x, y in product(range(298), range(298)):
            if self.cells[x, y, 3] == 0:
                self.cells[x, y, 3] = self.power_level_of_3x3_square(x, y)
            if self.cells[x, y, 3] > result:
                result = self.cells[x, y, 3]
                result_x = x
                result_y = y
        return result_x, result_y

    def maximum_square(self):
        result = -999
        result_x = None
        result_y = None
        result_size = None
        for size in range(1, 301):
            print("Checking size %d" % size)
            for x, y in product(range(301-size), range(301-size)):
                if self.cells[x, y, size] == 0:
                    if size % 2:
                        self.cells[x, y, size] = self.cells[x, y, ceil(size // 2)] \
                                            + self.cells[x + ceil(size // 2), y, floor(size // 2)] \
                                            + self.cells[x, y + ceil(size // 2), floor(size // 2)] \
                                            + self.cells[x + floor(size // 2), y + floor(size // 2), ceil(size // 2)] \
                                            - self.cells[x + floor(size // 2), y + floor(size // 2)]
                    else:
                        self.cells[x, y, size] = self.cells[x, y, ceil(size // 2)] \
                                            + self.cells[x + ceil(size // 2), y, floor(size // 2)] \
                                            + self.cells[x, y + ceil(size // 2), floor(size // 2)] \
                                            + self.cells[x + floor(size // 2), y + floor(size // 2), ceil(size // 2)]
                if self.cells[x, y, size] >= result:
                    result = self.cells[x, y, size]
                    result_x = x
                    result_y = y
                    result_size = size
        return result_x, result_y, result_size, result


def main():
    cells = CellSquare()

    for x, y in product(range(1, 301), range(1, 301)):
        cells.add_cell(Cell(x, y))

    max_x, max_y = cells.maximum_3x3_square()
    print("%d,%d" % (max_x, max_y))  # part 1

    max_x, max_y, max_size, pwr = cells.maximum_square()
    print("%d,%d,%d with power of %d" % (max_x, max_y, max_size, pwr))  # part 2


main()
