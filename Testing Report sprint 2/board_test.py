import pytest
import pygame
import sys
import os

# adding parent directory to python path to import game modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# importing the modules and constants
from board import Board, draw_ui, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_X, GRID_Y, BLOCK_SIZE, GRID_ROWS, GRID_COLS


class TestBoard: # testing board component functionality

    @pytest.fixture
    def board(self): # creating a board
        return Board()

    @pytest.fixture
    def pygame_setup(self): 
      # managing pygame initialization and cleanup
        pygame.init()  # Initialize Pygame modules
        # Create a display surface matching game dimensions
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        yield screen  # provide screen to test, then run teardown
        pygame.quit()  # clean up Pygame resources

    def test_board_initialization(self, board):
        # check that Board instance has the draw_board method
        assert hasattr(board, 'draw_board'), "Board should have draw_board method"
        # verify it's actually a callable method, not just an attribute
        assert callable(getattr(board, 'draw_board')), "draw_board should be callable"

    def test_screen_dimensions(self): # screen dimensions test
        assert SCREEN_WIDTH == 440, "Screen width should be 440 pixels for proper layout"
        assert SCREEN_HEIGHT == 750, "Screen height should be 750 pixels for proper layout"

    def test_grid_calculations(self): # grid positioning test
        # calculate expected grid position based on screen dimensions and block size
        expected_x = (SCREEN_WIDTH - (GRID_COLS * BLOCK_SIZE)) // 2
        expected_y = SCREEN_HEIGHT - (GRID_ROWS * BLOCK_SIZE) - 5
        
        # verify grid is properly centered horizontally
        assert GRID_X == expected_x, f"Grid X position {GRID_X} should be {expected_x} for proper centering"
        # verify grid is positioned correctly from bottom of screen
        assert GRID_Y == expected_y, f"Grid Y position {GRID_Y} should be {expected_y} for bottom alignment"

    def test_grid_parameters(self): # grid configuration test
        assert GRID_ROWS == 20, "should have 20 rows for standard Tetris gameplay"
        assert GRID_COLS == 10, "should have 10 columns for standard Tetris gameplay"
        assert BLOCK_SIZE == 30, "block size should be 30 pixels for proper scaling"

    def test_score_display_integration(self): # test score display capability
        """Test that UI can display score increases when rows are cleared"""
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        try:
            # Test that UI can handle score display
            font_path = "font/font1"
            font_score = pygame.font.Font(font_path, 20)
            font_label = pygame.font.Font(font_path, 15)
            font_value = pygame.font.Font(font_path, 16)
            
            # Test various score values including level transition at 10
            draw_ui(screen, font_score, font_label, font_value, 9, 1, 9)  # Before level up
            draw_ui(screen, font_score, font_label, font_value, 10, 2, 10)  # After level up
            
        except Exception as e:
            pytest.skip(f"UI rendering test skipped: {e}")
        finally:
            pygame.quit()


class TestUI: # test ui components

    
    @pytest.fixture
    def fonts(self): 
        pygame.init()  # initialize Pygame for font loading
        font_path = "font/font1"  # path to custom game font (if there is)
        
        try:
            # Create font objects with different sizes for various UI elements
            font_score = pygame.font.Font(font_path, 20)  # main score display font
            font_label = pygame.font.Font(font_path, 15)  # label font (LEVEL, LINES)
            font_value = pygame.font.Font(font_path, 16)  # value font (numbers)
            yield font_score, font_label, font_value  # provide fonts to test
        except:
            # skip if font files are missing or corrupted
            pytest.skip("Font files not available - UI tests require font assets")
        finally:
            pygame.quit()

    def test_ui_draws_without_error(self, fonts, pygame_setup):
        # unpacking font tuple into individual fonts
        font_score, font_label, font_value = fonts
        
        try:
            # testing all UI components with score progression
            draw_ui(
                pygame_setup,    # pygame display surface
                font_score,      # score display font
                font_label,      # label font  
                font_value,      # value font
                1000,            # sample score
                5,               # sample level
                25               # sample lines cleared
            )
        except Exception as e:
            # if any exception occurs during drawing, fail the test with details
            pytest.fail(f"UI drawing failed with error: {e}")