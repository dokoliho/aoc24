from solution import Solution
from collections import defaultdict
from itertools import combinations
import math

class Day09Solution(Solution):

    def __init__(self):
        super().__init__()
        self.day = 9
        self.expected_test_result_part_1 = 1928
        self.expected_test_result_part_2 = 2858

    def solve_part_1(self):
        files, gaps = self.split_input()
        return self.checksum(self.generate_block_sequence, files, gaps)

    def solve_part_2(self):
        files, gaps = self.split_input()
        return self.checksum(self.generate_block_sequence2, files, gaps)

    def checksum(self, generator, files, gaps):
        return sum([index * id for index, id in enumerate(generator(files, gaps))])


    def split_input(self):
        file_sizes = [int(x) for x in list(self.puzzle[0][0::2])]
        free_blocks = [int(x) for x in list(self.puzzle[0][1::2])]
        return file_sizes, free_blocks

    def generate_block_sequence(self, file_sizes, free_blocks):
        current_file = 0
        moving_file = len(file_sizes) - 1
        gap = 0
        while True:
            if file_sizes[current_file] > 0:
                file_sizes[current_file] -= 1
                yield current_file
            elif gap < len(free_blocks) and free_blocks[gap] > 0:
                while file_sizes[moving_file] == 0 and moving_file > current_file:
                    moving_file -= 1
                if moving_file <= current_file: return
                file_sizes[moving_file] -= 1
                free_blocks[gap] -= 1
                yield moving_file
            else:
                current_file += 1
                if current_file >= len(file_sizes): return
                gap += 1


    def file_sequence(self, file_sizes, free_blocks):

        file_pos = []
        gap_pos = []

        pos = 0
        free_blocks.append(0)
        for x in range(len(file_sizes)):
            file_pos.append(pos)
            pos += file_sizes[x] + free_blocks[x]
        free_blocks.pop()

        pos = file_sizes[0]
        for x in range(len(free_blocks)):
            gap_pos.append(pos)
            pos += free_blocks[x] + file_sizes[x+1]

        for moving_file in range(len(file_sizes)-1, -1, -1):
            for gap in range(len(free_blocks)):
                if gap >= moving_file: break
                if file_sizes[moving_file] <= free_blocks[gap]:
                    file_pos[moving_file] = gap_pos[gap]
                    gap_pos[gap] += file_sizes[moving_file]
                    if moving_file < len(free_blocks):
                        free_blocks[moving_file] += file_sizes[moving_file]
                    free_blocks[gap] -= file_sizes[moving_file]
                    break

        return sorted(enumerate(file_pos), key=lambda x: x[1])


    def generate_block_sequence2(self, file_sizes, free_blocks):
        file_sequence = self.file_sequence(file_sizes, free_blocks)
        curr_pos = 0
        for file, pos in file_sequence:
            while curr_pos < pos:
                yield 0
                curr_pos += 1
            for i in range(file_sizes[file]):
                yield file
                curr_pos += 1



if __name__ == "__main__":
    Day09Solution().test()
    Day09Solution().solve()
