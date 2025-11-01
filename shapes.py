import pygame

CELL_SIZE = 30  
BOARD_WIDTH = 10 
BOARD_HEIGHT = 20 

class Shape:
    """
    Class representing a single block shape in the game.
    Used to handle the block position, color, and movement logic.
    """

    def __init__(self, x, y, color):
        """
        Initialize a new shape object.

        Args:
            x (int): The horizontal position of the shape.
            y (int): The vertical position of the shape.
            color (tuple): RGB color of the shape.
        """
        self.x = x
        self.y = y
        self.color = color

    def move_down(self):
        """
        Move the shape one cell down on the board.
        """
        self.y += 1

    def move_left(self):
        """
        Move the shape one cell to the left.
        """
        self.x -= 1

    def move_right(self):
        """
        Move the shape one cell to the right.
        """
        self.x += 1

    def is_inside_board(self):
        """
        Check if the shape is still inside the board boundaries.

        Returns:
            bool: True if inside the board, False if outside.
        """
        return 0 <= self.x < BOARD_WIDTH and 0 <= self.y < BOARD_HEIGHT

    def get_coordinates(self):
        """
        Get the coordinates occupied by the shape on the grid.

        Returns:
            list: List of (x, y) tuples representing the block positions.
        """
        return [(self.x, self.y)]


class Board:
    """
    Class representing the game board grid.
    Handles drawing the grid and the active shape.
    """

    def __init__(self):
        """
        Initialize the game board with empty cells.
        """
        self.grid = [[(0, 0, 0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    def draw(self, screen, shape):
        """
        Draw the board grid and the current shape on the screen.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
            shape (Shape): The active shape object to draw.
        """

        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (40, 40, 40), rect, 1) 

        for (x, y) in shape.get_coordinates():
            if 0 <= y < BOARD_HEIGHT: 
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, shape.color, rect)


def main():
    """
    Main function to start and run the game loop.
    Handles game initialization, user input, and screen updates.
    """
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