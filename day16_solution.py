from aoc_tools.solution import Solution
from heapq import heappop, heappush

DIRECTIONS = [(1,0), (0, 1), (-1, 0), (0, -1)]

class D16S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 16
        self.expected_test_result_part_1 = 7036
        self.expected_test_result_part_2 = 45
        self.walls = None
        self.start = None
        self.end = None

    def solve_part_1(self):
        self.get_walls_start_end()
        result, _ = self.find_shortest_path()
        return result

    def solve_part_2(self):
        self.get_walls_start_end()
        _, visited = self.find_shortest_path()
        result = len(self.get_tiles(visited))
        return result

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

    def find_shortest_path(self):
        visited = {}
        direction = 0
        queue = []
        best = None
        heappush(queue, (0, (self.start, direction), None))
        while queue:
            dist, node, pred = heappop(queue)
            if node in visited:
                known_pred =  next(iter(visited[node]))
                if known_pred[0] < dist:
                    continue
            else:
                visited[node] = set()
            visited[node].add((dist, pred))
            if best and dist > best:
                break
            pos, direction = node
            if pos == self.end:
                best = dist
                continue
            step_ahead_pos = (pos[0] + DIRECTIONS[direction][0], pos[1] + DIRECTIONS[direction][1])
            if step_ahead_pos not in self.walls:
                heappush(queue, (dist + 1, (step_ahead_pos, direction), node))
            heappush(queue, (dist + 1000, (pos, (direction + 1) % 4), node))
            heappush(queue, (dist + 1000, (pos, (direction - 1) % 4), node))
        return best, visited

    def get_tiles(self, visited):
        tiles = set()
        for direction in range(4):
            node = (self.end, direction)
            tiles = self.get_tiles_from_node(node, visited, tiles)
        return tiles

    def get_tiles_from_node(self, node, visited, tiles):
        if node and node in visited:
            pos, _ = node
            tiles.add(pos)
            for _, pred in visited[node]:
                tiles = self.get_tiles_from_node(pred, visited, tiles)
        return tiles

if __name__ == "__main__":
    D16S().test()
    D16S().solve()
