from aoc_tools.solution import Solution
from heapq import heappop, heappush

DIRECTIONS = [(1,0), (0, 1), (-1, 0), (0, -1)]

class D18S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 18
        self.expected_test_result_part_1 = 22
        self.expected_test_result_part_2 = "6,1"
        self.width = 71
        self.height = 71
        self.steps = 1024
        self.memory = {}

    def solve_part_1(self):
        if self.is_test:
            self.width = 7
            self.height = 7
            self.steps = 12
        self.get_memory()
        length, _ = self.get_distance()
        return length

    def solve_part_2(self):
        if self.is_test:
            self.width = 7
            self.height = 7
            self.steps = 12
        self.get_memory()
        lower_bound = 0
        upper_bound = len(self.puzzle)
        while upper_bound - lower_bound > 1:
            self.steps = (upper_bound + lower_bound) // 2
            length, _ = self.get_distance()
            if length is not None:
                lower_bound = self.steps
            else:
                upper_bound = self.steps
        return self.puzzle[lower_bound]

    def get_memory(self):
        for i in range(len(self.puzzle)):
            pos = tuple([int(num) for num  in self.puzzle[i].split(",")])
            self.memory[pos] = i

    def get_distance(self):
        distances = {}
        queue = []
        predecessors = {}
        frontier = set([(0, 0)])
        heappush(queue, (0, (0, 0), None))
        while queue:
            if len(distances) % 100 == 0:
                pass
            step, pos, pred = heappop(queue)
            frontier.remove(pos)
            if pos in distances and distances[pos] < step:
                continue
            distances[pos] = step
            predecessors[pos] = pred
            if pos == (self.width - 1, self.height - 1):
                return step, self.get_path(pos, predecessors)
            for direction in DIRECTIONS:
                next_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if next_pos in frontier: continue
                if next_pos in distances: continue
                if next_pos[0] >= 0 and next_pos[0] < self.width and next_pos[1] >= 0 and next_pos[1] < self.height:
                    if next_pos not in self.memory or self.memory[next_pos] >= self.steps:
                        heappush(queue, (step + 1, next_pos, pos))
                        frontier.add(next_pos)
        return None, None

    def get_path(self, pos, predecessors):
        path = []
        while pos:
            path.append(pos)
            pos = predecessors[pos]
        path.reverse()
        return path

if __name__ == "__main__":
    D18S().test()
    D18S().solve()
