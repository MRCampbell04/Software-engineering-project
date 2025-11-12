import pygame
import sys
import random
from board import Board as UIBoard, draw_ui, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, GRID_X, GRID_Y, BLOCK_SIZE, GRID_ROWS, GRID_COLS
from shapes import Shape

# Constants
FPS = 60
FALL_SPEED_MS = 500

def load_font(path, size):
    try:
        return pygame.font.Font(path, size)
    except:
        return pygame.font.SysFont("arial", size)

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        # Initialize main screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris Game")

        self.clock = pygame.time.Clock()
        self.running = True
        self.ui_board = UIBoard()
        self.current_shape = Shape()
        self.last_fall_time = pygame.time.get_ticks()
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.current_shape.move(-1, 0, self.ui_board)
                elif event.key == pygame.K_RIGHT:
                    self.current_shape.move(1, 0, self.ui_board)
                elif event.key == pygame.K_DOWN:
                    self.current_shape.move(0, 1, self.ui_board)
                elif event.key == pygame.K_UP:
                    self.current_shape.rotate(self.ui_board)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall_time > FALL_SPEED_MS:
            self.current_shape.move(0, 1, self.ui_board)
            if self.current_shape.landed:
                self.ui_board.lock_shape(self.current_shape)
                self.current_shape = Shape()
                self.score += 10
            self.last_fall_time = current_time

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        draw_ui(self.screen, self.ui_board, self.current_shape, self.score)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
