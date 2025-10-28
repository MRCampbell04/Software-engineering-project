"""
Dev 3 – Game Rules & Integration
File: game.py

This script creates the game window, integrates Board and Shape,
and runs the basic game loop where one block moves down automatically.
"""

import pygame
from board import Board
from shapes import Shape

# -------------------- Setup --------------------
pygame.init()
SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris - Basic Version")

# Create objects
board = Board()
shape = Shape(x=4, y=0, color=(0, 255, 255))

# Timing
clock = pygame.time.Clock()
running = True

# -------------------- Game Loop --------------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background
    screen.fill((0, 0, 0))

    # Move shape down every second
    shape.move_down()

    # Stop the shape when it reaches the bottom (simple update)
    if not shape.is_inside_board():
        shape.y -= 1  # move it back up one step
        running = False  # stop the game loop (optional)

    # Draw grid and shape
    board.draw_board(screen)
    from shapes import Board as LogicBoard
    logic_board = LogicBoard()
    logic_board.draw(screen, shape)

    # Update display
    pygame.display.update()

    # Wait for 1 second before next move
    pygame.time.delay(1000)

# -------------------- End --------------------
pygame.quit()
