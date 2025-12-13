import pygame

# ---------------- Screen Settings ----------------

SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750

BLOCK_SIZE = 30
GRID_ROWS = 20
GRID_COLS = 10

GRID_X = (SCREEN_WIDTH - (GRID_COLS * BLOCK_SIZE)) // 2
GRID_Y = SCREEN_HEIGHT - (GRID_ROWS * BLOCK_SIZE) - 5

# ---------------- Colors ----------------

BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
WHITE = (255, 255, 255)


##
# @class Board
# @brief Represents the game board grid.
##
class Board:
    ##
    # @brief Initializes the board grid.
    ##
    def __init__(self):
        self.grid = [[(0,0,0) for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

    ##
    # @brief Draws the game board and borders.
    #
    # @param screen Pygame screen surface.
    ##
    def draw_board(self, screen):
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                x = GRID_X + c * BLOCK_SIZE
                y = GRID_Y + r * BLOCK_SIZE
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, GRAY, rect, 1)

        border_x = GRID_X - 1
        border_y = GRID_Y - 1
        border_width = GRID_COLS * BLOCK_SIZE + 4
        border_height = GRID_ROWS * BLOCK_SIZE + 2
        pygame.draw.rect(screen, WHITE, (border_x, border_y, border_width, border_height), 1)


##
# @brief Draws UI elements such as score, level, next and hold boxes.
#
# @param screen Pygame screen surface.
# @param font_score Font for score text.
# @param font_label Font for labels.
# @param font_value Font for values.
# @param score Current score.
# @param level Current level.
# @param lines Number of cleared lines.
#
# @return Rectangles of hold box, next box, and pause icon.
##
def draw_ui(screen, font_score, font_label, font_value, score, level, lines):

    score_box_rect = pygame.Rect(130, 15, 180, 35)
    pygame.draw.rect(screen, WHITE, score_box_rect, 2, border_radius=8)

    score_text = font_score.render(f"SCORE: {score}", True, WHITE)
    screen.blit(score_text, score_text.get_rect(center=score_box_rect.center))

    pause_icon = pygame.image.load("images/pause_icon.png")
    pause_icon = pygame.transform.scale(pause_icon, (35, 35))
    pause_rect = pause_icon.get_rect(center=(400, 35))
    screen.blit(pause_icon, pause_rect)

    labels_y = 80
    values_y = 105

    level_label = font_label.render("LEVEL", True, WHITE)
    screen.blit(level_label, (GRID_X - 40, labels_y))
    screen.blit(font_value.render(str(level), True, WHITE), (GRID_X - 35, values_y))

    lines_label = font_label.render("LINES", True, WHITE)
    screen.blit(lines_label, (GRID_X + 30, labels_y))
    screen.blit(font_value.render(str(lines), True, WHITE), (GRID_X + 35, values_y))

    next_box_rect = pygame.Rect(GRID_X + 160, values_y - 10, 120, 40)
    pygame.draw.rect(screen, WHITE, next_box_rect, 1, border_radius=5)

    hold_box_rect = pygame.Rect(GRID_X + 70, values_y - 10, 75, 40)
    pygame.draw.rect(screen, WHITE, hold_box_rect, 1, border_radius=5)

    return hold_box_rect, next_box_rect, pause_rect