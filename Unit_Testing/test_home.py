import unittest
import pygame
from unittest.mock import patch, MagicMock
import sys

# Import the module to be tested
import home
from home import Button, SCREEN_WIDTH, WHITE, BLACK, show_menu, draw_ui, game_loop

pygame.init()

# Fake screen for testing
SCREEN_HEIGHT = 750
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
font_default = pygame.font.Font(None, 32)
font_small = pygame.font.Font(None, 16)

class TestHome(unittest.TestCase):
    def setUp(self):
        self.screen = screen
        self.font = font_default

    ## ----------------------------------------------------
    ## 🎯 Button Class Tests (Covers __init__, draw, is_clicked)
    ## ----------------------------------------------------

    def test_button_draw_all_states(self):
        """Tests all four combinations of filled/outline and hovered/not-hovered."""
        btn_filled_outline = Button("States", 100, filled=False, hover_color=(200, 200, 200))
        btn_filled = Button("Filled", 150, filled=True, hover_color=(50, 50, 50))
        
        # 1. Hover Outside (Not Hovered) - Hits the 'current_color = self.color' path
        pygame.mouse.set_pos((0, 0))
        btn_filled_outline.draw(self.screen, self.font)
        btn_filled.draw(self.screen, self.font)
        
        # 2. Hover Inside (Hovered) - Hits the 'current_color = self.hover_color' path
        pygame.mouse.set_pos(btn_filled.rect.center)
        btn_filled_outline.draw(self.screen, self.font) # Outline + Hovered branch
        btn_filled.draw(self.screen, self.font)        # Filled + Hovered branch

    def test_button_init_hover_color_none(self):
        """Tests the branch where hover_color is None in __init__ (self.hover_color = hover_color or color)."""
        btn = Button("DefaultHover", 200, color=WHITE, hover_color=None)
        self.assertEqual(btn.hover_color, WHITE)

    def test_button_click_detection_all_cases(self):
        """Tests all branches of the is_clicked method."""
        btn = Button("ClickMe", 250)
        
        # 1. Successful Click (True)
        event_on = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=btn.rect.center)
        self.assertTrue(btn.is_clicked(event_on))
        
        # 2. Click off button (False collision)
        event_off = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(0,0))
        self.assertFalse(btn.is_clicked(event_off))
        
        # 3. Wrong button (False button)
        event_right_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=3, pos=btn.rect.center)
        self.assertFalse(btn.is_clicked(event_right_click))
        
        # 4. Wrong event type (False event type)
        event_up = pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=btn.rect.center)
        self.assertFalse(btn.is_clicked(event_up))

    ## ----------------------------------------------------
    ##  draw_ui Test
    ## ----------------------------------------------------

    def test_draw_ui_runs(self):
        """Ensures draw_ui executes all rendering paths without crashing."""
        draw_ui(self.screen, font_small, font_small, font_small, score=9999, level=10, lines=100)

    ## ----------------------------------------------------
    ##  show_menu Tests (Covers start, exit, and QUIT events)
    ## ----------------------------------------------------

    @patch("home.game_loop")
    @patch("pygame.event.get")
    def test_show_menu_start_exit_quit(self, mock_events, mock_game_loop):
        """Tests all control flow paths in show_menu: Start Game, Exit button, and pygame.QUIT."""
        
        # Events are consumed by the loop, so we provide the sequence:
        # 1. Click Start Game (Triggers game_loop)
        # 2. Pygame QUIT (Triggers SystemExit in menu loop)
        # 3. Click Exit button (Triggers SystemExit directly)
        
        start_pos = (SCREEN_WIDTH//2, 320 + 25) # Approximate center of Start Game button
        exit_pos = (SCREEN_WIDTH//2, 480 + 25)  # Approximate center of Exit button

        # SEQUENCE 1: Start Game click (should call game_loop then exit the menu)
        mock_events.side_effect = [[
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=start_pos)
        ], [
            pygame.event.Event(pygame.QUIT) # Quit to break the second menu loop run
        ]]
        mock_game_loop.side_effect = lambda screen: None # Game loop runs, returns to menu
        
        with self.assertRaises(SystemExit):
            show_menu(self.screen) # Runs until the second [pygame.QUIT] event

        mock_game_loop.assert_called_once()
        
        # SEQUENCE 2: Pygame QUIT event (should exit immediately)
        mock_events.side_effect = [[pygame.event.Event(pygame.QUIT)]]
        with self.assertRaises(SystemExit):
            show_menu(self.screen)

        # SEQUENCE 3: Exit Button click (should exit immediately)
        mock_events.side_effect = [[
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=exit_pos)
        ]]
        with self.assertRaises(SystemExit):
            show_menu(self.screen)
        
    ## ----------------------------------------------------
    ## 🎮 game_loop Test (Covers initial exit path)
    ## ----------------------------------------------------
    
    @patch("pygame.event.get")
    @patch("pygame.key.get_pressed", return_value=[0]*300)
    @patch("pygame.time.Clock")
    def test_game_loop_quit_event(self, mock_clock, mock_keys, mock_events):
        """Tests the immediate pygame.QUIT handler inside the game_loop."""
        # 1. Simulate QUIT to exit immediately
        mock_events.return_value = [pygame.event.Event(pygame.QUIT)]
        
        with self.assertRaises(SystemExit):
            game_loop(self.screen)
            
    ## ----------------------------------------------------
    ## 🖼️ Icon Loading Failure (To hit the try...except block)
    ## ----------------------------------------------------
    
    @patch("home.pygame.image.load", side_effect=pygame.error("Mock Load Error"))
    @patch("home.pygame.transform.scale")
    @patch("home.pygame.display.set_icon")
    @patch("home.pygame.display.set_mode")
    @patch("home.pygame.display.set_caption")
    @patch("home.pygame.font.Font", side_effect=lambda x, y: MagicMock())
    @patch("home.show_menu", side_effect=SystemExit) # Prevent infinite menu loop
    def test_image_loading_exception_path(self, mock_menu, mock_font, mock_caption, mock_mode, mock_icon, mock_scale, mock_load):
        """Forces the image loading to fail (except block), covering lines 43-52 in home.py."""
        
        # The main code block of home.py runs upon import. We need to reload it 
        # while the mock is active to force the exception path.
        with patch.object(home, 'red_icon', None, create=True) as mock_red, \
             patch.object(home, 'blue_icon', None, create=True) as mock_blue:
            try:
                importlib.reload(home)
            except SystemExit:
                pass
            
            # The test confirms the path was hit if no hard crash occurs (which our mocks prevent)
            mock_load.assert_called_with("images/red.png") 

# Required to run the reload test
import importlib 

if __name__ == "__main__":
    unittest.main(verbosity=2)