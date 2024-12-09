from solution import Solution

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
        pos = 0
        blocks = []
        for c in list(self.puzzle[0]):
            l = int(c)
            blocks.append((pos, l))
            pos += l
        files = [block for block in blocks[0::2]]
        gaps = [block for block in blocks[1::2]]
        return files, gaps

    def generate_block_sequence(self, files, gaps):
        file_sizes = [file[1] for file in files]
        free_blocks = [gap[1] for gap in gaps]
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


    def file_sequence(self, files, gaps):

        def file_size(index):
            return files[index][1]

        def file_pos(index):
            return files[index][0]

        def free_blocks(index):
            return gaps[index][1]

        def gap_pos(index):
            return gaps[index][0]


        for moving_file in range(len(files)-1, -1, -1):
            for gap in range(len(gaps)):
                if gap >= moving_file: break
                if file_size(moving_file) <= free_blocks(gap):
                    files[moving_file] = (gap_pos(gap), file_size(moving_file))
                    gaps[gap] = ( gap_pos(gap) + file_size(moving_file) ,
                                  free_blocks(gap) - file_size(moving_file))
                    if moving_file < len(gaps):
                        gaps[moving_file] = (gap_pos(moving_file),
                                     free_blocks(moving_file) + file_size(moving_file))
                    break

        file_pos = [file[0] for file in files]
        return sorted(enumerate(file_pos), key=lambda x: x[1])


    def generate_block_sequence2(self, files, gaps):
        file_sequence = self.file_sequence(files, gaps)
        curr_pos = 0
        for file, pos in file_sequence:
            while curr_pos < pos:
                yield 0
                curr_pos += 1
            for i in range(files[file][1]):
                yield file
                curr_pos += 1



if __name__ == "__main__":
    Day09Solution().test()
    Day09Solution().solve()
