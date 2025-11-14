import pygame
import sys
import random

# import layout & UI helpers from the board file you provided
from board import GRID_X, GRID_Y, BLOCK_SIZE, GRID_COLS, GRID_ROWS, draw_ui, BACKGROUND_COLOR, WHITE
# import shape factory from the shapes file you provided
from shapes import create_shape

SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750

# game logic grid uses the same GRID_COLS / GRID_ROWS from board.py
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
    next_box_rect = pygame.Rect(next_box_x + 17, 95, next_box_width, 40)  # matches draw_ui's y
    if next_shape:
        cx = next_box_rect.centerx
        cy = next_box_rect.centery
        for bx, by in next_shape.blocks:
            rx = cx + bx * 10
            ry = cy + by * 10
            r = pygame.Rect(rx - 8, ry - 8, 16, 16)
            pygame.draw.rect(screen, next_shape.color, r)


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    font_score = pygame.font.Font(font_path, 20)
    font_label = pygame.font.Font(font_path, 15)
    font_value = pygame.font.Font(font_path, 16)

    grid = make_empty_grid()
    current = create_shape()
    next_shape = create_shape()

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 500

    score = 0
    level = 1
    lines = 0
    running = True
    game_over = False

    while running:
        dt = clock.tick(60)
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
                        # simple scoring: 100 points per row (keeps original behavior)
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
        # draw board grid and UI from original board.py
        from board import Board as UIDrawer  # import here to avoid circular issues if running standalone
        uid = UIDrawer()
        uid.draw_board(screen)

        # draw fixed blocks (from logic grid) and current shape at GRID offsets
        draw_fixed_blocks(screen, grid)
        if not game_over:
            draw_shape(screen, current)

        # draw UI (score, level, lines, next/hold boxes)
        draw_ui(screen, font_score, font_label, font_value, score, level, lines)
        # draw simple preview for next inside the NEXT box
        draw_next_preview(screen, next_shape)

        if game_over:
            font_go = pygame.font.Font(None, 50)
            text = font_go.render("GAME OVER - Press Any Key to Restart", True, (200, 50, 50))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
