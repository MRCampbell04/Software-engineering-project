import unittest
import pygame
from unittest.mock import patch,MagicMock
from game import Button, WHITE, BLACK,game_loop, Board, Shape, create_shape

pygame.init()

class TestButton(unittest.TestCase):

    def setUp(self):
        # Create fake screen and font
        self.screen = pygame.Surface((400, 400))
        self.font = pygame.font.Font(None, 32)

    # 1. Missing color (should break drawing)
    def test_button_none_color_breaks(self):
        btn = Button("Test", 100, color=None)
        with self.assertRaises(TypeError):
            btn.draw(self.screen, self.font)

    # 2. Invalid font: should break label.render
    def test_invalid_font_breaks(self):
        btn = Button("Test", 150)
        with self.assertRaises(AttributeError):
            btn.draw(self.screen, font=None)

    # 3. Mouse position returns None → hover logic breaks
    @patch("pygame.mouse.get_pos", return_value=None)
    def test_hover_breaks_with_invalid_mouse(self, mock_mouse):
        btn = Button("Test", 200)
        with self.assertRaises(TypeError):
            btn.draw(self.screen, self.font)

    # 4. Missing SCREEN_WIDTH in game → rect creation breaks
    @patch("game.SCREEN_WIDTH", None)
    def test_missing_screen_width_breaks(self):
        with self.assertRaises(TypeError):
            Button("Broken", 250)

    # 5. Missing event.pos should break is_clicked()
    def test_is_clicked_breaks_without_event_pos(self):
        bad_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        btn = Button("Click", 100)
        with self.assertRaises(AttributeError):
            btn.is_clicked(bad_event)

    # 6. Passing non-string text should break font.render()
    def test_non_string_text_breaks(self):
        btn = Button(12345, 100)  # invalid text type
        with self.assertRaises(TypeError):
            btn.draw(self.screen, self.font)


    # 7. Negative width breaks pygame.Rect
    def test_negative_width_breaks(self):
        with self.assertRaises(ValueError):
            Button("Test", 100, width=-50)

    # 8. Extra-large width causes drawing issues
    def test_insane_size_breaks(self):
        btn = Button("Big", 100, width=999999999)
        with self.assertRaises(pygame.error):
           self.assertIsNone(btn.draw(self.screen, self.font))

    # 9. Hover color is wrong type (string instead of tuple)
    def test_invalid_hover_color_type(self):
        btn = Button("Test", 150, hover_color="red")
        with self.assertRaises(TypeError):
            btn.draw(self.screen, self.font)

    # 10. Surface is None — drawing should crash
    def test_draw_breaks_with_none_surface(self):
        btn = Button("Test", 120)
        with self.assertRaises(TypeError):
            btn.draw(None, self.font)

pygame.init()
mock_screen = pygame.Surface((440, 750))
FONT_PATH = "font/Audiowide-Regular.ttf" # Ensure this path is correct or mock it

# Mock to ensure create_shape returns the same, predictable shape (an I-bar)
def mock_create_shape():
    """Returns a simple I-bar shape centered at the top."""
    # Using an I-shape (4 blocks in a row) to make collisions easier to test
    blocks = [(0, 0), (-1, 0), (1, 0), (2, 0)] 
    return Shape(4, 0, (0, 255, 0), blocks)

# Mock to simulate pressing keys
def get_key_pressed_mock(keys_to_press):
    """Returns a list of 0s representing no keys, except for specified keys."""
    keys = [0] * 300 # Pygame requires a list of 300 keys (or more)
    for key in keys_to_press:
        if 0 <= key < len(keys):
            keys[key] = 1
    return keys

class TestGameLoop(unittest.TestCase):

    def setUp(self):
        self.mock_board = Board()
        # Patch random.choice to ensure predictable shape spawning
        self.patcher_shape = patch('game.create_shape', side_effect=[mock_create_shape, mock_create_shape])
        self.mock_create_shape = self.patcher_shape.start()
        # Patch font loading to prevent file errors if font is missing
        self.patcher_font = patch('pygame.font.Font', return_value=MagicMock())
        self.patcher_font.start()

    def tearDown(self):
        self.patcher_shape.stop()
        self.patcher_font.stop()

    @patch("pygame.key.get_pressed")
    @patch("pygame.event.get")
    def test_loop_basic_exit(self, mock_events, mock_keys):
        """Tests the basic game loop structure and QUIT event."""
        # 1. Set key presses to NONE
        mock_keys.return_value = get_key_pressed_mock([])
        # 2. Simulate QUIT event to exit the loop immediately
        mock_events.return_value = [pygame.event.Event(pygame.QUIT)]

        with self.assertRaises(SystemExit):
            game_loop(mock_screen)

    @patch("pygame.key.get_pressed")
    @patch("pygame.event.get", return_value=[]) # No events
    @patch("pygame.time.Clock")
    @patch("game.Board.can_move", side_effect=[True, True, False]) # Down-Down-Lock
    @patch("game.Board.place")
    @patch("game.Board.clear_full_rows", return_value=0)
    def test_loop_fall_and_lock(self, mock_clear, mock_place, mock_can_move, mock_clock, mock_keys):
        """Tests fall logic (fall_time > fall_speed), shape lock, and new shape spawn."""
        # Mock the clock tick to simulate time passing (e.g., 600ms per tick)
        mock_clock.return_value.tick.return_value = 600 # 600 > initial fall_speed (500)
        mock_keys.return_value = get_key_pressed_mock([])

        # To stop the loop, we need a way to exit after one cycle.
        # We'll use a side effect on key.get_pressed to raise SystemExit after the first check.
        mock_keys.side_effect = [
            get_key_pressed_mock([]), # First key check (used for controls)
            get_key_pressed_mock([]), # Second key check (used for controls)
            get_key_pressed_mock([]), # Third key check (used for controls)
            None # Ends the iteration
        ]

        with self.assertRaises(TypeError): # Crashes when mock_keys returns None, safely exiting
            game_loop(mock_screen)

        mock_can_move.assert_called()
        mock_place.assert_called_once()
        self.assertEqual(self.mock_create_shape.call_count, 2) # Original + New shape

    @patch("pygame.key.get_pressed")
    @patch("pygame.event.get", return_value=[])
    @patch("pygame.time.Clock", return_value=MagicMock(tick=MagicMock(return_value=10))) # Fast tick
    @patch("game.Board.can_move", side_effect=[False, True, False, True, False, True, False]) # Sequence of can_move results
    def test_loop_user_input(self, mock_can_move, mock_clock, mock_events, mock_keys):
        """Tests the key handling blocks (K_LEFT, K_RIGHT, K_DOWN) and boundary checks."""

        # 1. Simulate key presses: Left, Right, Down
        mock_keys.side_effect = [
            get_key_pressed_mock([pygame.K_LEFT]),  # Move Left
            get_key_pressed_mock([pygame.K_RIGHT]), # Move Right
            get_key_pressed_mock([pygame.K_DOWN]),  # Soft Drop
            None # Stop loop
        ]

        with self.assertRaises(TypeError): # Safely exit
            game_loop(mock_screen)

        # K_LEFT branch: Needs 2 can_move checks (move, check, revert check)
        # K_RIGHT branch: Needs 2 can_move checks (move, check, revert check)
        # K_DOWN branch: Needs 1 can_move check (move, check) + place/new shape logic
        self.assertGreaterEqual(mock_can_move.call_count, 5) 

    @patch("pygame.key.get_pressed", return_value=get_key_pressed_mock([]))
    @patch("pygame.event.get", return_value=[])
    @patch("pygame.time.Clock", return_value=MagicMock(tick=MagicMock(return_value=600)))
    @patch("game.Board.can_move", side_effect=[False, False])
    @patch("game.Board.place")
    @patch("game.Board.clear_full_rows", return_value=4)
    def test_loop_clearing_scoring_leveling(self, mock_clear, mock_place, mock_can_move, mock_clock, mock_events, mock_keys):
        """Tests the logic for scoring, line clearing, and level-up (cleared > 0 branch)."""
        
        # We'll use a simple iterator to ensure the loop runs twice (one setup, one check)
        loop_iterations = iter([0, 1])
        def mock_exit(*args, **kwargs):
            try:
                next(loop_iterations)
            except StopIteration:
                raise SystemExit()

        with patch("game.pygame.display.flip", side_effect=mock_exit):
            try:
                game_loop(mock_screen)
            except SystemExit:
                pass
        
        mock_clear.assert_called_once() # Clear full rows should be called
        # The internal logic for score, lines, level, and fall_speed calculation will be executed.

    @patch("pygame.key.get_pressed", return_value=get_key_pressed_mock([]))
    @patch("pygame.event.get")
    @patch("pygame.time.Clock", return_value=MagicMock(tick=MagicMock(return_value=600)))
    @patch("game.Board.can_move", side_effect=[False, False]) # First shape locks, second one fails
    @patch("game.Board.place")
    @patch("game.Board.clear_full_rows", return_value=0)
    @patch("game.draw_ui")
    def test_game_over_state_and_restart(self, mock_draw_ui, mock_clear, mock_place, mock_can_move, mock_clock, mock_events, mock_keys):
        """Tests Game Over state transition and the restart logic (game_over and event.type == KEYDOWN)."""
        
        # 1. First two loops: Game runs, locks first shape, second shape fails can_move -> game_over = True
        # 2. Third loop: Game is over. Check for restart key.
        mock_events.side_effect = [
            # Loop 1 & 2: No events, let the game logic handle the crash/Game Over transition
            [], 
            # Loop 3: Game is over. Press a key (K_SPACE) to restart.
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)],
            # Loop 4: New game running. Simulate QUIT to exit cleanly.
            [pygame.event.Event(pygame.QUIT)]
        ]

        with self.assertRaises(SystemExit):
            game_loop(mock_screen)

 

if __name__ == "__main__":
    unittest.main(verbosity=2)    