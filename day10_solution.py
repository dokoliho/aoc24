from solution import Solution
from collections import defaultdict

class D10S(Solution):

    class Position:
        def __init__(self, x, y, height):
            self._x = x
            self._y = y
            self._height = height
            self.connections = set()

        @property
        def x(self):
            return self._x

        @property
        def y(self):
            return self._y

        @property
        def height(self):
            return self._height

    def __init__(self):
        super().__init__()
        self.day = 10
        self.expected_test_result_part_1 = 36
        self.expected_test_result_part_2 = 81

    def solve_part_1(self):
        trail_map, level0 = self.read_map()
        return sum([self.trailhead_level(trail_map, head, set()) for head in level0])

    def solve_part_2(self):
        trail_map, level0 = self.read_map()
        return sum([self.distinct_trailhead_level(trail_map, head) for head in level0])

    def read_map(self):
        trail_map = {}
        level0 = []
        for row, line in enumerate(self.puzzle):
            for col, char in enumerate(line):
                key = (col, row)
                pos = D10S.Position(col, row, int(char))
                trail_map[key] = pos
                if pos.height == 0:
                    level0.append(pos)
        for key in trail_map:
            left = (key[0] - 1, key[1])
            right = (key[0] + 1, key[1])
            up = (key[0], key[1] - 1)
            down = (key[0], key[1] + 1)
            for new_key in [left, right, up, down]:
                if new_key in trail_map and trail_map[new_key].height == trail_map[key].height+1:
                    trail_map[key].connections.add(trail_map[new_key])
        return trail_map, level0

    def trailhead_level(self, trail_map, start, reached):
        if start.height == 9:
            if start not in reached:
                reached.add(start)
        else:
            for dest in start.connections:
                self.trailhead_level(trail_map, dest, reached)
        return len(reached)

    def distinct_trailhead_level(self, trail_map, start):
        if start.height == 9:
            return 1
        else:
            return sum([self.distinct_trailhead_level(trail_map, dest) for dest in start.connections])


if __name__ == "__main__":
    D10S().test()
    D10S().solve()
