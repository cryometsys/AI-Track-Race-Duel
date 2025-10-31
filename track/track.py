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


        # === Dynamic Checkered Flag at Start/Finish ===
        # if len(self.centerline) > 1:
        #     start = self.centerline[0]
        #     next_pt = self.centerline[1]

        #     # Tangent vector (direction of track)
        #     dx = next_pt[0] - start[0]
        #     dy = next_pt[1] - start[1]
            
        #     # Perpendicular vector (across the track)
        #     length = max(1e-6, math.hypot(dx, dy))
        #     perp_x = -dy / length
        #     perp_y = dx / length

        #     # Simpler version: just a perpendicular line
        #     mid = self.centerline[0]
        #     perp_end_x = mid[0] + perp_x * 40
        #     perp_end_y = mid[1] + perp_y * 40
        #     pygame.draw.line(surface, (255, 255, 255), 
        #                     (mid[0] - perp_x * 40, mid[1] - perp_y * 40),
        #                     (perp_end_x, perp_end_y), 4)
        #     # Flag dimensions
        #     flag_half_width = 30  # half of total width across track
        #     flag_height = 40      # along track direction (small)

        #     # Build 4 corners of the flag quad
        #     corners = [
        #         (start[0] + perp_x * -flag_half_width, start[1] + perp_y * -flag_half_width),
        #         (start[0] + perp_x * flag_half_width, start[1] + perp_y * flag_half_width),
        #         (start[0] + perp_x * flag_half_width + dx/length * flag_height, 
        #         start[1] + perp_y * flag_half_width + dy/length * flag_height),
        #         (start[0] + perp_x * -flag_half_width + dx/length * flag_height, 
        #         start[1] + perp_y * -flag_half_width + dy/length * flag_height)
        #     ]

        #     # Draw checkered pattern (alternating black/white rectangles)
        #     num_stripes = 8
        #     for i in range(num_stripes):
        #         color = (255, 255, 255) if i % 2 == 0 else (0, 0, 0)
        #         # Interpolate between left and right edges
        #         frac1 = i / num_stripes
        #         frac2 = (i + 1) / num_stripes

        #         x1 = corners[0][0] + (corners[1][0] - corners[0][0]) * frac1
        #         y1 = corners[0][1] + (corners[1][1] - corners[0][1]) * frac1
        #         x2 = corners[0][0] + (corners[1][0] - corners[0][0]) * frac2
        #         y2 = corners[0][1] + (corners[1][1] - corners[0][1]) * frac2
        #         x3 = corners[3][0] + (corners[2][0] - corners[3][0]) * frac2
        #         y3 = corners[3][1] + (corners[2][1] - corners[3][1]) * frac2
        #         x4 = corners[3][0] + (corners[2][0] - corners[3][0]) * frac1
        #         y4 = corners[3][1] + (corners[2][1] - corners[3][1]) * frac1

        #         pygame.draw.polygon(surface, color, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

        #     # Optional: "START" label (rotated)
        #     font = pygame.font.SysFont(None, 20)
        #     text = font.render("START", True, (255, 255, 0))
        #     text = pygame.transform.rotate(text, -math.degrees(math.atan2(dy, dx)))
        #     text_rect = text.get_rect(center=(start[0], start[1] - 30))
        #     surface.blit(text, text_rect)

        