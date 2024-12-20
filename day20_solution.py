from collections import defaultdict
from operator import add, sub

from aoc_tools.solution import Solution

DIRECTIONS = [(1,0), (0, 1), (-1, 0), (0, -1)]

class D20S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 20
        self.expected_test_result_part_1 = 0
        self.expected_test_result_part_2 = 285
        self.walls = None
        self.start = None
        self.end = None
        self.path = None
        self.pathmap = None

    def solve_part_1(self):
        self.get_walls_start_end()
        self.find_path()
        self.get_pathmap()
        cheats = set()
        for i in range(0, len(self.path)-2):
            cheats.update(self.find_cheats(i, 2))
        if self.is_test:
            for i in range(70):
                count = len([cheat for cheat in cheats if cheat[0] == i])
                if count > 0: print(f"There are {count} cheats that save {i} picoseconds.")
        return len([cheat for cheat in cheats if cheat[0] >=100])

    def solve_part_2(self):
        self.get_walls_start_end()
        self.find_path()
        self.get_pathmap()
        cheats = set()
        for i in range(0, len(self.path)-2):
            cheats.update(self.find_cheats(i, 20))
        if self.is_test:
            for i in range(50, 100):
                count = len([cheat for cheat in cheats if cheat[0] == i])
                if count > 0:  print(f"There are {count} cheats that save {i} picoseconds.")
        threshold = 50 if self.is_test else 100
        return len([cheat for cheat in cheats if cheat[0] >=threshold])

    def get_walls_start_end(self):
        self.walls = set()
        for row in range(len(self.puzzle)):
            for col in range(len(self.puzzle[row])):
                if self.puzzle[row][col] == '#':
                    self.walls.add((col, row))
                elif self.puzzle[row][col] == 'S':
                    self.start = (col, row)
                elif self.puzzle[row][col] == 'E':
                    self.end = (col, row)

    def find_path(self):
        self.path = [self.start]
        while self.path[-1] != self.end:
            for direction in DIRECTIONS:
                new_pos = (self.path[-1][0] + direction[0], self.path[-1][1] + direction[1])
                if new_pos in self.walls:
                    continue
                if new_pos in self.path:
                    continue
                self.path.append(new_pos)
                break

    def get_pathmap(self):
        self.pathmap = defaultdict(dict)
        for i in range(len(self.path)):
            col_dic = self.pathmap[self.path[i][0]]
            col_dic[self.path[i][1]] = i


    def find_cheats(self, start_index, max_man_distance):
        cheats = set()
        path_positions = self.reachable_positions(self.path[start_index], max_man_distance)
        for j in filter(lambda x: x > start_index, path_positions):
            path_distance = j-start_index
            man_distance = self.manhattan_distance(self.path[start_index], self.path[j])
            if man_distance> max_man_distance: continue
            if man_distance < path_distance:
                saving = path_distance - man_distance
                cheats.add((saving, self.path[start_index], self.path[j]))
        return cheats

    def reachable_positions(self, start, max_distance):
        positions = set()
        for col in range(0, max_distance + 1):
            if any([op(start[0], col) in self.pathmap for op in [add, sub]]):
                for row in range(0, max_distance + 1 - col):
                    if col == 0 and row == 0: continue
                    for op in [add, sub]:
                        col_dic = self.pathmap[op(start[0], col)]
                        for op1 in [add, sub]:
                            if op1(start[1], row) in col_dic:
                                positions.add(col_dic[op1(start[1], row)])
        return positions

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

if __name__ == "__main__":
    D20S().test()
    D20S().solve()
