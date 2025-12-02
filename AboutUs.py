import pygame
import sys 

pygame.init()

#الثوابت الخاصة بالالوان وابعاد الشاشة والخط
SCREEN_WIDTH = 440
SCREEN_HEIGHT = 750

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SILVER = (191, 191, 191)

PURPLE = (128, 0, 128) 
BLUE_LINE = (0, 0, 255) 
RED_LINE = (255, 0, 0) 
GREEN_LINE = (0, 255, 0)

font_path = "font/Audiowide-Regular.ttf" #######################

#عرض الشاشة
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris") 

project_title_font = pygame.font.Font(font_path, 39) 
manager_name_font = pygame.font.Font(font_path, 20)
scrum_master_font = pygame.font.Font(font_path, 16) 
team_title_font = pygame.font.Font(font_path, 15) 
member_name_font = pygame.font.Font(font_path, 11) 

#ايكون الرجوع
Back_Icon_orig = pygame.image.load("images/Back_Icon.png") 
Back_Icon_img = pygame.transform.scale(Back_Icon_orig, (35, 35))
 
#function خاصة بالاسامي 
def aboutus_screen():
    
    project_title = "Project Manger"
    project_manager = "Dr. Mustafa Herajy"
    scrum_master = "Shahd Shaher"

    teams_data = {
        "Arc Team": ["Bassel Mohamed", "Ahmed Ezzat", "Mohamed Essam", "Mohamed Shabana", "Amr Ashraf", "Eslem Hossam", "Yousef Elsery"],
        "Dev Team A": ["Hoda Ghonem", "Maysan Mohamed", "Dina Elhami", "Yasmine Saber", "Menna Usama"],
        "Dev Team B": ["Omar Gazr", "Mohmed Metwaly", "Ahmed Hosny", "Ahmed Nagy", "Ahmed Desouki", "Gamal Afifi"],
        "Dev Team C": ["Elsayed Mohamed", "Eyad Taha", "Abdelrahman Garhy", "Ahmed Hamada", "Mina Atef"],
        "Testing A": ["Menna Nasr", "Maryam Gharib", "Ruba Mohamed", "Aya Ibrahim", "Monia Nasry"],
        "Testing B": ["Yousef Zidan", "Ahmed Walid", "Omar Mosed", "Mohamed Samy", "Abram Michel", "Ali Mansour"],
        "Doc Team": ["Ahmed Shelby", "Ahmed Osama", "Ahmed Samaha", "Ahmed Beheiry", "Omar Shwareb"],
        "Integration Team": ["Alaa Naiem", "Omar Mohsen", "Daivid Azmy", "Omar Elamir", "Mahmoud Said"],
        "Deployment Team": ["Tasneem Elashry", "Loay Zakria", "Yousef Gabal"]
    }

    def draw_team_list(surface, title, members, x_start, y_start, font_title, font_member):
        y = y_start
        title_label = font_title.render(title + ":", True, WHITE)
        surface.blit(title_label, (x_start, y))
        y += font_title.get_height() + 5
        
        for member in members:
            member_label = font_member.render("• " + member, True, SILVER)
            surface.blit(member_label, (x_start, y))
            y += font_member.get_height() - 1 
        
        return y + 5

    back_button_rect = pygame.Rect(10, 20, 60, 50) 

    running_screen = True
    while running_screen:
        screen.fill(BLACK)
        
        Back_Icon_rect = Back_Icon_img.get_rect(center=(20, 30))
        screen.blit(Back_Icon_img, Back_Icon_rect)

        manager_title_label = project_title_font.render(project_title, True, WHITE)
        screen.blit(manager_title_label, (SCREEN_WIDTH//2- manager_title_label.get_width()//2, 35))
        
        manager_name_label = manager_name_font.render(project_manager, True, SILVER)
        screen.blit(manager_name_label, (SCREEN_WIDTH//2 - manager_name_label.get_width()//2, 90))
        
        scrum_master_label = scrum_master_font.render("Scrum Master: " + scrum_master, True, WHITE)
        screen.blit(scrum_master_label, (SCREEN_WIDTH//3 - scrum_master_label.get_width()//2, 125))


        pygame.draw.line(screen, PURPLE, (20, 150), (SCREEN_WIDTH - 20, 150), 2)

        y_cursor = 165
        x_col1 = 20
        x_col2 = SCREEN_WIDTH // 2 + 10

        y_end_arc = draw_team_list(screen, "Arc Team", teams_data["Arc Team"], x_col1, y_cursor, team_title_font, member_name_font)
        y_end_devA = draw_team_list(screen, "Dev Team A", teams_data["Dev Team A"], x_col2, y_cursor, team_title_font, member_name_font)
        y_line1 = max(y_end_arc, y_end_devA)
        pygame.draw.line(screen, BLUE_LINE, (20, y_line1), (SCREEN_WIDTH - 20, y_line1), 2)
        y_cursor = y_line1 + 15

        y_end_devB = draw_team_list(screen, "Dev Team B", teams_data["Dev Team B"], x_col1, y_cursor, team_title_font, member_name_font)
        y_end_devC = draw_team_list(screen, "Dev Team C", teams_data["Dev Team C"], x_col2, y_cursor, team_title_font, member_name_font)
        y_line2 = max(y_end_devB, y_end_devC)
        pygame.draw.line(screen, RED_LINE, (20, y_line2), (SCREEN_WIDTH - 20, y_line2), 2)
        y_cursor = y_line2 + 15

        y_end_testingA = draw_team_list(screen, "Testing A", teams_data["Testing A"], x_col1, y_cursor, team_title_font, member_name_font)
        y_end_testingB = draw_team_list(screen, "Testing B", teams_data["Testing B"], x_col2, y_cursor, team_title_font, member_name_font)
        y_line3 = max(y_end_testingA, y_end_testingB)
        pygame.draw.line(screen, GREEN_LINE, (20, y_line3), (SCREEN_WIDTH - 20, y_line3), 2)
        y_cursor = y_line3 + 15

        y_end_doc = draw_team_list(screen, "Doc Team", teams_data["Doc Team"], x_col1, y_cursor, team_title_font, member_name_font)
        y_end_integration = draw_team_list(screen, "Integration Team", teams_data["Integration Team"], x_col2, y_cursor, team_title_font, member_name_font)
        y_line4 = max(y_end_doc, y_end_integration)
        pygame.draw.line(screen, PURPLE, (20, y_line4), (SCREEN_WIDTH - 20, y_line4), 2)
        y_cursor = y_line4 + 15

        draw_team_list(screen, "Deployment Team", teams_data["Deployment Team"], x_col1, y_cursor, team_title_font, member_name_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
