# filename: test_board.py
import unittest
import pygame
from board import Board, draw_ui  # عدلي اسم الملف هنا

class TestBoardNew(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # نبدأ pygame مرة واحدة لكل الاختبارات
        pygame.init()
        pygame.font.init()
        # نعمل mock للشاشة بدل فتح نافذة فعلية
        cls.screen = pygame.Surface((440, 750))  # أو أي مقاسات مناسبة للشاشة

        # Fonts dummy
        cls.font_score = pygame.font.Font(None, 20)
        cls.font_label = pygame.font.Font(None, 15)
        cls.font_value = pygame.font.Font(None, 16)

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_board_instance(self):
        """Test if Board instance can be created without constructor"""
        board = Board()
        self.assertIsInstance(board, Board)

    def test_draw_board_runs(self):
        """Test draw_board runs without error"""
        board = Board()
        try:
            board.draw_board(self.screen)
        except Exception as e:
            self.fail(f"draw_board raised an exception: {e}")

    def test_draw_ui_runs(self):
        """Test draw_ui runs without error"""
        score = 0
        level = 1
        lines = 0
        try:
            draw_ui(self.screen, self.font_score, self.font_label, self.font_value, score, level, lines)
        except Exception as e:
            self.fail(f"draw_ui raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()