import pygame
import random

# Game Settings
CELL_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
HEADER_HEIGHT = 100
SCREEN_WIDTH = BOARD_WIDTH * CELL_SIZE
SCREEN_HEIGHT = BOARD_HEIGHT * CELL_SIZE + HEADER_HEIGHT

# Shape class
class Shape:
    def __init__(self, x, y, color, blocks, shape_type=None):
        self.x = x
        self.y = y
        self.color = color
        self.blocks = blocks
        self.shape_type = shape_type

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def get_coords(self):
        return [(self.x + bx, self.y + by) for bx, by in self.blocks]

    def clone(self):
        return Shape(self.x, self.y, self.color, self.blocks, self.shape_type)

# Create random Tetris shape
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

# Board class
class Board:
    def __init__(self):
        self.grid = [[(0,0,0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.level = 1

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
        self.clear_lines()

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(pixel == (0,0,0) for pixel in row)]
        lines_cleared = BOARD_HEIGHT - len(new_grid)

        for _ in range(lines_cleared):
            new_grid.insert(0, [(0,0,0) for _ in range(BOARD_WIDTH)])

        self.grid = new_grid
        self.score += lines_cleared
        self.level = 1 + (self.score // 10)

    # Draw board (Grid + solid shapes)
    def draw(self, screen, shape):
        offset_y = HEADER_HEIGHT

        # Board background
        pygame.draw.rect(screen, (0, 0, 0), (0, offset_y, SCREEN_WIDTH, SCREEN_HEIGHT - offset_y))

        # --- Draw grid only ---
        grid_color = (25, 25, 25)
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE + offset_y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, grid_color, rect, 1)

        # --- Draw placed blocks (solid) ---
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if self.grid[row][col] != (0, 0, 0):
                    rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE + offset_y, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, self.grid[row][col], rect)

        # --- Draw current shape (solid) ---
        if shape:
            for x, y in shape.get_coords():
                if 0 <= y < BOARD_HEIGHT:
                    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE + offset_y, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, shape.color, rect)

# Auto-scaling for shapes inside Hold/Next boxes
def draw_centered_shape(screen, shape, target_rect):
    if not shape:
        return

    xx = [bx for bx, by in shape.blocks]
    yy = [by for bx, by in shape.blocks]
    min_x, max_x = min(xx), max(xx)
    min_y, max_y = min(yy), max(yy)

    shape_w = (max_x - min_x + 1)
    shape_h = (max_y - min_y + 1)

    block_size = 12
    if shape_w * block_size > target_rect.width - 4:
        block_size = (target_rect.width - 4) // shape_w
    if shape_h * block_size > target_rect.height - 4:
        block_size = (target_rect.height - 4) // shape_h

    start_x = target_rect.centerx - (shape_w * block_size // 2)
    start_y = target_rect.centery - (shape_h * block_size // 2)

    for bx, by in shape.blocks:
        rel_x = bx - min_x
        rel_y = by - min_y
        rect = pygame.Rect(start_x + rel_x * block_size, start_y + rel_y * block_size, block_size, block_size)
        pygame.draw.rect(screen, shape.color, rect)
        pygame.draw.rect(screen, (200, 200, 200), rect, 1)

# Draw header UI
def draw_header(screen, font, next_shapes, level, lines):
    pygame.draw.rect(screen, (30, 30, 40), (0, 0, SCREEN_WIDTH, HEADER_HEIGHT))
    pygame.draw.line(screen, (255,255,255), (0, HEADER_HEIGHT-1), (SCREEN_WIDTH, HEADER_HEIGHT-1), 2)

    text_color = (200, 200, 200)

    # HOLD
    screen.blit(font.render("HOLD", True, text_color), (135, 10))
    hold_rect = pygame.Rect(125, 30, 60, 50)
    pygame.draw.rect(screen, (50, 50, 60), hold_rect)
    pygame.draw.rect(screen, (255, 255, 255), hold_rect, 1)

    if len(next_shapes) > 0:
        draw_centered_shape(screen, next_shapes[0], hold_rect)

    txt_swap = font.render("(C) Swap", True, (100, 100, 100))
    txt_swap = pygame.transform.scale(txt_swap, (int(txt_swap.get_width()*0.8), int(txt_swap.get_height()*0.8)))
    screen.blit(txt_swap, (125, 85))

    # NEXT
    screen.blit(font.render("NEXT", True, text_color), (220, 10))
    next_bg_rect = pygame.Rect(200, 30, 95, 50)
    pygame.draw.rect(screen, (50, 50, 60), next_bg_rect)
    pygame.draw.rect(screen, (255, 255, 255), next_bg_rect, 1)

    sub_width = next_bg_rect.width // 3
    future_shapes = next_shapes[1:4]

    for i, shp in enumerate(future_shapes):
        target = pygame.Rect(next_bg_rect.x + (i * sub_width), next_bg_rect.y, sub_width, next_bg_rect.height)
        draw_centered_shape(screen, shp, target)

# Main loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    font = pygame.font.Font(None, 20)
    clock = pygame.time.Clock()

    board = Board()

    next_shapes = [create_shape() for _ in range(5)]
    shape = create_shape()

    can_swap = True
    fall_time = 0
    fall_speed = 400
    game_over = False

    while True:
        dt = clock.tick(60)
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN and not game_over:

                # Swap with HOLD
                if event.key == pygame.K_c and can_swap:
                    current_temp = shape
                    shape = next_shapes[0]
                    next_shapes[0] = current_temp
                    shape.x, shape.y = 4, 0
                    next_shapes[0].x, next_shapes[0].y = 4, 0
                    can_swap = False

                # Move left
                if event.key == pygame.K_LEFT:
                    shape.move_left()
                    if not board.can_move(shape):
                        shape.move_right()

                # Move right
                elif event.key == pygame.K_RIGHT:
                    shape.move_right()
                    if not board.can_move(shape):
                        shape.move_left()

                # Soft drop
                elif event.key == pygame.K_DOWN:
                    shape.move_down()
                    if not board.can_move(shape):
                        shape.y -= 1
                        board.place(shape)

                        shape = next_shapes.pop(0)
                        next_shapes.append(create_shape())

                        can_swap = True
                        if not board.can_move(shape):
                            game_over = True

                # Rotate
                elif event.key == pygame.K_UP:
                    old_blocks = shape.blocks[:]
                    shape.blocks = [(-by, bx) for bx, by in shape.blocks]
                    if not board.can_move(shape):
                        shape.blocks = old_blocks

        # Gravity
        if not game_over:
            if fall_time > fall_speed:
                shape.move_down()
                if not board.can_move(shape):
                    shape.y -= 1
                    board.place(shape)

                    # Test shape
                    new_shape = next_shapes.pop(0)
                    if board.can_move(new_shape):
                        shape = new_shape
                        next_shapes.append(create_shape())
                        can_swap = True
                    else:
                        game_over = True

                fall_time = 0


        draw_header(screen, font, next_shapes, board.level, board.score)
        board.draw(screen, shape)
        pygame.display.flip()

if __name__ == "__main__":
    main()