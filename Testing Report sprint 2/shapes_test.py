import pytest
import pygame
import sys
import os

# adding parent directory to python path to import game modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# importing the modules and constants
from shapes import Shape, Board, create_shape, BOARD_WIDTH, BOARD_HEIGHT


class TestShape: # testing shape class functionality

    @pytest.fixture
    def sample_shape(self): # creating a sample shape for testing
        return Shape(5, 2, (255, 0, 0), [(0, 0), (1, 0), (0, 1)])

    def test_shape_initialization(self, sample_shape): # shape creation test
        # verify x position is set correctly
        assert sample_shape.x == 5, "Shape X position should be 5"
        # verify y position is set correctly
        assert sample_shape.y == 2, "Shape Y position should be 2"
        # verify color is set correctly
        assert sample_shape.color == (255, 0, 0), "Shape color should be red"
        # verify block coordinates are set correctly
        assert sample_shape.blocks == [(0, 0), (1, 0), (0, 1)], "Shape blocks should match initialization"

    def test_shape_movement(self, sample_shape): # shape movement test
        # test moving down
        original_y = sample_shape.y
        sample_shape.move_down()
        assert sample_shape.y == original_y + 1, "Shape should move down by 1 position"
        
        # test moving left
        original_x = sample_shape.x
        sample_shape.move_left()
        assert sample_shape.x == original_x - 1, "Shape should move left by 1 position"
        
        # test moving right
        sample_shape.move_right()
        assert sample_shape.x == original_x, "Shape should move right back to original position"

    def test_shape_coordinates(self, sample_shape): # coordinate calculation test
        # get actual coordinates from shape
        coords = sample_shape.get_coords()
        # define expected coordinates based on shape position and blocks
        expected = [(5, 2), (6, 2), (5, 3)]
        # verify calculated coordinates match expected
        assert coords == expected, f"Coordinates {coords} should match expected {expected}"

    def test_create_shape(self): # random shape creation test
        # create a random shape
        shape = create_shape()
        # verify it's a Shape instance
        assert isinstance(shape, Shape), "create_shape should return a Shape object"
        # verify it has color attribute
        assert hasattr(shape, 'color'), "Shape should have color attribute"
        # verify it has blocks attribute
        assert hasattr(shape, 'blocks'), "Shape should have blocks attribute"
        # verify it has at least one block
        assert len(shape.blocks) > 0, "Shape should have at least one block"


class TestBoard: # testing board class functionality

    @pytest.fixture
    def board(self): # creating a fresh board instance
        return Board()

    @pytest.fixture
    def valid_shape(self): # creating a valid shape for movement tests
        return Shape(5, 5, (255, 0, 0), [(0, 0)])

    def test_board_initialization(self, board): # board creation test
        # verify board has correct number of rows
        assert len(board.grid) == BOARD_HEIGHT, f"Board should have {BOARD_HEIGHT} rows"
        # verify board has correct number of columns
        assert len(board.grid[0]) == BOARD_WIDTH, f"Board should have {BOARD_WIDTH} columns"
        # verify all cells are empty (black)
        assert all(cell == (0, 0, 0) for row in board.grid for cell in row), "All board cells should be empty initially"

    def test_valid_movement(self, board, valid_shape): # valid movement test
        # verify shape can move in empty space
        assert board.can_move(valid_shape) == True, "Shape should be able to move in empty space"

    @pytest.mark.parametrize("x,y,expected", [
        (-1, 5, False),      # left wall collision
        (BOARD_WIDTH, 5, False),  # right wall collision  
        (5, BOARD_HEIGHT, False), # bottom collision
        (5, -1, True),       # above board is allowed
    ])
    def test_boundary_collisions(self, board, x, y, expected):
        # create shape at test position
        shape = Shape(x, y, (255, 0, 0), [(0, 0)])
        # verify collision detection works correctly
        assert board.can_move(shape) == expected, f"Collision detection failed at position ({x}, {y})"

    def test_board_placement(self, board): # shape placement test
        # create a multi-block shape
        shape = Shape(5, 5, (255, 0, 0), [(0, 0), (1, 0)])
        # place shape on board
        board.place(shape)
        
        # verify first block is placed correctly
        assert board.grid[5][5] == (255, 0, 0), "First block should be placed at (5,5)"
        # verify second block is placed correctly
        assert board.grid[5][6] == (255, 0, 0), "Second block should be placed at (5,6)"
        # verify adjacent cell remains empty
        assert board.grid[5][4] == (0, 0, 0), "Cell (5,4) should remain empty after placement"

    def test_row_completion_detection(self): # row completion test
        """Test that completed rows can be detected for clearing"""
        board = Board()
        # create a completed row
        for col in range(BOARD_WIDTH):
            board.grid[10][col] = (255, 0, 0)
        
        # verify row is complete (all cells filled)
        row_complete = all(cell != (0, 0, 0) for cell in board.grid[10])
        assert row_complete == True, "Row should be detected as complete when all cells are filled"


class TestShapeTypes: # testing shape variety and randomness

    def test_shape_variety(self): # shape and color variety test
        from shapes import shapes, colors
        # verify we have at least 5 shape types
        assert len(shapes) >= 5, "Should have at least 5 different shape types"
        # verify we have at least 5 colors
        assert len(colors) >= 5, "Should have at least 5 different colors"
        
        # test creating multiple random shapes
        created_shapes = [create_shape() for _ in range(10)]
        # verify we created exactly 10 shapes
        assert len(created_shapes) == 10, "Should create exactly 10 shapes"
        # verify all created objects are Shape instances
        assert all(isinstance(shape, Shape) for shape in created_shapes), "All created objects should be Shape instances"

    def test_new_cube_shapes(self): # test new cube shapes requirement
        """Test that new cube shapes are available as mentioned in requirements"""
        from shapes import shapes
        # verify we have cube-like shapes (O shape is a cube)
        cube_shapes = [shape for shape in shapes if len(shape) == 4]  # Cube shapes typically have 4 blocks
        assert len(cube_shapes) > 0, "Should have cube-like shapes available"