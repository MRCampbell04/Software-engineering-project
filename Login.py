import pygame
import sys


##
# @class LoginScreen
# @brief Displays and manages login input.
##
class LoginScreen:

    ##
    # @brief Constructor for LoginScreen.
    #
    # @param screen Pygame display surface.
    ##
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_WIDTH = 440
        self.SCREEN_HEIGHT = 750

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.font_path = "font/Audiowide-Regular.ttf"
        self.title_font = pygame.font.Font(self.font_path, 60)
        self.input_font = pygame.font.Font(self.font_path, 24)

        window_icon = pygame.image.load("images/1.png")
        pygame.display.set_icon(window_icon)

        self.user_text = ""
        self.input_rect = pygame.Rect(40, 420, 360, 50)
        self.is_active = True
        self.continue_pressed = False

    ##
    # @brief Handles keyboard and mouse events.
    #
    # @param event Pygame event.
    ##
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.is_active:
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            elif event.key == pygame.K_RETURN:
                self.continue_pressed = True
            else:
                self.user_text += event.unicode

    ##
    # @brief Draws login screen.
    ##
    def draw(self):
        self.screen.fill(self.BLACK)

        title = self.title_font.render("CubeTicks", True, self.WHITE)
        self.screen.blit(title, (self.SCREEN_WIDTH//2 - title.get_width()//2, 280))

        pygame.draw.rect(self.screen, (50, 50, 50), self.input_rect)
        text_surface = self.input_font.render(self.user_text, True, self.WHITE)
        self.screen.blit(text_surface, (self.input_rect.x + 10, self.input_rect.y + 10))