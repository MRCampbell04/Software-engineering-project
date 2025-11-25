import pygame
import random
import sys

## @brief Width of game window.
SCREEN_WIDTH = 440

## @brief Height of game window.
SCREEN_HEIGHT = 750

## @brief Size of each cell.
CELL_SIZE = 30

## @brief Number of columns in board.
BOARD_WIDTH = 10

## @brief Number of rows in board.
BOARD_HEIGHT = 20

## @brief Grid X starting position.
GRID_X = (SCREEN_WIDTH - (BOARD_WIDTH * CELL_SIZE)) // 2

## @brief Grid Y starting position.
GRID_Y = SCREEN_HEIGHT - (BOARD_HEIGHT * CELL_SIZE) - 5

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200,50,50)
LIGHT_RED = (230,80,80)
SILVER = (191,191,191)

font_path = "font/Audiowide-Regular.ttf"


# ======================================================
#                       SHAPE
# ======================================================
## @class Shape
## @brief Represents a Tetris shape and its movement.
class Shape:

    ## @brief Creates a new shape.
    ## @param x Starting X position.
    ## @param y Starting Y position.
    ## @param color Shape color.
    ## @param blocks List of block offsets.
    def __init__(self, x, y, color, blocks):
        self.x = x
        self.y = y
        self.color = color
        self.blocks = blocks

    ## @brief Moves shape down.
    def move_down(self):
        self.y += 1

    ## @brief Moves shape left.
    def move_left(self):
        self.x -= 1

    ## @brief Moves shape right.
    def move_right(self):
        self.x += 1

    ## @brief Gets absolute coords of the shape.
    ## @return List of (x,y) positions.
    def get_coords(self):
        return [(self.x + bx, self.y + by) for bx, by in self.blocks]


## @brief Creates random shape.
## @return Shape object.
def create_shape():
    shapes = [
        [(0,0),(1,0),(0,1),(1,1)],   
        [(0,0),(-1,0),(1,0),(2,0)],
        [(0,0),(0,1),(0,2),(1,2)],
        [(0,0),(-1,0),(1,0),(0,1)],
        [(0,0),(1,0),(0,1),(-1,1)]
    ]
    colors = [
        (255,0,0),(0,255,0),(0,0,255),
        (255,255,0),(255,165,0),(128,0,128)
    ]
    return Shape(4, 0, random.choice(colors), random.choice(shapes))



# ======================================================
#                       BOARD
# ======================================================
## @class Board
## @brief Represents the game grid.
class Board:

    ## @brief Initializes empty grid.
    def __init__(self):
        self.grid = [[(0,0,0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    ## @brief Checks if shape can move.
    ## @param shape Shape to test.
    ## @return True if valid move.
    def can_move(self, shape):
        for x, y in shape.get_coords():
            if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
                return False
            if y >= 0 and self.grid[y][x] != (0,0,0):
                return False
        return True

    ## @brief Locks shape into grid.
    ## @param shape Shape to place.
    def place(self, shape):
        for x, y in shape.get_coords():
            if 0 <= y < BOARD_HEIGHT:
                self.grid[y][x] = shape.color

    ## @brief Clears completed rows.
    ## @return Number of cleared rows.q
    def clear_full_rows(self):
        full_rows = [
            i for i, row in enumerate(self.grid)
            if all(cell != (0,0,0) for cell in row)
        ]
        for row in full_rows:
            del self.grid[row]
            self.grid.insert(0, [(0,0,0)] * BOARD_WIDTH)
        return len(full_rows)

    ## @brief Draws board and current shape.
    ## @param screen Display surface.
    ## @param shape Active shape.
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



# ======================================================
#                     BUTTON CLASS
# ======================================================
## @class Button
## @brief UI button for menu interactions.
class Button:

    ## @brief Creates a button.
    ## @param text Button label.
    ## @param y Vertical position.
    ## @param width Button width.
    ## @param height Button height.
    ## @param color Border color.
    ## @param text_color Text color.
    ## @param hover_color Color when hovered.
    ## @param filled Whether button is filled.
    def __init__(self, text, y, width=270, height=50, color=WHITE,
                 text_color=WHITE, hover_color=None, filled=False):

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

    ## @brief Draws the button.
    ## @param surface Screen surface.
    ## @param font Font object.
    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)
        color = self.hover_color if hovered else self.color

        if self.filled:
            pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        else:
            pygame.draw.rect(surface, color, self.rect, 2, border_radius=self.border_radius)

        label = font.render(self.text, True, self.text_color)
        surface.blit(label, (
            self.rect.centerx - label.get_width()/2,
            self.rect.centery - label.get_height()/2
        ))

    ## @brief Checks if button clicked.
    ## @param event Mouse event.
    ## @return True if clicked.
    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))



# ======================================================
#                     MENU FUNCTION
# ======================================================
## @brief Shows main menu.
## @param screen Display surface.
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



# ======================================================
#                     UI FUNCTION
# ======================================================
## @brief Draws score, level, and lines.
def draw_ui(screen, font_score, font_label, font_value, score, level, lines):
    score_box = pygame.Rect((SCREEN_WIDTH-180)//2, 15, 180, 35)
    pygame.draw.rect(screen, WHITE, score_box, 2, border_radius=8)

    score_text = font_score.render(f"SCORE: {score}", True, WHITE)
    screen.blit(score_text, score_text.get_rect(center=score_box.center))

    # Level
    level_label = font_label.render("LEVEL", True, WHITE)
    level_value = font_value.render(str(level), True, WHITE)
    screen.blit(level_label, (GRID_X - 40, 80))
    screen.blit(level_value, (GRID_X - 40, 105))

    # Lines
    lines_label = font_label.render("LINES", True, WHITE)
    lines_value = font_value.render(str(lines), True, WHITE)
    screen.blit(lines_label, (GRID_X + 30, 80))
    screen.blit(lines_value, (GRID_X + 30, 105))



# ======================================================
#                     GAME LOOP
# ======================================================
## @brief Main game logic loop.
## @param screen Display surface.
def game_loop(screen):

    clock = pygame.time.Clock()
    board = Board()
    shape = create_shape()
    fall_time = 0
    fall_speed = 500
    game_over = False

    score = 0
    level = 1
    lines_cleared = 0

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
                board = Board()
                shape = create_shape()
                fall_time = 0
                game_over = False
                score = 0
                level = 1
                lines_cleared = 0

        if not game_over:
            if fall_time > fall_speed:
                shape.move_down()

                if not board.can_move(shape):
                    shape.y -= 1
                    board.place(shape)
                    cleared = board.clear_full_rows()

                    if cleared > 0:
                        lines_cleared += cleared
                        score += cleared * 100
                        level = lines_cleared // 5 + 1
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
                        lines_cleared += cleared
                        score += cleared * 100
                        level = lines_cleared // 5 + 1
                        fall_speed = max(100, 500 - (level-1)*50)

                    new_shape = create_shape()
                    if not board.can_move(new_shape):
                        game_over = True
                    else:
                        shape = new_shape

        screen.fill(BLACK)
        board.draw(screen, shape)
        draw_ui(screen, font_score, font_label, font_value, score, level, lines_cleared)

        if game_over:
            go_font = pygame.font.Font(None, 50)
            text = go_font.render("GAME OVER - Press Any Key to Restart", True, RED)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()/2, SCREEN_HEIGHT//2))

        pygame.display.flip()



# ======================================================
#                     MAIN FUNCTION
# ======================================================
## @brief Starts the game.
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    show_menu(screen)
    pygame.quit()

if __name__ == "__main__":
    main()