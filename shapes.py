import pygame
import random

# Game settings
CELL_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

##
# @class Shape
# @brief Represents a falling Tetris shape with coordinates and movement.
#
class Shape:

    ##
    # @brief Constructor for creating a shape.
    # @param x Starting X position.
    # @param y Starting Y position.
    # @param color RGB color of the shape.
    # @param blocks Relative block coordinates of the piece.
    #
    def __init__(self, x, y, color, blocks):
        self.x = x
        self.y = y
        self.color = color
        self.blocks = blocks

    ##
    # @brief Moves the shape down by 1 cell.
    #
    def move_down(self):
        self.y += 1

    ##
    # @brief Moves the shape left by 1 cell.
    #
    def move_left(self):
        self.x -= 1

    ##
    # @brief Moves the shape right by 1 cell.
    #
    def move_right(self):
        self.x += 1

    ##
    # @brief Returns absolute coordinates of the shape on the board.
    # @return List of (x,y) cell positions.
    #
    def get_coords(self):
        return [(self.x + bx, self.y + by) for bx, by in self.blocks]


##
# @brief Creates and returns a random shape.
# @return Shape object with random color and type.
#
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


##
# @class Board
# @brief Handles grid data, collision detection, placing shapes, and drawing.
#
class Board:

    ##
    # @brief Initializes an empty game grid.
    #
    def __init__(self):
        self.grid = [[(0,0,0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    ##
    # @brief Checks if a shape can move to its current coordinates.
    # @param shape The falling shape.
    # @return True if movement is valid, False otherwise.
    #
    def can_move(self, shape):
        for x, y in shape.get_coords():
            if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
                return False
            if y >= 0 and self.grid[y][x] != (0,0,0):
                return False
        return True

    ##
    # @brief Fixes the shape blocks into the board grid.
    # @param shape The shape to be placed.
    #
    def place(self, shape):
        for x, y in shape.get_coords():
            if 0 <= y < BOARD_HEIGHT:
                self.grid[y][x] = shape.color

    ##
    # @brief Draws the board grid and the current falling shape.
    # @param screen The game display surface.
    # @param shape Currently falling shape.
    #
    def draw(self, screen, shape):
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                rect = pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (40,40,40), rect, 1)

                if self.grid[row][col] != (0,0,0):
                    pygame.draw.rect(screen, self.grid[row][col], rect)

        for x, y in shape.get_coords():
            if 0 <= y < BOARD_HEIGHT:
                rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, shape.color, rect)


##
# @brief Main game loop: handles gameplay, falling, drawing, and input.
#
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
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
                    new_shape = create_shape()
                    if not board.can_move(new_shape):
                        game_over = True
                    else:
                        shape = new_shape

        screen.fill((0,0,0))
        board.draw(screen, shape)
        pygame.display.flip()

    pygame.quit()


main()