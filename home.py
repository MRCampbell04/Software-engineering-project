import pygame
import sys
import urllib.request
import io

# ------------------- Constants -------------------
SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
LIGHT_RED = (230, 80, 80)
SILVER = (191, 191, 191)

font_path = "font/Audiowide-Regular.ttf"

#icon 
window_icon = pygame.image.load("images/1.png") 
pygame.display.set_icon(window_icon)

# ------------------- Load Images from GitHub -------------------

def load_image_from_url(url):
    with urllib.request.urlopen(url) as response:
        data = response.read()
        image_file = io.BytesIO(data)
        return pygame.image.load(image_file).convert_alpha()

# GitHub images
BLUE_ICON_URL = "https://raw.githubusercontent.com/MRCampbell04/Software-engineering-project/Dev-C/images/blue.png"
RED_ICON_URL = "https://raw.githubusercontent.com/MRCampbell04/Software-engineering-project/Dev-C/images/red.png"

blue_icon = None
red_icon = None


# ------------------- Button Class -------------------
class Button:
    def __init__(self, text, y, width=270, height=50, color=WHITE, text_color=BLACK, hover_color=SILVER, filled=True):
        self.text = text
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color
        self.hover_color = hover_color
        self.filled = filled
        self.rect = pygame.Rect(SCREEN_WIDTH//2 - width//2, y, width, height)
        self.border_radius = 12

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

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN and
            event.button == 1 and
            self.rect.collidepoint(event.pos)
        )


# ------------------- Home Page -------------------
def show_home(screen):
    global blue_icon, red_icon

    if blue_icon is None:
        blue_icon = load_image_from_url(BLUE_ICON_URL)
        red_icon = load_image_from_url(RED_ICON_URL)

    pygame.font.init()

    tetris_font = pygame.font.Font(font_path, 70)
    welcome_font = pygame.font.Font(font_path, 32)
    button_font = pygame.font.Font(font_path, 32)

    start_button = Button("Start Game", 320)
    leaderboard_button = Button("Leaderboard", 400)
    about_button = Button("AboutUs", 480)
    exit_button = Button("Exit", 580, width=200, color=RED,
                         text_color=WHITE, hover_color=LIGHT_RED, filled=True)

    running = True
    while running:
        screen.fill(BLACK)

        # Tetris (Top)
        title = tetris_font.render("CubeTicks", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()/2, 150))

        # Welcome (Under Tetris)
        welcome = welcome_font.render("Welcome", True, WHITE)
        screen.blit(welcome, (SCREEN_WIDTH//2 - welcome.get_width()/2, 250))

        # Draw icons
        screen.blit(red_icon, (SCREEN_WIDTH - red_icon.get_width() - 40, 40))  # top right
        screen.blit(blue_icon, (40, SCREEN_HEIGHT - blue_icon.get_height() - 30))  # bottom left

        # Buttons
        start_button.draw(screen, button_font)
        leaderboard_button.draw(screen, button_font)
        about_button.draw(screen, button_font)
        exit_button.draw(screen, button_font)

        # Events
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

