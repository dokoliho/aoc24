from functools import cache

from aoc_tools.solution import Solution
import networkx as nx
from itertools import pairwise


class D21S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 21
        self.expected_test_result_part_1 = 126384
        self.expected_test_result_part_2 = 154115708116294
        self.numeric_keyboard = None
        self.directional_keyboard = None


    def solve_part_1(self):
        self.generate_keyboards()
        sum = 0
        for line in self.puzzle:
            num_part = int(line[:-1])
            radiation_sequences = self.all_shortest_paths(line)
            if self.is_test and num_part == 29:
                assert len(radiation_sequences) == 3
                assert '<A^A>^^AvvvA' in radiation_sequences
                assert '<A^A^>^AvvvA' in radiation_sequences
                assert '<A^A^^>AvvvA' in radiation_sequences
                assert self.get_best_length(line, 0) == len('<A^A^^>AvvvA')


            freezing_sequences = []
            for s in radiation_sequences:
                freezing_sequences.extend(self.all_shortest_paths(s))
            if self.is_test and num_part == 29:
                assert 'v<<A>>^A<A>AvA<^AA>A<vAAA>^A' in freezing_sequences
                assert self.get_best_length(line, 1) == len('v<<A>>^A<A>AvA<^AA>A<vAAA>^A')

            historian_sequences = []
            for s in freezing_sequences:
                historian_sequences.extend(self.all_shortest_paths(s))
            historian_len = min(map(len, historian_sequences))
            historian_sequences =  [sequence for sequence in historian_sequences if len(sequence) == historian_len]

            if self.is_test:
                assert self.get_best_length(line, 2) == historian_len


            if self.is_test:
                expected = None
                length = 0
                if num_part == 29:
                    expected = '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'
                    length = 68
                elif num_part == 980:
                    expected = '<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A'
                    length = 60
                elif num_part == 179:
                    expected = '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'
                    length = 68
                elif num_part == 456:
                    expected = '<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A'
                    length = 64
                elif num_part == 379:
                    expected = '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'
                    length = 64
                assert expected in historian_sequences
                assert length == len(expected)
                assert length == len(historian_sequences[0])

            sum += historian_len * num_part
        return sum

    def solve_part_2(self):
        self.generate_keyboards()
        sum = 0
        for line in self.puzzle:
            num_part = int(line[:-1])
            # 0 is numerical -> direction
            # 1-25 are directions
            min_length = self.get_best_length(line, 25)
            sum += min_length * num_part
        return sum

    def generate_keyboards(self):
        numeric_edges = [
            ('7', '8', {'symbol': '>'}),
            ('8', '9', {'symbol': '>'}),
            ('4', '5', {'symbol': '>'}),
            ('5', '6', {'symbol': '>'}),
            ('1', '2', {'symbol': '>'}),
            ('2', '3', {'symbol': '>'}),
            ('0', 'A', {'symbol': '>'}),

            ('8', '7', {'symbol': '<'}),
            ('9', '8', {'symbol': '<'}),
            ('5', '4', {'symbol': '<'}),
            ('6', '5', {'symbol': '<'}),
            ('2', '1', {'symbol': '<'}),
            ('3', '2', {'symbol': '<'}),
            ('A', '0', {'symbol': '<'}),

            ('7', '4', {'symbol': 'v'}),
            ('8', '5', {'symbol': 'v'}),
            ('9', '6', {'symbol': 'v'}),
            ('4', '1', {'symbol': 'v'}),
            ('5', '2', {'symbol': 'v'}),
            ('6', '3', {'symbol': 'v'}),
            ('2', '0', {'symbol': 'v'}),
            ('3', 'A', {'symbol': 'v'}),

            ('4', '7', {'symbol': '^'}),
            ('5', '8', {'symbol': '^'}),
            ('6', '9', {'symbol': '^'}),
            ('1', '4', {'symbol': '^'}),
            ('2', '5', {'symbol': '^'}),
            ('3', '6', {'symbol': '^'}),
            ('0', '2', {'symbol': '^'}),
            ('A', '3', {'symbol': '^'}),
        ]
        self.numeric_keyboard = nx.DiGraph()
        self.numeric_keyboard.add_edges_from(numeric_edges)

        directional_edges = [
            ('^', 'A', {'symbol': '>'}),
            ('<', 'v', {'symbol': '>'}),
            ('v', '>', {'symbol': '>'}),

            ('A', '^', {'symbol': '<'}),
            ('>', 'v', {'symbol': '<'}),
            ('v', '<', {'symbol': '<'}),

            ('^', 'v', {'symbol': 'v'}),
            ('A', '>', {'symbol': 'v'}),

            ('v', '^', {'symbol': '^'}),
            ('>', 'A', {'symbol': '^'}),
            ]
        self.directional_keyboard = nx.DiGraph()
        self.directional_keyboard.add_edges_from(directional_edges)

    def all_shortest_paths(self, sequence):
        prefixes = [""]
        keyboard = self.numeric_keyboard if sequence[0].isdigit() else self.directional_keyboard
        for start, end in pairwise('A'+sequence):
            prefixes = self.extend_prefixes(prefixes, keyboard, start, end)
        return prefixes

    def extend_prefixes(self, prefixes, keyboard, start, end):
        suffixes = self.get_all_paths_on_keyboard(keyboard, start, end)
        new_prefixes = []
        new_prefixes.extend(prefix + suffix + 'A' for prefix in prefixes for suffix in suffixes)
        return new_prefixes


    @cache
    def get_all_paths_on_keyboard(self, keyboard, start, end):
        paths = []
        for path in nx.all_shortest_paths(keyboard, start, end):
            edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            symbols = [keyboard.get_edge_data(*edge)['symbol'] for edge in edges]
            paths.append("".join(symbols))
        return paths

    @cache
    def get_best_length(self, sequence, level):
        result = 0
        keyboard = self.numeric_keyboard if sequence[0].isdigit() else self.directional_keyboard
        for start, end in pairwise('A' + sequence):
            paths = self.get_all_paths_on_keyboard(keyboard, start, end)
            if level == 0:
                length = min(len(path) for path in paths) + 1 if paths else 1 # +1 for the 'A' at the end
                result += length
                continue

            if not paths:
                result += 1 # +1 for the 'A' at the end
                continue

            lengths = set()
            for path in paths:
                lengths.add(self.get_best_length(path + 'A', level - 1))
            result += min(lengths)

        return result

if __name__ == "__main__":
    D21S().test()
    D21S().solve()
