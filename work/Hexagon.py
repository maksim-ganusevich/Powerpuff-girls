
class Hex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def add(a, b):
    return Hex(a.x + b.x, a.y + b.y, a.z + b.z)

def subtract(a, b):
    return Hex(a.x - b.x, a.y - b.y, a.z - b.z)

def distance(a, b):
    vec = subtract(a, b)
    return (abs(vec.x) + abs(vec.y) + abs(vec.z)) / 2

def hex_round(frac):
    x = round(frac.x)
    y = round(frac.y)
    z = round(frac.z)

    x_diff = abs(x - frac.x)
    y_diff = abs(y - frac.y)
    z_diff = abs(z - frac.z)

    if x_diff > y_diff and x_diff > z_diff:
        x = -y-z
    elif y_diff > z_diff:
        y = -x-z
    else:
        z = -x-y

    return Hex(x, y, z)

def lerp(a, b, t): # for floats
    return a + (b - a) * t

def hex_lerp(a, b, t): # for hexes
    return Hex(lerp(a.x, b.x, t),
                lerp(a.y, b.y, t),
                lerp(a.z, b.z, t))

def move_to(a, b, speed_points):
    N = distance(a, b)
    if N <= speed_points:
        return b
    return hex_round(hex_lerp(a, b, 1.0/N * speed_points))