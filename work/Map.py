from work.Hexagon import Hex


class Map:
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    @staticmethod
    def get_instance():
        return Map.__instance

    def set_values(self, map_size: int, base_dict: dict, obstacles_dict: dict) -> None:
        self.map_size = map_size
        self.base = []
        self.obstacles = []
        for b in base_dict:
            self.base.append(Hex(b['x'], b['y'], b['z']))
        for o in obstacles_dict:
            self.obstacles.append(Hex(o['x'], o['y'], o['z']))

    def in_map_boundaries(self, hex: Hex) -> bool:
        return max(abs(hex.x), abs(hex.y), abs(hex.z)) <= self.map_size

    # all hexes in the area with self as center
    def get_hexes_in_range(self, center, n) -> []:
        results = []
        for x in range(-n, n+1):
            for y in range(max(-n, -x-n), min(n, -x+n)+1):
                res = center + Hex(x, y, -x-y)
                if self.in_map_boundaries(res):
                    results.append(res)
        return results

    # only hexes on the edge of the area
    def get_hexes_of_circle(self, center, r) -> []:
        results = []
        x = -r
        for y in range(0, r):
            vector = Hex(x, y, -x-y)
            res = center + vector
            if self.in_map_boundaries(res):
                results.append(res)
            for i in range(5):
                vector = Hex(-vector.y, -vector.z, -vector.x)  # rotate 60 degrees
                res = center + vector
                if self.in_map_boundaries(res):
                    results.append(res)
        return results

    def get_hexes_of_axes(self, center, d) -> []:
        directions = [
            Hex(+1, 0, -1), Hex(+1, -1, 0), Hex(0, -1, +1),
            Hex(-1, 0, +1), Hex(-1, +1, 0), Hex(0, +1, -1),
        ]
        results = []
        for i in range(1, d + 1):
            for dir in directions:
                res = center + dir * i
                if self.in_map_boundaries(res):
                    results.append(res)
        return results
