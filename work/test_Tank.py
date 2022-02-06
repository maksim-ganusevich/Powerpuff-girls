import unittest
from work.Hexagon import Hex
from work.Tanks import *


class TestTank(unittest.TestCase):

    def test_move(self) -> None:
        ht = HeavyTank("", 1, {"x": 0, "y": 0, "z": 0}, "")  # 1 hex per move
        self.assertEqual(ht.move(Hex(0, 3, -3)), Hex(0, 1, -1))
        self.assertEqual(ht.move(Hex(2, -1, -1)), Hex(1, 0, -1))
        self.assertEqual(ht.move(Hex(-10, 10, 0)), Hex(0, 1, -1))
        self.assertEqual(ht.move(Hex(-1000, 1000, 0)), Hex(-1, 2, -1))

        mt = MediumTank("", 1, {"x": 0, "y": 0, "z": 0}, "")  # 2 hexes per move
        self.assertEqual(mt.move(Hex(3, 0, -3)), Hex(2, 0, -2))
        self.assertEqual(mt.move(Hex(3, 0, -3)), Hex(3, 0, -3))
        self.assertEqual(mt.move(Hex(0, 10, -10)), Hex(2, 2, -4))
        self.assertEqual(mt.move(Hex(1000, 0, -1000)), Hex(4, 2, -6))

        lt = LightTank("", 1, {"x": 0, "y": 0, "z": 0}, "")  # 3 hexes per move
        self.assertEqual(lt.move(Hex(3, 0, -3)), Hex(3, 0, -3))
        self.assertEqual(lt.move(Hex(0, 2, -2)), Hex(0, 2, -2))
        self.assertEqual(lt.move(Hex(0, 10, -10)), Hex(0, 5, -5))
        self.assertEqual(lt.move(Hex(0, 10, -10)), Hex(0, 8, -8))
        self.assertEqual(lt.move(Hex(0, 100000, -100000)), Hex(0, 11, -11))

    def range_correct(self, center: Hex, r: int, firing_range: []) -> bool:
        for h in firing_range:
            if Hex.distance(center, h) > r or not h.in_map_boundaries():
                return False
        return True

    def circle_range_correct(self, center: Hex, r: int, firing_range: []) -> bool:
        for h in firing_range:
            if Hex.distance(center, h) != r or not h.in_map_boundaries():
                return False
        return True

    def axes_range_correct(self, center: Hex, r: int, firing_range: []) -> bool:
        for h in firing_range:
            axes = h - center
            if Hex.distance(center, h) > r or not h.in_map_boundaries()\
                    or (axes.x != 0 and axes.y != 0 and axes.z != 0):
                return False
        return True

    def test_get_firing_range(self) -> None:
        ht = HeavyTank("", 1, {"x": 11, "y": -11, "z": 0}, "")  # range r=2, standing on the edge
        self.assertTrue(self.range_correct(ht.position, 2, ht.get_firing_range()))

        md = MediumTank("", 1, {"x": 11, "y": -11, "z": 0}, "")  # circle with r=2, standing on the edge
        self.assertTrue(self.circle_range_correct(md.position, 2, md.get_firing_range()))
        md.position = Hex(0, 0, 0)  # standing in the center
        self.assertTrue(self.circle_range_correct(md.position, 2, md.get_firing_range()))

        spg = SPG("", 1, {"x": 8, "y": -10, "z": 2}, "")  # circle with r=3, standing close to the edge
        self.assertTrue(self.circle_range_correct(spg.position, 3, spg.get_firing_range()))

        atSpg = AtSPG("", 1, {"x": 0, "y": 0, "z": 0}, "")  # axes with r=3, standing in the center
        self.assertTrue(self.axes_range_correct(atSpg.position, 3, atSpg.get_firing_range()))
        md.position = Hex(-8, -3, 11)
        self.assertTrue(self.axes_range_correct(atSpg.position, 3, atSpg.get_firing_range()))


if __name__ == '__main__':
    unittest.main()
