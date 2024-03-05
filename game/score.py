import pygame
import game.constants as c

class Score:
    def __init__(self):
        self.score = 3
        self.font = pygame.font.SysFont('Arial', 20)

    def increase_score(self):
        self.score += 1

    def draw(self, display):
        text = self.font.render(f'Score: {self.score}', True, c.WHITE)
        display.blit(text, (0, 0))