import unittest
from unittest.mock import patch, MagicMock
import pygame
from game import draw_mini_shape
from shapes import Shape

pygame.init()


class TestDrawMiniShape(unittest.TestCase):

    def setUp(self):
        self.screen = pygame.Surface((200, 200))
        # Rect to render inside
        self.rect = pygame.Rect(50, 50, 100, 100)

        # Dummy 2x2 shape
        self.shape = Shape(
            x=0,
            y=0,
            color=(255, 0, 0),
            blocks=[(0, 0), (1, 0), (0, 1), (1, 1)]
        )

    #Test1:If shape is None => should NOT crash and should NOT draw ----
    @patch("pygame.draw.rect")
    def test_draw_mini_shape_none(self, mock_draw):
        draw_mini_shape(self.screen, None, self.rect)
        mock_draw.assert_not_called()

    #Test2:Valid shape => pygame.draw.rect should be called 2 times per block
    @patch("pygame.draw.rect")
    def test_draw_mini_shape_draws(self, mock_draw):
        draw_mini_shape(self.screen, self.shape, self.rect)

        self.assertEqual(mock_draw.call_count, 8)

    #Test :Ensure function handles scaling correctly without crashing
    @patch("pygame.draw.rect")
    def test_draw_mini_shape_scaling(self, mock_draw):
        # Make a large shape to force scaling logic
        big_shape = Shape(
            x=0,
            y=0,
            color=(0, 255, 0),
            blocks=[(x, y) for x in range(5) for y in range(5)] 
        )

        draw_mini_shape(self.screen, big_shape, self.rect)

        # Should still draw all blocks
        self.assertEqual(mock_draw.call_count, 50)


if __name__ == "__main__":
    unittest.main()
    

