import pygame

SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750

BLOCK_SIZE = 30
GRID_ROWS = 20
GRID_COLS = 10

GRID_X = (SCREEN_WIDTH - (GRID_COLS * BLOCK_SIZE)) // 2
GRID_Y = SCREEN_HEIGHT - (GRID_ROWS * BLOCK_SIZE) - 5

BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
WHITE = (255, 255, 255)

BACKGROUND_COLOR = BLACK
GRID_COLOR = GRAY

class Board:
##    def __init__(self):
##        self.grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    def draw_board(self, screen):
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                x = GRID_X + c * BLOCK_SIZE
                y = GRID_Y + r * BLOCK_SIZE
                
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)
        
        border_x = GRID_X - 1
        border_y = GRID_Y - 1
        border_width = GRID_COLS * BLOCK_SIZE + 4
        border_height = GRID_ROWS * BLOCK_SIZE + 2
        pygame.draw.rect(screen, WHITE, (border_x, border_y, border_width, border_height), 1)

def draw_ui(screen, font_score, font_label, font_value, score, level, lines):
    
    score_box_width = 180
    score_box_height = 35
    score_box_x = (SCREEN_WIDTH - score_box_width) // 2
    score_box_y = 15
    score_box_rect = pygame.Rect(score_box_x, score_box_y, score_box_width, score_box_height)
    pygame.draw.rect(screen, WHITE, score_box_rect, 2, border_radius=8)
    
    score_text_surf = font_score.render(f"SCORE: {score}", True, WHITE)
    score_text_rect = score_text_surf.get_rect(center=score_box_rect.center)
    screen.blit(score_text_surf, score_text_rect)
    
    window_icon = pygame.image.load("images/1.png") 
    pygame.display.set_icon(window_icon)
 
    pause_icon_img = pygame.image.load("images/pause_icon.png")
    pause_icon_img = pygame.transform.scale(pause_icon_img, (35, 35))
    pause_icon_rect = pause_icon_img.get_rect(center=(400, 35))
    screen.blit(pause_icon_img, pause_icon_rect)
   
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

    grid_right = GRID_X + (GRID_COLS * BLOCK_SIZE)
    
    next_box_width = 120
    next_box_x = grid_right - next_box_width - 5
    next_label = font_label.render("NEXT", True, WHITE)
    next_label_x = next_box_x + 17 + (next_box_width - next_label.get_width()) // 2
    screen.blit(next_label, (next_label_x, 70))
    next_box_rect = pygame.Rect(next_box_x+17, box_top_y, next_box_width, box_height)
    pygame.draw.rect(screen, WHITE, next_box_rect, 1, border_radius=5)

    hold_box_width = 75
    hold_box_x = next_box_x - hold_box_width + 5
    hold_label = font_label.render("HOLD", True, WHITE)
    hold_label_x = hold_box_x  + (hold_box_width - hold_label.get_width()) // 2
    screen.blit(hold_label, (hold_label_x, 70))
    hold_box_rect = pygame.Rect(hold_box_x, box_top_y, hold_box_width, box_height)
    pygame.draw.rect(screen, WHITE, hold_box_rect, 1, border_radius=5)

def main():
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("tetris") #Name of Game
    
    font_path = "font/Audiowide-Regular.ttf"
    font_score = pygame.font.Font(font_path, 20)
    font_label = pygame.font.Font(font_path, 15)
    font_value = pygame.font.Font(font_path, 16)
    
    board = Board()
    
    score = 0
    level = 1
    lines = 0
    
    running = True
    clock = pygame.time.Clock()
    
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

main()