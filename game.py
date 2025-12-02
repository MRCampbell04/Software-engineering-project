import pygame
import sys
from shapes import Shape,Board, create_shape, CELL_SIZE, BOARD_WIDTH, BOARD_HEIGHT
from board import  GRID_X, GRID_Y, BLACK, WHITE
from home import Button, RED, font_path

# ------------------- Game Loop -------------------
def game_loop(screen):
    clock = pygame.time.Clock()
    board = Board()
    shape = create_shape()
    fall_time = 0
    fall_speed = 500
    game_over = False

    score = 0
    level = 1
    lines_cleared = 0

    font_score = pygame.font.Font(font_path, 20)
    font_label = pygame.font.Font(font_path, 15)
    font_value = pygame.font.Font(font_path, 16)

    # حالة اللعبة
    state = "home"

    # إعداد الأزرار
    start_button = Button("Start Game", 320)
    leaderboard_button = Button("Leaderboard", 400)
    about_button = Button("About Us", 480)
    exit_button = Button("Exit", 580, width=200, color=RED, text_color=WHITE, hover_color=(230,80,80), filled=True)
    buttons = [start_button, leaderboard_button, about_button, exit_button]

    running = True
    while running:
        dt = clock.tick(60)
        if state == "playing":
            fall_time += dt

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
                board = Board()
                shape = create_shape()
                fall_time = 0
                game_over = False
                score = 0
                level = 1
                lines_cleared = 0
                state = "playing"

        screen.fill(BLACK)

        if state == "home":
            # رسم Home Page
            title_font = pygame.font.Font(font_path, 80)
            title = title_font.render("Welcome", True, WHITE)
            name = pygame.font.Font(font_path, 40).render("Tetris", True, WHITE)
            screen.blit(title, (440//2 - title.get_width()//2, 120))
            screen.blit(name, (440//2 - name.get_width()//2, 230))
            for btn in buttons:
                btn.draw(screen, pygame.font.Font(font_path, 32))

        elif state == "playing":
            # تحكم اللعبة
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                shape.move_left()
                if not board.can_move(shape):
                    shape.move_right()
            if keys[pygame.K_RIGHT]:
                shape.move_right()
                if not board.can_move(shape):
                    shape.move_left()
            if keys[pygame.K_DOWN]:
                shape.move_down()
                if not board.can_move(shape):
                    shape.y -= 1
                    board.place(shape)
                    cleared = board.clear_full_rows()
                    if cleared > 0:
                        lines_cleared += cleared
                        score += cleared * 100
                        level = lines_cleared // 5 + 1
                        fall_speed = max(100, 500 - (level-1)*50)
                    new_shape = create_shape()
                    if not board.can_move(new_shape):
                        game_over = True
                        state = "game_over"
                    else:
                        shape = new_shape

            if fall_time > fall_speed:
                shape.move_down()
                if not board.can_move(shape):
                    shape.y -= 1
                    board.place(shape)
                    cleared = board.clear_full_rows()
                    if cleared > 0:
                        lines_cleared += cleared
                        score += cleared * 100
                        level = lines_cleared // 5 + 1
                        fall_speed = max(100, 500 - (level-1)*50)
                    new_shape = create_shape()
                    if not board.can_move(new_shape):
                        game_over = True
                        state = "game_over"
                    else:
                        shape = new_shape
                fall_time = 0

            # رسم اللعبة
            #shape.draw(screen, board)
            board.draw(screen, shape)
            draw_ui(screen, font_score, font_label, font_value, score, level, lines_cleared)

        elif state == "game_over":
            font_go = pygame.font.Font(None, 50)
            text = font_go.render("GAME OVER - Press Any Key to Restart", True, RED)
            screen.blit(text, (440//2 - text.get_width()//2, 750//2))

        pygame.display.flip()

# ------------------- Main UI -------------------
def draw_ui(screen, font_score, font_label, font_value, score, level, lines):
    # Score Box
    score_box_width = 180
    score_box_height = 35
    score_box_x = (440 - score_box_width) // 2
    score_box_y = 15
    score_box_rect = pygame.Rect(score_box_x, score_box_y, score_box_width, score_box_height)
    pygame.draw.rect(screen, WHITE, score_box_rect, 2, border_radius=8)
    score_text_surf = font_score.render(f"SCORE: {score}", True, WHITE)
    score_text_rect = score_text_surf.get_rect(center=score_box_rect.center)
    screen.blit(score_text_surf, score_text_rect)

    # Level & Lines
    labels_y = 80
    values_y = 105
    box_top_y = values_y - 10
    box_height = 40

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

# ------------------- Main -------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((440, 750))
    pygame.display.set_caption("Tetris")

    game_loop(screen)
    pygame.quit()

if __name__ == "__main__":
    main()

