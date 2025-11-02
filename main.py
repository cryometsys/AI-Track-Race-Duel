import pygame
import sys
import math

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, CAR1_COLOR, CAR2_COLOR, CAR_WIDTH, CAR_HEIGHT
from track.track import Track
from car.car import Car
from ai.heuristic_agent import HeuristicAgent
from utils.geometry import get_track_heading

def main():
    
    # pygame setup
    pygame.init()
    font = pygame.font.SysFont(None, 36)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Race Track Duel")
    clock = pygame.time.Clock()

    # Track setup
    track = Track()

    # Car initialization
    start_index = 0
    start_pos = track.centerline[start_index]
    start_angle = get_track_heading(track.centerline, start_index)

    # Perpendicular vector to heading
    perp_x = -math.sin(start_angle)
    perp_y = math.cos(start_angle)

    # Car positions
    car1_pos = (start_pos[0] + perp_x * 15, start_pos[1] + perp_y * 15)
    car2_pos = (start_pos[0] - perp_x * 15, start_pos[1] - perp_y * 15)

    car1 = Car(car1_pos[0], car1_pos[1], angle=start_angle, color=CAR1_COLOR)
    car2 = Car(car2_pos[0], car2_pos[1], angle=start_angle, color=CAR2_COLOR)


    # Agent1 -> Cautious AI: values safety over speed
    agent1 = HeuristicAgent(
        lookahead_depth=3,
        progress_weight=0.5, # Speed and safety trade-off
        centering_weight=0.3, # Strongly penalizes drifting
        off_track_penalty=1000
    )

    # Agent2 -> Aggressive AI: pushes forward, tolerates more risk
    agent2 = HeuristicAgent(
        lookahead_depth=3,
        progress_weight=1.2, # Values progress more
        centering_weight=0.05, # Doesn't care much about centering
        off_track_penalty=1000
    )

    # Race completion flags
    race_finished = False
    winner = None

    # Actual game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Track details 
        _, curvature1, _ = car1.get_track_info(track)
        _, curvature2, _ = car2.get_track_info(track)

        # Speed controlling
        car1.ai_control_speed(curvature1)
        car2.ai_control_speed(curvature2)

        # Steering controlling
        action1 = agent1.decide_action(car1, track)
        action2 = agent2.decide_action(car2, track)

        if action1 == "left": car1.turn_left()
        elif action1 == "right": car1.turn_right()

        if action2 == "left": car2.turn_left()
        elif action2 == "right": car2.turn_right()

        # Update physics
        car1.update()
        car2.update()

        # Lap count upgrade
        car1.update_lap_progress(track)
        car2.update_lap_progress(track)

        if not race_finished:
            if car1.lap_complete:
                winner = "Car 1"
                race_finished = True
                car1.speed = car2.speed = 0

            elif car2.lap_complete:
                winner = "Car 2"
                race_finished = True
                car1.speed = car2.speed = 0

        # Draw
        screen.fill((30, 100, 30))
        track.draw(screen)
        car1.draw(screen)
        car2.draw(screen)

        # Speed text display
        car1_speed_text = font.render(f"Car1 - {car1.speed:.1f}", True, (255, 0, 0))
        car2_speed_text = font.render(f"Car2 - {car2.speed:.1f}", True, (0, 0, 255))

        screen_width, screen_height = screen.get_size()

        car1_lap_count = font.render(f"Current Lap - {car1.lap_count}", True, (255, 0, 0))
        car2_lap_count = font.render(f"Current Lap - {car2.lap_count}", True, (0, 0, 255))

        # Car1 speed
        screen.blit(car1_speed_text, (10, 10))
        screen.blit(car1_lap_count, (10, 30))
        # Car2 speed
        screen.blit(car2_speed_text, (screen_width - car2_speed_text.get_width() - 10, 10))
        screen.blit(car2_lap_count, (screen_width - car2_lap_count.get_width() - 10, 30))

        # Victory text
        if race_finished:
            font = pygame.font.SysFont(None, 72)
            text = font.render(f"{winner} Wins!", True, (255, 255, 0))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()