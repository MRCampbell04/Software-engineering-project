# test_login.py
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import unittest
from Login import LoginScreen   # ← اسم الملف والكلاس الصح

class TestLogin(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((440, 750))
        self.login = LoginScreen(self.screen)

    def tearDown(self):
        pygame.quit()

    # -------------------------------
    # Test 1: initial values
    # -------------------------------
    def test_initial_state(self):
        self.assertEqual(self.login.user_text, "")
        self.assertTrue(self.login.is_active)
        self.assertFalse(self.login.continue_pressed)

    # -------------------------------
    # Test 2: typing text
    # -------------------------------
    def test_typing_text(self):
        event = pygame.event.Event(pygame.KEYDOWN, {"unicode": "A", "key": pygame.K_a})
        self.login.handle_event(event)
        self.assertEqual(self.login.user_text, "A")

    # -------------------------------
    # Test 3: backspace works
    # -------------------------------
    def test_backspace(self):
        self.login.user_text = "ABC"
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_BACKSPACE})
        self.login.handle_event(event)
        self.assertEqual(self.login.user_text, "AB")


# -------------------------------
# Run unittest مباشرة من Spyder
# -------------------------------
if __name__ == "__main__":
    unittest.main()
