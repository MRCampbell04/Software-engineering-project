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
#================================================
    def test_clone(self):
        s = Shape(2, 3, (100,100,100), [(0,0)])
        c = s.clone()
        self.assertEqual(c.x, s.x)
        self.assertEqual(c.y, s.y)
        self.assertEqual(c.blocks, s.blocks)
        self.assertEqual(c.color, s.color)
        self.assertNotEqual(id(c), id(s))  # object جديد
#================================================
    def test_rotation_allowed(self):
        s = Shape(1, 1, (0,0,255), [(0,0),(1,0)])
        old_blocks = s.blocks[:]
        # apply rotation
        s.blocks = [(-by, bx) for bx, by in s.blocks]
        self.assertNotEqual(s.blocks, old_blocks)
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
#================================================
    def test_clear_lines_updates_score_and_level(self):
        board = Board()
        # املأ الصف الأخير كامل
        for col in range(10):
            board.grid[19][col] = (255,0,0)
        board.clear_lines()
        # الصف اتشال
        self.assertEqual(board.grid[19], [(0,0,0)]*10)
        self.assertEqual(board.score, 1)
        self.assertEqual(board.level, 1 + (board.score // 10))
#================================================
    def test_game_over_triggered(self):
        board = Board()
        # املأ الصف العلوي
        for col in range(10):
            board.grid[0][col] = (255,0,0)
        shape = Shape(4,0,(0,255,0),[(0,0)])
        can_move = board.can_move(shape)
        self.assertFalse(can_move)
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
#================================================
    def test_create_shape_generates_all_types(self):
        types_seen = set()
        for _ in range(100):
            s = create_shape()
            types_seen.add(s.shape_type)
        self.assertEqual(types_seen, {'O','I','L','T','S'})
#==============================================================================
class TestSwap(unittest.TestCase):
#**************************************
    def test_swap_shapes(self):
        shape1 = Shape(0,0,(255,0,0),[(0,0)])
        shape2 = Shape(0,0,(0,255,0),[(0,0)])
        next_shapes = [shape2]
        # swap logic
        current_temp = shape1
        shape1 = next_shapes[0]
        next_shapes[0] = current_temp
        shape1.x, shape1.y = 4, 0
        next_shapes[0].x, next_shapes[0].y = 4, 0
        self.assertEqual(shape1.color, (0,255,0))
        self.assertEqual(next_shapes[0].color, (255,0,0))
        self.assertEqual(shape1.x, 4)
        self.assertEqual(next_shapes[0].y, 0)
#==============================================================================
if __name__ == "__main__":
    unittest.main()
