from aoc_tools.solution import Solution
from collections import defaultdict
from itertools import combinations
import math

class Day08Solution(Solution):

    def __init__(self):
        super().__init__()
        self.day = 8
        self.expected_test_result_part_1 = 14
        self.expected_test_result_part_2 = 34
        self.antennas = None
        self.width = None
        self.height = None

    def solve_part_1(self):
        self.find_antennas()
        locations = set()
        for antenna in self.antennas:
            for loc1, loc2 in combinations(self.antennas[antenna], 2):
                locations.update(self.get_antinodes1(loc1, loc2))
        return len(locations)

    def solve_part_2(self):
        self.find_antennas()
        locations = set()
        for antenna in self.antennas:
            for loc1, loc2 in combinations(self.antennas[antenna], 2):
                locations.update(self.get_antinodes2(loc1, loc2))
        return len(locations)

    def find_antennas(self):
        self.antennas = defaultdict(list)
        for row, line in enumerate(self.puzzle):
            for col, antenna in enumerate(line):
                if antenna != '.':
                    self.antennas[antenna].append((col, row))
        self.width = len(self.puzzle[0])
        self.height = len(self.puzzle)

    def get_antinodes1(self, loc1, loc2):
        diff = (loc2[0] - loc1[0], loc2[1] - loc1[1])
        result = set()
        a1 = (loc1[0] - diff[0], loc1[1] - diff[1])
        if self.is_in_bounds(a1):
            result.add(a1)
        a2 = (loc2[0] + diff[0], loc2[1] + diff[1])
        if self.is_in_bounds(a2):
            result.add(a2)
        return result

    def get_antinodes2(self, loc1, loc2):
        xd = loc2[0] - loc1[0]
        yd = loc2[1] - loc1[1]
        gcd = math.gcd(xd, yd)
        diff = (xd // gcd, yd // gcd)
        result = set()
        current = loc1
        while self.is_in_bounds(current):
            result.add(current)
            current = (current[0] + diff[0], current[1] + diff[1])
        current = loc1
        while self.is_in_bounds(current):
            result.add(current)
            current = (current[0] - diff[0], current[1] - diff[1])
        return result

    def is_in_bounds(self, loc):
        return 0 <= loc[0] < self.width and 0 <= loc[1] < self.height

    def print_locations(self, locations):
        for row in range(self.height):
            for col in range(self.width):
                if (col, row) in locations:
                    print('#', end='')
                else:
                    print(self.puzzle[row][col], end='')
            print()


if __name__ == "__main__":
    Day08Solution().test()
    Day08Solution().solve()
