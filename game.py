import pygame
import sys
from shapes import Shape, create_shape, CELL_SIZE, BOARD_WIDTH, BOARD_HEIGHT
from board import Board, draw_ui, GRID_X, GRID_Y, BLACK, WHITE
from home import font_path, show_home
from Login import LoginScreen
from AboutUs import AboutUsScreen
from Leaderboard import LeaderboardScreen


# ----------------- Draw mini preview for HOLD / NEXT -----------------

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



# ------------------- Game Helper Functions -------------------

def can_move(grid, shape):
    for x, y in shape.get_coords():
        if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
            return False
        if y >= 0 and grid[y][x] != (0, 0, 0):
            return False
    return True


def place_shape(grid, shape):
    for x, y in shape.get_coords():
        if 0 <= y < BOARD_HEIGHT:
            grid[y][x] = shape.color


def clear_full_rows(grid):
    cleared = 0
    new_grid = []
    for row in grid:
        if (0,0,0) not in row:
            cleared += 1
        else:
            new_grid.append(row)

    for _ in range(cleared):
        new_grid.insert(0, [(0,0,0) for _ in range(BOARD_WIDTH)])

    return new_grid, cleared



# ------------------- Main Game Loop -------------------

def game_loop(screen):

    clock = pygame.time.Clock()
    board = Board()

    current_shape = create_shape()
    next_shapes = [create_shape() for _ in range(3)]
    hold_shape = None
    can_hold = True

    fall_time = 0
    fall_speed = 700

    grid = [[(0,0,0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    score = 0
    level = 1
    lines = 0
    game_over = False
    paused = False

    state = "home"

    font_score = pygame.font.Font(font_path, 20)
    font_label = pygame.font.Font(font_path, 15)
    font_value = pygame.font.Font(font_path, 16)

    login_screen = LoginScreen(screen)
    about_screen = AboutUsScreen(screen)
    leaderboard_screen = LeaderboardScreen(screen)

    current_player_name = "Guest"

    pause_button_rect = pygame.Rect(370, 10, 60, 40)

    running = True
    while running:

        dt = clock.tick(60)
        if state == "playing" and not paused:
            fall_time += dt

        # ---------------------- EVENTS ----------------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # LOGIN PAGE
            if state == "login":
                login_screen.handle_event(event)
                if login_screen.continue_pressed:
                    current_player_name = login_screen.user_text or "Unknown"
                    login_screen.continue_pressed = False
                    state = "playing"

            # LEADERBOARD PAGE
            elif state == "leaderboard":
                leaderboard_screen.handle_event(event)
                if leaderboard_screen.back_pressed:
                    leaderboard_screen.back_pressed = False
                    state = "home"

            # ABOUT PAGE
            elif state == "about":
                about_screen.handle_event(event)
                if about_screen.back_pressed:
                    about_screen.back_pressed = False
                    state = "home"

            # PAUSE BUTTON
            if state == "playing" and event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(event.pos):
                    paused = not paused

            # Pause Menu Buttons
            if paused:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    resume_rect = pygame.Rect(120, 300, 200, 50)
                    quit_rect = pygame.Rect(120, 400, 200, 50)
                    if resume_rect.collidepoint(event.pos):
                        paused = False
                    elif quit_rect.collidepoint(event.pos):
                        paused = False
                        state = "home"

        # ---------------------- GAMEPLAY ----------------------
        if state == "playing" and not game_over and not paused:

            keys = pygame.key.get_pressed()

            # MOVE LEFT
            if keys[pygame.K_LEFT]:
                current_shape.move_left()
                if not can_move(grid, current_shape):
                    current_shape.move_right()

            # MOVE RIGHT
            if keys[pygame.K_RIGHT]:
                current_shape.move_right()
                if not can_move(grid, current_shape):
                    current_shape.move_left()

            # ROTATE
            if keys[pygame.K_UP]:
                old = current_shape.blocks[:]
                current_shape.blocks = [(-by, bx) for bx, by in current_shape.blocks]
                if not can_move(grid, current_shape):
                    current_shape.blocks = old

            # HOLD (C)
            if keys[pygame.K_c] and can_hold:
                if hold_shape is None:
                    hold_shape = current_shape
                    current_shape = next_shapes.pop(0)
                    next_shapes.append(create_shape())
                else:
                    hold_shape, current_shape = current_shape, hold_shape

                current_shape.x, current_shape.y = 4, 0
                can_hold = False

            # SOFT DROP
            if keys[pygame.K_DOWN]:
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
                        game_over = True
                        state = "game_over"

            # GRAVITY
            if fall_time > fall_speed:
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
                        leaderboard_screen.save_score(current_player_name, score)
                        game_over = True
                        state = "game_over"

                fall_time = 0

        # ---------------------- DRAWING ----------------------
        screen.fill(BLACK)

        if state == "home":
            action = show_home(screen)
            if action == "start":
                state = "login"
            elif action == "leaderboard":
                state = "leaderboard"
            elif action == "about":
                state = "about"

        elif state == "login":
            login_screen.draw()

        elif state == "about":
            about_screen.draw()

        elif state == "playing":

            # Draw board grid
            board.draw_board(screen)

            # Draw placed blocks
            for r in range(BOARD_HEIGHT):
                for c in range(BOARD_WIDTH):
                    if grid[r][c] != (0, 0, 0):
                        pygame.draw.rect(
                            screen,
                            grid[r][c],
                            (GRID_X + c * CELL_SIZE, GRID_Y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        )

            # Draw current falling shape
            for x, y in current_shape.get_coords():
                if y >= 0:
                    pygame.draw.rect(
                        screen,
                        current_shape.color,
                        (GRID_X + x * CELL_SIZE, GRID_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )

            # Draw UI (score + boxes)
            hold_rect, next_rect, pause_rect = draw_ui(
                screen, font_score, font_label, font_value,
                score, level, lines
            )

            # Draw HOLD mini preview
            if hold_shape:
                draw_mini_shape(screen, hold_shape, hold_rect)

            # Draw NEXT preview
            draw_mini_shape(screen, next_shapes[0], next_rect)

        # -------------- PAUSE MENU --------------
        if paused:
            overlay = pygame.Surface((440, 750))
            overlay.set_alpha(190)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0,0))

            font_btn = pygame.font.Font(font_path, 32)

            resume_rect = pygame.Rect(120, 300, 200, 50)
            quit_rect = pygame.Rect(120, 400, 200, 50)

            pygame.draw.rect(screen, WHITE, resume_rect)
            pygame.draw.rect(screen, WHITE, quit_rect)

            screen.blit(font_btn.render("Resume", True, BLACK), (resume_rect.x+35, resume_rect.y+10))
            screen.blit(font_btn.render("Quit", True, BLACK), (quit_rect.x+60, quit_rect.y+10))

        # ----------- GAME OVER SCREEN ----------
        elif state == "game_over":

            screen.fill(BLACK)

            font_go = pygame.font.Font(None, 50)
            go_text = font_go.render("GAME OVER", True, (255,0,0))
            screen.blit(go_text, (220 - go_text.get_width()//2, 200))

            button_font = pygame.font.Font(font_path, 32)

            retry_rect = pygame.Rect(120, 350, 200, 50)
            home_rect = pygame.Rect(70, 410, 300, 80)

            pygame.draw.rect(screen, WHITE, retry_rect)
            pygame.draw.rect(screen, WHITE, home_rect)

            screen.blit(button_font.render("Retry", True, BLACK),
                        (retry_rect.centerx - 50, retry_rect.centery - 20))

            screen.blit(button_font.render("Back to Home", True, BLACK),
                        (home_rect.centerx - 110, home_rect.centery - 20))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if retry_rect.collidepoint(event.pos):
                        grid = [[(0,0,0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
                        current_shape = create_shape()
                        next_shapes = [create_shape() for _ in range(3)]
                        hold_shape = None
                        score = 0
                        lines = 0
                        can_hold = True
                        game_over = False
                        state = "playing"

                    elif home_rect.collidepoint(event.pos):
                        state = "home"

        elif state == "leaderboard":
            leaderboard_screen.draw(current_player_name, score)

        pygame.display.flip()



# ---------------- MAIN ----------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((440, 750))
    pygame.display.set_caption("Tetris")
    game_loop(screen)
    pygame.quit()


if __name__ == "__main__":
    main()
