import pygame

pygame.init()

#دي الثوابت
SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
LIGHT_RED = (230, 80, 80)
SILVER=(191, 191, 191)

font_path = "font/Audiowide-Regular.ttf"

#تجهيز الشاشة و خطوط الكلام
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

title_font = pygame.font.Font(font_path, 80)
button_font = pygame.font.Font(font_path, 32)
game_font = pygame.font.Font(font_path, 40)

###icon game
window_icon = pygame.image.load("images/1.png") 
pygame.display.set_icon(window_icon)    

#استدعاء الايكون وظبط حجمها
try:
    red_icon = pygame.image.load("images/red.png")
    blue_icon = pygame.image.load("images/blue.png")
    red_icon = pygame.transform.scale(red_icon, (125, 85))
    blue_icon = pygame.transform.scale(blue_icon, (125, 85))
except:
    red_icon = blue_icon = None
#كلاس لضبط الزراير وخصائصها
class Button:
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

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.hover_color if is_hovered else self.color

        if self.filled:
            pygame.draw.rect(surface, current_color, self.rect, border_radius=self.border_radius)
        else:
            pygame.draw.rect(surface, current_color, self.rect, 2, border_radius=self.border_radius)

        label = button_font.render(self.text, True, self.text_color)
        surface.blit(label, (self.rect.centerx - label.get_width()/2, self.rect.centery - label.get_height()/2))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)
#تجهيز الازرار (حجم-لون الخط-لون الوقوف على الزرار-الزر ممتلئ اللون)
buttons = [
    Button("Start Game", 320, text_color=BLACK, hover_color=SILVER, filled=True),
    Button("Leaderboard", 400, text_color=BLACK, hover_color=SILVER, filled=True),
    Button("AboutUs", 480, text_color=BLACK, hover_color=SILVER, filled=True),
    Button("Exit", 580, width=200, color=RED, text_color=WHITE, hover_color=LIGHT_RED, filled=True)
]

running = True
#حلقة اللعبة الرئيسية: بنرسم كل حاجة ونتابع الأحداث ونحدث الشاشة
while running:
    screen.fill(BLACK)

    screen.blit(red_icon, (305, 20))
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

#غلق اللعبة
pygame.quit()
