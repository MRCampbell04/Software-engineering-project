# game.py
import pygame
import sys
from board import Board as UIBoard, draw_ui, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, GRID_X, GRID_Y, BLOCK_SIZE, GRID_ROWS, GRID_COLS
from shapes import Shape

FPS = 60
FALL_SPEED_MS = 500  # default fall speed (ms)

def load_font(path, size):
    try:
        return pygame.font.Font(path, size)
    except Exception:
        return pygame.font.SysFont("Arial", size)

def draw_current_shape(screen, shape):
    # draw shape cells using board's GRID_X, GRID_Y and BLOCK_SIZE
    for (x, y) in shape.get_coordinates():
        if y >= 0:
            px = GRID_X + x * BLOCK_SIZE
            py = GRID_Y + y * BLOCK_SIZE
            rect = pygame.Rect(px, py, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, shape.color, rect)
            pygame.draw.rect(screen, (40, 40, 40), rect, 1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris - Demo")

        # fonts
        # try common folder name variations
        font_candidates = ["font/Audiowide-Regular.ttf", "Font/Audiowide-Regular.ttf"]
        font_path = None
        for p in font_candidates:
            try:
                open(p).close()
                font_path = p
                break
            except Exception:
                continue

        self.font_score = load_font(font_path, 20) if font_path else pygame.font.SysFont("Arial", 20)
        self.font_label = load_font(font_path, 15) if font_path else pygame.font.SysFont("Arial", 15)
        self.font_value = load_font(font_path, 16) if font_path else pygame.font.SysFont("Arial", 16)

        # UI board
        self.ui_board = UIBoard()

        # game objects
        self.current = Shape(x=4, y=0, color=(0, 255, 255))
        self.score = 0
        self.level = 1
        self.lines = 0

        # timing
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
            if not self.current.is_inside_board():
                self.current.move_right()
        if keys[pygame.K_RIGHT]:
            self.current.move_right()
            if not self.current.is_inside_board():
                self.current.move_left()
        if keys[pygame.K_DOWN]:
            # soft drop
            self.current.move_down()
            if not self.current.is_inside_board():
                self.current.y -= 1

        if keys[pygame.K_SPACE]:
            # hard drop (move down until would leave board)
            while self.current.is_inside_board():
                self.current.move_down()
            self.current.y -= 1
            # after hard drop, spawn new piece next loop
            self.spawn_new_piece()

    def spawn_new_piece(self):
        self.current = Shape(x=GRID_COLS // 2, y=0, color=(0, 255, 255))

    def update(self, dt):
        if self.game_over or self.paused:
            return

        self.fall_timer += dt
        if self.fall_timer >= self.fall_speed:
            self.current.move_down()
            self.fall_timer = 0

            if not self.current.is_inside_board():
                # revert
                self.current.y -= 1
                # simple landing behavior: spawn new piece
                # (no stacking/line-clear in this demo)
                # if the piece is at top and cannot move -> game over
                if self.current.y <= 0:
                    self.game_over = True
                else:
                    self.spawn_new_piece()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        # draw UI board and UI elements
        self.ui_board.draw_board(self.screen)
        draw_ui(self.screen, self.font_score, self.font_label, self.font_value, self.score, self.level, self.lines)

        # draw current falling piece
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
        self.current = Shape(x=GRID_COLS // 2, y=0, color=(0, 255, 255))
        self.score = 0
        self.level = 1
        self.lines = 0
        self.fall_timer = 0
        self.game_over = False
        self.paused = False

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
