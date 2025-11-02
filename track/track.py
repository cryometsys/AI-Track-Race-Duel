# track/track.py
import pygame
import random

import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TRACK_COLOR, TRACK_BORDER_COLOR, TRACK_WIDTH


class Track:
    def __init__(self):
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.width = TRACK_WIDTH
        
        self.centerline = self._generate_oval()

        # Close loop (ensure first == last)
        if self.centerline[0] != self.centerline[-1]:
            self.centerline.append(self.centerline[0])

        # Place 4 evenly spaced checkpoints
        total = len(self.centerline) - 1  # exclude duplicate last point
        self.checkpoint_indices = [0, total // 4, total // 2, 3 * total // 4]
        self.checkpoints = [self.centerline[i] for i in self.checkpoint_indices]

    # -------------------------------------------------
    # Smooth oval with realistic racing curvature
    # -------------------------------------------------
    def _generate_oval(self):
        random.seed()

        points = []
        cx, cy = self.center_x, self.center_y

        # Track parameters
        base_radius = 300
        num_segments = 10  # total distinct track sections
        segment_points = 30  # resolution per segment
        angle = 0

        # Define track segments (angle change per segment)
        segments = []
        for _ in range(num_segments):
            seg_type = random.choice(["straight", "curve_smooth", "curve_tight"])
            if seg_type == "straight":
                angle_change = random.uniform(0.1, 0.3)  # gentle forward segment
                radius = base_radius + random.uniform(-30, 30)
            elif seg_type == "curve_smooth":
                angle_change = random.uniform(0.4, 0.8)
                radius = base_radius + random.uniform(-60, 60)
            else:  # curve_tight
                angle_change = random.uniform(1.0, 1.5)
                radius = base_radius + random.uniform(-120, -60)
            segments.append((seg_type, angle_change, radius))

        # Generate points around
        total_angle = 0
        for seg_type, angle_change, radius in segments:
            for i in range(segment_points):
                t = i / segment_points
                local_angle = angle + t * angle_change
                x = cx + radius * math.cos(local_angle)
                y = cy + radius * math.sin(local_angle)
                points.append((x, y))
            angle += angle_change
            total_angle += angle_change

        # Close loop smoothly by blending back to start
        start_x, start_y = points[0]
        end_x, end_y = points[-1]
        for i in range(10):
            t = i / 10
            x = end_x + t * (start_x - end_x)
            y = end_y + t * (start_y - end_y)
            points.append((x, y))

        # Normalize to center
        avg_x = sum(p[0] for p in points) / len(points)
        avg_y = sum(p[1] for p in points) / len(points)
        points = [(x - avg_x + cx, y - avg_y + cy) for (x, y) in points]

        return points

    # # -------------------------------------------------
    # # Figure-8 layout (overlapping cross section)
    # # -------------------------------------------------
    # def _generate_figure8(self):
    #     cx, cy = self.center_x, self.center_y
    #     r = 130
    #     gap = 40  # center gap between loops
    #     points = []

    #     # Left loop (counterclockwise)
    #     for i in range(100):
    #         a = 2 * math.pi * i / 100
    #         x = cx - gap - r * math.cos(a)
    #         y = cy + r * math.sin(a)
    #         points.append((x, y))

    #     # Right loop (clockwise)
    #     for i in range(100):
    #         a = 2 * math.pi * i / 100
    #         x = cx + gap + r * math.cos(a + math.pi)
    #         y = cy + r * math.sin(a + math.pi)
    #         points.append((x, y))

    #     return points

    # # -------------------------------------------------
    # # Tight technical track with mix of 90° and curved turns
    # # -------------------------------------------------
    # def _generate_technical(self):
    #     """Compact track with mixed tight corners and short straights."""
    #     cx, cy = self.center_x, self.center_y
    #     points = []

    #     # Define control points of the track (like a blueprint)
    #     control = [
    #         (cx + 200, cy + 150),
    #         (cx + 200, cy - 100),
    #         (cx, cy - 200),
    #         (cx - 200, cy - 100),
    #         (cx - 200, cy + 50),
    #         (cx, cy + 200),
    #     ]

    #     # Interpolate smoothly between control points
    #     for i in range(len(control)):
    #         x1, y1 = control[i]
    #         x2, y2 = control[(i + 1) % len(control)]
    #         for t in range(25):
    #             u = t / 25
    #             px = x1 + (x2 - x1) * u
    #             py = y1 + (y2 - y1) * u
    #             points.append((px, py))

    #     return points

    # # -------------------------------------------------
    # # Simple loop circuit with a realistic chicane
    # # -------------------------------------------------
    # def _generate_simple_loop(self):
    #     """Large loop with smooth turns and a fast chicane section."""
    #     cx, cy = self.center_x, self.center_y
    #     radius = 240
    #     points = []

    #     # Main circle (about 85%)
    #     for i in range(85):
    #         a = 2 * math.pi * i / 100
    #         points.append((cx + radius * math.cos(a), cy + radius * math.sin(a)))

    #     # Add a fast chicane (left-right-left kink)
    #     start_x, start_y = points[-1]
    #     chicane = [
    #         (start_x - 60, start_y - 10),
    #         (start_x - 90, start_y + 20),
    #         (start_x - 50, start_y + 40),
    #         (start_x, start_y + 20),
    #     ]
    #     points.extend(chicane)

    #     # Close the remaining arc
    #     for i in range(85, 100):
    #         a = 2 * math.pi * i / 100
    #         points.append((cx + radius * math.cos(a), cy + radius * math.sin(a)))

    #     return points

    def draw(self, surface):
        if len(self.centerline) > 1:
            pygame.draw.lines(surface, TRACK_COLOR, True, self.centerline, self.width)
            pygame.draw.lines(surface, TRACK_BORDER_COLOR, True, self.centerline, 2)
        pygame.draw.lines(surface, (255, 255, 0), True, self.centerline, 1)
