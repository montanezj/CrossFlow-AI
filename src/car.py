import pygame

# --- Constants ---
WIDTH, HEIGHT = 800, 800
ROAD_WIDTH = 120
CENTER = WIDTH // 2
LANE_OFFSET = ROAD_WIDTH // 4  # Distance from center line to center of a lane (30px)

# Car Dimensions
CAR_LENGTH = 40
CAR_WIDTH = 20

class Car:
    def __init__(self, direction, speed=2):
        self.direction = direction
        self.speed = speed
        self.crashed = False

        # Set Spawn Position and Color based on Direction (Right-Hand Traffic)
        if direction == "WEST": # Moving Left (Top Lane)
            self.x = WIDTH
            self.y = CENTER - LANE_OFFSET - (CAR_WIDTH // 2)
            self.color = (0, 100, 255) # Blue
            self.dx, self.dy = -speed, 0
            self.rect = pygame.Rect(self.x, self.y, CAR_LENGTH, CAR_WIDTH)

        elif direction == "EAST": # Moving Right (Bottom Lane)
            self.x = -CAR_LENGTH
            self.y = CENTER + LANE_OFFSET - (CAR_WIDTH // 2)
            self.color = (255, 50, 50) # Red
            self.dx, self.dy = speed, 0
            self.rect = pygame.Rect(self.x, self.y, CAR_LENGTH, CAR_WIDTH)

        elif direction == "NORTH": # Moving Up (Right Lane)
            self.x = CENTER + LANE_OFFSET - (CAR_WIDTH // 2)
            self.y = HEIGHT
            self.color = (255, 215, 0) # Yellow
            self.dx, self.dy = 0, -speed
            # Note: Swap width/length for vertical cars
            self.rect = pygame.Rect(self.x, self.y, CAR_WIDTH, CAR_LENGTH)

        elif direction == "SOUTH": # Moving Down (Left Lane)
            self.x = CENTER - LANE_OFFSET - (CAR_WIDTH // 2)
            self.y = -CAR_LENGTH
            self.color = (160, 32, 240) # Purple
            self.dx, self.dy = 0, speed
            self.rect = pygame.Rect(self.x, self.y, CAR_WIDTH, CAR_LENGTH)

    def move(self):
        if not self.crashed:
            self.x += self.dx
            self.y += self.dy

            # Update the rect position for drawing and collisions
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)