import pygame
import sys

from home import show_menu       # <-- مهم جداً
from board import Board, GRID_X, GRID_Y, BLOCK_SIZE, GRID_COLS, GRID_ROWS, BACKGROUND_COLOR, WHITE, BLACK
from shapes import create_shape

SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750
EMPTY = (0, 0, 0)

def make_empty_grid():
    return [[EMPTY for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

def can_move(grid, shape):
    for x, y in shape.get_coords():
        if x < 0 or x >= GRID_COLS or y >= GRID_ROWS:
            return False
        if y >= 0 and grid[y][x] != EMPTY:
            return False
    return True

def place_shape(grid, shape):
    for x, y in shape.get_coords():
        if 0 <= y < GRID_ROWS and 0 <= x < GRID_COLS:
            grid[y][x] = shape.color

def clear_full_rows(grid):
    new_grid = [row for row in grid if any(cell == EMPTY for cell in row)]
    cleared = GRID_ROWS - len(new_grid)
    for _ in range(cleared):
        new_grid.insert(0, [EMPTY for _ in range(GRID_COLS)])
    return new_grid, cleared

def draw_fixed_blocks(screen, grid):
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            if grid[r][c] != EMPTY:
                rect = pygame.Rect(GRID_X + c * BLOCK_SIZE, GRID_Y + r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, grid[r][c], rect)

def draw_shape(screen, shape):
    for x, y in shape.get_coords():
        if 0 <= y < GRID_ROWS and 0 <= x < GRID_COLS:
            rect = pygame.Rect(GRID_X + x * BLOCK_SIZE, GRID_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, shape.color, rect)

def game_loop(screen):
    clock = pygame.time.Clock()

    grid = make_empty_grid()
    current = create_shape()
    next_shape = create_shape()

    fall_time = 0
    fall_speed = 500

    score = 0
    lines = 0
    level = 1
    game_over = False

    font = pygame.font.SysFont(None, 24)

    while True:
        dt = clock.tick(60)
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over and event.type == pygame.KEYDOWN:
                return show_menu(screen)   # ← يرجع للمنيو بعد الجيم أوفر

        if not game_over:
            # falling
            if fall_time > fall_speed:
                current.move_down()
                if not can_move(grid, current):
                    current.y -= 1
                    place_shape(grid, current)

                    grid, cleared = clear_full_rows(grid)
                    if cleared > 0:
                        score += cleared * 100
                        lines += cleared
                        level = lines // 5 + 1
                        fall_speed = max(100, 500 - (level-1)*40)

                    current = next_shape
                    next_shape = create_shape()
                    if not can_move(grid, current):
                        game_over = True

                fall_time = 0

            # movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                current.move_left()
                if not can_move(grid, current):
                    current.move_right()

            if keys[pygame.K_RIGHT]:
                current.move_right()
                if not can_move(grid, current):
                    current.move_left()

            if keys[pygame.K_DOWN]:
                current.move_down()
                if not can_move(grid, current):
                    current.y -= 1
                    place_shape(grid, current)
                    grid, cleared = clear_full_rows(grid)
                    if cleared > 0:
                        score += cleared * 100
                        lines += cleared
                        level = lines // 5 + 1
                        fall_speed = max(100, 500 - (level-1)*40)
                    current = next_shape
                    next_shape = create_shape()

        # draw
        screen.fill(BACKGROUND_COLOR)

        board = Board()
        board.draw(screen, current)

        draw_fixed_blocks(screen, grid)
        draw_shape(screen, current)

        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    show_menu(screen)      # ← ← ← هنا بيتفتح الـ HOME أول ما اللعبة تشتغل

if __name__ == "__main__":
    main()
