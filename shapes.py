import pygame
import random

# Game settings
CELL_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Shape class
class Shape:
    def __init__(self, x, y, color, blocks):
        self.x = x                  # Horizontal position
        self.y = y                  # Vertical position
        self.color = color          # Shape color
        self.blocks = blocks        # Relative block coordinates

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    # Rotate 90°: (x, y) -> (-y, x)
    def rotate(self):
        rotated = [(-by, bx) for bx, by in self.blocks]
        old_blocks = self.blocks
        self.blocks = rotated
        return old_blocks

    def get_coords(self):
        return [(self.x + bx, self.y + by) for bx, by in self.blocks]


def create_shape():
    shapes = [
        [(0,0),(1,0),(0,1),(1,1)],   # O
        [(0,0),(-1,0),(1,0),(2,0)],  # I
        [(0,0),(0,1),(0,2),(1,2)],   # L
        [(0,0),(-1,0),(1,0),(0,1)],  # T
        [(0,0),(1,0),(0,1),(-1,1)]   # S
    ]
    colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,165,0),(128,0,128)]
    return Shape(4, 0, random.choice(colors), random.choice(shapes))


# Board class
class Board:
    def __init__(self):
        self.grid = [[(0,0,0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    def can_move(self, shape):
        for x, y in shape.get_coords():
            if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
                return False
            if y >= 0 and self.grid[y][x] != (0,0,0):
                return False
        return True

    def place(self, shape):
        for x, y in shape.get_coords():
            if 0 <= y < BOARD_HEIGHT:
                self.grid[y][x] = shape.color

    def draw(self, screen, shape):
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                rect = pygame.Rect(col*CELL_SIZE,row*CELL_SIZE,CELL_SIZE,CELL_SIZE)
                pygame.draw.rect(screen,(40,40,40),rect,1)
                if self.grid[row][col] != (0,0,0):
                    pygame.draw.rect(screen,self.grid[row][col],rect)

        for x, y in shape.get_coords():
            if 0 <= y < BOARD_HEIGHT:
                rect = pygame.Rect(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE)
                pygame.draw.rect(screen,shape.color,rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_WIDTH*CELL_SIZE, BOARD_HEIGHT*CELL_SIZE))
    pygame.display.set_caption("Simple Shapes Game")

    clock = pygame.time.Clock()
    board = Board()
    shape = create_shape()

    fall_time = 0
    fall_speed = 400
    game_over = False

    running = True
    while running:
        dt = clock.tick(60)
        fall_time += dt

        # Auto fall
        if not game_over:
            if fall_time > fall_speed:
                shape.move_down()
                if not board.can_move(shape):
                    shape.y -= 1
                    board.place(shape)
                    new_shape = create_shape()
                    if not board.can_move(new_shape):
                        game_over = True
                    else:
                        shape = new_shape
                fall_time = 0

        # EVENT HANDLING (rotation + movement)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and not game_over:

                # Rotate once
                if event.key == pygame.K_UP:
                    old_blocks = shape.rotate()
                    if not board.can_move(shape):
                        shape.blocks = old_blocks

                # Move left once
                if event.key == pygame.K_LEFT:
                    shape.move_left()
                    if not board.can_move(shape):
                        shape.move_right()

                # Move right once
                if event.key == pygame.K_RIGHT:
                    shape.move_right()
                    if not board.can_move(shape):
                        shape.move_left()

                # Fast drop (one cell per press)
                if event.key == pygame.K_DOWN:
                    shape.move_down()
                    if not board.can_move(shape):
                        shape.y -= 1
                        board.place(shape)
                        new_shape = create_shape()
                        if not board.can_move(new_shape):
                            game_over = True
                        else:
                            shape = new_shape

        # Draw
        screen.fill((0,0,0))
        board.draw(screen,shape)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
