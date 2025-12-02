import pygame
import sys
from shapes import Shape, create_shape, CELL_SIZE, BOARD_WIDTH, BOARD_HEIGHT
from board import Board, draw_ui, GRID_X, GRID_Y, BLACK, WHITE
from home import Button, RED, font_path  # افتراضياً عندك Home Page وButton

# ------------------- Game Logic Functions -------------------

def can_move(grid, shape):
    """تحقق إذا الشكل ممكن يتحرك بدون اصطدام"""
    for x, y in shape.get_coords():
        if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
            return False
        if y >= 0 and grid[y][x] != (0,0,0):
            return False
    return True

def place_shape(grid, shape):
    """ثبت الشكل في الشبكة"""
    for x, y in shape.get_coords():
        if 0 <= y < BOARD_HEIGHT:
            grid[y][x] = shape.color

def clear_full_rows(grid):
    """مسح الصفوف المليانة وتحريك الباقي لأسفل"""
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

    # الشبكة داخل game.py
    grid = [[(0,0,0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    score = 0
    level = 1
    lines_cleared = 0
    game_over = False

    # Home Page Buttons
    state = "home"
    start_button = Button("Start Game", 320)
    leaderboard_button = Button("Leaderboard", 400)
    about_button = Button("About Us", 480)
    exit_button = Button("Exit", 580, width=200, color=RED, text_color=WHITE, hover_color=(230,80,80), filled=True)
    buttons = [start_button, leaderboard_button, about_button, exit_button]

    font_score = pygame.font.Font(font_path, 20)
    font_label = pygame.font.Font(font_path, 15)
    font_value = pygame.font.Font(font_path, 16)

    running = True
    while running:
        dt = clock.tick(60)
        if state == "playing":
            fall_time += dt

        # حدث اللعبة
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if state == "home":
                for btn in buttons:
                    if btn.is_clicked(event):
                        if btn.text == "Start Game":
                            state = "playing"
                        elif btn.text == "Exit":
                            pygame.quit()
                            sys.exit()
                        elif btn.text == "Leaderboard":
                            print("Leaderboard pressed")
                        elif btn.text == "About Us":
                            print("About Us pressed")
            elif state == "game_over" and event.type == pygame.KEYDOWN:
                # إعادة تشغيل اللعبة
                grid = [[(0,0,0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
                current_shape = create_shape()
                fall_time = 0
                game_over = False
                score = 0
                level = 1
                lines_cleared = 0
                state = "playing"

        # التحكم بالكيبورد
        if state == "playing" and not game_over:
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

            # Automatic fall
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
                fall_time = 0

        # رسم كل شيء
        screen.fill(BLACK)

        if state == "home":
            title_font = pygame.font.Font(font_path, 80)
            title = title_font.render("Welcome", True, WHITE)
            name = pygame.font.Font(font_path, 40).render("Tetris", True, WHITE)
            screen.blit(title, (440//2 - title.get_width()//2, 120))
            screen.blit(name, (440//2 - name.get_width()//2, 230))
            for btn in buttons:
                btn.draw(screen, pygame.font.Font(font_path, 32))

        elif state == "playing":
            # رسم الشبكة
            board.draw_board(screen)
            # رسم الأشكال الثابتة
            for r in range(BOARD_HEIGHT):
                for c in range(BOARD_WIDTH):
                    color = grid[r][c]
                    if color != (0,0,0):
                        x = GRID_X + c * CELL_SIZE
                        y = GRID_Y + r * CELL_SIZE
                        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, color, rect)
            # رسم الشكل الحالي
            for x, y in current_shape.get_coords():
                if y >= 0:
                    px = GRID_X + x * CELL_SIZE
                    py = GRID_Y + y * CELL_SIZE
                    pygame.draw.rect(screen, current_shape.color, (px, py, CELL_SIZE, CELL_SIZE))

            draw_ui(screen, font_score, font_label, font_value, score, level, lines_cleared)

        elif state == "game_over":
            font_go = pygame.font.Font(None, 36)
            text = font_go.render("GAME OVER - Press Any Key", True, RED)
            screen.blit(text, (440//2 - text.get_width()//2, 750//2))

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
