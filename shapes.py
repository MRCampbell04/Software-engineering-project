import pygame
import random

# ---------------- Game Constants ----------------

## Size of a single block in pixels
CELL_SIZE = 30

## Number of columns in the board
BOARD_WIDTH = 10

## Number of rows in the board
BOARD_HEIGHT = 20


##
# @class Shape
# @brief Represents a Tetris shape.
# Handles movement, rotation, and block coordinates.
##
class Shape:
    ##
    # @brief Constructor for Shape.
    #
    # @param x Initial x position.
    # @param y Initial y position.
    # @param color RGB color of the shape.
    # @param blocks Relative block coordinates.
    # @param shape_type Identifier of shape type.
    ##
    def __init__(self, x, y, color, blocks, shape_type=None):
        self.x = x
        self.y = y
        self.color = color
        self.blocks = blocks
        self.shape_type = shape_type

    ## Moves shape one cell down
    def move_down(self):
        self.y += 1

    ## Moves shape one cell left
    def move_left(self):
        self.x -= 1

    ## Moves shape one cell right
    def move_right(self):
        self.x += 1

    ##
    # @brief Returns absolute coordinates of shape blocks.
    #
    # @return List of (x, y) tuples.
    ##
    def get_coords(self):
        return [(self.x + bx, self.y + by) for bx, by in self.blocks]

    ##
    # @brief Creates a copy of the shape.
    #
    # @return New Shape object.
    ##
    def clone(self):
        return Shape(self.x, self.y, self.color, self.blocks, self.shape_type)


##
# @brief Creates a random Tetris shape.
#
# @return Shape object.
##
def create_shape():
    shapes_data = [
        ([(0,0),(0,1),(1,0),(1,1)], (255,255,0), 'O'),
        ([(0,0),(-1,0),(1,0),(2,0)], (0,255,255), 'I'),
        ([(0,0),(0,1),(0,2),(1,2)], (255,165,0), 'L'),
        ([(0,0),(-1,0),(1,0),(0,1)], (128,0,128), 'T'),
        ([(0,0),(1,0),(0,1),(-1,1)], (0,255,0), 'S'),
    ]

    blocks, color, type_name = random.choice(shapes_data)
    return Shape(4, 0, color, blocks, type_name)