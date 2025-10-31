# car/car.py
import math
import pygame

from config import CAR_WIDTH, CAR_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT
from utils.geometry import closest_point_on_track, compute_curvature, distance
from ai.fuzzy import get_acceleration_action

class Car:
    def __init__(self, x, y, angle=0.0, color=(255, 255, 255)):
        # x and y refer to the position of the car; angle refers to the orientation of the car(in radian)
        self.x = x
        self.y = y
        self.angle = angle
        
        # The acceleration, brake and turn motions of the car
        self.speed = 0.0
        self.max_speed = 8.0
        self.acceleration_rate = 0.3
        self.brake_rate = 0.4
        self.turn_rate = 0.08
        
        # Car design
        self.color = color
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT

    def accelerate(self):
        self.speed = min(self.speed + self.acceleration_rate, self.max_speed)

    def brake(self):
        self.speed = max(self.speed - self.brake_rate, 0.0)

    def turn_left(self):
        self.angle -= self.turn_rate

    def turn_right(self):
        self.angle += self.turn_rate

    def maintain(self):
        self.speed = max(self.speed - 0.05, 0.0)

    def update(self):
        """Update position based on current speed and angle."""
        # Move in the direction the car is facing
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Optional: wrap around screen or clamp (we'll add track bounds later)
        # For now, allow moving off-screen during testing

    def get_track_info(self, track):
        """Returns (progress_index, curvature, distance_to_center)"""
        car_pos = (self.x, self.y)
        closest_point, idx = closest_point_on_track(car_pos, track.centerline)
        
        # Distance to centerline (for heuristic)
        dist_to_center = distance(car_pos, closest_point)
        
        # Estimate curvature using next few points
        n = len(track.centerline)
        p0 = track.centerline[(idx - 1) % n]
        p1 = track.centerline[idx]
        p2 = track.centerline[(idx + 1) % n]
        curvature = compute_curvature(p0, p1, p2)
        
        return idx, curvature, dist_to_center

    def ai_control_speed(self, curvature: float):
        """Use fuzzy logic to set acceleration based on speed and curvature."""
        acc_command = get_acceleration_action(self.speed, curvature)
        
        # Convert continuous command to discrete actions
        if acc_command > 0.3:
            self.accelerate()
        elif acc_command < -0.3:
            self.brake()
        else:
            self.maintain()  # includes mild friction

    def draw(self, surface):
        """Draw the car as a rotated rectangle."""
        # Create a surface for the car
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(car_surface, self.color, (0, 0, self.width, self.height))
        pygame.draw.rect(car_surface, (0, 0, 0), (0, 0, self.width, self.height), 1)  # border

        # Rotate around center
        rotated_car = pygame.transform.rotate(car_surface, -math.degrees(self.angle))
        rect = rotated_car.get_rect(center=(self.x, self.y))
        surface.blit(rotated_car, rect.topleft)