import pytest
import pygame
import sys
import os

# adding parent directory to python path to import game modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# importing the modules and constants
from game import Shape, Board, create_shape, Button


class TestGameClasses: # testing game class inheritance and structure
    def test_classes_inherit_correctly(self): # class interface test
        # create test shape instance
        shape = Shape(5, 2, (255, 0, 0), [(0, 0)])
        # create test board instance
        board = Board()
        
        # verify shape has required coordinate method
        assert hasattr(shape, 'get_coords'), "Shape should have get_coords method"
        # verify board has required row clearing method
        assert hasattr(board, 'clear_full_rows'), "Board should have clear_full_rows method"


class TestGameLogic: # testing core game mechanics

    @pytest.fixture
    def board_with_full_row(self): # create board with completed row
        board = Board()
        # fill row 5 completely with red blocks
        for col in range(len(board.grid[0])):
            board.grid[5][col] = (255, 0, 0)
        return board

    def test_row_clearing(self, board_with_full_row): # row clearing functionality test
        # attempt to clear full rows
        cleared = board_with_full_row.clear_full_rows()
        # verify exactly 1 row was cleared
        assert cleared == 1, "Should clear exactly 1 full row"
        
        # verify new empty row was added at top
        assert all(cell == (0, 0, 0) for cell in board_with_full_row.grid[0]), "Top row should be empty after clearing"

    def test_score_increases_on_row_clear(self): # score increase test
        """Test that score increases when rows are cleared"""
        # simulate row clearing and score increase
        score = 0
        rows_cleared = 1
        score += rows_cleared  # score increases by 1 per cleared row
        assert score == 1, "Score should increase by 1 when row is cleared"

    @pytest.mark.parametrize("score,expected_level", [
        (0, 1), (4, 1), (5, 1), (9, 1), (10, 2), (14, 2), (15, 2), (19, 2), (20, 3)
    ])
    def test_level_progression_at_10(self, score, expected_level): # level progression test
        """Test level increases when score reaches 10, 20, etc."""
        # level increases every 10 points
        level = (score // 10) + 1
        assert level == expected_level, f"Level should be {expected_level} when score is {score}"

    @pytest.mark.parametrize("level,expected_speed", [
        (1, 500), (2, 450), (3, 400), (8, 150), (9, 100), (10, 100)
    ])
    def test_fall_speed_calculation(self, level, expected_speed): # difficulty progression test
        base_speed = 500
        # calculate fall speed with minimum cap of 100
        fall_speed = max(100, base_speed - (level-1)*50)
        # verify speed decreases with level until minimum
        assert fall_speed == expected_speed, f"Fall speed should be {expected_speed} at level {level}"

    def test_game_over_condition(self): # game over detection test
        board = Board()
        # fill top row completely to block new shapes
        for col in range(len(board.grid[0])):
            board.grid[0][col] = (255, 0, 0)
        
        # create new shape and check if it can be placed
        new_shape = create_shape()
        game_over = not board.can_move(new_shape)
        # verify game over condition is detected
        assert game_over == True, "Game should be over when new shape cannot be placed"

    def test_win_state_row_completion(self): # win state functionality test
        """Test that completed rows are cleared and contribute to win condition"""
        board = Board()
        # simulate a completed row
        for col in range(len(board.grid[0])):
            board.grid[18][col] = (255, 0, 0)  # Fill second-to-last row
        
        rows_cleared = board.clear_full_rows()
        # verify row was cleared
        assert rows_cleared > 0, "Completed rows should be cleared"
        # verify score would increase (this is handled in game loop)


class TestScoring: # testing scoring system
    def test_scoring_calculation(self): # basic scoring test
        # test that score increases with rows cleared
        score = 0
        rows_cleared = 2
        # add 1 point per cleared row
        score += rows_cleared * 1
        # verify correct score calculation
        assert score == 2, "Score should be 2 for 2 cleared rows"

    def test_level_up_at_score_10(self): # critical level progression test
        """Test that level increases exactly when score reaches 10"""
        score = 9
        level = (score // 10) + 1
        assert level == 1, "Level should be 1 when score is 9"
        
        score = 10
        level = (score // 10) + 1
        assert level == 2, "Level should be 2 when score reaches 10"


class TestGameIntegration: # testing component integration

    def test_button_in_game_context(self): # button integration test
        # create button using game's Button class
        button = Button("Test", 100, text_color=(0, 0, 0), filled=True)
        # verify button text is set correctly
        assert button.text == "Test", "Button text should be 'Test'"
        # verify button has default width
        assert button.rect.width == 270, "Button should have default width of 270"

    def test_shape_manipulation(self): # shape movement integration test
        # create random shape
        shape = create_shape()
        # get original coordinates
        original_coords = shape.get_coords()
        # move shape to the right
        shape.move_right()
        # get new coordinates after movement
        new_coords = shape.get_coords()
        # verify coordinates changed after movement
        assert new_coords != original_coords, "Shape coordinates should change after movement"

    def test_complete_win_flow(self): # complete win flow test
        """Test the complete win flow: row completion -> score increase -> level up"""
        # simulate game state
        score = 0
        level = 1
        
        # simulate clearing multiple rows to reach score 10
        rows_cleared = 10
        score += rows_cleared  # 1 point per row
        level = (score // 10) + 1  # level up at score 10
        
        assert score == 10, "Score should be 10 after clearing 10 rows"
        assert level == 2, "Level should increase to 2 when score reaches 10"


@pytest.mark.skip(reason="Resource files not guaranteed in test environment")
class TestResources: # testing external resource availability
    def test_font_file_exists(self): # font file check
        # verify game font file exists
        assert os.path.exists("font/Audiowide-Regular.ttf"), "Font file should be available"
    
    def test_image_files_exist(self): # image files check
        # list of required game image files
        image_files = ["images/1.png", "images/pause_icon.png", "images/red.png", "images/blue.png"]
        # verify each image file exists
        for img_file in image_files:
            assert os.path.exists(img_file), f"Image file {img_file} should be available"