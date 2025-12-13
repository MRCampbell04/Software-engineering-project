import pygame
import sys
from shapes import Shape, create_shape, CELL_SIZE, BOARD_WIDTH, BOARD_HEIGHT
from board import Board, draw_ui, GRID_X, GRID_Y, BLACK, WHITE
from home import font_path, show_home
from Login import LoginScreen
from AboutUs import AboutUsScreen
from Leaderboard import LeaderboardScreen


##
# @brief Draws a mini preview of a shape inside a given rectangle.
# Used for displaying HOLD and NEXT shapes.
#
# @param screen The pygame screen surface.
# @param shape The shape to be drawn.
# @param rect The rectangle where the shape is rendered.
##
def draw_mini_shape(screen, shape, rect):
    if not shape:
        return

    xs = [bx for bx, by in shape.blocks]
    ys = [by for bx, by in shape.blocks]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    w = max_x - min_x + 1
    h = max_y - min_y + 1

    block = 12
    if w * block > rect.width - 6:
        block = (rect.width - 6) // w
    if h * block > rect.height - 6:
        block = (rect.height - 6) // h

    start_x = rect.centerx - (w * block) // 2
    start_y = rect.centery - (h * block) // 2

    for bx, by in shape.blocks:
        rx = bx - min_x
        ry = by - min_y
        px = start_x + rx * block
        py = start_y + ry * block
        pygame.draw.rect(screen, shape.color, (px, py, block, block))
        pygame.draw.rect(screen, (200, 200, 200), (px, py, block, block), 1)


##
# @brief Checks whether the shape can move to its current position.
#
# @param grid The current game grid.
# @param shape The active falling shape.
# @return True if the move is valid, False otherwise.
##
def can_move(grid, shape):
    for x, y in shape.get_coords():
        if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
            return False
        if y >= 0 and grid[y][x] != (0, 0, 0):
            return False
    return True


##
# @brief Places the shape permanently on the grid.
#
# @param grid The game grid.
# @param shape The shape to be placed.
##
def place_shape(grid, shape):
    for x, y in shape.get_coords():
        if 0 <= y < BOARD_HEIGHT:
            grid[y][x] = shape.color


##
# @brief Clears fully filled rows from the grid.
#
# @param grid The game grid.
# @return Tuple containing the updated grid and number of cleared rows.
##
def clear_full_rows(grid):
    cleared = 0
    new_grid = []
    for row in grid:
        if (0, 0, 0) not in row:
            cleared += 1
        else:
            new_grid.append(row)

    for _ in range(cleared):
        new_grid.insert(0, [(0, 0, 0) for _ in range(BOARD_WIDTH)])

    return new_grid, cleared


##
# @brief Resets all game variables to their initial state.
#
# @return Tuple containing all initial game state variables.
##
def reset_game():
    return (
        [[(0, 0, 0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)],
        create_shape(),
        [create_shape() for _ in range(3)],
        None,
        True,
        0,
        0,
        1,
        0,
        False,
        False
    )


##
# @brief Main game loop.
# Handles game states, events, logic, and rendering.
#
# @param screen The pygame screen surface.
##
def game_loop(screen):
    clock = pygame.time.Clock()
    board = Board()

    score_saved = False
    final_score = 0

    grid, current_shape, next_shapes, hold_shape, can_hold, score, lines, level, fall_time, game_over, paused = reset_game()

    state = "home"

    font_score = pygame.font.Font(font_path, 20)
    font_label = pygame.font.Font(font_path, 15)
    font_value = pygame.font.Font(font_path, 16)

    login_screen = LoginScreen(screen)
    about_screen = AboutUsScreen(screen)
    leaderboard_screen = LeaderboardScreen(screen)

    current_player_name = None
    pause_button_rect = pygame.Rect(370, 10, 60, 40)

    running = True
    while running:
        dt = clock.tick(60)

        if state == "playing" and not paused:
            fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == "login":
                login_screen.handle_event(event)
                if login_screen.continue_pressed:
                    current_player_name = login_screen.user_text.strip()
                    login_screen.continue_pressed = False
                    state = "playing"

            elif state == "leaderboard":
                leaderboard_screen.handle_event(event)
                if leaderboard_screen.back_pressed:
                    leaderboard_screen.back_pressed = False
                    state = "home"

            elif state == "about":
                about_screen.handle_event(event)
                if about_screen.back_pressed:
                    about_screen.back_pressed = False
                    state = "home"

            if state == "playing" and event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(event.pos):
                    paused = True

        # ================= GAME LOGIC =================

        if state == "playing" and not paused and not game_over:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                current_shape.move_left()
                if not can_move(grid, current_shape):
                    current_shape.move_right()

            if keys[pygame.K_RIGHT]:
                current_shape.move_right()
                if not can_move(grid, current_shape):
                    current_shape.move_left()

            if keys[pygame.K_UP]:
                old_blocks = current_shape.blocks[:]
                current_shape.blocks = [(-by, bx) for bx, by in current_shape.blocks]
                if not can_move(grid, current_shape):
                    current_shape.blocks = old_blocks

            if fall_time > 700:
                current_shape.move_down()
                if not can_move(grid, current_shape):
                    current_shape.y -= 1
                    place_shape(grid, current_shape)
                    grid, cleared = clear_full_rows(grid)
                    if cleared:
                        score += cleared * 100
                        lines += cleared

                    current_shape = next_shapes.pop(0)
                    next_shapes.append(create_shape())
                    can_hold = True

                    if not can_move(grid, current_shape):
                        if not score_saved and current_player_name:
                            leaderboard_screen.save_score(current_player_name, score)
                            final_score = score
                            score_saved = True
                        game_over = True
                        state = "game_over"

                fall_time = 0

        pygame.display.flip()


##
# @brief Initializes pygame and starts the game.
##
def main():
    pygame.init()
    screen = pygame.display.set_mode((440, 750))
    pygame.display.set_caption("CubeTicks")
    game_loop(screen)
    pygame.quit()


if __name__ == "__main__":
    main()