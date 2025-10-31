import pygame
import sys
import math

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, CAR1_COLOR, CAR2_COLOR, CAR_WIDTH, CAR_HEIGHT
from track.track import Track
from car.car import Car


def main():
    
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Race Track Duel")
    clock = pygame.time.Clock()

    track = Track()

    # Car positions
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    car1 = Car(center_x - 50, center_y, angle=0.0, color=CAR1_COLOR)
    car2 = Car(center_x + 50, center_y, angle=math.pi, color=CAR2_COLOR)  # facing left


    # Actual game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # === TEMPORARY: Keyboard control for testing ===
        keys = pygame.key.get_pressed()
        # Car 1: WASD
        if keys[pygame.K_a]: car1.turn_left()
        if keys[pygame.K_d]: car1.turn_right()
        if keys[pygame.K_w]: car1.accelerate()
        if keys[pygame.K_s]: car1.brake()
        # Car 2: Arrow keys
        if keys[pygame.K_LEFT]: car2.turn_left()
        if keys[pygame.K_RIGHT]: car2.turn_right()
        if keys[pygame.K_UP]: car2.accelerate()
        if keys[pygame.K_DOWN]: car2.brake()

        # Update physics
        car1.update()
        car2.update()

        # Draw
        screen.fill((30, 100, 30))
        track.draw(screen)
        car1.draw(screen)
        car2.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()