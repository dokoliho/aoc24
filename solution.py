from time import perf_counter as pfc


class Solution:

    def __init__(self):
        self.puzzle = None
        self.day = 0
        self.expected_test_result_part_1 = 1
        self.expected_test_result_part_2 = 2

    def read_puzzle(self, filename):
        with open(filename) as file:
            self.puzzle = [line.strip() for line in file]

    def solve_part_1(self):
        return 1

    def solve_part_2(self):
        return 2

    def solve(self):
        filename = f"day{self.day:02d}_input.txt"
        self.read_puzzle(filename)
        start = pfc()
        result1 = self.solve_part_1()
        print(f"Teil 1: {result1} ({pfc() - start:.4f}s)")
        start = pfc()
        result2 = self.solve_part_2()
        print(f"Teil 2: {result2} ({pfc() - start:.4f}s)")

    def test(self):
        filename = f"day{self.day:02d}_test_input.txt"
        self.read_puzzle(filename)
        start = pfc()
        result1 = self.solve_part_1()
        print(f"Test Teil 1: {result1} ({pfc() - start:.4f}s)")
        assert result1 == self.expected_test_result_part_1, \
            f"Expected {self.expected_test_result_part_1} but got {result1}"
        start = pfc()
        result2 = self.solve_part_2()
        assert result2 == self.expected_test_result_part_2, \
            f"Expected {self.expected_test_result_part_2} but got {result2}"
        print(f"Test Teil 2: {result2} ({pfc() - start:.4f}s)")
