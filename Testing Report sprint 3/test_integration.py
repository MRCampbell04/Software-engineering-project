import pytest
import pygame
import json
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Import game modules
from shapes import Shape, create_shape, Board as ShapesBoard, BOARD_WIDTH, BOARD_HEIGHT
from board import Board as UIBoard
from game import can_move, place_shape, clear_full_rows, draw_mini_shape
from Login import LoginScreen
from AboutUs import AboutUsScreen
from Leaderboard import LeaderboardScreen


class TestShapeBoardIntegration:
    """Test integration between Shape class and Board class"""

    @pytest.fixture
    def board(self):
        return ShapesBoard()

    @pytest.fixture
    def shape(self):
        return create_shape()

    def test_shape_placement_on_board(self, board, shape):
        """Test that shapes can be placed on the board correctly"""
        # Move shape to bottom
        shape.y = BOARD_HEIGHT - 1

        # Place shape
        board.place(shape)

        # Verify shape blocks are on board
        shape_coords = shape.get_coords()
        for x, y in shape_coords:
            if 0 <= y < BOARD_HEIGHT and 0 <= x < BOARD_WIDTH:
                assert board.grid[y][x] == shape.color

    def test_shape_movement_validation(self, board):
        """Test that board correctly validates shape movements"""
        shape = create_shape()

        # Valid position
        assert board.can_move(shape) == True

        # Move shape out of bounds (left)
        shape.x = -5
        assert board.can_move(shape) == False

        # Move shape out of bounds (right)
        shape.x = BOARD_WIDTH + 5
        assert board.can_move(shape) == False

        # Move shape out of bounds (bottom)
        shape.y = BOARD_HEIGHT + 5
        assert board.can_move(shape) == False

    def test_line_clearing_with_score(self, board):
        """Test that clearing lines updates score correctly"""
        initial_score = board.score

        # Fill a complete row
        for col in range(BOARD_WIDTH):
            board.grid[BOARD_HEIGHT - 1][col] = (255, 255, 255)

        # Clear lines
        board.clear_lines()

        # Verify score increased
        assert board.score == initial_score + 1

        # Verify row is cleared
        assert all(cell == (0, 0, 0) for cell in board.grid[BOARD_HEIGHT - 1])

    def test_multiple_line_clearing(self, board):
        """Test clearing multiple lines at once"""
        # Fill three complete rows
        for row in range(BOARD_HEIGHT - 3, BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                board.grid[row][col] = (255, 0, 0)

        initial_score = board.score
        board.clear_lines()

        # Score should increase by 3
        assert board.score == initial_score + 3

    def test_shape_collision_detection(self, board):
        """Test that shapes collide with placed blocks"""
        # Place a block at the bottom
        board.grid[BOARD_HEIGHT - 1][5] = (255, 0, 0)

        # Create shape above it
        shape = Shape(5, BOARD_HEIGHT - 2, (0, 255, 0), [(0, 0)])

        # Should be able to move
        assert board.can_move(shape) == True

        # Move down - should collide
        shape.move_down()
        assert board.can_move(shape) == False


class TestGameLogicIntegration:
    """Test integration of game logic functions"""

    @pytest.fixture
    def empty_grid(self):
        return [[(0, 0, 0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    def test_can_move_with_grid(self, empty_grid):
        """Test movement validation with game grid"""
        shape = create_shape()

        # Valid position
        assert can_move(empty_grid, shape) == True

        # Block the position
        coords = shape.get_coords()
        if coords:
            x, y = coords[0]
            if 0 <= y < BOARD_HEIGHT and 0 <= x < BOARD_WIDTH:
                empty_grid[y][x] = (255, 0, 0)
                assert can_move(empty_grid, shape) == False

    def test_place_and_clear_integration(self, empty_grid):
        """Test placing shapes and clearing rows together"""
        # Create shapes to fill a row
        for col in range(BOARD_WIDTH):
            shape = Shape(col, BOARD_HEIGHT - 1, (255, 0, 0), [(0, 0)])
            place_shape(empty_grid, shape)

        # Verify row is filled
        assert all(cell != (0, 0, 0) for cell in empty_grid[BOARD_HEIGHT - 1])

        # Clear rows
        new_grid, cleared = clear_full_rows(empty_grid)

        # Verify one row was cleared
        assert cleared == 1

        # Verify new bottom row is empty
        assert all(cell == (0, 0, 0) for cell in new_grid[BOARD_HEIGHT - 1])

    def test_shape_rotation_and_placement(self, empty_grid):
        """Test rotating a shape and placing it"""
        shape = create_shape()
        original_blocks = shape.blocks[:]

        # Rotate shape
        shape.blocks = [(-by, bx) for bx, by in shape.blocks]

        # Should still be valid
        assert can_move(empty_grid, shape) == True

        # Place rotated shape
        place_shape(empty_grid, shape)

        # Verify blocks are placed
        coords = shape.get_coords()
        placed_count = sum(1 for x, y in coords
                           if 0 <= y < BOARD_HEIGHT and 0 <= x < BOARD_WIDTH
                           and empty_grid[y][x] != (0, 0, 0))
        assert placed_count > 0


class TestUIIntegration:
    """Test integration between UI components"""

    @pytest.fixture
    def screen(self):
        pygame.init()
        return pygame.display.set_mode((440, 750))

    def test_login_to_game_flow(self, screen):
        """Test login screen integration with game flow"""
        login = LoginScreen(screen)

        # Simulate user input
        login.user_text = "TestPlayer"
        login.continue_pressed = True

        # Verify state
        assert login.user_text == "TestPlayer"
        assert login.continue_pressed == True

    def test_leaderboard_data_persistence(self, screen):
        """Test leaderboard saves and loads scores correctly"""
        leaderboard = LeaderboardScreen(screen)

        # Clean test file
        test_file = "test_leaderboard.json"
        leaderboard.file_name = test_file

        try:
            # Save score
            leaderboard.save_score("Player1", 1000)
            leaderboard.save_score("Player2", 1500)
            leaderboard.save_score("Player3", 500)

            # Reload
            leaderboard.scores = leaderboard.load_scores()

            # Verify scores are sorted
            assert len(leaderboard.scores) == 3
            assert leaderboard.scores[0]['score'] == 1500
            assert leaderboard.scores[1]['score'] == 1000
            assert leaderboard.scores[2]['score'] == 500

        finally:
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_aboutus_navigation(self, screen):
        """Test About Us screen navigation"""
        about = AboutUsScreen(screen)

        # Simulate back button press
        mock_event = Mock()
        mock_event.type = pygame.MOUSEBUTTONDOWN
        mock_event.pos = about.back_rect.center

        about.handle_event(mock_event)

        assert about.back_pressed == True

    def test_board_ui_integration(self, screen):
        """Test board drawing with UI elements"""
        board = UIBoard()

        # Verify grid initialization
        assert len(board.grid) == 20  # GRID_ROWS
        assert len(board.grid[0]) == 10  # GRID_COLS

        # Test drawing (shouldn't raise errors)
        try:
            board.draw_board(screen)
            success = True
        except Exception as e:
            success = False
            print(f"Drawing failed: {e}")

        assert success == True


class TestEndToEndScenarios:
    """Test complete game scenarios"""

    @pytest.fixture
    def game_state(self):
        pygame.init()
        screen = pygame.display.set_mode((440, 750))
        board = ShapesBoard()
        shape = create_shape()
        return {
            'screen': screen,
            'board': board,
            'shape': shape,
            'grid': [[(0, 0, 0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        }

    def test_complete_game_cycle(self, game_state):
        """Test a complete game cycle: spawn, move, place, clear"""
        board = game_state['board']
        shape = game_state['shape']
        grid = game_state['grid']

        # 1. Spawn shape
        assert shape is not None

        # 2. Move shape down
        original_y = shape.y
        shape.move_down()
        assert shape.y == original_y + 1

        # 3. Move to bottom
        while can_move(grid, shape):
            shape.move_down()
        shape.y -= 1  # Step back to valid position

        # 4. Place shape
        place_shape(grid, shape)

        # 5. Verify placement
        coords = shape.get_coords()
        placed = False
        for x, y in coords:
            if 0 <= y < BOARD_HEIGHT and 0 <= x < BOARD_WIDTH:
                if grid[y][x] != (0, 0, 0):
                    placed = True
                    break

        assert placed == True

    def test_game_over_scenario(self, game_state):
        """Test game over condition"""
        grid = game_state['grid']

        # Fill top rows
        for row in range(3):
            for col in range(BOARD_WIDTH):
                grid[row][col] = (255, 0, 0)

        # Try to spawn new shape
        new_shape = create_shape()
        new_shape.y = 0

        # Should not be able to move (game over)
        game_over = not can_move(grid, new_shape)

        assert game_over == True

    def test_scoring_system_integration(self, game_state):
        """Test complete scoring system"""
        board = game_state['board']
        grid = game_state['grid']

        initial_score = board.score
        initial_level = board.level

        # Fill and clear one line
        for col in range(BOARD_WIDTH):
            grid[BOARD_HEIGHT - 1][col] = (255, 0, 0)

        new_grid, cleared = clear_full_rows(grid)

        # Update board with cleared lines (simulating game logic)
        board.grid = new_grid
        board.score += cleared
        board.level = 1 + (board.score // 10)

        assert board.score == initial_score + 1

        # Fill and clear 10 more lines to test level up
        for _ in range(10):
            for col in range(BOARD_WIDTH):
                board.grid[BOARD_HEIGHT - 1][col] = (255, 0, 0)
            board.clear_lines()

        # Level should have increased
        assert board.level > initial_level


class TestDataFlowIntegration:
    """Test data flow between components"""

    def test_leaderboard_game_integration(self):
        """Test game score flows to leaderboard correctly"""
        pygame.init()
        screen = pygame.display.set_mode((440, 750))

        leaderboard = LeaderboardScreen(screen)
        test_file = "test_integration_leaderboard.json"
        leaderboard.file_name = test_file

        try:
            # Simulate game ending with score
            player_name = "IntegrationTest"
            final_score = 2500

            # Save to leaderboard
            leaderboard.save_score(player_name, final_score)

            # Verify it's saved and sorted correctly
            leaderboard.scores = leaderboard.load_scores()

            found = False
            for entry in leaderboard.scores:
                if entry['name'] == player_name and entry['score'] == final_score:
                    found = True
                    break

            assert found == True

        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_login_to_leaderboard_flow(self):
        """Test player name flows from login to leaderboard"""
        pygame.init()
        screen = pygame.display.set_mode((440, 750))

        # Login phase
        login = LoginScreen(screen)
        login.user_text = "FlowTestPlayer"
        player_name = login.user_text

        # Game phase (simulated)
        score = 3000

        # Leaderboard phase
        leaderboard = LeaderboardScreen(screen)
        test_file = "test_flow_leaderboard.json"
        leaderboard.file_name = test_file

        try:
            leaderboard.save_score(player_name, score)
            leaderboard.scores = leaderboard.load_scores()

            # Verify player appears in leaderboard
            player_entry = next(
                (entry for entry in leaderboard.scores
                 if entry['name'] == player_name and entry['score'] == score),
                None
            )

            assert player_entry is not None
            assert player_entry['name'] == "FlowTestPlayer"
            assert player_entry['score'] == 3000

        finally:
            if os.path.exists(test_file):
                os.remove(test_file)


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
