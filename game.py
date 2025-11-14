import pygame
from shapes import Shape, create_shape, LogicBoard
from board import GameBoardUI

pygame.init()

# ثوابت اللعبة
SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris Game")

clock = pygame.time.Clock()


# ----------------------------------------
#     دالة مسح السطور المكتملة
# ----------------------------------------

def clear_full_lines(board):
    full_lines = 0
    new_grid = []

    for row in board.grid:
        if (0,0,0) not in row:     # لو السطر كله متملّي
            full_lines += 1
        else:
            new_grid.append(row)

    # ضيف فوقهم سطور فاضية بنفس العدد
    for _ in range(full_lines):
        new_grid.insert(0, [(0,0,0) for _ in range(board.width)])

    board.grid = new_grid

    return full_lines



# ----------------------------------------
#               MAIN GAME
# ----------------------------------------

def main():

    # UI Board
    ui = GameBoardUI()

    # Logic Board (الشبكة الحقيقية)
    logic = LogicBoard()

    # أول قطعة
    current_shape = create_shape()

    fall_timer = 0
    fall_speed = 500   # سرعة سقوط القطعة (ms)

    running = True
    while running:

        dt = clock.tick(FPS)
        fall_timer += dt

        # الأحداث
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ------ حركة اللاعب ------
        keys = pygame.key.get_pressed()

        # يمين
        if keys[pygame.K_RIGHT]:
            current_shape.move_right()
            if not logic.can_move(current_shape):
                current_shape.move_left()

        # شمال
        if keys[pygame.K_LEFT]:
            current_shape.move_left()
            if not logic.can_move(current_shape):
                current_shape.move_right()

        # لتحت أسرع
        if keys[pygame.K_DOWN]:
            current_shape.move_down()
            if not logic.can_move(current_shape):
                current_shape.y -= 1
                logic.place(current_shape)
                clear_full_lines(logic)
                current_shape = create_shape()


        # ------ السقوط التلقائي ------
        if fall_timer > fall_speed:
            current_shape.move_down()
            if not logic.can_move(current_shape):
                current_shape.y -= 1
                logic.place(current_shape)
                
                # مسح السطور
                clear_full_lines(logic)

                # قطعة جديدة
                current_shape = create_shape()

            fall_timer = 0

        # ------ رسم الشاشة ------
        screen.fill((0,0,0))

        # نرسم الجريد UI (من ملف board.py)
        ui.draw_board(screen)

        # نرسم الشبكة + القطعة (من ملف shapes.py)
        logic.draw(screen, current_shape)

        pygame.display.update()

    pygame.quit()



if __name__ == "__main__":
    main()
