from solution import Solution


class Day06Solution(Solution):

    DIRECTIONS = {'^': (-1, 0), 'v': (1, 0), '>': (0, 1), '<': (0, -1)}
    TURN_SEQUENCE = ['^', '>', 'v', '<']

    def __init__(self):
        super().__init__()
        self.day = 6
        self.expected_test_result_part_1 = 41
        self.expected_test_result_part_2 = 6

    def solve_part_1(self):
        puzzle = self.puzzle
        guard = self.find_guard(puzzle)
        blocks = self.find_blocks(puzzle)
        visited, _ = self.move_guard(guard, puzzle, blocks)
        positions = set([(row, col) for row, col, _ in visited])
        return len(positions)

    def find_guard(self, puzzle):
        for row in range(len(puzzle)):
            for col in range(len(puzzle[row])):
                if puzzle[row][col] in self.TURN_SEQUENCE:
                    return row, col, puzzle[row][col]
        return None

    def find_blocks(self, puzzle):
        blocks = []
        for row in range(len(puzzle)):
            for col in range(len(puzzle[row])):
                if puzzle[row][col] == '#':
                    blocks.append((row, col))
        return blocks

    def move_guard(self, guard, puzzle, blocks):
        visited = set()
        while True:
            if guard in visited:
                return visited, True
            visited.add(guard)
            row, col, direction = guard
            new_row = row + self.DIRECTIONS[direction][0]
            new_col = col + self.DIRECTIONS[direction][1]
            if new_row < 0 or new_row >= len(puzzle) or new_col < 0 or new_col >= len(puzzle[new_row]):
                break
            if (new_row, new_col) in blocks:
                new_direction = self.TURN_SEQUENCE[(self.TURN_SEQUENCE.index(direction) + 1) % 4]
                guard = (row, col, new_direction)
                continue
            guard = (new_row, new_col, direction)
        return visited, False


    def solve_part_2(self):
        puzzle = self.puzzle
        guard = self.find_guard(puzzle)
        blocks = set(self.find_blocks(puzzle))
        visited, _ = self.move_guard(guard, puzzle, blocks)
        locations = self.extract_locations(visited)
        cycles_blocks = set()
        for block in locations:
            if block == guard[:2]:
                continue
            blocks.add(block)
            _, cycle = self.move_guard(guard, puzzle, blocks)
            if cycle:
                cycles_blocks.add(block)
            blocks.remove(block)
        return len(cycles_blocks)

    @staticmethod
    def extract_locations(visited):
        return {(row, col) for row, col, _ in visited}


if __name__ == "__main__":
    Day06Solution().test()
    Day06Solution().solve()
