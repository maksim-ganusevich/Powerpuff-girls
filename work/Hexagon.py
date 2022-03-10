from typing import Dict
from typing import List


class Hex:

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

    def __lt__(self, other):
        return max(abs(self.x), abs(self.y), abs(self.z)) <= max(abs(other.x), abs(other.y), abs(other.z))

    def __repr__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'

    def __hash__(self):
        return hash(repr(self))

    def to_dict(self) -> Dict[str, int]:
        return {'x': self.x, 'y': self.y, 'z': self.z}

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

    @staticmethod
    def dict_to_hex_list(dct: dict) -> List["Hex"]:
        res = []
        for h in dct:
            res.append(Hex(h['x'], h['y'], h['z']))
        return res

    def normalize(self):
        length = self.distance(Hex(0, 0, 0), self)
        return Hex(self.x // length, self.y // length, self.z // length)

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

    def convert_to_dict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}
