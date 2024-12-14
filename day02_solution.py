from aoc_tools.solution import Solution
import itertools

class Day02Solution(Solution):

    def __init__(self):
        super().__init__()
        self.day = 2
        self.expected_test_result_part_1 = 2
        self.expected_test_result_part_2 = 4

    def solve_part_1(self):
        return sum([1 for report in self.puzzle if self.is_valid_report(list(map(int, report.split())))])

    def is_valid_report(self, report):
        is_increasing = lambda x: x[0] < x[1] < x[0] + 4
        is_decreasing = lambda x: x[0] > x[1] > x[0] - 4
        all_increasing = all(map(is_increasing, itertools.pairwise(report)))
        all_decreasing = all(map(is_decreasing, itertools.pairwise(report)))
        return all_decreasing or all_increasing

    def solve_part_2(self):
        return sum([1 for report in self.puzzle if self.is_valid_report2(list(map(int, report.split())))])

    def is_valid_report2(self, report):
        one_out_reports =  [report[:i] + report[i + 1:] for i in range(len(report))]
        return self.is_valid_report(report) or any([self.is_valid_report(report) for report in one_out_reports])


if __name__ == "__main__":
    Day02Solution().test()
    Day02Solution().solve()
