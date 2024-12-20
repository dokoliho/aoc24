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

    def solve_part_1(self):
        self.get_walls_start_end()
        path = self.find_path()
        cheats = set()
        for i in range(0, len(path)-2):
            cheats.update(self.find_cheats_in_path(i, 2, path))
        if self.is_test:
            for i in range(70):
                count = len([cheat for cheat in cheats if cheat[0] == i])
                if count > 0: print(f"There are {count} cheats that save {i} picoseconds.")
        return len([cheat for cheat in cheats if cheat[0] >=100])

    def solve_part_2(self):
        self.get_walls_start_end()
        path = self.find_path()
        cheats = set()
        for i in range(0, len(path)-2):
            cheats.update(self.find_cheats_in_path(i, 20, path))
        if self.is_test:
            for i in range(50, 100):
                count = len([cheat for cheat in cheats if cheat[0] == i])
                if count > 0:  print(f"There are {count} cheats that save {i} picoseconds.")
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

    def find_cheats_in_path(self, start_index, max_ham_distance, path):
        cheats = set()
        for j in range(start_index + 1, len(path)):
            path_distance = j-start_index
            ham_distance = self.hamming_distance(path[start_index], path[j])
            if ham_distance> max_ham_distance: continue
            if ham_distance < path_distance:
                saving = path_distance - ham_distance
                cheats.add((saving, path[start_index], path[j]))
        return cheats

    def hamming_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

if __name__ == "__main__":
    D20S().test()
    D20S().solve()
