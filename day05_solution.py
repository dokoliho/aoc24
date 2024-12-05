from solution import Solution
from functools import cmp_to_key

class Day03Solution(Solution):

    def __init__(self):
        super().__init__()
        self.day = 5
        self.expected_test_result_part_1 = 143
        self.expected_test_result_part_2 = 123
        self.order = {}
        self.sequences = []

    def solve_part_1(self):
        self.init_data()
        sum = 0
        for sequence in self.sequences:
            sorted = self.sorted_sequence(sequence)
            if sequence == sorted:
                sum += sequence[len(sequence) // 2]
        return sum

    def init_data(self):
        is_order_line = True
        self.order.clear()
        self.sequences.clear()
        for line in self.puzzle:
            if line == "":
                is_order_line = False
                continue
            if is_order_line:
                first, second = tuple(map(int, line.split("|")))
                if first not in self.order:
                    self.order[first] = []
                self.order[first].append(second)
            else:
                self.sequences.append(list(map(int, line.split(","))))

    def solve_part_2(self):
        self.init_data()
        sum = 0
        for sequence in self.sequences:
            sorted = self.sorted_sequence(sequence)
            if sequence != sorted:
                sum += sorted[len(sorted) // 2]
        return sum

    def sorted_sequence(self, sequence):
        def compare(a, b):
            if a in self.order and b in self.order[a]:
                return -1
            if b in self.order and a in self.order[b]:
                return 1
            return 0
        return sorted(sequence, key=cmp_to_key(compare))



if __name__ == "__main__":
    Day03Solution().test()
    Day03Solution().solve()
