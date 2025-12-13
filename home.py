import pygame
import sys

# ------------------- الثوابت -------------------
SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
LIGHT_RED = (230, 80, 80)
SILVER = (191, 191, 191)

font_path = "font/Audiowide-Regular.ttf"

# ------------------- زرار -------------------
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
        is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.hover_color if is_hovered else self.color
        if self.filled:
            pygame.draw.rect(surface, current_color, self.rect, border_radius=self.border_radius)
        else:
            pygame.draw.rect(surface, current_color, self.rect, 2, border_radius=self.border_radius)
        label = font.render(self.text, True, self.text_color)
        surface.blit(label, (self.rect.centerx - label.get_width()/2, self.rect.centery - label.get_height()/2))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

# ------------------- دالة Home Page -------------------
def show_home(screen):
    pygame.font.init()
    title_font = pygame.font.Font(font_path, 80)
    button_font = pygame.font.Font(font_path, 32)

    # تجهيز الزرار
    start_button = Button("Start Game", 320)
    leaderboard_button = Button("Leaderboard", 400)
    about_button = Button("About Us", 480)
    exit_button = Button("Exit", 580, width=200, color=RED, text_color=WHITE, hover_color=LIGHT_RED, filled=True)

    buttons = [start_button, leaderboard_button, about_button, exit_button]

    running = True
    while running:
        screen.fill(BLACK)

        # رسم العنوان
        title = title_font.render("Welcome", True, WHITE)
        name = pygame.font.Font(font_path, 40).render("Tetris", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()/2, 120))
        screen.blit(name, (SCREEN_WIDTH//2 - name.get_width()/2, 230))

        # رسم الزرار
        for btn in buttons:
            btn.draw(screen, button_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # التعامل مع الضغط على الزرار
            if start_button.is_clicked(event):
                running = False  # نخرج من Home وتبدأ اللعبة
            if leaderboard_button.is_clicked(event):
                print("Leaderboard pressed")  # مؤقتاً، ممكن تضيف صفحة حقيقية لاحقاً
            if about_button.is_clicked(event):
                print("About Us pressed")  # مؤقتاً
            if exit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        pygame.display.flip()

pygame.quit()
