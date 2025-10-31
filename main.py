import pygame
import sys
import math

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, CAR1_COLOR, CAR2_COLOR, CAR_WIDTH, CAR_HEIGHT
from track.track import Track
from car.car import Car


def main():
    
    # pygame setup
    pygame.init()
    font = pygame.font.SysFont(None, 36)
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
        else: car1.maintain()

        # Car 2: Arrow keys
        if keys[pygame.K_LEFT]: car2.turn_left()
        if keys[pygame.K_RIGHT]: car2.turn_right()
        if keys[pygame.K_UP]: car2.accelerate()
        if keys[pygame.K_DOWN]: car2.brake()
        else: car2.maintain()
        
        # Update physics
        car1.update()
        car2.update()

        # Curvature, speed display
        # idx1, curve1, dist1 = car1.get_track_info(track)
        # idx2, curve2, dist2 = car2.get_track_info(track)
        # print(f"Car1 - Curve: {curve1:.3f}, Dist to center: {dist1:.1f}")
        # print(f"Car2 - Curve: {curve2:.3f}, Dist to center: {dist2:.1f}")

        # Draw
        screen.fill((30, 100, 30))
        track.draw(screen)
        car1.draw(screen)
        car2.draw(screen)

        # Render speed text
        car1_speed_text = font.render(f"Car1 - {car1.speed:.1f}", True, (255, 0, 0))
        car2_speed_text = font.render(f"Car2 - {car2.speed:.1f}", True, (0, 0, 255))

        # Get screen dimensions for positioning
        screen_width, screen_height = screen.get_size()

        # Draw Car1 speed at top-left
        screen.blit(car1_speed_text, (10, 10))

        # Draw Car2 speed at top-right
        screen.blit(car2_speed_text, (screen_width - car2_speed_text.get_width() - 10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()