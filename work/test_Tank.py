import unittest
from work.Hexagon import Hex
from work.Tanks import AtSPG, HeavyTank, LightTank, MediumTank, SPG
from work import Map


class TestTank(unittest.TestCase):

    def test_move(self) -> None:
        Map.init_values(11, [], [])
        ht = HeavyTank(0, 1, {"x": 0, "y": 0, "z": 0}, 0)  # 1 hex per move
        self.assertTrue(ht.move(Hex(0, 3, -3)))
        self.assertTrue(ht.move(Hex(2, -1, -1)))
        self.assertTrue(ht.move(Hex(-10, 10, 0)))

        Map.init_values(11, [], [{"x": 1, "y": -1, "z": 0}, {"x": 1, "y": 0, "z": -1}])
        lt = LightTank(0, 1, {"x": 0, "y": 0, "z": 0}, 0)  # 3 hexes per move
        lt.move(Hex(4, -2, -2))
        self.assertEqual(lt.position, Hex(2, 0, -2))
        lt.move(Hex(4, -2, -2))
        self.assertEqual(lt.position, Hex(4, -2, -2))

    @staticmethod
    def range_correct(center: Hex, r: int, firing_range: []) -> bool:
        for h in firing_range:
            if Hex.distance(center, h) > r or not h.in_map_boundaries():
                return False
        return True

    @staticmethod
    def circle_range_correct(center: Hex, r: int, firing_range: []) -> bool:
        for h in firing_range:
            if Hex.distance(center, h) != r or not h.in_map_boundaries():
                return False
        return True

    @staticmethod
    def axes_range_correct(center: Hex, r: int, firing_range: []) -> bool:
        for h in firing_range:
            axes = h - center
            if Hex.distance(center, h) > r or not h.in_map_boundaries() \
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
