class Hex:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Hex(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Hex(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

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

    # all hexes in the area with self as center
    def get_hexes_in_range(self, n: int) -> []:
        results = []
        for x in range(-n, n + 1):
            for y in range(max(-n, -x - n), min(n, -x + n) + 1):
                z = -x - y
                results.append(self + Hex(x, y, z))
        return results

    # only hexes on the edge of the area
    def get_hexes_of_circle(self, r: int) -> []:
        results = []
        x = -r
        for y in range(0, r + 1):
            z = -x - y
            results.append(self + Hex(x, y, z))
            results.append(self + Hex(-x, y - r, z - r))
        for x in range(-r + 1, r):
            y = max(-r, -x - r)
            z = -x - y
            results.append(self + Hex(x, y, z))
            y = min(r, -x + r)
            z = -x - y
            results.append(self + Hex(x, y, z))
        return results

    def get_hexes_of_axes(self, d) -> []:
        results = []
        for i in range(1, d + 1):
            results.append(self + Hex(0, i, -i))
            results.append(self + Hex(0, -i, i))
            results.append(self + Hex(i, 0, -i))
            results.append(self + Hex(-i, 0, i))
            results.append(self + Hex(i, -i, 0))
            results.append(self + Hex(-i, i, 0))
        return results
