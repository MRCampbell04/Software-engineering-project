import pygame
import sys

class LoginScreen:
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_WIDTH = 440
        self.SCREEN_HEIGHT = 750

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.DARK_GREY = (51, 51, 51)
        self.RED = (211, 47, 47)
        self.GREEN = (118, 255, 3)
        self.BLUE = (33, 150, 243)
        self.AMBER = (255, 193, 7)

        # Fonts
        self.font_path = "font/Audiowide-Regular.ttf"
        self.title_font = pygame.font.Font(self.font_path, 60)
        self.label_font = pygame.font.Font(self.font_path, 20)
        self.input_font = pygame.font.Font(self.font_path, 24)
        self.btn_font = pygame.font.Font(self.font_path, 22)
        #icon 
        window_icon = pygame.image.load("images/1.png") 
        pygame.display.set_icon(window_icon)

        # Input
        self.user_text = ""
        self.input_rect = pygame.Rect(40, 420, 360, 50)
        self.is_active = True

        # Flags
        self.continue_pressed = False  # detect Continue button click

        # Load continue icon
        self.continue_icon = pygame.image.load("images/Continue.png")
        self.continue_icon = pygame.transform.scale(self.continue_icon, (35, 35))
        self.continue_rect = self.continue_icon.get_rect(center=(285, 515))

    def draw_header_shapes(self):
        block_size = 30
        # Red blocks
        start_x_red = 60
        start_y_red = 150
        pygame.draw.rect(self.screen, self.RED, (start_x_red, start_y_red, block_size, block_size))
        pygame.draw.rect(self.screen, self.RED, (start_x_red + block_size + 2, start_y_red, block_size, block_size))
        pygame.draw.rect(self.screen, self.RED, (start_x_red + (block_size * 2) + 4, start_y_red, block_size, block_size))
        pygame.draw.rect(self.screen, self.RED, (start_x_red + (block_size * 2) + 4, start_y_red + block_size + 2, block_size, block_size))
        # Green blocks
        start_x_green = 200
        start_y_green = 80
        pygame.draw.rect(self.screen, self.GREEN, (start_x_green, start_y_green, block_size, block_size))
        pygame.draw.rect(self.screen, self.GREEN, (start_x_green, start_y_green + block_size + 2, block_size, block_size))
        pygame.draw.rect(self.screen, self.GREEN, (start_x_green, start_y_green + (block_size * 2) + 4, block_size, block_size))
        pygame.draw.rect(self.screen, self.GREEN, (start_x_green + block_size + 2, start_y_green + block_size + 2, block_size, block_size))
        # Blue blocks
        start_x_blue = 300
        start_y_blue = 170
        pygame.draw.rect(self.screen, self.BLUE, (start_x_blue, start_y_blue, block_size, block_size))
        pygame.draw.rect(self.screen, self.BLUE, (start_x_blue + block_size + 2, start_y_blue, block_size, block_size))
        pygame.draw.rect(self.screen, self.BLUE, (start_x_blue, start_y_blue + block_size + 2, block_size, block_size))
        pygame.draw.rect(self.screen, self.BLUE, (start_x_blue + block_size + 2, start_y_blue + block_size + 2, block_size, block_size))

    def draw_mini_grid(self, x, y, color):
        size = 10
        gap = 2
        positions = [(0,0), (1,0), (0,1), (1,1)]
        for r, c in positions:
            pygame.draw.rect(self.screen, color, (x + (size+gap)*c, y + (size+gap)*r, size, size))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.is_active = True
            else:
                self.is_active = False

            if self.continue_rect.collidepoint(event.pos):
                self.continue_pressed = True

        if event.type == pygame.KEYDOWN and self.is_active:
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            elif event.key == pygame.K_RETURN:
                self.continue_pressed = True
            else:
                if len(self.user_text) < 20:
                    self.user_text += event.unicode

    def draw(self):
        self.screen.fill(self.BLACK)
        self.draw_header_shapes()
        # Title
        title_surf = self.title_font.render("CubeTicks", True, self.WHITE)
        self.screen.blit(title_surf, (self.SCREEN_WIDTH//2 - title_surf.get_width()//2, 280))
        # Input label
        label_surf = self.label_font.render("User Name", True, self.WHITE)
        self.screen.blit(label_surf, (self.input_rect.x, self.input_rect.y - 30))
        # Input box
        pygame.draw.rect(self.screen, self.DARK_GREY, self.input_rect, border_radius=8)
        text_surface = self.input_font.render(self.user_text, True, self.WHITE)
        self.screen.blit(text_surface, (self.input_rect.x + 10, self.input_rect.y + 10))
        # Cursor
        if self.is_active and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = self.input_rect.x + 10 + text_surface.get_width()
            pygame.draw.line(self.screen, self.WHITE, (cursor_x, self.input_rect.y + 10), (cursor_x, self.input_rect.y + 40), 2)
        # Continue button
        cont_text = self.btn_font.render("Continue", True, self.WHITE)
        self.screen.blit(self.continue_icon, self.continue_rect)
        self.screen.blit(cont_text, (self.SCREEN_WIDTH//2 - cont_text.get_width()//2, 500))
        # Footer
        self.draw_mini_grid(65, 680, self.AMBER)
        footer_text = self.label_font.render("Let the games begin!", True, self.WHITE)
        self.screen.blit(footer_text, (self.SCREEN_WIDTH//2 - footer_text.get_width()//2, 680))
        self.draw_mini_grid(350, 680, self.GREEN)

# Run standalone
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((440, 750))
    login = LoginScreen(screen)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            login.handle_event(event)
        login.draw()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()
