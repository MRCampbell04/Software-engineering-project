import unittest
from shapes import Shape, Board, create_shape
#==============================================================================
class TestShape(unittest.TestCase):
#**************************************
    def test_move_left(self):
        s = Shape(5, 5, (255,0,0), [(0,0)])
        s.move_left()
        self.assertEqual(s.x, 4)
#================================================
    def test_move_right(self):
        s = Shape(5, 5, (255,0,0), [(0,0)])
        s.move_right()
        self.assertEqual(s.x, 6)
#================================================
    def test_move_down(self):
        s = Shape(5, 5, (255,0,0), [(0,0)])
        s.move_down()
        self.assertEqual(s.y, 6)
#================================================
    def test_get_coords(self):
        s = Shape(3, 4, (255,0,0), [(0,0),(1,0)])
        coords = s.get_coords()
        self.assertEqual(coords, [(3,4),(4,4)])
#==============================================================================
class TestBoard(unittest.TestCase):
#**************************************
    def test_can_move_inside_board(self):
        board = Board()
        s = Shape(5, 5, (255,0,0), [(0,0)])
        self.assertTrue(board.can_move(s))
#================================================
    def test_can_move_outside_left(self):
        board = Board()
        s = Shape(-1, 5, (255,0,0), [(0,0)])
        self.assertFalse(board.can_move(s))
#================================================       
    def test_can_move_outside_right(self):
        board = Board()
        s = Shape(10, 5, (255,0,0), [(0,0)])  
        self.assertFalse(board.can_move(s))
#================================================
    def test_can_move_outside_bottom(self):
        board = Board()
        s = Shape(5, 20, (255,0,0), [(0,0)])
        self.assertFalse(board.can_move(s))
#================================================
    def test_can_move_collision(self):
        board = Board()
        board.grid[5][5] = (255,255,0)
        s = Shape(5, 5, (0,255,0), [(0,0)])
        self.assertFalse(board.can_move(s))
#================================================
    def test_place(self):
        board = Board()
        s = Shape(2, 3, (100,100,100), [(0,0)])
        board.place(s)
        self.assertEqual(board.grid[3][2], (100,100,100))
#==============================================================================
class TestCreateShape(unittest.TestCase):
#**************************************
    def test_create_shape_type(self):
        s = create_shape()
        self.assertIsInstance(s, Shape)
#================================================
    def test_create_shape_position(self):
        s = create_shape()
        self.assertEqual(s.x, 4)
        self.assertEqual(s.y, 0)
#================================================
    def test_create_shape_blocks(self):
        s = create_shape()
        self.assertIsInstance(s.blocks, list)
        self.assertTrue(len(s.blocks) >= 4)
#================================================
    def test_create_shape_color(self):
        s = create_shape()
        self.assertIsInstance(s.color, tuple)
        self.assertEqual(len(s.color), 3)
#==============================================================================
if __name__ == "__main__":
    unittest.main()
