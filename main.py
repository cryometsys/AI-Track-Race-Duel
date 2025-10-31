import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, CAR1_COLOR, CAR2_COLOR, CAR_WIDTH, CAR_HEIGHT
from track.track import Track

def main():
    
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Race Track Duel")
    clock = pygame.time.Clock()

    track = Track()

    # Car positions
    car1_pos = (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)
    car2_pos = (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2)


    # Actual game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 100, 30))
        track.draw(screen)

        # Drawing cars
        pygame.draw.rect(screen, CAR1_COLOR, (*car1_pos, CAR_WIDTH, CAR_HEIGHT))
        pygame.draw.rect(screen, CAR2_COLOR, (*car2_pos, CAR_WIDTH, CAR_HEIGHT))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()