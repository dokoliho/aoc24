from aoc_tools.solution import Solution


class D15S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 15
        self.expected_test_result_part_1 = 10092
        self.expected_test_result_part_2 = 2
        self.path = ""
        self.map = {}
        self.robot = None
        self.height = None
        self.width = None

    def solve_part_1(self):
        self.get_map_and_path()
        for direction in self.path:
            self.make_step(direction)
        result = self.sum_of_coordinates()
        return result

    def solve_part_2(self):
        return 2

    def get_map_and_path(self):
        path_section = False
        for row, line in enumerate(self.puzzle):
            if line == "":
                self.height = row
                self.width = len(self.puzzle[0])
                path_section = True
                continue
            if path_section:
                self.path += line
            else:
                for col, char in enumerate(line):
                    if char == "#" or char == "O":
                        self.map[(col,row)] = char
                    elif char == "@":
                        self.robot =(col,row)

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

    def get_row_map(self, row_num):
        return sorted([(o[0], self.map[o]) for o in self.map if o[1] == row_num], key=lambda x: x[0])

    def get_col_map(self, col_num):
        return sorted([(o[1], self.map[o]) for o in self.map if o[0] == col_num], key=lambda x: x[0])

    def make_step(self, direction):
        obj, selector, delta, get_pos = self.get_affected_objects(direction)
        wall = next((i for i, o in enumerate(obj) if o[1] == "#"), None)
        while wall>0 and abs(obj[wall-1][0] - obj[wall][0]) == 1:
            wall -= 1
        if obj[wall][0] == self.robot[selector]+delta:
            return # no movement, wall ahead
        obj = obj[:wall]
        index = 0
        pusher = list(self.robot)
        inserts = []
        while index < len(obj) and obj[index][0] == pusher[selector]+delta:
            old_pos = get_pos(obj[index][0])
            new_pos = get_pos(obj[index][0] + delta)
            del(self.map[old_pos])
            inserts.append((new_pos, obj[index][1]))
            pusher[selector] += delta
            index += 1

        for pos, char in inserts:
            self.map[pos] = char

        new_robot_pos = list(self.robot)
        new_robot_pos[selector] = new_robot_pos[selector]+delta
        self.robot = tuple(new_robot_pos)


    def get_affected_objects(self, direction):
        if direction in "^":
            line = self.get_col_map(self.robot[0])
            line = list(reversed([o for o in line if o[0] < self.robot[1]]))
            get_pos = lambda x: (self.robot[0],x)
            return  line, 1, -1, get_pos
        elif direction in "v":
            line = self.get_col_map(self.robot[0])
            line = [o for o in line if o[0] > self.robot[1]]
            get_pos = lambda x: (self.robot[0],x)
            return line, 1, 1, get_pos
        elif direction in "<":
            line = self.get_row_map(self.robot[1])
            line = list(reversed([o for o in line if o[0] < self.robot[0]]))
            get_pos = lambda x: (x,self.robot[1])
            return line, 0, -1, get_pos
        elif direction in ">":
            line = self.get_row_map(self.robot[1])
            line = [o for o in line if o[0] > self.robot[0]]
            get_pos = lambda x: (x,self.robot[1])
            return line, 0, 1, get_pos
        raise ValueError(f"Invalid direction {direction}")


    def sum_of_coordinates(self):
        coordinates = [p for p in self.map if self.map[p] == "O"]
        return sum([p[1]*100+p[0] for p in coordinates])


if __name__ == "__main__":
    D15S().test()
    D15S().solve()
