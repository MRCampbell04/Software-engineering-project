import pygame
import sys
import random
from board import Board as UIBoard, draw_ui, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, GRID_X, GRID_Y, BLOCK_SIZE, GRID_ROWS, GRID_COLS
from shapes import Shape

FPS = 60
FALL_SPEED_MS = 500

def load_font(path, size):
    try:
        return pygame.font.Font(path, size)
    except Exception:
        return pygame.font.SysFont("Arial", size)

def draw_current_shape(screen, shape):
    for (x, y) in shape.get_coordinates():
        if y >= 0:
            px = GRID_X + x * BLOCK_SIZE
            py = GRID_Y + y * BLOCK_SIZE
            rect = pygame.Rect(px, py, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, shape.color, rect)
            pygame.draw.rect(screen, (40, 40, 40), rect, 1)

def draw_fixed_blocks(screen, board):
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            color = board[y][x]
            if color:
                px = GRID_X + x * BLOCK_SIZE
                py = GRID_Y + y * BLOCK_SIZE
                rect = pygame.Rect(px, py, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (40, 40, 40), rect, 1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris - Demo")

        font_candidates = ["font/Audiowide-Regular.ttf", "Font/Audiowide-Regular.ttf"]
        font_path = None
        for p in font_candidates:
            try:
                open(p).close()
                font_path = p
                break
            except Exception:
                continue

        self.font_score = load_font(font_path, 20)
        self.font_label = load_font(font_path, 15)
        self.font_value = load_font(font_path, 16)
        self.ui_board = UIBoard()

        self.colors = [
            (0, 255, 255),
            (255, 255, 0),
            (128, 0, 128),
            (0, 255, 0),
            (255, 0, 0),
            (255, 165, 0),
            (0, 0, 255),
        ]

        self.current = Shape(x=4, y=0, color=random.choice(self.colors))
        self.score = 0
        self.level = 1
        self.lines = 0
        self.board = [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

        self.clock = pygame.time.Clock()
        self.fall_speed = FALL_SPEED_MS
        self.fall_timer = 0

        self.running = True
        self.paused = False
        self.game_over = False

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if event.key == pygame.K_r and self.game_over:
                    self.restart()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.current.move_left()
            if not self.is_valid_position():
                self.current.move_right()
        if keys[pygame.K_RIGHT]:
            self.current.move_right()
            if not self.is_valid_position():
                self.current.move_left()
        if keys[pygame.K_DOWN]:
            self.soft_drop()
        if keys[pygame.K_SPACE]:
            self.hard_drop()

    def is_valid_position(self):
        for x, y in self.current.get_coordinates():
            if x < 0 or x >= GRID_COLS or y >= GRID_ROWS:
                return False
            if y >= 0 and self.board[y][x] is not None:
                return False
        return True

    def soft_drop(self):
        self.current.move_down()
        if not self.is_valid_position():
            self.current.y -= 1
            self.lock_piece()
            self.spawn_new_piece()

    def hard_drop(self):
        while self.is_valid_position():
            self.current.move_down()
        self.current.y -= 1
        self.lock_piece()
        self.spawn_new_piece()

    def lock_piece(self):
        for x, y in self.current.get_coordinates():
            if y >= 0 and 0 <= x < GRID_COLS:
                self.board[y][x] = self.current.color
        cleared = self.clear_lines()
        if cleared > 0:
            self.lines += cleared
            self.score += cleared * 100
            if self.lines % 10 == 0:
                self.level += 1
                self.fall_speed = max(100, self.fall_speed - 50)

    def clear_lines(self):
        new_board = []
        cleared = 0
        for y in range(GRID_ROWS):
            if all(self.board[y][x] is not None for x in range(GRID_COLS)):
                cleared += 1
            else:
                new_board.append(self.board[y])
        for _ in range(cleared):
            new_board.insert(0, [None for _ in range(GRID_COLS)])
        self.board = new_board
        return cleared

    def spawn_new_piece(self):
        self.current = Shape(x=GRID_COLS // 2, y=0, color=random.choice(self.colors))
        if not self.is_valid_position():
            self.game_over = True

    def update(self, dt):
        if self.game_over or self.paused:
            return
        self.fall_timer += dt
        if self.fall_timer >= self.fall_speed:
            self.current.move_down()
            if not self.is_valid_position():
                self.current.y -= 1
                self.lock_piece()
                self.spawn_new_piece()
            self.fall_timer = 0

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.ui_board.draw_board(self.screen)
        draw_ui(self.screen, self.font_score, self.font_label, self.font_value, self.score, self.level, self.lines)
        draw_fixed_blocks(self.screen, self.board)
        draw_current_shape(self.screen, self.current)

        if self.paused:
            small = pygame.font.SysFont("Arial", 36)
            text = small.render("PAUSED", True, (255, 255, 0))
            r = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, r)

        if self.game_over:
            font = pygame.font.Font(None, 48)
            text = font.render("GAME OVER", True, (255, 0, 0))
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            self.screen.blit(text, rect)
            small = pygame.font.Font(None, 28)
            tip = small.render("Press R to restart", True, (255, 255, 255))
            rect2 = tip.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(tip, rect2)

        pygame.display.flip()

    def restart(self):
        self.board = [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.current = Shape(x=GRID_COLS // 2, y=0, color=random.choice(self.colors))
        self.score = 0
        self.level = 1
        self.lines = 0
        self.fall_speed = FALL_SPEED_MS
        self.fall_timer = 0
        self.paused = False
        self.game_over = False

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS)
            self.process_events()
            self.handle_input()
            self.update(dt)
            self.draw()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()
