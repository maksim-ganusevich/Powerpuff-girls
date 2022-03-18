import unittest
from work.Hexagon import Hex
from work import Astar
from work.Map import Map


class TestPath(unittest.TestCase):

    def test_clear_path(self) -> None:
        Map().size = 11

        path = Astar.find_all_paths(Hex(0, 0, 0), Hex(-2, -3, 5))
        self.assertEqual(len(path), 12)
        path = Astar.find_all_paths(Hex(0, 0, 0), Hex(0, 5, -5))
        self.assertEqual(len(path), 6)
        path = Astar.find_all_paths(Hex(0, 0, 0), Hex(-1, 2, -1))
        self.assertEqual(len(path), 4)

    def test_path_with_obstacles(self) -> None:
        Map().size = 11

        Map().obstacles = [Hex(0, 1, -1)]
        path = Astar.find_all_paths(Hex(0, 0, 0), Hex(0, 2, -2))
        self.assertEqual(len(path), 6)
        Map().obstacles = [Hex(-1, 2, -1)]
        path = Astar.find_all_paths(Hex(0, 0, 0), Hex(-2, 3, -1))
        self.assertEqual(len(path), 4)
        Map().obstacles = [Hex(2, 0, -2)]
        path = Astar.find_all_paths(Hex(0, 0, 0), Hex(3, 0, -3))
        self.assertEqual(len(path), 9)
        Map().obstacles = [Hex(1, 0, -1), Hex(0, 1, -1)]
        path = Astar.find_all_paths(Hex(0, 0, 0), Hex(1, 1, -2))
        self.assertEqual(len(path), 8)
        Map().obstacles = [Hex(1, 0, -1), Hex(0, 1, -1), Hex(-1, 1, 0)]
        path = Astar.find_all_paths(Hex(0, 0, 0), Hex(1, 1, -2))
        self.assertEqual(len(path), 5)

        Map().obstacles = [Hex(-1, 0, 1)]
        path = Astar.find_all_paths(Hex(0, 0, 0), Hex(-5, 0, 5))
        self.assertEqual(len(path), 15)

        Map().obstacles = [Hex(-1, 0, 1), Hex(0, -1, 1), Hex(1, -1, 0), Hex(1, 0, -1), Hex(0, 1, -1)]
        path = Astar.find_all_paths(Hex(0, 0, 0), Hex(2, -2, 0))
        self.assertEqual(len(path), 13)
