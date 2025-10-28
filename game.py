"""
game.py
-------
A short and simple Tetris controller that uses the provided
Board (UI) and Shape (logic) modules.

This file keeps logic minimal: one falling piece, left/right/down
movement, automatic fall, simple landing detection and restart.
"""

import pygame
from board import Board as BoardUI
from shapes import Shape

# Basic settings
SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750
FPS = 60
FALL_SPEED_MS = 500  # piece falls every 500 ms by default


class Game:
    """Minimal Tetris-like game controller."""

    def __init__(self):
        """Initialize pygame, screen, boards, piece and timers."""
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris - Simple")

        # UI board draws grid and UI boxes (from board.py)
        self.ui_board = BoardUI()

        # Shape from shapes.py (single block implementation supplied)
        self.shape = Shape(x=4, y=0, color=(0, 255, 255))

        # Timing and control
        self.clock = pygame.time.Clock()
        self.fall_timer = 0
        self.fall_speed = FALL_SPEED_MS

        # Game state
        self.running = True
        self.game_over = False

    def process_events(self):
        """Handle events like quit and key presses for restart."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and self.game_over:
                # Restart the game when R is pressed after game over
                if event.key == pygame.K_r:
                    self.reset()

    def handle_input(self):
        """Handle continuous key input (left/right/down)."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.shape.move_left()
            if not self.shape.is_inside_board():
                self.shape.move_right()
        if keys[pygame.K_RIGHT]:
            self.shape.move_right()
            if not self.shape.is_inside_board():
                self.shape.move_left()
        if keys[pygame.K_DOWN]:
            # Soft drop
            self.shape.move_down()
            if not self.shape.is_inside_board():
                self.shape.y -= 1

    def update(self, dt):
        """Update fall timer and move piece down when needed."""
        if self.game_over:
            return

        self.fall_timer += dt
        if self.fall_timer >= self.fall_speed:
            self.shape.move_down()
            self.fall_timer = 0

            # If shape left the board after moving down, revert and end.
            if not self.shape.is_inside_board():
                self.shape.y -= 1
                self.game_over = True

    def draw(self):
        """Draw UI board, shape and overlay messages."""
        self.screen.fill((0, 0, 0))
        self.ui_board.draw_board(self.screen)

        # Draw current shape
        try:
            from shapes import Board as LogicBoard
            logic_board = LogicBoard()
            logic_board.draw(self.screen, self.shape)
        except Exception:
            coords = self.shape.get_coordinates()
            for x, y in coords:
                rect = pygame.Rect(x * 30, y * 30, 30, 30)
                pygame.draw.rect(self.screen, self.shape.color, rect)

        # Display "Game Over" text
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

    def reset(self):
        """Reset game state to initial values."""
        self.shape = Shape(x=4, y=0, color=(0, 255, 255))
        self.fall_timer = 0
        self.game_over = False

    def run(self):
        """Main loop: process events, input, update and draw."""
        while self.running:
            dt = self.clock.tick(FPS)
            self.process_events()

            if not self.game_over:
                self.handle_input()
                self.update(dt)

            self.draw()

        pygame.quit()


if __name__ == "__main__":
    Game().run()

