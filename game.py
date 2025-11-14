# game.py
# Main game integration file
# - Uses the existing modules: shapes.py (logic) and board.py (UI)
# - Does NOT modify any external files
# - Comments are in English only

import pygame
import sys
import time

# Import modules as they are (do not change other files).
# There are two different Board classes: one in shapes.py (logic board)
# and one in board.py (UI drawing). We will reference them with module
# qualification to avoid name collisions.
import shapes      # shapes.py contains: Shape, create_shape, Board (logic)
import board       # board.py contains: Board (UI), draw_ui, constants

pygame.init()
pygame.font.init()

# Use the UI module's constants for layout
SCREEN_WIDTH = getattr(board, "SCREEN_WIDTH", 440)
SCREEN_HEIGHT = getattr(board, "SCREEN_HEIGHT", 750)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris Game")

clock = pygame.time.Clock()
FPS = 60

# Fonts (use the font path from board.py if available)
FONT_PATH = getattr(board, "font_path", None)
if FONT_PATH:
    FONT_SMALL = pygame.font.Font(FONT_PATH, 18)
    FONT_MED = pygame.font.Font(FONT_PATH, 22)
    FONT_BIG = pygame.font.Font(FONT_PATH, 40)
else:
    FONT_SMALL = pygame.font.SysFont("arial", 18)
    FONT_MED = pygame.font.SysFont("arial", 22)
    FONT_BIG = pygame.font.SysFont("arial", 40)

# Aliases for clarity
LogicBoard = shapes.Board        # logic grid and collision from shapes.py
CreateShape = shapes.create_shape
ShapeClass = shapes.Shape       # shape constructor if needed

# UI constants from board.py
GRID_X = getattr(board, "GRID_X", 70)
GRID_Y = getattr(board, "GRID_Y", 50)
BLOCK_SIZE = getattr(board, "BLOCK_SIZE", 30)
GRID_COLS = getattr(board, "GRID_COLS", 10)
GRID_ROWS = getattr(board, "GRID_ROWS", 20)

# Game state variables (initialized in run_game)
current_shape = None
next_shape = None
hold_shape = None
hold_used = False

logic_board = None   # instance of LogicBoard
ui_board = None      # instance of board.Board (UI)

score = 0
level = 1
total_lines = 0

# fall_speed in milliseconds (will be lowered as level increases)
BASE_FALL_SPEED = 600
fall_speed = BASE_FALL_SPEED
fall_timer = 0

paused = False
game_over = False


# -------------------------
# Utility helpers
# -------------------------
def recalc_speed():
    """Recalculate fall speed based on level."""
    global fall_speed
    fall_speed = max(100, BASE_FALL_SPEED - (level - 1) * 50)


def rotate_clockwise(blocks):
    """
    Rotate a list of relative block coordinates clockwise.
    (x, y) -> (-y, x)
    """
    return [(-by, bx) for bx, by in blocks]


def can_place_with_blocks(shape, new_blocks, dx=0, dy=0):
    """
    Create a temporary shape with new_blocks and optional offset and test collision.
    Returns True if placement is valid.
    """
    temp = ShapeClass(shape.x + dx, shape.y + dy, shape.color, new_blocks)
    return logic_board.can_move(temp)


def clear_full_lines():
    """
    Clear completed lines from logic_board.grid.
    Update score, total_lines, and level accordingly.
    Returns number of cleared lines.
    """
    global score, total_lines, level
    grid = logic_board.grid
    cleared = 0
    new_grid = []

    for row in grid:
        if (0, 0, 0) not in row:
            cleared += 1
        else:
            new_grid.append(row)

    # Insert empty rows on top equal to number cleared
    for _ in range(cleared):
        new_grid.insert(0, [(0, 0, 0) for _ in range(len(grid[0]))])

    if cleared > 0:
        logic_board.grid = new_grid
        # simple scoring: 100 points per line times level
        score += cleared * 100 * level
        total_lines += cleared
        level = 1 + (total_lines // 10)
        recalc_speed()

    return cleared


# -------------------------
# Drawing helpers
# -------------------------
def draw_placed_blocks():
    """
    Draw blocks from logic_board.grid onto the UI grid coordinates.
    This prevents using shapes.draw (which draws its own grid at (0,0)).
    """
    grid = logic_board.grid
    for r in range(min(len(grid), GRID_ROWS)):
        for c in range(min(len(grid[0]), GRID_COLS)):
            color = grid[r][c]
            if color != (0, 0, 0):
                x = GRID_X + c * BLOCK_SIZE
                y = GRID_Y + r * BLOCK_SIZE
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (10, 10, 10), rect, 1)


def draw_shape_on_ui(shape):
    """
    Draw the current falling shape on the UI grid.
    Use shape.get_coords() which returns (x + bx, y + by).
    """
    for bx, by in shape.get_coords():
        # Only draw visible rows
        if by >= 0 and by < GRID_ROWS and bx >= 0 and bx < GRID_COLS:
            x = GRID_X + bx * BLOCK_SIZE
            y = GRID_Y + by * BLOCK_SIZE
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, shape.color, rect)
            pygame.draw.rect(screen, (10, 10, 10), rect, 1)


def draw_next_and_hold(next_piece, hold_piece):
    """
    Draw the NEXT preview and HOLD boxes using board.draw_ui or manual draw.
    We'll use board.draw_ui if it exists; otherwise draw simple boxes.
    """
    # try to use draw_ui (board.py supplies draw_ui)
    try:
        # board.draw_ui(screen, font_score, font_label, font_value, score, level, lines)
        board.draw_ui(screen, FONT_SMALL, FONT_SMALL, FONT_SMALL, score, level, total_lines)
    except Exception:
        # fallback simple HUD: draw small boxes on right side
        hud_x = SCREEN_WIDTH - 170
        hud_y = 80
        pygame.draw.rect(screen, (30, 30, 30), (hud_x, hud_y, 150, 220), border_radius=6)
        # NEXT label
        label = FONT_SMALL.render("NEXT", True, (255,255,255))
        screen.blit(label, (hud_x + 10, hud_y + 10))
        # draw next piece small
        if next_piece:
            base_x = hud_x + 20
            base_y = hud_y + 40
            for bx, by in next_piece.blocks:
                rx = base_x + (bx + 2) * (BLOCK_SIZE // 2)
                ry = base_y + (by + 1) * (BLOCK_SIZE // 2)
                rect = pygame.Rect(rx, ry, BLOCK_SIZE // 2, BLOCK_SIZE // 2)
                pygame.draw.rect(screen, next_piece.color, rect)
                pygame.draw.rect(screen, (10,10,10), rect, 1)
        # HOLD
        label2 = FONT_SMALL.render("HOLD (C)", True, (255,255,255))
        screen.blit(label2, (hud_x + 10, hud_y - 60))
        if hold_piece:
            base_x = hud_x + 20
            base_y = hud_y - 30
            for bx, by in hold_piece.blocks:
                rx = base_x + (bx + 2) * (BLOCK_SIZE // 2)
                ry = base_y + (by + 1) * (BLOCK_SIZE // 2)
                rect = pygame.Rect(rx, ry, BLOCK_SIZE // 2, BLOCK_SIZE // 2)
                pygame.draw.rect(screen, hold_piece.color, rect)
                pygame.draw.rect(screen, (10,10,10), rect, 1)


def draw_pause_overlay():
    """Draw semi-transparent paused overlay."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    txt = FONT_BIG.render("PAUSED", True, (255,255,255))
    screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, SCREEN_HEIGHT//2 - 40))
    sub = FONT_MED.render("Press P to resume", True, (200,200,200))
    screen.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, SCREEN_HEIGHT//2 + 10))


def draw_game_over_overlay():
    """Draw game over overlay with restart instructions."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    txt = FONT_BIG.render("GAME OVER", True, (255,50,50))
    screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, SCREEN_HEIGHT//2 - 60))
    sub = FONT_MED.render(f"Score: {score}", True, (255,255,255))
    screen.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, SCREEN_HEIGHT//2))
    info = FONT_SMALL.render("Press R to restart or ESC to quit", True, (200,200,200))
    screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, SCREEN_HEIGHT//2 + 40))


# -------------------------
# Main game loop function
# -------------------------
def run_game():
    """Run a single play session. Call this from home.py if you add the import there."""
    global current_shape, next_shape, hold_shape, hold_used
    global logic_board, ui_board, fall_timer, score, level, total_lines
    global paused, game_over

    # initialize board instances
    logic_board = LogicBoard()
    ui_board = board.Board()  # board.Board is UI board from board.py

    # initialize shapes
    current_shape = CreateShape()
    next_shape = CreateShape()
    hold_shape = None
    hold_used = False

    # reset scores
    score = 0
    level = 1
    total_lines = 0
    recalc_speed()

    fall_timer = 0
    paused = False
    game_over = False

    running = True
    while running:
        dt = clock.tick(FPS)
        fall_timer += dt

        # --- events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # keyboard controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

                if game_over:
                    # restart or quit on game over screen
                    if event.key == pygame.K_r:
                        # restart by reinitializing state
                        return run_game()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                # ignore movement keys if paused or game over
                if not paused and not game_over:
                    # left
                    if event.key == pygame.K_LEFT:
                        current_shape.move_left()
                        if not logic_board.can_move(current_shape):
                            current_shape.move_right()

                    # right
                    if event.key == pygame.K_RIGHT:
                        current_shape.move_right()
                        if not logic_board.can_move(current_shape):
                            current_shape.move_left()

                    # soft drop
                    if event.key == pygame.K_DOWN:
                        current_shape.move_down()
                        if not logic_board.can_move(current_shape):
                            current_shape.y -= 1
                            logic_board.place(current_shape)
                            cleared = clear_full_lines()
                            if cleared:
                                # score updated inside clear_full_lines
                                pass
                            current_shape = next_shape
                            next_shape = CreateShape()
                            hold_used = False

                    # hard drop (space)
                    if event.key == pygame.K_SPACE:
                        # drop until collision
                        while True:
                            current_shape.move_down()
                            if not logic_board.can_move(current_shape):
                                current_shape.y -= 1
                                logic_board.place(current_shape)
                                cleared = clear_full_lines()
                                current_shape = next_shape
                                next_shape = CreateShape()
                                hold_used = False
                                break

                    # rotate (up)
                    if event.key == pygame.K_UP:
                        # attempt rotation with basic kicks
                        old_blocks = current_shape.blocks[:]
                        new_blocks = rotate_clockwise(old_blocks)

                        # try center rotation
                        if can_place_with_blocks(current_shape, new_blocks, 0, 0):
                            current_shape.blocks = new_blocks
                        else:
                            # try small kicks
                            kicked = False
                            for dx, dy in [(-1,0),(1,0),(-2,0),(2,0),(0,-1)]:
                                if can_place_with_blocks(current_shape, new_blocks, dx, dy):
                                    current_shape.x += dx
                                    current_shape.y += dy
                                    current_shape.blocks = new_blocks
                                    kicked = True
                                    break
                            if not kicked:
                                # rotation invalid -> keep old blocks
                                current_shape.blocks = old_blocks

                    # hold (c)
                    if event.key == pygame.K_c and not hold_used:
                        if hold_shape is None:
                            hold_shape = current_shape
                            current_shape = next_shape
                            next_shape = CreateShape()
                        else:
                            hold_shape, current_shape = current_shape, hold_shape
                        # reset position of current
                        current_shape.x = max(0, GRID_COLS // 2 - 1)
                        current_shape.y = 0
                        hold_used = True

        # --- automatic falling if not paused and not game over ---
        if not paused and not game_over:
            if fall_timer >= fall_speed:
                current_shape.move_down()
                if not logic_board.can_move(current_shape):
                    # step back and lock piece
                    current_shape.y -= 1
                    logic_board.place(current_shape)
                    cleared = clear_full_lines()
                    # spawn next piece
                    current_shape = next_shape
                    next_shape = CreateShape()
                    hold_used = False

                    # if new piece cannot be placed -> game over
                    if not logic_board.can_move(current_shape):
                        game_over = True

                fall_timer = 0

        # --- drawing ---
        screen.fill((0,0,0))

        # draw UI board (grid & border)
        try:
            ui_board.draw_board(screen)
        except Exception:
            # fallback: draw grid lines using constants
            for r in range(GRID_ROWS):
                for c in range(GRID_COLS):
                    x = GRID_X + c * BLOCK_SIZE
                    y = GRID_Y + r * BLOCK_SIZE
                    pygame.draw.rect(screen, (30,30,30), (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

        # draw blocks from logic board
        draw_placed_blocks()

        # draw current falling shape mapped to UI
        if current_shape:
            draw_shape_on_ui(current_shape)

        # draw next and hold + scoreboard area
        draw_next_and_hold(next_shape, hold_shape)

        # overlays
        if paused:
            draw_pause_overlay()

        if game_over:
            draw_game_over_overlay()

        pygame.display.flip()

    # end of run_game
    pygame.quit()
    sys.exit()


# allow direct run of game.py for testing
if __name__ == "__main__":
    run_game()
