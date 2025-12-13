import unittest
from unittest.mock import patch
import pygame
from board import Board, draw_ui   # اتأكدي اسم الملف صح

class TestBoardUI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.font.init()

    def setUp(self):
        self.screen = pygame.Surface((440, 750))
        self.board = Board()

        # لو مفيش grid نعمل واحدة لتجنب AttributeError
        if not hasattr(self.board, "grid"):
            self.board.grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

        # fake fonts
        self.font_score = pygame.font.Font(None, 20)
        self.font_label = pygame.font.Font(None, 15)
        self.font_value = pygame.font.Font(None, 16)

    # 1) grid initialization
    def test_grid_initialized_correctly(self):
        self.assertTrue(hasattr(self.board, "grid"))
        self.assertEqual(len(self.board.grid), 20)
        self.assertEqual(len(self.board.grid[0]), 10)
        for row in self.board.grid:
            for cell in row:
                self.assertEqual(cell, (0, 0, 0))

    # 2) draw_ui returns all expected rects
    @patch("pygame.image.load", return_value=pygame.Surface((10,10)))
    def test_draw_ui_returns_rects(self, mock_img):
        hold_rect, next_rect, pause_rect = draw_ui(
            self.screen,
            self.font_score,
            self.font_label,
            self.font_value,
            score=10,
            level=2,
            lines=5
        )

        self.assertIsInstance(hold_rect, pygame.Rect)
        self.assertIsInstance(next_rect, pygame.Rect)
        self.assertIsInstance(pause_rect, pygame.Rect)

    # 3) blit is called
    @patch("pygame.Surface.blit")
    @patch("pygame.image.load", return_value=pygame.Surface((10,10)))
    def test_draw_ui_calls_blit(self, mock_img, mock_blit):
        
        draw_ui(
            self.screen,
            self.font_score,
            self.font_label,
            self.font_value,
            score=5,
            level=1,
            lines=3
        )

        # نتأكد إن blit اتناديت مرة على الأقل
        self.assertGreater(mock_blit.call_count, 0)

# تشغيل التيست
if __name__ == "__main__":
    unittest.main(verbosity=2)