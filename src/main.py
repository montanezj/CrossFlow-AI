import pygame
import sys
import random
from car import Car  # Import the new class

# --- Configuration ---
WIDTH, HEIGHT = 800, 800
FPS = 60
BG_COLOR = (30, 30, 30)
ROAD_COLOR = (50, 50, 50)
LINE_COLOR = (255, 215, 0)

# Road Dimensions
ROAD_WIDTH = 120
CENTER = WIDTH // 2
ROAD_START = CENTER - (ROAD_WIDTH // 2)
ROAD_END = CENTER + (ROAD_WIDTH // 2)

def draw_env(screen):
    screen.fill(BG_COLOR)
    # Roads
    pygame.draw.rect(screen, ROAD_COLOR, (ROAD_START, 0, ROAD_WIDTH, HEIGHT))
    pygame.draw.rect(screen, ROAD_COLOR, (0, ROAD_START, WIDTH, ROAD_WIDTH))

    # Yellow Dividers
    line_thickness = 4
    offset = line_thickness // 2
    pygame.draw.rect(screen, LINE_COLOR, (CENTER - offset, 0, line_thickness, ROAD_START))
    pygame.draw.rect(screen, LINE_COLOR, (CENTER - offset, ROAD_END, line_thickness, HEIGHT - ROAD_END))
    pygame.draw.rect(screen, LINE_COLOR, (0, CENTER - offset, ROAD_START, line_thickness))
    pygame.draw.rect(screen, LINE_COLOR, (ROAD_END, CENTER - offset, WIDTH - ROAD_END, line_thickness))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CrossFlow AI - Traffic Sandbox")
    clock = pygame.time.Clock()

    # --- SPAWN TEST CARS ---
    # We create a list to hold all active cars
    cars = []

    # Add one of each to test the lanes
    cars.append(Car("WEST", speed=3))
    cars.append(Car("EAST", speed=4))
    cars.append(Car("NORTH", speed=2))
    cars.append(Car("SOUTH", speed=5))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Press SPACE to reset cars (Manual Reset Test)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cars = [Car("WEST"), Car("EAST"), Car("NORTH"), Car("SOUTH")]

        # 1. Update
        for car in cars:
            car.move()

        # 2. Draw
        draw_env(screen)
        for car in cars:
            car.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()