class Hex:
    __map_size = 11

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Hex(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Hex(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Hex(self.x * other, self.y * other, self.z * other)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'

    @staticmethod
    def distance(a, b):
        vec = a - b
        return (abs(vec.x) + abs(vec.y) + abs(vec.z)) / 2

    @staticmethod
    def lerp(a, b, t):  # for floats
        return a + (b - a) * t

    @staticmethod
    def hex_lerp(a, b, t):  # for hexes
        return Hex(Hex.lerp(a.x, b.x, t),
                   Hex.lerp(a.y, b.y, t),
                   Hex.lerp(a.z, b.z, t))

    def hex_round(self):
        x = round(self.x)
        y = round(self.y)
        z = round(self.z)

        x_diff = abs(x - self.x)
        y_diff = abs(y - self.y)
        z_diff = abs(z - self.z)

        if x_diff > y_diff and x_diff > z_diff:
            x = -y - z
        elif y_diff > z_diff:
            y = -x - z
        else:
            z = -x - y

        return Hex(x, y, z)

    def in_map_boundaries(self):
        return max(abs(self.x), abs(self.y), abs(self.z)) <= self.__map_size

    # all hexes in the area with self as center
    def get_hexes_in_range(self, n) -> []:
        results = []
        for x in range(-n, n+1):
            for y in range(max(-n, -x-n), min(n, -x+n)+1):
                res = self + Hex(x, y, -x-y)
                if res.in_map_boundaries():
                    results.append(res)
        return results

    # only hexes on the edge of the area
    def get_hexes_of_circle(self, r) -> []:
        results = []
        x = -r
        for y in range(0, r+1):  # straight lines on both edges
            res1 = self + Hex(x, y, -x-y)
            res2 = self + Hex(-x, y-r, -x-y-r)
            if res1.in_map_boundaries():
                results.append(res1)
            if res2.in_map_boundaries():
                results.append(res2)
        for x in range(-r+1, r):  # top and bottom hexes in the middle
            y = max(-r, -x-r)
            res1 = self + Hex(x, y, -x-y)
            y = min(r, -x+r)
            res2 = self + Hex(x, y, -x-y)
            if res1.in_map_boundaries():
                results.append(res1)
            if res2.in_map_boundaries():
                results.append(res2)
        return results

    def get_hexes_of_axes(self, d) -> []:
        directions = [
            Hex(+1, 0, -1), Hex(+1, -1, 0), Hex(0, -1, +1),
            Hex(-1, 0, +1), Hex(-1, +1, 0), Hex(0, +1, -1),
        ]
        results = []
        for i in range(1, d+1):
            for dir in directions:
                res = self + dir * i
                if res.in_map_boundaries():
                    results.append(res)
        return results
