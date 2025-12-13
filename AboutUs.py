import pygame
import sys

class AboutUsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_WIDTH = 440
        self.SCREEN_HEIGHT = 750

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.SILVER = (191, 191, 191)
        self.PURPLE = (128, 0, 128)
        self.BLUE_LINE = (0, 0, 255)
        self.RED_LINE = (255, 0, 0)
        self.GREEN_LINE = (0, 255, 0)
        #icon 
        window_icon = pygame.image.load("images/1.png") 
        pygame.display.set_icon(window_icon)

        # Fonts
        self.font_path = "font/Audiowide-Regular.ttf"
        self.project_title_font = pygame.font.Font(self.font_path, 39)
        self.manager_name_font = pygame.font.Font(self.font_path, 20)
        self.scrum_master_font = pygame.font.Font(self.font_path, 16)
        self.team_title_font = pygame.font.Font(self.font_path, 15)
        self.member_name_font = pygame.font.Font(self.font_path, 11)

        # Teams data
        self.teams_data = {
            "Arc Team": ["Bassel Mohamed", "Ahmed Ezzat", "Mohamed Essam", "Mohamed Shabana", "Amr Ashraf", "Eslem Hossam", "Yousef Elsery"],
            "Dev Team A": ["Hoda Ghonem", "Maysan Mohamed", "Dina Elhami", "Yasmine Saber", "Menna Usama"],
            "Dev Team B": ["Omar Gazr", "Mohmed Metwaly", "Ahmed Hosny", "Ahmed Nagy", "Ahmed Desouki", "Gamal Afifi"],
            "Dev Team C": ["Elsayed Mohamed", "Eyad Mohamed", "Abdelrahman Garhy", "Ahmed Hamada", "Mina Atef"],
            "Testing A": ["Menna Nasr", "Maryam Gharib", "Ruba Mohamed", "Aya Ibrahim", "Monia Nasry"],
            "Testing B": ["Yousef Zidan", "Ahmed Walid", "Omar Mosed", "Mohamed Samy", "Abram Michel", "Ali Mansour"],
            "Doc Team": ["Ahmed Shelby", "Ahmed Osama", "Ahmed Samaha", "Ahmed Beheiry", "Omar Shwareb"],
            "Integration Team": ["Alaa Naiem", "Omar Mohsen", "Daivid Azmy", "Omar Elamir", "Mahmoud Said"],
            "Deployment Team": ["Tasneem Elashry", "Loay Zakria", "Yousef Gabal"]
        }

        # Load back icon
        self.back_icon = pygame.image.load("images/Back_Icon.png")
        self.back_icon = pygame.transform.scale(self.back_icon, (35, 35))
        self.back_rect = self.back_icon.get_rect(center=(20, 30))

        # Flag
        self.back_pressed = False

    def draw_team_list(self, title, members, x_start, y_start):
        y = y_start
        title_label = self.team_title_font.render(title + ":", True, self.WHITE)
        self.screen.blit(title_label, (x_start, y))
        y += self.team_title_font.get_height() + 5
        for member in members:
            member_label = self.member_name_font.render("• " + member, True, self.SILVER)
            self.screen.blit(member_label, (x_start, y))
            y += self.member_name_font.get_height() - 1
        return y + 5

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                self.back_pressed = True

    def draw(self):
        self.screen.fill(self.BLACK)
        # Draw back icon
        self.screen.blit(self.back_icon, self.back_rect)
        # Project title
        title_label = self.project_title_font.render("Project Manger", True, self.WHITE)
        self.screen.blit(title_label, (self.SCREEN_WIDTH//2 - title_label.get_width()//2, 35))
        manager_label = self.manager_name_font.render("Dr. Mustafa Herajy", True, self.SILVER)
        self.screen.blit(manager_label, (self.SCREEN_WIDTH//2 - manager_label.get_width()//2, 90))
        scrum_label = self.scrum_master_font.render("Scrum Master: Shahd Shaher", True, self.WHITE)
        self.screen.blit(scrum_label, (self.SCREEN_WIDTH//3 - scrum_label.get_width()//2, 125))
        # Draw teams
        y_cursor = 165
        x_col1 = 20
        x_col2 = self.SCREEN_WIDTH // 2 + 10

        y_end_arc = self.draw_team_list("Arc Team", self.teams_data["Arc Team"], x_col1, y_cursor)
        y_end_devA = self.draw_team_list("Dev Team A", self.teams_data["Dev Team A"], x_col2, y_cursor)
        y_line1 = max(y_end_arc, y_end_devA)
        pygame.draw.line(self.screen, self.BLUE_LINE, (20, y_line1), (self.SCREEN_WIDTH - 20, y_line1), 2)
        y_cursor = y_line1 + 15

        y_end_devB = self.draw_team_list("Dev Team B", self.teams_data["Dev Team B"], x_col1, y_cursor)
        y_end_devC = self.draw_team_list("Dev Team C", self.teams_data["Dev Team C"], x_col2, y_cursor)
        y_line2 = max(y_end_devB, y_end_devC)
        pygame.draw.line(self.screen, self.RED_LINE, (20, y_line2), (self.SCREEN_WIDTH - 20, y_line2), 2)
        y_cursor = y_line2 + 15

        y_end_testingA = self.draw_team_list("Testing A", self.teams_data["Testing A"], x_col1, y_cursor)
        y_end_testingB = self.draw_team_list("Testing B", self.teams_data["Testing B"], x_col2, y_cursor)
        y_line3 = max(y_end_testingA, y_end_testingB)
        pygame.draw.line(self.screen, self.GREEN_LINE, (20, y_line3), (self.SCREEN_WIDTH - 20, y_line3), 2)
        y_cursor = y_line3 + 15

        y_end_doc = self.draw_team_list("Doc Team", self.teams_data["Doc Team"], x_col1, y_cursor)
        y_end_integration = self.draw_team_list("Integration Team", self.teams_data["Integration Team"], x_col2, y_cursor)
        y_line4 = max(y_end_doc, y_end_integration)
        pygame.draw.line(self.screen, self.PURPLE, (20, y_line4), (self.SCREEN_WIDTH - 20, y_line4), 2)
        y_cursor = y_line4 + 15

        self.draw_team_list("Deployment Team", self.teams_data["Deployment Team"], x_col1, y_cursor)

# Run standalone
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((440, 750))
    about = AboutUsScreen(screen)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            about.handle_event(event)
        about.draw()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

