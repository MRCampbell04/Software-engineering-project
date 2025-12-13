import pygame
import sys


##
# @class AboutUsScreen
# @brief Handles rendering and interaction of the About Us screen.
##
class AboutUsScreen:

    ##
    # @brief Constructor for AboutUsScreen.
    #
    # @param screen Pygame display surface.
    ##
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_WIDTH = 440
        self.SCREEN_HEIGHT = 750

        # -------- Colors --------
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.SILVER = (191, 191, 191)
        self.PURPLE = (128, 0, 128)
        self.BLUE_LINE = (0, 0, 255)
        self.RED_LINE = (255, 0, 0)
        self.GREEN_LINE = (0, 255, 0)

        # Window icon
        window_icon = pygame.image.load("images/1.png")
        pygame.display.set_icon(window_icon)

        # -------- Fonts --------
        self.font_path = "font/Audiowide-Regular.ttf"
        self.project_title_font = pygame.font.Font(self.font_path, 39)
        self.manager_name_font = pygame.font.Font(self.font_path, 20)
        self.scrum_master_font = pygame.font.Font(self.font_path, 16)
        self.team_title_font = pygame.font.Font(self.font_path, 15)
        self.member_name_font = pygame.font.Font(self.font_path, 11)

        # -------- Teams Data --------
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

        # Back button
        self.back_icon = pygame.image.load("images/Back_Icon.png")
        self.back_icon = pygame.transform.scale(self.back_icon, (35, 35))
        self.back_rect = self.back_icon.get_rect(center=(20, 30))

        self.back_pressed = False

    ##
    # @brief Draws a team list with its members.
    #
    # @param title Team name.
    # @param members List of team members.
    # @param x_start X position.
    # @param y_start Y position.
    #
    # @return Ending Y position.
    ##
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

    ##
    # @brief Handles mouse click events.
    #
    # @param event Pygame event.
    ##
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                self.back_pressed = True

    ##
    # @brief Draws the About Us screen.
    ##
    def draw(self):
        self.screen.fill(self.BLACK)
        self.screen.blit(self.back_icon, self.back_rect)

        title_label = self.project_title_font.render("Project Manager", True, self.WHITE)
        self.screen.blit(title_label, (self.SCREEN_WIDTH//2 - title_label.get_width()//2, 35))

        manager_label = self.manager_name_font.render("Dr. Mustafa Herajy", True, self.SILVER)
        self.screen.blit(manager_label, (self.SCREEN_WIDTH//2 - manager_label.get_width()//2, 90))

        scrum_label = self.scrum_master_font.render("Scrum Master: Shahd Shaher", True, self.WHITE)
        self.screen.blit(scrum_label, (self.SCREEN_WIDTH//3 - scrum_label.get_width()//2, 125))

        y_cursor = 165
        x_col1 = 20
        x_col2 = self.SCREEN_WIDTH // 2 + 10

        y1 = self.draw_team_list("Arc Team", self.teams_data["Arc Team"], x_col1, y_cursor)
        y2 = self.draw_team_list("Dev Team A", self.teams_data["Dev Team A"], x_col2, y_cursor)
        pygame.draw.line(self.screen, self.BLUE_LINE, (20, max(y1, y2)), (self.SCREEN_WIDTH - 20, max(y1, y2)), 2)