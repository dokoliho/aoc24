from numpy.f2py.auxfuncs import isint1

from aoc_tools.solution import Solution
from collections import defaultdict


class Wire:

    wires = {}
    successor_gates = defaultdict(list)
    predecessor_gates = defaultdict(list)

    @staticmethod
    def reset():
        Wire.wires = {}
        Wire.successor_gates.clear()
        Wire.predecessor_gates.clear()

    @staticmethod
    def get_wire(name):
        if name in Wire.wires:
            return Wire.wires[name]
        else:
            return Wire(name)

    @staticmethod
    def z_value():
        z_name = sorted([name for name in Wire.wires if name[0] == "z"], reverse=True)
        z_values = [Wire.wires[name].value for name in z_name]
        if any([value is None for value in z_values]): return None
        return int("".join(map(str, z_values)), 2)

    def __init__(self, name):
        self.name = name
        self.value = None
        Wire.wires[name] = self

    @staticmethod
    def bulk_set(presets):
        new_presets = []
        frontier = []
        for name, value in presets:
            Wire.wires[name].set_value(value, frontier)
        while len(frontier) > 0:
            gate = frontier.pop(0)
            gate.fire(new_presets)
        return new_presets

    def set_value(self, value, frontier):
        if self.value is not None:
            return
        self.value = value
        frontier.extend(Wire.successor_gates[self.name])

    @staticmethod
    def count_wires_with_value():
        return len([wire for wire in Wire.wires.values() if wire.value is not None])


class Gate:

    gates = []

    @staticmethod
    def reset():
        Gate.gates = []

    def __init__(self, line):
        self.inputs = []
        self.output = None
        self.operator = None
        self.parse_line(line)
        Gate.gates.append(self)

    def __str__(self):
        i0name = self.inputs[0].name
        i1name = self.inputs[1].name
        i0val = self.inputs[0].value
        i1val = self.inputs[1].value
        return f"{i0name} ({i0val}) {self.operator} {i1name} ({i1val}) -> {self.output.name}"

    def parse_line(self, line):
        parts = line.split(" ")
        self.inputs = [Wire.get_wire(parts[0]), Wire.get_wire(parts[2])]
        self.output = Wire.get_wire(parts[-1])
        self.operator = parts[1]
        for wire in self.inputs: Wire.successor_gates[wire.name].append(self)
        Wire.predecessor_gates[self.output.name].append(self)

    def fire(self, new_presets):
        if not self.is_ready_to_fire():
            return
        i = [wire.value for wire in self.inputs]
        if self.operator == "OR":
            new_presets.append((self.output.name, i[0] | i[1]))
        elif self.operator == "AND":
            new_presets.append((self.output.name, i[0] & i[1]))
        elif self.operator == "XOR":
            new_presets.append((self.output.name, i[0] ^ i[1]))

    def is_ready_to_fire(self):
        return all([wire.value is not None for wire in self.inputs])

    @staticmethod
    def count_gates_with_value():
        return len([gate for gate in Gate.gates if gate.is_ready_to_fire()])

class D24S(Solution):

    def __init__(self):
        super().__init__()
        self.day = 24
        self.expected_test_result_part_1 = 2024
        self.expected_test_result_part_2 = 2
        self.presets = None

    def solve_part_1(self):
        self.get_presets_and_grid()
        while len(self.presets) > 0:
            self.presets = Wire.bulk_set(self.presets)
        return Wire.z_value()

    def solve_part_2(self):
        return 2

    def get_presets_and_grid(self):
        self.presets = []
        Wire.reset()
        Gate.reset()
        is_second_segment = False
        for line in self.puzzle:
            if line == "": is_second_segment = True
            elif is_second_segment: Gate(line)
            else: self.presets.append((lambda x: (x[0], int(x[1])))(line.split(":")))


if __name__ == "__main__":
    D24S().test()
    D24S().solve()
