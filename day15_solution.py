from aoc_tools.solution import Solution


class D15S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 15
        self.expected_test_result_part_1 = 10092
        self.expected_test_result_part_2 = 9021
        self.path = None
        self.map = None
        self.robot = None
        self.height = None
        self.width = None

    def solve_part_1(self):
        self.get_map_and_path()
        for direction in self.path:
            self.make_step(direction)
        result = self.sum_of_coordinates("O")
        return result

    def solve_part_2(self):
        self.get_map_and_path(part_2=True)
        for direction in self.path:
            self.make_step(direction)
        result = self.sum_of_coordinates("[")
        return result

    def get_map_and_path(self, part_2=False):
        self.map = {}
        self.path = ""
        factor = 1 if not part_2 else 2
        box_shape = ["O"] if not part_2 else ["[","]"]
        path_section = False
        for row, line in enumerate(self.puzzle):
            if line == "":
                self.height = row
                self.width = len(self.puzzle[0]) * factor
                path_section = True
                continue
            if path_section:
                self.path += line
            else:
                for col, char in enumerate(line):
                    if char == "#":
                        for i in range(factor):
                            self.map[(col*factor+i,row)] = char
                    if char == "O":
                        for i in range(factor):
                            self.map[(col*factor+i,row)] = box_shape[i]
                    elif char == "@":
                        self.robot =(col*factor,row)

    def display_map(self):
        for row in range(self.height):
            for col in range(self.width):
                pos = (col,row)
                if pos == tuple(self.robot):
                    print("@", end="")
                elif pos not in self.map:
                    print(" ", end="")
                else:
                    print(self.map[pos], end="")
            print()

    def sum_of_coordinates(self, char):
        coordinates = [p for p in self.map if self.map[p] == char]
        return sum([p[1]*100+p[0] for p in coordinates])

    def make_step(self, direction):
        dx, dy = self.get_direction(direction)
        new_robot = (self.robot[0]+dx, self.robot[1]+dy)
        if not self.is_movable(new_robot, dx, dy):
            return
        self.move(new_robot, dx, dy)
        self.robot = new_robot

    def is_movable(self, pos, dx, dy):
        if pos not in self.map:
            return True
        if self.map[pos] == "#":
            return False
        char = self.map[pos]
        pos = (pos[0]+dx, pos[1]+dy)
        if dy == 0 or char == "O":
            return self.is_movable(pos, dx, dy)
        else:
            if char == "[":
                peer = (pos[0]+1, pos[1])
            else:
                peer = (pos[0]-1, pos[1])
            return self.is_movable(pos, dx, dy) and self.is_movable(peer, dx, dy)

    def move(self, pos, dx, dy):
        if pos not in self.map:
            return
        char = self.map[pos]
        if char == "#":
            raise ValueError("Cannot move to wall")
        if dy == 0 or char == "O":
            self.push_one_pos(pos, dx, dy)
        else:
            if self.map[pos] == "[":
                peer = (pos[0]+1, pos[1])
            else:
                peer = (pos[0]-1, pos[1])
            self.push_one_pos(pos, dx, dy)
            self.push_one_pos(peer, dx, dy)

    def push_one_pos(self, pos, dx, dy):
        char = self.map[pos]
        del (self.map[pos])
        pos = (pos[0] + dx, pos[1] + dy)
        self.move(pos, dx, dy)
        self.map[pos] = char

    def get_direction(self, direction):
        if direction in "^":
            return 0, -1
        elif direction in "v":
            return 0, 1
        elif direction in "<":
            return -1, 0
        elif direction in ">":
            return 1, 0
        raise ValueError(f"Invalid direction {direction}")


if __name__ == "__main__":
    D15S().test()
    D15S().solve()
