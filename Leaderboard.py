import pygame
import json
import os

class LeaderboardScreen:
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_WIDTH = 440
        self.SCREEN_HEIGHT = 750
        self.font_path = "font/Audiowide-Regular.ttf"  
        #icon 
        window_icon = pygame.image.load("images/1.png") 
        pygame.display.set_icon(window_icon)

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.NEON_GREEN = (180, 255, 0)
        self.GRAY = (100, 100, 100)
        self.AMBER = (255, 193, 7)

        self.title_font = pygame.font.Font(self.font_path, 40)
        self.entry_font = pygame.font.Font(self.font_path, 20)
        self.score_font = pygame.font.Font(self.font_path, 16)
        
        self.file_name = "leaderboard_data.json"
        self.scores = self.load_scores()
        
        self.back_pressed = False
        self.back_rect = pygame.Rect(20, 40, 40, 40)

        self.trophy_img = pygame.image.load('images/trophy.png') 
        self.trophy_img = pygame.transform.scale(self.trophy_img, (50, 50))
        self.trophy_rect = self.trophy_img.get_rect(center=(220, 100))
    def draw_mini_grid(self, x, y, color):
        size = 10
        gap = 2
        positions = [(0,0), (1,0), (0,1), (1,1)]
        for r, c in positions:
            pygame.draw.rect(self.screen, color, (x + (size+gap)*c, y + (size+gap)*r, size, size))

    def load_scores(self):
        if not os.path.exists(self.file_name):
            return []
        try:
            with open(self.file_name, 'r') as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                return sorted(data, key=lambda x: x['score'], reverse=True)
        except Exception as e:
            return []

    def save_score(self, name, score):
        normalized_name = name.lower()

        existing = None
        for entry in self.scores:
            if entry['name'].lower() == normalized_name:
                existing = entry
                break

        if existing:
            if score > existing['score']:
                existing['score'] = score
        else:
            self.scores.append({'name': name, 'score': score})

        self.scores = sorted(self.scores, key=lambda x: x['score'], reverse=True)

        with open(self.file_name, 'w') as f:
            json.dump(self.scores, f)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                self.back_pressed = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.back_pressed = True

    def draw(self, current_user_name=None, current_user_score=0):
        self.screen.fill(self.BLACK)

        self.back_icon = pygame.image.load("images/Back_Icon.png")
        self.back_icon = pygame.transform.scale(self.back_icon, (35, 35))
        self.back_rect = self.back_icon.get_rect(center=(20, 30))
        self.screen.blit(self.back_icon, self.back_rect)

        self.screen.blit(self.trophy_img, self.trophy_rect)
        self.draw_mini_grid(100, 100, self.AMBER)
        self.draw_mini_grid(320, 100, self.AMBER)

        start_y = 180
        top_scores = self.scores[:7]

        for index, entry in enumerate(top_scores):
            y_pos = start_y + (index * 75)

            name_surf = self.entry_font.render(entry['name'], True, self.WHITE)
            self.screen.blit(name_surf, (40, y_pos))

            score_surf = self.score_font.render(f"Score: {entry['score']}", True, self.GRAY)
            self.screen.blit(score_surf, (40, y_pos + 25))

            rank_surf = self.entry_font.render(f"#{index + 1}", True, self.WHITE)
            self.screen.blit(rank_surf, (380, y_pos + 10))

            pygame.draw.line(self.screen, (50, 50, 50), (40, y_pos + 55), (400, y_pos + 55), 1)

        footer_y = 650
        pygame.draw.line(self.screen, self.WHITE, (0, footer_y), (440, footer_y), 2)
        for i in range(0, 440, 20):
            pygame.draw.line(self.screen, self.BLACK, (i, footer_y), (i+10, footer_y), 2)

        if current_user_name:
            curr_name_surf = self.entry_font.render(f"{current_user_name} (You)", True, self.WHITE)
            curr_score_surf = self.score_font.render(f"Score: {current_user_score}", True, self.GRAY)

            try:
                user_rank = next(i+1 for i, entry in enumerate(self.scores)
                                if entry['name'] == current_user_name and entry['score'] == current_user_score)
            except StopIteration:
                user_rank = len(self.scores) + 1

            rank_surf = self.entry_font.render(f"#{user_rank}", True, self.WHITE)

            self.screen.blit(curr_name_surf, (40, footer_y + 30))
            self.screen.blit(curr_score_surf, (40, footer_y + 55))
            self.screen.blit(rank_surf, (380, footer_y + 40))