import pygame

CELL_SIZE = 30  
BOARD_WIDTH = 10 
BOARD_HEIGHT = 20 

class Shape:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def is_inside_board(self):
        return 0 <= self.x < BOARD_WIDTH and 0 <= self.y < BOARD_HEIGHT

    def get_coordinates(self):
        return [(self.x, self.y)]


class Board:
    def __init__(self):
        self.grid = [[(0, 0, 0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    def draw(self, screen, shape):
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (40, 40, 40), rect, 1) 

        for (x, y) in shape.get_coordinates():
            if 0 <= y < BOARD_HEIGHT: 
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, shape.color, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE))
    pygame.display.set_caption("Blocks Logic & Movement")

    clock = pygame.time.Clock()
    running = True

    board = Board()
    shape = Shape(x=4, y=0, color=(255, 0, 0))

    fall_time = 0
    fall_speed = 500 

    while running:
        dt = clock.tick(60)
        fall_time += dt

        if fall_time > fall_speed:
            shape.move_down()
            fall_time = 0

            if not shape.is_inside_board():
                shape.y -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            shape.move_left()
            if not shape.is_inside_board():
                shape.move_right()
        if keys[pygame.K_RIGHT]:
            shape.move_right()
            if not shape.is_inside_board():
                shape.move_left()
        if keys[pygame.K_DOWN]:
            shape.move_down()
            if not shape.is_inside_board():
                shape.y -= 1

        screen.fill((0, 0, 0))
        board.draw(screen, shape)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
