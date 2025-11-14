import pygame
import sys
import time
from shapes import Bag, create_shape, Shape
from board import Board, GRID_X, GRID_Y


SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200,50,50)
font_path = "font/Audiowide-Regular.ttf"


# scoring by lines cleared at once
SCORE_TABLE = {1:100, 2:300, 3:500, 4:800}


# fallback speed by level (ms per cell drop)
def level_speed(level):
# Simple mapping, can be tuned
return max(50, 800 - (level-1)*40)




def draw_side_info(screen, score, level, lines, next_shape, hold_shape, fonts):
font_score, font_label, font_value = fonts
# Score box
score_box_width = 180
score_box_height = 35
score_box_x = (SCREEN_WIDTH - score_box_width) // 2
score_box_y = 15
score_box_rect = pygame.Rect(score_box_x, score_box_y, score_box_width, score_box_height)
pygame.draw.rect(screen, WHITE, score_box_rect, 2, border_radius=8)
score_text_surf = font_score.render(f"SCORE: {score}", True, WHITE)
score_text_rect = score_text_surf.get_rect(center=score_box_rect.center)
screen.blit(score_text_surf, score_text_rect)


# Level/Lines
labels_y = 80
values_y = 105
level_x = GRID_X - 40
level_label = font_label.render("LEVEL", True, WHITE)
level_value = font_value.render(str(level), True, WHITE)
screen.blit(level_label, (level_x, labels_y))
screen.blit(level_value, (level_x + (level_label.get_width() - level_value.get_width()) // 2, values_y))


lines_x = GRID_X + 30
lines_label = font_label.render("LINES", True, WHITE)
lines_value = font_value.render(str(lines), True, WHITE)
screen.blit(lines_label, (lines_x, labels_y))
screen.blit(lines_value, (lines_x + (lines_label.get_width() - lines_value.get_width()) // 2, values_y))


# Next box (simple preview)
grid_right = GRID_X + 10*30
next_box_width = 120
next_box_x = grid_right - next_box_width - 5
next_label = font_label.render("NEXT", True, WHITE)
next_label_x = next_box_x + 17 + (next_box_width - next_label.get_width()) // 2
screen.blit(hold_label, (hold_labe
