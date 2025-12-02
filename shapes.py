import pygame
import random

# Game settings
CELL_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Shape class
class Shape:
    def __init__(self, x, y, color, blocks):
        self.x = x                # Horizontal position
        self.y = y                # Vertical position
        self.color = color        # Shape color
        self.blocks = blocks      # Relative block coordinates

    # Move down
    def move_down(self):
        self.y += 1

    # Move left
    def move_left(self):
        self.x -= 1

    # Move right
    def move_right(self):
        self.x += 1

    # Get all block coordinates on the board
    def get_coords(self):
        return [(self.x + bx, self.y + by) for bx, by in self.blocks]

# Create a random shape
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
        # Game grid, each cell stores color, (0,0,0) means empty
        self.grid = [[(0,0,0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    # Check if the shape can move without collision
    def can_move(self, shape):
        for x, y in shape.get_coords():
            if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:  # Out of board
                return False
            if y >= 0 and self.grid[y][x] != (0,0,0):          # Block exists
                return False
        return True

    # Place the shape on the board
    def place(self, shape):
        for x, y in shape.get_coords():
            if 0 <= y < BOARD_HEIGHT:
                self.grid[y][x] = shape.color

    # Draw board and current shape
    def draw(self, screen, shape):
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                rect = pygame.Rect(col*CELL_SIZE,row*CELL_SIZE,CELL_SIZE,CELL_SIZE)
                pygame.draw.rect(screen,(40,40,40),rect,1)  # Light grid
                if self.grid[row][col] != (0,0,0):          # Draw fixed blocks
                    pygame.draw.rect(screen,self.grid[row][col],rect)
        # Draw current falling shape
        for x, y in shape.get_coords():
            if 0 <= y < BOARD_HEIGHT:
                rect = pygame.Rect(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE)
                pygame.draw.rect(screen,shape.color,rect)
'''
# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_WIDTH*CELL_SIZE,BOARD_HEIGHT*CELL_SIZE))
    pygame.display.set_caption("Simple Shapes Game")

    clock = pygame.time.Clock()
    board = Board()
    shape = create_shape()
    fall_time = 0
    fall_speed = 400          # Fall speed in milliseconds
    game_over = False         # Game over flag 

    running = True
    while running:
        dt = clock.tick(60)   # Frame rate
        fall_time += dt

        # Automatic falling
        if not game_over:
            if fall_time > fall_speed:
                shape.move_down()
                if not board.can_move(shape):  # Reached bottom or another block
                    shape.y -= 1
                    board.place(shape)        # Fix the shape
                    # Create new shape
                    new_shape = create_shape()
                    if not board.can_move(new_shape):
                        game_over = True       # Stop game if no space
                    else:
                        shape = new_shape
                fall_time = 0

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player controls
        if not game_over:
            keys = pygame.key.get_pressed()
            # Move left
            if keys[pygame.K_LEFT]:
                shape.move_left()
                if not board.can_move(shape):
                    shape.move_right()
            # Move right
            if keys[pygame.K_RIGHT]:
                shape.move_right()
                if not board.can_move(shape):
                    shape.move_left()
            # Move down faster
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
                        
        # Draw everything
        screen.fill((0,0,0))
        board.draw(screen,shape)
        pygame.display.flip()

    pygame.quit()


main()'''
