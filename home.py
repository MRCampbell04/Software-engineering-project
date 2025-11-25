import pygame

pygame.init()

# ------------------ Constants ------------------

##
# @brief Screen width.
#
SCREEN_WIDTH = 440

##
# @brief Screen height.
#
SCREEN_HEIGHT = 750

##
# @brief RGB color definitions.
#
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
LIGHT_RED = (230, 80, 80)
SILVER = (191, 191, 191)

##
# @brief Path to the game font file.
#
font_path = "font/Audiowide-Regular.ttf"

# ------------------ Screen & Fonts ------------------

##
# @brief Creates the main window and loads fonts.
#
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

title_font = pygame.font.Font(font_path, 80)
button_font = pygame.font.Font(font_path, 32)
game_font = pygame.font.Font(font_path, 40)

##
# @brief Loads the game icon.
#
window_icon = pygame.image.load("images/1.png")
pygame.display.set_icon(window_icon)

# ------------------ Icon Loading ------------------

##
# @brief Loads and scales UI icons (red & blue).
#
try:
    red_icon = pygame.image.load("images/red.png")
    blue_icon = pygame.image.load("images/blue.png")
    red_icon = pygame.transform.scale(red_icon, (125, 85))
    blue_icon = pygame.transform.scale(blue_icon, (125, 85))
except:
    red_icon = blue_icon = None

# ------------------ Button Class ------------------

##
# @class Button
# @brief Represents a clickable UI button in the menu.
#
class Button:

    ##
    # @brief Initializes button properties.
    # @param text Button text.
    # @param y Vertical position.
    # @param width Button width.
    # @param height Button height.
    # @param color Button color.
    # @param text_color Color of the text.
    # @param hover_color Color when hovered.
    # @param filled Whether button is filled or outlined.
    #
    def __init__(self, text, y, width=270, height=50, color=WHITE, text_color=WHITE, hover_color=None, filled=False):
        self.text = text
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color
        self.hover_color = hover_color or color
        self.filled = filled
        self.rect = pygame.Rect(SCREEN_WIDTH//2 - width//2, y, width, height)
        self.border_radius = 12

    ##
    # @brief Draws the button on the screen.
    # @param surface The display surface.
    #
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.hover_color if is_hovered else self.color

        if self.filled:
            pygame.draw.rect(surface, current_color, self.rect, border_radius=self.border_radius)
        else:
            pygame.draw.rect(surface, current_color, self.rect, 2, border_radius=self.border_radius)

        label = button_font.render(self.text, True, self.text_color)
        surface.blit(label, (self.rect.centerx - label.get_width()/2,
                             self.rect.centery - label.get_height()/2))

    ##
    # @brief Checks if the button was clicked.
    # @param event Mouse click event.
    # @return True if clicked.
    #
    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

# ------------------ Buttons Setup ------------------

##
# @brief Creates all menu buttons.
#
buttons = [
    Button("Start Game", 320, text_color=BLACK, hover_color=SILVER, filled=True),
    Button("Leaderboard", 400, text_color=BLACK, hover_color=SILVER, filled=True),
    Button("AboutUs", 480, text_color=BLACK, hover_color=SILVER, filled=True),
    Button("Exit", 580, width=200, color=RED, text_color=WHITE, hover_color=LIGHT_RED, filled=True)
]

# ------------------ Main Loop ------------------

##
# @brief Main menu loop: draws elements and handles events.
#
running = True
while running:
    screen.fill(BLACK)

    if red_icon:
        screen.blit(red_icon, (305, 20))
    if blue_icon:
        screen.blit(blue_icon, (20, 650))

    Title = title_font.render("Welcome", True, WHITE)
    Name_Of_Game = game_font.render("Tetris", True, WHITE)

    screen.blit(Title, (SCREEN_WIDTH//2 - Title.get_width()/2, 120))
    screen.blit(Name_Of_Game, (SCREEN_WIDTH//2 - Name_Of_Game.get_width()/2, 230))

    for btn in buttons:
        btn.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

# ------------------ Quit Game ------------------
pygame.quit()