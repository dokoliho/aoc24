from solution import Solution


class Day01Solution(Solution):

    def __init__(self):
        super().__init__()
        self.day = 1
        self.expected_test_result_part_1 = 11
        self.expected_test_result_part_2 = 31

    def solve_part_1(self):
        return sum(self.calculate_distances())

    def solve_part_2(self):
        return sum(self.calculate_similarity_scores())

    def calculate_distances(self):
        left, right = self.split_puzzle()
        left = sorted(map(int, left))
        right = sorted(map(int, right))
        return [abs(l - r) for l, r in zip(left, right)]

    def calculate_similarity_scores(self):
        left, right = self.split_puzzle()
        left = map(int, left)
        right = list(map(int, right))
        right_counts = {num: right.count(num) for num in set(right)}
        return [right_counts.get(num, 0) * num for num in left]

    def split_puzzle(self):
        return zip(*[line.split() for line in self.puzzle])


if __name__ == "__main__":
    Day01Solution().test()
    Day01Solution().solve()
