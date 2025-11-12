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

# ------------------- Button Class -------------------
class Button:
    def __init__(self, text, y, width=270, height=50, color=WHITE, text_color=WHITE, hover_color=None, filled=False):
        self.text = text
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color
        self.hover_color = hover_color or color
        self.filled = filled
        self.rect = pygame.Rect(SCREEN_WIDTH//2 - width//2, y, width, height)
        self.border_radius = 12

    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.hover_color if is_hovered else self.color

        if self.filled:
            pygame.draw.rect(surface, current_color, self.rect, border_radius=self.border_radius)
        else:
            pygame.draw.rect(surface, current_color, self.rect, 2, border_radius=self.border_radius)

        label = font.render(self.text, True, self.text_color)
        surface.blit(label, (self.rect.centerx - label.get_width()/2, self.rect.centery - label.get_height()/2))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

# ------------------- Menu -------------------
def show_menu(screen):
    title_font = pygame.font.Font(font_path, 80)
    button_font = pygame.font.Font(font_path, 32)

    buttons = [
        Button("Start Game", 320, text_color=BLACK, hover_color=SILVER, filled=True),
        Button("Exit", 480, width=200, color=RED, text_color=WHITE, hover_color=LIGHT_RED, filled=True)
    ]

    running = True
    while running:
        screen.fill(BLACK)
        title = title_font.render("Welcome", True, WHITE)
        name = pygame.font.Font(font_path, 40).render("Tetris", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()/2, 120))
        screen.blit(name, (SCREEN_WIDTH//2 - name.get_width()/2, 230))

        for btn in buttons:
            btn.draw(screen, button_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for btn in buttons:
                if btn.is_clicked(event):
                    if btn.text == "Start Game":
                        game_loop(screen)
                        running = False
                    elif btn.text == "Exit":
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()

# ------------------- Game Loop -------------------
def game_loop(screen):
    clock = pygame.time.Clock()
    board = Board()
    shape = create_shape()
    fall_time = 0
    fall_speed = 500  # ⚡ متوسط السرعة
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
                pygame.quit()
                sys.exit()

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

        screen.fill(BLACK)
        board.draw(screen, shape)
        if game_over:
            font = pygame.font.Font(None, 50)
            text = font.render("GAME OVER", True, RED)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))
        pygame.display.flip()

# ------------------- Main -------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    show_menu(screen)
    pygame.quit()

if __name__ == "__main__":
    main()
