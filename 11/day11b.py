# This idea is not mine. I found it on Reddit when trying to find inspiration
# why my code does not work.
# It uses https://en.wikipedia.org/wiki/Summed-area_table

# Solves only part 2


from itertools import product
from collections import defaultdict


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


class SummedAreaTable:
    def __init__(self, cell_square: CellSquare):
        self.cells = defaultdict(int)
        for x, y in product(range(1, 301), range(1, 301)):
            self.cells[x, y] = cell_square.cells[x, y] + self.cells[x, y - 1] + self.cells[x - 1, y] \
                               - self.cells[x - 1, y - 1]

    def power_of_square(self, x_1, y_1, x_2, y_2):
        return self.cells[x_2, y_2] + self.cells[x_1 - 1, y_1 - 1] - self.cells[x_2, y_1 - 1] - self.cells[x_1 - 1, y_2]

    def maximal_square_from_coordinates(self, x, y):
        maximum = -9999
        max_size = None
        for size in range(1, min(301-x, 301-y)):
            power = self.power_of_square(x, y, x + size - 1, y + size - 1)
            if maximum < power:
                maximum = power
                max_size = size
        return maximum, max_size

    def maximal_square(self):
        maximum = 0
        max_x = None
        max_y = None
        max_size = None
        for x, y in product(range(1, 301), range(1, 301)):
            from_these, size = self.maximal_square_from_coordinates(x, y)
            if maximum < from_these:
                maximum = from_these
                max_x = x
                max_y = y
                max_size = size
        return max_x, max_y, max_size, maximum


def main():
    cells = CellSquare()

    for x, y in product(range(1, 301), range(1, 301)):
        cells.add_cell(Cell(x, y))

    table = SummedAreaTable(cells)
    max_x, max_y, max_size, pwr = table.maximal_square()
    print("%d,%d,%d with power of %d" % (max_x, max_y, max_size, pwr))  # part 2


main()
