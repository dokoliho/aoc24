from aoc_tools.solution import Solution
from collections import defaultdict


class Wire:

    wires = {}
    successor_gates = defaultdict(list)
    predecessor_gates = defaultdict(list)
    max_cycle = -1

    @staticmethod
    def get_wire(name):
        if name in Wire.wires:
            return Wire.wires[name]
        else:
            return Wire(name)

    @staticmethod
    def z_value(cycle):
        z_name = sorted([name for name in Wire.wires if name[0] == "z"], reverse=True)
        z_values = [Wire.wires[name].get_value_at_cycle(cycle) for name in z_name]
        if any([value is None for value in z_values]): return None
        return int("".join(map(str, z_values)), 2)


    def __init__(self, name):
        self.name = name
        self.value = []
        Wire.wires[name] = self

    def set_value(self, value, cycle):
        Wire.max_cycle = max(Wire.max_cycle, cycle)
        self.value.append((cycle, value))
        for gate in Wire.successor_gates[self]:
            if gate.operator == "OR" and value == 1:
                gate.output.set_value(1, cycle+1)
                continue
            peer = [wire for wire in gate.inputs if wire != self][0]
            peer_value = peer.get_value_at_cycle(cycle)
            if peer_value is None: continue
            if gate.operator == "AND":
                gate.output.set_value(value & peer_value, cycle+1)
            elif gate.operator == "XOR":
                gate.output.set_value(value ^ peer_value, cycle+1)
            elif gate.operator == "OR":
                gate.output.set_value(value | peer_value, cycle+1)
            else:
                raise Exception("Unknown operator")

    def get_value_at_cycle(self, cycle):
        entries = list(filter(lambda x: x[0] <= cycle, self.value))
        if len(entries) == 0: return None
        return entries[-1][1]


class Gate:

    def __init__(self, line):
        self.inputs = []
        self.output = None
        self.operator = None
        self.parse_line(line)


    def parse_line(self, line):
        parts = line.split(" ")
        self.inputs = [Wire.get_wire(parts[0]), Wire.get_wire(parts[2])]
        self.output = Wire.get_wire(parts[-1])
        self.operator = parts[1]
        for wire in self.inputs: Wire.successor_gates[wire].append(self)
        Wire.predecessor_gates[self.output].append(self)


class D24S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 24
        self.expected_test_result_part_1 = 2024
        self.expected_test_result_part_2 = 2
        self.presets = None

    def solve_part_1(self):
        self.get_presets_and_grid()
        for preset in self.presets:
            Wire.get_wire(preset[0]).set_value(preset[1], 0)
        decimal_value = Wire.z_value(Wire.max_cycle)
        return decimal_value

    def solve_part_2(self):
        return 2

    def get_presets_and_grid(self):
        self.presets = []
        is_second_segment = False
        for line in self.puzzle:
            if line == "": is_second_segment = True
            elif is_second_segment: Gate(line)
            else: self.presets.append((lambda x: (x[0], int(x[1])))(line.split(":")))


if __name__ == "__main__":
    D24S().test()
    D24S().solve()
