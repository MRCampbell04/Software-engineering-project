import pygame
from board import Board, draw_ui, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR
from shapes import create_shape

pygame.init()

font_path = "font/Audiowide-Regular.ttf"
font_score = pygame.font.Font(font_path, 20)
font_label = pygame.font.Font(font_path, 15)
font_value = pygame.font.Font(font_path, 16)


def run_game():
    # تشغيل نافذة اللعبة
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris - Game")

    clock = pygame.time.Clock()

    # استدعاء كائن البورد والشكل
    board = Board()
    shape = create_shape()

    # متغيرات اللعبة
    score = 0
    level = 1
    lines = 0

    fall_time = 0
    fall_speed = 450
    running = True

    while running:

        dt = clock.tick(60)
        fall_time += dt

        # ---------------- Events ----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # حركة يمين
        if keys[pygame.K_RIGHT]:
            shape.move_right()
            if not board.can_move(shape):
                shape.move_left()

        # حركة شمال
        if keys[pygame.K_LEFT]:
            shape.move_left()
            if not board.can_move(shape):
                shape.move_right()

        # حركة نزول أسرع
        if keys[pygame.K_DOWN]:
            shape.move_down()
            if not board.can_move(shape):
                shape.y -= 1
                board.place(shape)
                shape = create_shape()

        # -------- Auto Fall --------
        if fall_time > fall_speed:
            shape.move_down()
            if not board.can_move(shape):
                shape.y -= 1
                board.place(shape)
                shape = create_shape()

            fall_time = 0

        # ---------------- Draw ----------------
        screen.fill(BACKGROUND_COLOR)

        board.draw(screen, shape)
        draw_ui(screen, font_score, font_label, font_value, score, level, lines)

        pygame.display.update()

    pygame.quit()


# تشغيل اللعبة مباشرة
if __name__ == "__main__":
    run_game()
