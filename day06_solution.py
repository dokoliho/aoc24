from mimetypes import guess_type

from solution import Solution
from collections import defaultdict
import copy

class Day06Solution(Solution):

    directions = {'^': (-1, 0), 'v': (1, 0), '>': (0, 1), '<': (0, -1)}
    turn_sequence = ['^', '>', 'v', '<']

    def __init__(self):
        super().__init__()
        self.day = 6
        self.expected_test_result_part_1 = 41
        self.expected_test_result_part_2 = 6

    def solve_part_1(self):
        puzzle = copy.deepcopy(self.puzzle)
        guard = self.find_guard(puzzle)
        count = 0
        continue_loop, guard, count = self.move_guard(guard, puzzle, count)
        while continue_loop:
            continue_loop, guard, count = self.move_guard(guard, puzzle, count)
        for line in puzzle:
            print(line)
        return count

    def find_guard(self, puzzle):
        for row in range(len(puzzle)):
            for col in range(len(puzzle[row])):
                if puzzle[row][col] in self.turn_sequence:
                    return row, col, puzzle[row][col]
        return None

    def move_guard(self, guard, puzzle, count=0, visited=None):
        row, col, direction = guard
        destination = (row + self.directions[direction][0], col + self.directions[direction][1])
        if destination[0] < 0 or destination[0] >= len(puzzle) or destination[1] < 0 or destination[1] >= len(puzzle[row]):
            count = self.mark_position(count, puzzle, row, col)
            if visited is not None:
                visited[(row, col)].add(direction)
            return False, guard, count
        if puzzle[destination[0]][destination[1]] == '#':
            new_direction = self.turn_sequence[(self.turn_sequence.index(direction) + 1) % 4]
            if visited is not None:
                visited[(row, col)].add(direction)
            return True, (row, col, new_direction), count
        count = self.mark_position(count, puzzle, row, col)
        if visited is not None:
            visited[(row, col)].add(direction)
            if direction in visited[(destination[0], destination[1])]:
                return False, (destination[0], destination[1], direction), -1
        return True, (destination[0], destination[1], direction), count

    def mark_position(self, count, puzzle, row, col):
        if puzzle[row][col] != 'X':
            count += 1
            chars = list(puzzle[row])
            chars[col] = 'X'
            puzzle[row] = ''.join(chars)
        return count

    def solve_part_2(self):
        puzzle = copy.deepcopy(self.puzzle)
        guard = self.find_guard(puzzle)
        initial_guard_pos = (guard[0], guard[1])
        continue_loop, guard, _ = self.move_guard(guard, puzzle)
        blocks = 0
        while continue_loop:
            continue_loop, new_guard, count = self.move_guard(guard, puzzle)
            row, col, direction = new_guard
            if (row, col) != (guard[0], guard[1]) and (row, col) != initial_guard_pos:
                visited = defaultdict(set)
                if self.check_block_position(row, col, guard, copy.deepcopy(puzzle), visited):
                    blocks += 1
            guard = new_guard
        return blocks

    def check_block_position(self, row, col, guard, puzzle, visited):
        chars = list(puzzle[row])
        chars[col] = '#'
        puzzle[row] = ''.join(chars)
        continue_loop, guard, count = self.move_guard(guard, puzzle, 0, visited)
        while continue_loop and count != -1:
            continue_loop, guard, count = self.move_guard(guard, puzzle, 0, visited)
        return count == -1


if __name__ == "__main__":
    Day06Solution().test()
    Day06Solution().solve()
