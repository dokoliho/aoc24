from collections import defaultdict
from solution import Solution


DIRECTIONS = { "UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0) }




class D12S(Solution):

    class Plant:
        def __init__(self, plant):
            self._species = plant
            self._parent = self
            self._rank = 0
            self._fences = 4
            self._sides = 4

        def __repr__(self):
            return f"{self._species} / {self._sides}"

        @property
        def species(self):
            return self._species

        @property
        def fences(self):
            return self._fences

        @fences.setter
        def fences(self, value):
            self._fences = value

        @property
        def region(self):
            return self.find_set()

        @property
        def sides(self):
            return self._sides

        @sides.setter
        def sides(self, value):
            self._sides = value

        def find_set(self):
            if self._parent != self:
                self._parent = self._parent.find_set()
            return self._parent

        def link(self, other):
            if self._rank > other._rank:
                other._parent = self
            else:
                self._parent = other
                if self._rank == other._rank:
                    other._rank += 1

        def union(self, other):
            root1 = self.find_set()
            root2 = other.find_set()
            root1.link(root2)


    def __init__(self):
        super().__init__()
        self.day = 12
        self.expected_test_result_part_1 = 1930
        self.expected_test_result_part_2 = 1206

    def solve_part_1(self):
        garden_map = self.read_input()
        regions = self.find_regions(garden_map)
        result = sum([size*fences for size, fences, _ in regions.values()])
        return result

    def solve_part_2(self):
        garden_map = self.read_input()
        self.find_sides(garden_map)
        regions = self.find_regions(garden_map)
        result = sum([size*sides for size, _, sides in regions.values()])
        return result

    def read_input(self):
        garden_map = {}
        for x in range(len(self.puzzle[0])):
            for y in range(len(self.puzzle)):
                garden_map[(x, y)] = D12S.Plant(self.puzzle[y][x])
        for x in range(len(self.puzzle[0])):
            for y in range(len(self.puzzle)):
                for dir, (dx, dy) in DIRECTIONS.items():
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in garden_map and garden_map[(x, y)].species == garden_map[(nx, ny)].species:
                        garden_map[(x, y)].union(garden_map[(x + dx, y + dy)])
                        garden_map[(x, y)].fences -= 1
        return garden_map

    def find_sides(self, garden_map):
        for x in range(len(self.puzzle[0])):
            for y in range(len(self.puzzle)):
                sides = set(DIRECTIONS.keys())
                species = garden_map[(x, y)].species
                neighbours = {(dx, dy): getattr(garden_map.get((x+dx, y+dy), None), 'species', None)
                              for dx in [-1, 0, 1] for dy in [-1, 0, 1]}
                # Remove sides that are connected to the same species
                for dir, (dx, dy) in DIRECTIONS.items():
                    if neighbours[(dx, dy)] == species:
                        sides.remove(dir)
                # Remove sides that are assigned to other spots in the same region
                if "UP" in sides:
                    if neighbours[(-1, 0)] == species and neighbours[(-1, -1)] != species:
                        sides.remove("UP")
                if "DOWN" in sides:
                    if neighbours[(-1, 0)] == species and neighbours[(-1, 1)] != species:
                        sides.remove("DOWN")
                if "LEFT" in sides:
                    if neighbours[(0, -1)] == species and neighbours[(-1, -1)] != species:
                        sides.remove("LEFT")
                if "RIGHT" in sides:
                    if neighbours[(0, -1)] == species and neighbours[(1, -1)] != species:
                        sides.remove("RIGHT")
                garden_map[(x, y)].sides = len(sides)

    def find_regions(self, garden_map):
        regions = defaultdict(lambda: (0, 0, 0))
        for plant in garden_map.values():
            size_of_region, fences, sides = regions[plant.region]
            regions[plant.region] = (size_of_region + 1, fences + plant.fences, sides + plant.sides)
        return regions

    def print_map(self, garden_map):
        for y in range(len(self.puzzle)):
            for x in range(len(self.puzzle[0])):
                print(garden_map[(x, y)].sides, end="")
            print()

if __name__ == "__main__":
    D12S().test()
    D12S().solve()
