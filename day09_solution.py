from solution import Solution

class Day09Solution(Solution):

    class Segment:
        def __init__(self, start, length):
            self._start = start
            self._length = length

        @property
        def start(self):
            return self._start

        @property
        def length(self):
            return self._length

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
        segments = []
        for c in list(self.puzzle[0]):
            l = int(c)
            segments.append(Day09Solution.Segment(pos, l))
            pos += l
        files = [segment for segment in segments[0::2]]
        gaps = [segment for segment in segments[1::2]]
        return files, gaps

    def generate_block_sequence(self, files, gaps):
        file_sizes = [file.length for file in files]
        free_blocks = [gap.length for gap in gaps]
        current_file = 0
        moving_file = len(files) - 1
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
        for moving_file in range(len(files)-1, -1, -1):
            for gap in range(len(gaps)):
                if gap >= moving_file: break
                length = files[moving_file].length
                if length <= gaps[gap].length:
                    files[moving_file] = Day09Solution.Segment(
                            gaps[gap].start,
                            length)
                    gaps[gap] = Day09Solution.Segment(
                            gaps[gap].start + length,
                            gaps[gap].length - length)
                    if moving_file < len(gaps):
                        gaps[moving_file] = Day09Solution.Segment(
                            gaps[moving_file].start,
                            gaps[moving_file].length + length)
                    break

        file_pos = [file.start for file in files]
        return sorted(enumerate(file_pos), key=lambda x: x[1])


    def generate_block_sequence2(self, files, gaps):
        file_sequence = self.file_sequence(files, gaps)
        curr_pos = 0
        for file, pos in file_sequence:
            while curr_pos < pos:
                yield 0
                curr_pos += 1
            for i in range(files[file].length):
                yield file
                curr_pos += 1



if __name__ == "__main__":
    Day09Solution().test()
    Day09Solution().solve()
