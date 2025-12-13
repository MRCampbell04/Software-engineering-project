import pygame
import json
import os


##
# @class LeaderboardScreen
# @brief Displays the leaderboard screen.
##
class LeaderboardScreen:

    ##
    # @brief Constructor for LeaderboardScreen.
    #
    # @param screen Pygame display surface.
    ##
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_WIDTH = 440
        self.SCREEN_HEIGHT = 750
        self.font_path = "font/Audiowide-Regular.ttf"

        window_icon = pygame.image.load("images/1.png")
        pygame.display.set_icon(window_icon)

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (100, 100, 100)

        self.title_font = pygame.font.Font(self.font_path, 40)
        self.entry_font = pygame.font.Font(self.font_path, 20)
        self.score_font = pygame.font.Font(self.font_path, 16)

        self.file_name = "leaderboard_data.json"
        self.scores = self.load_scores()

        self.back_pressed = False
        self.back_rect = pygame.Rect(20, 40, 40, 40)

    ##
    # @brief Loads scores from JSON file.
    #
    # @return List of scores.
    ##
    def load_scores(self):
        if not os.path.exists(self.file_name):
            return []
        try:
            with open(self.file_name, 'r') as f:
                return sorted(json.load(f), key=lambda x: x['score'], reverse=True)
        except:
            return []

    ##
    # @brief Saves a new score.
    #
    # @param name Player name.
    # @param score Player score.
    ##
    def save_score(self, name, score):
        self.scores.append({'name': name, 'score': score})
        self.scores = sorted(self.scores, key=lambda x: x['score'], reverse=True)
        with open(self.file_name, 'w') as f:
            json.dump(self.scores, f)

    ##
    # @brief Handles back navigation.
    #
    # @param event Pygame event.
    ##
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                self.back_pressed = True

    ##
    # @brief Draws leaderboard screen.
    ##
    def draw(self):
        self.screen.fill(self.BLACK)

        y = 180
        for i, entry in enumerate(self.scores[:7]):
            self.screen.blit(self.entry_font.render(entry['name'], True, self.WHITE), (40, y))
            self.screen.blit(self.score_font.render(f"Score: {entry['score']}", True, self.GRAY), (40, y + 25))
            y += 75