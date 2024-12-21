from itertools import pairwise

from aoc_tools.solution import Solution
import networkx as nx

class D21S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 21
        self.expected_test_result_part_1 = 126384
        self.expected_test_result_part_2 = 2
        self.numeric_keyboard = None
        self.directional_keyboard = None


    def solve_part_1(self):
        self.generate_keyboards()
        sum = 0
        for line in self.puzzle:
            num_part = int(line[:-1])
            radiation_sequences = self.all_shortest_paths(line, self.numeric_keyboard)
            if self.is_test and num_part == 29:
                assert len(radiation_sequences) == 3
                assert '<A^A>^^AvvvA' in radiation_sequences
                assert '<A^A^>^AvvvA' in radiation_sequences
                assert '<A^A^^>AvvvA' in radiation_sequences

            freezing_sequences = []
            for s in radiation_sequences:
                freezing_sequences.extend(self.all_shortest_paths(s, self.directional_keyboard))
            if self.is_test and num_part == 29:
                assert 'v<<A>>^A<A>AvA<^AA>A<vAAA>^A' in freezing_sequences

            historian_sequences = []
            for s in freezing_sequences:
                historian_sequences.extend(self.all_shortest_paths(s, self.directional_keyboard))
            historian_len = min(map(len, historian_sequences))
            historian_sequences =  [sequence for sequence in historian_sequences if len(sequence) == historian_len]

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


            print(f"Line: {line}, len: {historian_len}, num: {num_part}")

            sum += historian_len * num_part
        return sum

    def solve_part_2(self):
        return 2

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

    def all_shortest_paths(self, string, keyboard):
        prefixes = [""]
        for start, end in pairwise('A'+string):
            new_prefixes = []
            for path in nx.all_shortest_paths(keyboard, start, end):
                edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
                symbols = [keyboard.get_edge_data(*edge)['symbol'] for edge in edges]
                for prefix in prefixes:
                    new_prefixes.append(prefix + "".join(symbols)+'A')
            prefixes = new_prefixes
        return prefixes

if __name__ == "__main__":
    D21S().test()
    D21S().solve()
