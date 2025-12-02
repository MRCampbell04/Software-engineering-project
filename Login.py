import pygame
import sys
def main():
    pygame.init()

    # --- الثوابت ---
    SCREEN_WIDTH = 440
    SCREEN_HEIGHT = 750

    # الألوان
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARK_GREY = (51, 51, 51)  
    RED = (211, 47, 47)       
    GREEN = (118, 255, 3)     
    BLUE = (33, 150, 243)     
    AMBER = (255, 193, 7)    

    # إعداد الشاشة
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    ###icon game
    window_icon = pygame.image.load("images/1.png") 
    pygame.display.set_icon(window_icon)   
    # --- الخطوط ---
    font_path = "font/Audiowide-Regular.ttf"
    title_font = pygame.font.Font(font_path, 60)
    label_font = pygame.font.Font(font_path, 20)
    input_font = pygame.font.Font(font_path, 24)
    btn_font = pygame.font.Font(font_path, 22)
    user_text = ''
    input_rect = pygame.Rect(40, 420, 360, 50) 
    active_color = WHITE
    passive_color = DARK_GREY
    is_active = True 


    def draw_header_shapes(surface):
        block_size = 30
        
        start_x_red = 60
        start_y_red = 150
        pygame.draw.rect(surface, RED, (start_x_red, start_y_red, block_size, block_size))
        pygame.draw.rect(surface, RED, (start_x_red + block_size + 2, start_y_red, block_size, block_size))
        pygame.draw.rect(surface, RED, (start_x_red + (block_size * 2) + 4, start_y_red, block_size, block_size))
        pygame.draw.rect(surface, RED, (start_x_red + (block_size * 2) + 4, start_y_red + block_size + 2, block_size, block_size))

        start_x_green = 200
        start_y_green = 80
        pygame.draw.rect(surface, GREEN, (start_x_green, start_y_green, block_size, block_size))
        pygame.draw.rect(surface, GREEN, (start_x_green, start_y_green + block_size + 2, block_size, block_size))
        pygame.draw.rect(surface, GREEN, (start_x_green, start_y_green + (block_size * 2) + 4, block_size, block_size))
        pygame.draw.rect(surface, GREEN, (start_x_green + block_size + 2, start_y_green + block_size + 2, block_size, block_size))

        start_x_blue = 300
        start_y_blue = 170
        pygame.draw.rect(surface, BLUE, (start_x_blue, start_y_blue, block_size, block_size))
        pygame.draw.rect(surface, BLUE, (start_x_blue + block_size + 2, start_y_blue, block_size, block_size))
        pygame.draw.rect(surface, BLUE, (start_x_blue, start_y_blue + block_size + 2, block_size, block_size))
        pygame.draw.rect(surface, BLUE, (start_x_blue + block_size + 2, start_y_blue + block_size + 2, block_size, block_size))

    def draw_mini_grid(surface, x, y, color):
        size = 10
        gap = 2
        positions = [(0,0), (1,0), (0,1), (1,1)]
        for r, c in positions:
            pygame.draw.rect(surface, color, (x + (size+gap)*c, y + (size+gap)*r, size, size))

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    is_active = True
                else:
                    is_active = False
                
                continue_rect = pygame.Rect(SCREEN_WIDTH//2 - 70, 500, 140, 40) 
                if continue_rect.collidepoint(event.pos):
                    print(f"Logging in with name: {user_text}")
                    
            if event.type == pygame.KEYDOWN:
                if is_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        print(f"Submitted: {user_text}")
                    else:
                        if len(user_text) < 20:
                            user_text += event.unicode

        draw_header_shapes(screen)
        
        title_surf = title_font.render("TETRIS", True, WHITE)
        screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 280))

        label_surf = label_font.render("User Name", True, WHITE)
        screen.blit(label_surf, (input_rect.x, input_rect.y - 30))
        
        pygame.draw.rect(screen, DARK_GREY, input_rect, border_radius=8)
        text_surface = input_font.render(user_text, True, WHITE)
        screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))
        
        if is_active and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = input_rect.x + 10 + text_surface.get_width()
            pygame.draw.line(screen, WHITE, (cursor_x, input_rect.y + 10), (cursor_x, input_rect.y + 40), 2)

        cont_text = btn_font.render("Continue ", True, WHITE)
        pause_icon_img = pygame.image.load("images/Continue.png")
        pause_icon_img = pygame.transform.scale(pause_icon_img, (35, 35))
        pause_icon_rect = pause_icon_img.get_rect(center=(285, 515))
        screen.blit(pause_icon_img, pause_icon_rect)
        screen.blit(cont_text, (SCREEN_WIDTH//2 - cont_text.get_width()//2, 500))
        

        # 5. الفوتر (About)
        draw_mini_grid(screen, 65, 680, AMBER) 
        
        about_text = label_font.render("Let the games begin!", True, WHITE)
        screen.blit(about_text, (SCREEN_WIDTH//2 - about_text.get_width()//2, 680))
        
        draw_mini_grid(screen, 350, 680, GREEN) 

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()
# main()