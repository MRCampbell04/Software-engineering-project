import pygame
import random
import sys

# ------------------- Constants -------------------
SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750

CELL_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

GRID_X = (SCREEN_WIDTH - (BOARD_WIDTH * CELL_SIZE)) // 2
GRID_Y = SCREEN_HEIGHT - (BOARD_HEIGHT * CELL_SIZE) - 5

BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
LIGHT_RED = (230, 80, 80)
SILVER = (191, 191, 191)

font_path = "font/Audiowide-Regular.ttf"

# ------------------- Shape Class -------------------
class Shape:
    def __init__(self, x, y, color, blocks):
        self.x = x
        self.y = y
        self.color = color
        self.blocks = blocks

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

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

# ------------------- Board Class -------------------
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

    def clear_full_rows(self):
        full_rows = [i for i, row in enumerate(self.grid) if all(cell != (0,0,0) for cell in row)]
        for row in full_rows:
            del self.grid[row]
            self.grid.insert(0, [(0,0,0) for _ in range(BOARD_WIDTH)])
        return len(full_rows)

    def draw(self, screen, shape):
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                rect = pygame.Rect(GRID_X + col*CELL_SIZE, GRID_Y + row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen,(40,40,40),rect,1)
                if self.grid[row][col] != (0,0,0):
                    pygame.draw.rect(screen,self.grid[row][col],rect)
        for x, y in shape.get_coords():
            if 0 <= y < BOARD_HEIGHT:
                rect = pygame.Rect(GRID_X + x*CELL_SIZE, GRID_Y + y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen,shape.color,rect)

# ------------------- UI Functions -------------------
def draw_ui(screen, font_score, font_label, font_value, score, level, lines):
    # Score box
    score_box_width = 180
    score_box_height = 35
    score_box_x = (SCREEN_WIDTH - score_box_width) // 2
    score_box_y = 15
    score_box_rect = pygame.Rect(score_box_x, score_box_y, score_box_width, score_box_height)
    pygame.draw.rect(screen, WHITE, score_box_rect, 2, border_radius=8)
    score_text_surf = font_score.render(f"SCORE: {score}", True, WHITE)
    score_text_rect = score_text_surf.get_rect(center=score_box_rect.center)
    screen.blit(score_text_surf, score_text_rect)

    # Level and Lines
    labels_y = 80
    values_y = 105
    box_top_y = values_y - 10
    box_height = 40

    level_x = GRID_X - 40
    level_label = font_label.render("LEVEL", True, WHITE)
    level_value = font_value.render(str(level), True, WHITE)
    screen.blit(level_label, (level_x, labels_y))
    screen.blit(level_value, (level_x + (level_label.get_width() - level_value.get_width()) // 2, values_y))

    lines_x = GRID_X + 30
    lines_label = font_label.render("LINES", True, WHITE)
    lines_value = font_value.render(str(lines), True, WHITE)
    screen.blit(lines_label, (lines_x, labels_y))
    screen.blit(lines_value, (lines_x + (lines_label.get_width() - lines_value.get_width()) // 2, values_y))

# ------------------- Game Loop -------------------
def game_loop(screen):
    clock = pygame.time.Clock()
    board = Board()
    shape = create_shape()
    fall_time = 0
    fall_speed = 500
    game_over = False

    score = 0
    level = 1
    lines = 0

    font_score = pygame.font.Font(font_path, 20)
    font_label = pygame.font.Font(font_path, 15)
    font_value = pygame.font.Font(font_path, 16)

    running = True
    while running:
        dt = clock.tick(60)
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over and event.type == pygame.KEYDOWN:
                # Restart the game
                board = Board()
                shape = create_shape()
                fall_time = 0
                game_over = False
                score = 0
                level = 1
                lines = 0

        if not game_over:
            if fall_time > fall_speed:
                shape.move_down()
                if not board.can_move(shape):
                    shape.y -= 1
                    board.place(shape)
                    cleared = board.clear_full_rows()
                    if cleared > 0:
                        lines += cleared
                        score += cleared * 100
                        level = lines // 5 + 1
                        fall_speed = max(100, 500 - (level-1)*50)
                    new_shape = create_shape()
                    if not board.can_move(new_shape):
                        game_over = True
                    else:
                        shape = new_shape
                fall_time = 0

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
                    cleared = board.clear_full_rows()
                    if cleared > 0:
                        lines += cleared
                        score += cleared * 100
                        level = lines // 5 + 1
                        fall_speed = max(100, 500 - (level-1)*50)
                    new_shape = create_shape()
                    if not board.can_move(new_shape):
                        game_over = True
                    else:
                        shape = new_shape

        # Draw everything
        screen.fill(BLACK)
        board.draw(screen, shape)
        draw_ui(screen, font_score, font_label, font_value, score, level, lines)

        # Game Over text
        if game_over:
            font_go = pygame.font.Font(None, 50)
            text = font_go.render("GAME OVER - Press Any Key to Restart", True, RED)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))

        pygame.display.flip()

# ------------------- Main -------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    game_loop(screen)
    pygame.quit()

if __name__ == "__main__":
    main()
