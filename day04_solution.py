from solution import Solution
import re

class Day04Solution(Solution):

    def __init__(self):
        super().__init__()
        self.day = 4
        self.expected_test_result_part_1 = 18
        self.expected_test_result_part_2 = 9

    def solve_part_1(self):
        count = 0
        puzzle = self.puzzle
        count += self.count_word_in_puzzle(puzzle, "XMAS")
        count += self.count_word_in_puzzle(puzzle, "XMAS"[::-1])
        puzzle = self.transpose(puzzle)
        count += self.count_word_in_puzzle(puzzle, "XMAS")
        count += self.count_word_in_puzzle(puzzle, "XMAS"[::-1])
        puzzle = self.diagonals_starting_top_left(self.puzzle)
        count += self.count_word_in_puzzle(puzzle, "XMAS")
        count += self.count_word_in_puzzle(puzzle, "XMAS"[::-1])
        puzzle = self.diagonals_starting_top_right(self.puzzle)
        count += self.count_word_in_puzzle(puzzle, "XMAS")
        count += self.count_word_in_puzzle(puzzle, "XMAS"[::-1])
        return count

    def count_word_in_line(self, word, line):
        return len(re.findall(word, line))

    def count_word_in_puzzle(self, puzzle, word):
        return sum([self.count_word_in_line(word, line) for line in puzzle])

    def transpose(self, puzzle):
        t = list(map(list, zip(*puzzle)))
        return [''.join(row) for row in t]

    def diagonals_starting_top_left(self, puzzle):
        n = len(puzzle)
        diamond = []
        for d in range(2 * n - 1):
            diagonal = []
            if d < n:
                row, col = 0, d
            else:
                row, col = d - n + 1, n - 1
            while row < n and col >= 0:
                diagonal.append(puzzle[row][col])
                row += 1
                col -= 1
            diamond.append("".join(diagonal))
        return diamond

    def diagonals_starting_top_right(self, puzzle):
        n = len(puzzle)
        diamond = []
        for d in range(2 * n - 1):
            diagonal = []
            if d < n:
                row, col = d, n-1
            else:
                row, col = n - 1, 2 * n - 2 - d
            while row >= 0 and col >= 0:
                diagonal.append(puzzle[row][col])
                row -= 1
                col -= 1
            diamond.append("".join(diagonal))
        return diamond

    def solve_part_2(self):
        count = 0
        for x in range(1, len(self.puzzle)-1):
            for y in range(1, len(self.puzzle)-1):
                if self.is_mas(x, y):
                    count += 1
        return count

    def is_mas(self, x, y):
        if self.puzzle[x][y] != "A":
            return False
        diag1 = self.puzzle[x-1][y-1] + self.puzzle[x][y] + self.puzzle[x+1][y+1]
        diag2 = self.puzzle[x-1][y+1] + self.puzzle[x][y] + self.puzzle[x+1][y-1]
        if diag1 != "MAS" and diag1 != "MAS"[::-1]:
            return False
        if diag2 != "MAS" and diag2 != "MAS"[::-1]:
            return False
        return True


if __name__ == "__main__":
    Day04Solution().test()
    Day04Solution().solve()
