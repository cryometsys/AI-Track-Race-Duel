import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TRACK_COLOR, TRACK_BORDER_COLOR, TRACK_WIDTH
import math

class Track:
    def __init__(self, seed = None):
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2

        self.radius = 250
        self.width = TRACK_WIDTH
        
        # Centerline generation => list(x, y)
        self.centerline = []
        num_points = 100
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            self.centerline.append((x, y))

        self.centerline.append(self.centerline[0])

        # Using every N point as checkpoints; 4 checkpoints per lap
        self.checkpoint_indices = [0, 25, 50, 75]
        self.checkpoints = [self.centerline[i] for i in self.checkpoint_indices]

    def draw(self, surface):
        outer_radius = self.radius + self.width // 2
        inner_radius = self.radius - self.width // 2
        
        # Track design
        pygame.draw.circle(surface, TRACK_COLOR, (self.center_x, self.center_y), outer_radius)
        
        # Inner circle
        pygame.draw.circle(surface, (30, 100, 30), (self.center_x, self.center_y), inner_radius)
        
        # Track borders
        pygame.draw.circle(surface, TRACK_BORDER_COLOR, (self.center_x, self.center_y), outer_radius, 2)
        pygame.draw.circle(surface, TRACK_BORDER_COLOR, (self.center_x, self.center_y), inner_radius, 2)

        # Centerline
        pygame.draw.lines(surface, (255, 255, 0), True, self.centerline, 1)