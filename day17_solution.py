from aoc_tools.solution import Solution


def adv(a, b, c, operand, pc):
    operand = combo(a, b, c, operand)
    return a >> operand, b, c, pc + 2, None

def bxl(a, b, c, operand, pc):
    return a, b ^ operand, c, pc + 2, None

def bst(a, b, c, operand, pc):
    operand = combo(a, b, c, operand)
    return a, operand & 0b111, c, pc + 2, None

def jnz(a, b, c, operand, pc):
    return a, b, c, pc + 2 if a == 0 else operand, None

def bxc(a, b, c, _, pc):
    return a, b ^ c, c, pc + 2, None

def out(a, b, c, operand, pc):
    operand = combo(a, b, c, operand)
    return a, b, c, pc + 2, operand & 0b111

def bdv(a, b, c, operand, pc):
    operand = combo(a, b, c, operand)
    return a, a >> operand, c, pc + 2, None

def cdv(a, b, c, operand, pc):
    operand = combo(a, b, c, operand)
    return a, b, a >> operand, pc + 2, None

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
        self.get_initial_values()
        screen =  self.run_instructions(self.a, self.b, self.c, self.instructions)
        return ",".join(map(str, screen))

    def run_instructions(self, a, b, c, instructions):
        pc = 0
        screen = []
        while pc < len(self.instructions):
            op_code = self.instructions[pc]
            command = COMMANDS[op_code]
            a, b, c, pc, programm_output = command(a, b, c, instructions[pc + 1], pc)
            if programm_output is not None: screen.append(programm_output)
        return screen

    def solve_part_2(self):
        if self.is_test:
            result = self.solve_part_2_test()
        else:
            result = self.solve_part_2_real()
        return result

    def solve_part_2_test(self):
        self.puzzle = [
            "Register A: 2024",
            "Register B: 0",
            "Register C: 0",
            "",
            "Program: 0, 3, 5, 4, 3, 0",
        ]
        self.get_initial_values()
        result = self.find_valid_a(0, (0,0), 0)
        print(self.run_instructions(result, self.b, self.c, self.instructions))
        return result

    def solve_part_2_real(self):
        self.get_initial_values()
        result =  self.find_valid_a(0, (0,0), 0)
        print(self.run_instructions(result, self.b, self.c, self.instructions))
        return result

    def find_valid_a(self, fixed, presets, instruction_index):
        if instruction_index >= len(self.instructions): return fixed
        value, length = presets
        for candidate in range(1024):
            candidate_low = candidate & 0b111  # Last 3 bits
            candidate_high = candidate >> 3  # Remaining 7 bits
            mask = (1 << length) - 1  # Generate a mask for the relevant bits
            if (candidate & mask) != value: continue
            test_value = (candidate << (instruction_index * 3)) + fixed
            screen = self.run_instructions(test_value, self.b, self.c, self.instructions)
            if len(screen) < instruction_index + 1: continue
            if not all(a == b for a, b in zip(screen, self.instructions[:instruction_index + 1])): continue
            new_fixed = fixed | (candidate_low << (instruction_index * 3))
            new_presets = (candidate_high, 7)
            result = self.find_valid_a(new_fixed, new_presets, instruction_index + 1)
            if result is not None: return result
        return None

    def get_initial_values(self):
        self.a = int(self.puzzle[0].split(":")[1])
        self.b = int(self.puzzle[1].split(":")[1])
        self.c = int(self.puzzle[2].split(":")[1])
        self.instructions = list(map(int, self.puzzle[4].split(":")[1].split(",")))

if __name__ == "__main__":
    D17S().test()
    D17S().solve()
