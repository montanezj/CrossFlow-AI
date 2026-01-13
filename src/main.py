import pygame
import sys
from car import Car

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
    """Draws the roads and lane markers"""
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

def reset_simulation():
    """Resets the environment with fresh cars"""
    cars = []
    # Spawning cars with slightly different speeds to force potential collisions
    cars.append(Car("WEST", speed=4))
    cars.append(Car("EAST", speed=3))
    cars.append(Car("NORTH", speed=5))
    cars.append(Car("SOUTH", speed=3))
    return cars

def check_collisions(cars):
    """Checks if any car has hit another car"""
    # Simple O(N^2) check - acceptable for low number of cars
    for i, car_a in enumerate(cars):
        for j, car_b in enumerate(cars):
            if i != j: # Don't check a car against itself
                if car_a.rect.colliderect(car_b.rect):
                    return True # CRASH DETECTED
    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CrossFlow AI - Traffic Sandbox")
    clock = pygame.time.Clock()

    # Initial Spawn
    cars = reset_simulation()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Manual Reset
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cars = reset_simulation()

        # 1. Move Cars
        for car in cars:
            car.move()

        # 2. Check Collisions
        if check_collisions(cars):
            print("CRASH! Resetting simulation...") # Console log for debugging
            cars = reset_simulation()

        # 3. Clean up cars that leave the screen (Optional memory management)
        # Keeps list small so collision check stays fast
        cars = [c for c in cars if -50 < c.x < WIDTH + 50 and -50 < c.y < HEIGHT + 50]

        # If screen is empty, respawn (so you don't stare at empty road)
        if len(cars) == 0:
            cars = reset_simulation()

        # 4. Draw
        draw_env(screen)
        for car in cars:
            car.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()