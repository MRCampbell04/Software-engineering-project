import unittest
import pygame
from home import Button, show_home, SCREEN_WIDTH, SCREEN_HEIGHT

# -------------------- BUTTON TESTS --------------------
class TestButton(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize pygame once for all tests
        pygame.init()
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.font.init()
        cls.screen = pygame.display.get_surface()

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


# -------------------- HOME SCREEN TESTS --------------------
class TestShowHome(unittest.TestCase):

    def setUp(self):
        # Re-initialize display before each test to avoid "video system not initialized"
        pygame.display.init()
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.font.init()
        self.screen = pygame.display.get_surface()
        pygame.event.clear()

    def test_show_home_quit_event(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        with self.assertRaises(SystemExit):
            show_home(self.screen)

    def test_show_home_start_button(self):
        start_btn = Button("Start Game", 320)
        click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=start_btn.rect.center, button=1)
        pygame.event.post(click_event)

        try:
            show_home(self.screen)
        except SystemExit:
            self.fail("show_home exited entire program instead of just breaking loop")


# -------------------- CLEANUP --------------------
    @classmethod
    def tearDownClass(cls):
        pygame.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
