from aoc_tools.solution import Solution


class D15S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 15
        self.expected_test_result_part_1 = 10092
        self.expected_test_result_part_2 = 9021
        self.path = ""
        self.map = {}
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
        # self.puzzle = [
        #     "#######",
        #     "#...#.#",
        #     "#.....#",
        #     "#..OO@#",
        #     "#..O..#",
        #     "#.....#",
        #     "#######",
        #     "",
        #     "<vv<<^^<<^^",
        # ]
        self.get_map2_and_path()
        for direction in self.path:
            self.make_step2(direction)
        result = self.sum_of_coordinates("[")
        return result

    def get_map_and_path(self):
        self.map = {}
        self.path = ""
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

    def get_map2_and_path(self):
        self.map = {}
        self.path = ""
        path_section = False
        for row, line in enumerate(self.puzzle):
            if line == "":
                self.height = row
                self.width = len(self.puzzle[0]) * 2
                path_section = True
                continue
            if path_section:
                self.path += line
            else:
                for col, char in enumerate(line):
                    if char == "#":
                        self.map[(col*2,row)] = char
                        self.map[(col*2+1,row)] = char
                    elif char == "O":
                        self.map[(col*2,row)] = "["
                        self.map[(col*2+1,row)] = "]"
                    elif char == "@":
                        self.robot =(col*2,row)

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


    def sum_of_coordinates(self, char):
        coordinates = [p for p in self.map if self.map[p] == char]
        return sum([p[1]*100+p[0] for p in coordinates])


    def make_step2(self, direction):
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
        if dy == 0:
            return self.is_movable(pos, dx, dy)
        else:
            if char == "[":
                peer = (pos[0]+1, pos[1])
            else:
                peer = (pos[0]-1, pos[1])
            return (self.is_movable(pos, dx, dy) and
                    self.is_movable(peer, dx, dy))

    def move(self, pos, dx, dy):
        if pos not in self.map:
            return
        if self.map[pos] == "#":
            raise ValueError("Cannot move to wall")
        if dy == 0:
            self.move_on_element(pos, dx, dy)
        else:
            if self.map[pos] == "[":
                peer = (pos[0]+1, pos[1])
            else:
                peer = (pos[0]-1, pos[1])
            self.move_on_element(pos, dx, dy)
            self.move_on_element(peer, dx, dy)

    def move_on_element(self, pos, dx, dy):
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
