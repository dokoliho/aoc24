from aoc_tools.solution import Solution
from functools import cache

class D11S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 11
        self.expected_test_result_part_1 = 55312
        self.expected_test_result_part_2 = 65601038650482

    def solve_part_1(self):
        nums = list(map(int, self.puzzle[0].split()))
        result = sum([self.blink_number(num, 25) for num in nums])
        return result

    def solve_part_2(self):
        nums = list(map(int, self.puzzle[0].split()))
        result = sum([self.blink_number(num, 75) for num in nums])
        print(self.blink_number.cache_info())
        return result

    @cache
    def blink_number(self, num, count):
        if count == 0:
            return 1
        else:
            if num == 0:
                return self.blink_number (1, count - 1)
            if len(str(num)) % 2 == 0:
                left = int(str(num)[:len(str(num))//2])
                right = int(str(num)[len(str(num))//2:])
                return self.blink_number(left, count - 1) + self.blink_number(right, count - 1)
            return self.blink_number(num * 2024, count - 1)


if __name__ == "__main__":
    D11S().test()
    D11S().solve()
