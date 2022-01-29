class Hex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Hex(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Hex(self.x - other.x, self.y - other.y, self.z - other.z)

    def distance(self, other):
        vec = self - other
        return (abs(vec.x) + abs(vec.y) + abs(vec.z)) / 2

    def __hex_round(self):
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

    def __lerp(self, a, b, t):  # for floats
        return a + (b - a) * t

    def __hex_lerp(self, other, t):  # for hexes
        return Hex(self.__lerp(self.x, other.x, t),
                   self.__lerp(self.y, other.y, t),
                   self.__lerp(self.z, other.z, t))

    def move_to(self, b, speed_points):
        N = self.distance(b)
        if N <= speed_points:
            return b
        return self.__hex_lerp(b, 1.0 / N * speed_points).__hex_round()
