import pygame

SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750

BLOCK_SIZE = 30
GRID_ROWS = 20
GRID_COLS = 10

GRID_X = (SCREEN_WIDTH - (GRID_COLS * BLOCK_SIZE)) // 2
GRID_Y = SCREEN_HEIGHT - (GRID_ROWS * BLOCK_SIZE) - 5

BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
WHITE = (255, 255, 255)

BACKGROUND_COLOR = BLACK
GRID_COLOR = GRAY

class Board:
    def draw_board(self, screen):
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                x = GRID_X + c * BLOCK_SIZE
                y = GRID_Y + r * BLOCK_SIZE
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)
        
        border_x = GRID_X - 1
        border_y = GRID_Y - 1
        border_width = GRID_COLS * BLOCK_SIZE + 4
        border_height = GRID_ROWS * BLOCK_SIZE + 2
        pygame.draw.rect(screen, WHITE, (border_x, border_y, border_width, border_height), 1)

def draw_ui(screen, font_score, font_label, font_value, score, level, lines):
    # نفس الكود اللي عندك هنا
    # رسم score, level, lines, hold, next
    pass  # خلي الكود هنا بدون أي loop أو display.set_mode
