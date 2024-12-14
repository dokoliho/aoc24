from aoc_tools.solution import Solution

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

class D10S(Solution):

    class Position:
        def __init__(self, height):
            self._height = height
            self.connections = None

        @property
        def height(self):
            return self._height

    def __init__(self):
        super().__init__()
        self.day = 10
        self.expected_test_result_part_1 = 36
        self.expected_test_result_part_2 = 81

    def solve_part_1(self):
        trail_map = self.read_map()
        level0 = list(filter(lambda x: x.height == 0, trail_map.values()))
        return sum([self.trailhead_level(trail_map, head, set()) for head in level0])

    def solve_part_2(self):
        trail_map = self.read_map()
        level0 = list(filter(lambda x: x.height == 0, trail_map.values()))
        return sum([self.distinct_trailhead_level(trail_map, head) for head in level0])

    def read_map(self):
        trail_map = {}
        for row, line in enumerate(self.puzzle):
            for col, char in enumerate(line):
                height = int(char)
                pos = self.Position(height)
                trail_map[(col, row)] = pos
        for key in trail_map:
            trail_map[key].connections = self.reachable_neighbours(trail_map, key)
        return trail_map

    def reachable_neighbours(self, trail_map, key):
        reachable = set()
        for direction in DIRECTIONS:
            new_key = (key[0] + direction[0], key[1] + direction[1])
            if new_key in trail_map and trail_map[new_key].height == trail_map[key].height + 1:
                reachable.add(trail_map[new_key])
        return reachable

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
