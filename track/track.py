import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TRACK_COLOR, TRACK_BORDER_COLOR, TRACK_WIDTH

class Track:
    def __init__(self):
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        
        # Track dimensions
        self.inner_radius = 150
        self.outer_radius = self.inner_radius + TRACK_WIDTH

    def draw(self, surface):
        # Background
        pygame.draw.circle(surface, TRACK_COLOR, (self.center_x, self.center_y), self.outer_radius)

        # Inner circle
        pygame.draw.circle(surface, (30, 100, 30), (self.center_x, self.center_y), self.inner_radius)
        
        # Border
        pygame.draw.circle(surface, TRACK_BORDER_COLOR, (self.center_x, self.center_y), self.outer_radius, 3)
        pygame.draw.circle(surface, TRACK_BORDER_COLOR, (self.center_x, self.center_y), self.inner_radius, 3)