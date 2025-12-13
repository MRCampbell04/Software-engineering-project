import pygame
import sys
import urllib.request
import io

# ---------------- Constants ----------------

SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
LIGHT_RED = (230, 80, 80)
SILVER = (191, 191, 191)

font_path = "font/Audiowide-Regular.ttf"


##
# @brief Loads image from a URL.
#
# @param url Image URL.
# @return Pygame image surface.
##
def load_image_from_url(url):
    with urllib.request.urlopen(url) as response:
        data = response.read()
        return pygame.image.load(io.BytesIO(data)).convert_alpha()


BLUE_ICON_URL = "https://raw.githubusercontent.com/MRCampbell04/Software-engineering-project/Dev-C/images/blue.png"
RED_ICON_URL = "https://raw.githubusercontent.com/MRCampbell04/Software-engineering-project/Dev-C/images/red.png"

blue_icon = None
red_icon = None


##
# @class Button
# @brief Represents a clickable UI button.
##
class Button:
    ##
    # @brief Button constructor.
    ##
    def __init__(self, text, y, width=270, height=50, color=WHITE,
                 text_color=BLACK, hover_color=SILVER, filled=True):

        self.text = text
        self.rect = pygame.Rect(SCREEN_WIDTH//2 - width//2, y, width, height)
        self.color = color
        self.text_color = text_color
        self.hover_color = hover_color
        self.filled = filled
        self.border_radius = 12

    ##
    # @brief Draws the button.
    #
    # @param surface Pygame screen.
    # @param font Font used for text.
    ##
    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

        if self.filled:
            pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        else:
            pygame.draw.rect(surface, color, self.rect, 2, border_radius=self.border_radius)

        label = font.render(self.text, True, self.text_color)
        surface.blit(label, label.get_rect(center=self.rect.center))

    ##
    # @brief Checks if button is clicked.
    #
    # @param event Pygame event.
    # @return True if clicked.
    ##
    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


##
# @brief Displays the home screen.
#
# @param screen Pygame screen surface.
# @return Action selected by user.
##
def show_home(screen):
    global blue_icon, red_icon

    if blue_icon is None:
        blue_icon = load_image_from_url(BLUE_ICON_URL)
        red_icon = load_image_from_url(RED_ICON_URL)

    pygame.font.init()

    title_font = pygame.font.Font(font_path, 70)
    button_font = pygame.font.Font(font_path, 32)

    start_button = Button("Start Game", 320)
    leaderboard_button = Button("Leaderboard", 400)
    about_button = Button("AboutUs", 480)
    exit_button = Button("Exit", 580, width=200, color=RED,
                         text_color=WHITE, hover_color=LIGHT_RED)

    while True:
        screen.fill(BLACK)

        title = title_font.render("CubeTicks", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 180)))

        screen.blit(red_icon, (SCREEN_WIDTH - 90, 40))
        screen.blit(blue_icon, (40, SCREEN_HEIGHT - 100))

        start_button.draw(screen, button_font)
        leaderboard_button.draw(screen, button_font)
        about_button.draw(screen, button_font)
        exit_button.draw(screen, button_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_button.is_clicked(event):
                return "start"
            if leaderboard_button.is_clicked(event):
                return "leaderboard"
            if about_button.is_clicked(event):
                return "about"
            if exit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        pygame.display.flip()