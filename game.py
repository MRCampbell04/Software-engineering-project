import pygame
from board import Board, draw_ui, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR

def main():
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris Game")

    font_path = "font/Audiowide-Regular.ttf"
    font_score = pygame.font.Font(font_path, 20)
    font_label = pygame.font.Font(font_path, 15)
    font_value = pygame.font.Font(font_path, 16)
    
    board = Board()
    score = 0
    level = 1
    lines = 0
    
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BACKGROUND_COLOR)
        board.draw_board(screen)
        draw_ui(screen, font_score, font_label, font_value, score, level, lines)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
