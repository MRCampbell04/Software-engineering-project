import pygame
import sys
import random

# نستورد الثوابت و fonctions من board.py و shape.py اللي انتِ بعتيهم
from board import GRID_X, GRID_Y, BLOCK_SIZE, GRID_COLS, GRID_ROWS, draw_ui, BACKGROUND_COLOR, WHITE
from shape import create_shape, Shape

SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750

EMPTY = (0, 0, 0)
font_path = "font/Audiowide-Regular.ttf"


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


def draw_next_preview(screen, next_shape):
    grid_right = GRID_X + (GRID_COLS * BLOCK_SIZE)
    next_box_width = 120
    next_box_x = grid_right - next_box_width - 5
    # box_top_y must match draw_ui box top: draw_ui used "box_top_y = values_y - 10" where values_y = 105
    box_top_y = 105 - 10
    next_box_rect = pygame.Rect(next_box_x + 17, box_top_y, next_box_width, 40)
    if next_shape:
        cx = next_box_rect.centerx
        cy = next_box_rect.centery
        for bx, by in next_shape.blocks:
            rx = cx + bx * 10
            ry = cy + by * 10
            r = pygame.Rect(rx - 8, ry - 8, 16, 16)
            pygame.draw.rect(screen, next_shape.color, r)


def game_loop(screen):
    pygame.init()
    clock = pygame.time.Clock()

    grid = make_empty_grid()
    current = create_shape()
    next_shape = create_shape()

    fall_time = 0
    fall_speed = 500

    score = 0
    level = 1
    lines = 0
    game_over = False

    font_score = pygame.font.Font(font_path, 20)
    font_label = pygame.font.Font(font_path, 15)
    font_value = pygame.font.Font(font_path, 16)

    running = True
    while running:
        dt = clock.tick(60)
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over and event.type == pygame.KEYDOWN:
                grid = make_empty_grid()
                current = create_shape()
                next_shape = create_shape()
                fall_time = 0
                fall_speed = 500
                score = 0
                level = 1
                lines = 0
                game_over = False

        if not game_over:
            if fall_time > fall_speed:
                current.move_down()
                if not can_move(grid, current):
                    current.y -= 1
                    place_shape(grid, current)
                    grid, cleared = clear_full_rows(grid)
                    if cleared > 0:
                        lines += cleared
                        score += cleared * 100
                        level = lines // 5 + 1
                        fall_speed = max(100, 500 - (level - 1) * 50)
                    current = next_shape
                    next_shape = create_shape()
                    if not can_move(grid, current):
                        game_over = True
                fall_time = 0

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
                        lines += cleared
                        score += cleared * 100
                        level = lines // 5 + 1
                        fall_speed = max(100, 500 - (level - 1) * 50)
                    current = next_shape
                    next_shape = create_shape()
                    if not can_move(grid, current):
                        game_over = True

        screen.fill(BACKGROUND_COLOR)

        # draw empty board grid using your Board.draw_board (keeps original design)
        from board import Board as UIDrawer
        uid = UIDrawer()
        uid.draw_board(screen)

        # draw fixed blocks and current falling piece
        draw_fixed_blocks(screen, grid)
        if not game_over:
            draw_shape(screen, current)

        # draw UI (score, level, lines, next/hold boxes)
        draw_ui(screen, font_score, font_label, font_value, score, level, lines)
        draw_next_preview(screen, next_shape)

        if game_over:
            font_go = pygame.font.Font(None, 50)
            text = font_go.render("GAME OVER - Press Any Key to Restart", True, (200, 50, 50))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    game_loop(screen)
