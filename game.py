import pygame
import sys
from shapes import Shape, create_shape, CELL_SIZE, BOARD_WIDTH, BOARD_HEIGHT
from board import Board, draw_ui, GRID_X, GRID_Y, BLACK, WHITE
from home import font_path, show_home
from Login import LoginScreen
from AboutUs import AboutUsScreen
from Leaderboard import LeaderboardScreen

# ------------------- Game Logic Functions -------------------

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

# ------------------- Game Loop -------------------

def game_loop(screen):
    clock = pygame.time.Clock()
    board = Board()
    current_shape = create_shape()
    fall_time = 0
    fall_speed = 800

    grid = [[(0,0,0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    score = 0
    level = 1
    lines_cleared = 0
    game_over = False
    paused = False

    state = "home"

    font_score = pygame.font.Font(font_path, 20)
    font_label = pygame.font.Font(font_path, 15)
    font_value = pygame.font.Font(font_path, 16)

    # Initialize pages
    login_screen = LoginScreen(screen)
    about_screen = AboutUsScreen(screen)
    leaderboard_screen = LeaderboardScreen(screen)

    current_player_name = "Guest"

    # Pause button rectangle
    pause_button_rect = pygame.Rect(370, 10, 60, 40)  #                 أعلى يمين

    running = True
    while running:
        dt = clock.tick(60)
        if state == "playing" and not paused:
            fall_time += dt

        # -------------------- Events --------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Login page
            if state == "login":
                login_screen.handle_event(event)
                if login_screen.continue_pressed:
                    current_player_name = login_screen.user_text
                    if current_player_name.strip() == "":
                        current_player_name = "Unknown"
                    login_screen.continue_pressed = False
                    state = "playing"

            # Leaderboard page
            elif state == "leaderboard":
                leaderboard_screen.handle_event(event)
                if leaderboard_screen.back_pressed:
                    leaderboard_screen.back_pressed = False
                    state = "home"

            # About Us page
            elif state == "about":
                about_screen.handle_event(event)
                if about_screen.back_pressed:
                    about_screen.back_pressed = False
                    state = "home"

            # Game over
            elif state == "game_over" and event.type == pygame.KEYDOWN:
                if score > 0:
                    leaderboard_screen.save_score(current_player_name, score)
                grid = [[(0,0,0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
                current_shape = create_shape()
                fall_time = 0
                game_over = False
                score = 0
                level = 1
                lines_cleared = 0
                state = "playing"

            # Pause toggle
            if state == "playing" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pause_button_rect.collidepoint(event.pos):
                    paused = not paused

            # Pause menu buttons
            if paused:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Resume button
                    resume_rect = pygame.Rect(120, 300, 200, 50)
                    quit_rect = pygame.Rect(120, 400, 200, 50)
                    if resume_rect.collidepoint(event.pos):
                        paused = False
                    elif quit_rect.collidepoint(event.pos):
                        paused = False
                        state = "home"

        # -------------------- Gameplay Controls --------------------
        if state == "playing" and not game_over and not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                current_shape.move_left()
                if not can_move(grid, current_shape):
                    current_shape.move_right()
            if keys[pygame.K_RIGHT]:
                current_shape.move_right()
                if not can_move(grid, current_shape):
                    current_shape.move_left()
            if keys[pygame.K_DOWN]:
                current_shape.move_down()
                if not can_move(grid, current_shape):
                    current_shape.y -= 1
                    place_shape(grid, current_shape)
                    grid, cleared = clear_full_rows(grid)
                    if cleared > 0:
                        lines_cleared += cleared
                        score += cleared * 100
                        level = lines_cleared // 5 + 1
                        fall_speed = max(100, 500 - (level-1)*50)
                    current_shape = create_shape()
                    if not can_move(grid, current_shape):
                        game_over = True
                        state = "game_over"

            if keys[pygame.K_UP]:
                old_blocks = current_shape.rotate()
                if not can_move(grid, current_shape):
                    current_shape.blocks = old_blocks

            if fall_time > fall_speed:
                current_shape.move_down()
                if not can_move(grid, current_shape):
                    current_shape.y -= 1
                    place_shape(grid, current_shape)
                    grid, cleared = clear_full_rows(grid)
                    if cleared > 0:
                        lines_cleared += cleared
                        score += cleared * 100
                        level = lines_cleared // 5 + 1
                        fall_speed = max(100, 500 - (level-1)*50)
                    current_shape = create_shape()
                    if not can_move(grid, current_shape):
                        game_over = True
                        state = "game_over"
                        leaderboard_screen.save_score(current_player_name, score)
                fall_time = 0

        # -------------------- Drawing --------------------
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
            board.draw_board(screen)
            for r in range(BOARD_HEIGHT):
                for c in range(BOARD_WIDTH):
                    color = grid[r][c]
                    if color != (0,0,0):
                        x = GRID_X + c * CELL_SIZE
                        y = GRID_Y + r * CELL_SIZE
                        pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            for x, y in current_shape.get_coords():
                if y >= 0:
                    px = GRID_X + x * CELL_SIZE
                    py = GRID_Y + y * CELL_SIZE
                    pygame.draw.rect(screen, current_shape.color, (px, py, CELL_SIZE, CELL_SIZE))
            draw_ui(screen, font_score, font_label, font_value, score, level, lines_cleared)

        # Pause menu overlay
        if paused:
            overlay = pygame.Surface((440, 750))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0,0))

            # Resume button
            resume_rect = pygame.Rect(120, 300, 200, 50)
            quit_rect = pygame.Rect(120, 400, 200, 50)
            pygame.draw.rect(screen, WHITE, resume_rect)
            pygame.draw.rect(screen, WHITE, quit_rect)
            font_btn = pygame.font.Font(font_path, 32)
            screen.blit(font_btn.render("Resume", True, BLACK), (resume_rect.x + 35, resume_rect.y + 10))
            screen.blit(font_btn.render("Quit", True, BLACK), (quit_rect.x + 60, quit_rect.y + 10))

        elif state == "game_over":
            font_go = pygame.font.Font(None, 36)
            text = font_go.render("GAME OVER - Press Any Key", True, (255,0,0))
            screen.blit(text, (440//2 - text.get_width()//2, 750//2))

        elif state == "leaderboard":
            leaderboard_screen.draw(current_player_name, score)

        pygame.display.flip()

# ------------------- Main -------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((440, 750))
    pygame.display.set_caption("Tetris")
    game_loop(screen)
    pygame.quit()

if __name__ == "__main__":
    main()
