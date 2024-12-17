from aoc_tools.solution import Solution

screen = []

def adv(a, b, c, operand, pc):
    operand = combo(a, b, c, operand)
    return (a >> operand, b, c, pc+2)

def bxl(a, b, c, operand, pc):
    return (a, b ^ operand, c, pc+2)

def bst(a, b, c, operand, pc):
    operand = combo(a, b, c, operand)
    return (a, operand & 0b111, c, pc+2)

def jnz(a, b, c, operand, pc):
    return (a, b, c, pc+2 if a == 0 else operand)

def bxc(a, b, c, _, pc):
    return (a, b ^ c, c, pc+2)

def out(a, b, c, operand, pc):
    global screen
    operand = combo(a, b, c, operand)
    screen.append(operand & 0b111)
    return (a, b, c, pc+2)

def bdv(a, b, c, operand, pc):
    operand = combo(a, b, c, operand)
    return (a, a >> operand, c, pc+2)

def cdv(a, b, c, operand, pc):
    operand = combo(a, b, c, operand)
    return (a, b, a >> operand, pc+2)

def combo(a, b, c, operand):
    if operand == 4:
        return a
    elif operand == 5:
        return b
    elif operand == 6:
        return c
    elif operand == 7:
        raise ValueError("Invalid operand")
    else:
        return operand


COMMANDS = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]

class D17S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 17
        self.expected_test_result_part_1 = "4,6,3,5,6,3,5,2,1,0"
        self.expected_test_result_part_2 = 117440
        self.a = None
        self.b = None
        self.c = None
        self.instructions = None

    def solve_part_1(self):
        global screen
        self.get_initial_values()
        pc = 0
        screen = []
        while pc < len(self.instructions):
            command = COMMANDS[self.instructions[pc]]
            self.a, self.b, self.c, pc = command(self.a, self.b, self.c, self.instructions[pc+1], pc)
        return ",".join(map(str, screen))

    def solve_part_2(self):
        global screen
        self.puzzle = [
            "Register A: 2024",
            "Register B: 0",
            "Register C: 0",
            "",
            "Program: 0, 3, 5, 4, 3, 0",
        ]
        self.get_initial_values()
        a = 0
        while True:
            pc = 0
            screen = []
            b, c = self.b, self.c
            while pc < len(self.instructions):
                command = COMMANDS[self.instructions[pc]]
                a, b, c, pc = command(a, b, c, self.instructions[pc+1], pc)
                if not all(a == b for a, b in zip(screen, self.instructions)):
                    break
            if screen == self.instructions:
                return a
            a = a + 1
            if (a%100) == 0: print(a)

    def get_initial_values(self):
        self.a = int(self.puzzle[0].split(":")[1])
        self.b = int(self.puzzle[1].split(":")[1])
        self.c = int(self.puzzle[2].split(":")[1])
        self.instructions = list(map(int, self.puzzle[4].split(":")[1].split(",")))

if __name__ == "__main__":
    D17S().test()
    D17S().solve()
