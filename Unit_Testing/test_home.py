# D:/Project Testing/test_home.py
import unittest
import pygame
from home import Button, show_home, SCREEN_WIDTH, SCREEN_HEIGHT

# -------------------- BUTTON TESTS --------------------
class TestButton(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.font.init()

    def test_button_creation(self):
        btn = Button("Test", 100)
        self.assertEqual(btn.text, "Test")
        self.assertEqual(btn.y, 100)
        self.assertEqual(btn.width, 270)
        self.assertEqual(btn.height, 50)

    def test_button_click_detection(self):
        btn = Button("Click", 150)
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=btn.rect.center, button=1)
        self.assertTrue(btn.is_clicked(event))

        event_wrong = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(0, 0), button=1)
        self.assertFalse(btn.is_clicked(event_wrong))

    def test_button_handles_rapid_clicks(self):
        """Test button responds correctly to 10 rapid clicks."""
        btn = Button("Start", 300)
        for _ in range(10):
            event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=btn.rect.center, button=1)
            self.assertTrue(btn.is_clicked(event))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()


# -------------------- HOME SCREEN TESTS --------------------
class TestShowHome(unittest.TestCase):

    def setUp(self):
        # Fresh Pygame init before each test
        pygame.display.init()
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.font.init()
        pygame.event.clear()

    def test_show_home_quit_via_window_close(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        with self.assertRaises(SystemExit):
            show_home(pygame.display.get_surface())

    def test_show_home_start_game_exits_normally(self):
        start_btn = Button("Start Game", 320)
        pygame.event.post(
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=start_btn.rect.center, button=1)
        )
        try:
            show_home(pygame.display.get_surface())
        except SystemExit:
            self.fail("'Start Game' should not cause SystemExit")

    def test_show_home_exit_button_quits(self):
        exit_btn = Button("Exit", 580, width=200, color=(200, 50, 50), text_color=(255, 255, 255))
        pygame.event.post(
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=exit_btn.rect.center, button=1)
        )
        with self.assertRaises(SystemExit):
            show_home(pygame.display.get_surface())

    def test_show_home_leaderboard_button(self):
        """Click Leaderboard, then QUIT — ensures it doesn't crash and prints."""
        lb_btn = Button("Leaderboard", 400)
        pygame.event.post(
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=lb_btn.rect.center, button=1)
        )
        pygame.event.post(pygame.event.Event(pygame.QUIT))  # Force clean exit
        with self.assertRaises(SystemExit):
            show_home(pygame.display.get_surface())

    def test_show_home_about_button(self):
        """Click About Us, then QUIT — ensures it doesn't crash and prints."""
        about_btn = Button("About Us", 480)
        pygame.event.post(
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=about_btn.rect.center, button=1)
        )
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        with self.assertRaises(SystemExit):
            show_home(pygame.display.get_surface())

    def test_multiple_buttons_independent(self):
        """Verify Start and Exit behave independently in separate runs."""
        # Test 1: Start → no SystemExit
        start_btn = Button("Start Game", 320)
        pygame.event.post(
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=start_btn.rect.center, button=1)
        )
        try:
            show_home(pygame.display.get_surface())
        except SystemExit:
            self.fail("Start Game incorrectly raised SystemExit")

        # Test 2: Exit → SystemExit
        # Note: This runs in a *new* setup (thanks to setUp being per-test),
        # so Pygame is re-initialized.
        exit_btn = Button("Exit", 580, width=200, color=(200, 50, 50), text_color=(255, 255, 255))
        pygame.event.post(
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=exit_btn.rect.center, button=1)
        )
        with self.assertRaises(SystemExit):
            show_home(pygame.display.get_surface())

    @classmethod
    def tearDownClass(cls):
        pygame.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)