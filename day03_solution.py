from solution import Solution
import re

class Day03Solution(Solution):

    def __init__(self):
        super().__init__()
        self.day = 3
        self.expected_test_result_part_1 = 161
        self.expected_test_result_part_2 = 48

    def solve_part_1(self):
        code = ''.join(self.puzzle)
        return self.sum_the_muls(code)

    def sum_the_muls(self, code):
        muls = re.findall(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)', code)
        results = [int(x) * int(y) for x, y in muls]
        return sum(results)

    def solve_part_2(self):
        code = ''.join(self.puzzle)
        code = self.extract_valid_code(code)
        return self.sum_the_muls(''.join(code))

    def extract_valid_code(self, code):
        start = "do()"
        stop = "don't()"
        code = start + code + stop
        valid_chunks = re.findall(rf'{re.escape(start)}(.*?){re.escape(stop)}', code)
        return ''.join(valid_chunks)


if __name__ == "__main__":
    Day03Solution().test()
    Day03Solution().solve()
