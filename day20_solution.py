from aoc_tools.solution import Solution

DIRECTIONS = [(1,0), (0, 1), (-1, 0), (0, -1)]

class D20S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 20
        self.expected_test_result_part_1 = 0
        self.expected_test_result_part_2 = 2
        self.walls = None
        self.start = None
        self.end = None

    def solve_part_1(self):
        self.get_walls_start_end()
        path = self.find_path()
        cheats = self.find_cheats_part_1(path)
        if self.is_test:
            for i in range(70):
                count = len([cheat for cheat in cheats if cheat[0] == i])
                if count > 0: print(f"Found {count} cheats of length {i}")
        return len([cheat for cheat in cheats if cheat[0] >=100])

    def solve_part_2(self):
        self.get_walls_start_end()
        path = self.find_path()
        cheats = self.find_cheats_part_2(path)
        treshold = 50 if self.is_test else 100
        return len([cheat for cheat in cheats if cheat[0] >=treshold])

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
        path = [self.start]
        while path[-1] != self.end:
            for direction in DIRECTIONS:
                new_pos = (path[-1][0] + direction[0], path[-1][1] + direction[1])
                if new_pos in self.walls:
                    continue
                if new_pos in path:
                    continue
                path.append(new_pos)
                break
        return path

    def find_cheats_part_1(self, path):
        cheats = set()
        for i in range(0, len(path)-2):
            cheats.update(self.find_cheats_of_length(path[i], 2, path))
        return cheats

    def find_cheats_part_2(self, path):
        cheats = set()
        for i in range(0, len(path)-20):
            print(f"Checking {i} of {len(path)-20}")
            cheats.update(self.find_cheats_of_length(path[i], 20, path))
            print(f"Found {len(cheats)} cheats")
        return cheats

    def find_cheats(self, path):
        cheats = []
        for i in range(0, len(path)-2):
            for direction in DIRECTIONS:
                new_pos = (path[i][0] + direction[0]*2, path[i][1] + direction[1]*2)
                try:
                    j = path.index(new_pos)
                    if j > i+2:
                        cheats.append((j-i-2, path[i], new_pos))
                except ValueError:
                    continue
            pass
        return cheats

    def find_cheats_of_length(self, start, count, path, pos=None, pico=None, cheats=None):
        if cheats is None:
            cheats = set()
        if pos is None:
            pos = start
            pico = path.index(start)
        if count == 0:
            return cheats
        for direction in DIRECTIONS:
            new_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if abs(start[0] - new_pos[0]) < abs(start[0] - pos[0]):
                continue
            if abs(start[1] - new_pos[1]) < abs(start[1] - pos[1]):
                continue
            if new_pos not in self.walls:
                try:
                    j = path.index(new_pos)
                    if j > pico + 1:
                        cheats.add((j-pico - 1, start, new_pos))
                except ValueError:
                    pass
            self.find_cheats_of_length(start, count-1, path, new_pos, pico+1, cheats)
        return cheats

if __name__ == "__main__":
    D20S().test()
    D20S().solve()
