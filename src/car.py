import pygame
import math

# --- Constants ---
WIDTH, HEIGHT = 800, 800
ROAD_WIDTH = 120
CENTER = WIDTH // 2
LANE_OFFSET = ROAD_WIDTH // 4

# Car Dimensions
CAR_LENGTH = 40
CAR_WIDTH = 20

class Car:
    def __init__(self, direction, speed=2):
        self.direction = direction
        self.base_speed = speed # Remember the original speed
        self.speed = speed
        self.crashed = False

        # Sensor Data
        self.radar_length = 200  # How far the car can see
        self.distance_to_obstacle = 200 # Default to max range

        # Position Logic (Right-Hand Traffic)
        if direction == "WEST":
            self.x, self.y = WIDTH, CENTER - LANE_OFFSET - (CAR_WIDTH // 2)
            self.color = (0, 100, 255) # Blue
            self.angle = 180
            self.rect = pygame.Rect(self.x, self.y, CAR_LENGTH, CAR_WIDTH)

        elif direction == "EAST":
            self.x, self.y = -CAR_LENGTH, CENTER + LANE_OFFSET - (CAR_WIDTH // 2)
            self.color = (255, 50, 50) # Red
            self.angle = 0
            self.rect = pygame.Rect(self.x, self.y, CAR_LENGTH, CAR_WIDTH)

        elif direction == "NORTH":
            self.x, self.y = CENTER + LANE_OFFSET - (CAR_WIDTH // 2), HEIGHT
            self.color = (255, 215, 0) # Yellow
            self.angle = 90
            self.rect = pygame.Rect(self.x, self.y, CAR_WIDTH, CAR_LENGTH)

        elif direction == "SOUTH":
            self.x, self.y = CENTER - LANE_OFFSET - (CAR_WIDTH // 2), -CAR_LENGTH
            self.color = (160, 32, 240) # Purple
            self.angle = 270
            self.rect = pygame.Rect(self.x, self.y, CAR_WIDTH, CAR_LENGTH)

    def move(self):
        if not self.crashed:
            # Simple Movement based on direction angle
            if self.direction == "EAST": self.x += self.speed
            elif self.direction == "WEST": self.x -= self.speed
            elif self.direction == "NORTH": self.y -= self.speed
            elif self.direction == "SOUTH": self.y += self.speed

            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

    def check_radar(self, cars):
        """Casts a ray to measure distance to the nearest car ahead"""

        # 1. Determine the 'tip' of the car to start the laser from
        start_x, start_y = self.rect.center

        # 2. Cast the beam step-by-step
        # We step 10 pixels at a time to save CPU (vs 1 pixel)
        for d in range(0, self.radar_length, 10):

            # Calculate the point 'd' pixels away in the correct direction
            # Math: x = start + cos(angle) * dist
            # Note: Pygame angles are weird, but for 90-degree turns this simple logic works:
            if self.direction == "EAST":
                check_x = start_x + (CAR_LENGTH/2) + d
                check_y = start_y
            elif self.direction == "WEST":
                check_x = start_x - (CAR_LENGTH/2) - d
                check_y = start_y
            elif self.direction == "NORTH":
                check_x = start_x
                check_y = start_y - (CAR_LENGTH/2) - d
            elif self.direction == "SOUTH":
                check_x = start_x
                check_y = start_y + (CAR_LENGTH/2) + d

            # 3. Collision Check
            # Look through all OTHER cars to see if our beam hits them
            hit = False
            for car in cars:
                if car != self:
                    if car.rect.collidepoint(check_x, check_y):
                        self.distance_to_obstacle = d
                        hit = True
                        break # Stop beam at first hit

            if hit:
                break

        else:
            # If loop finishes without break, path is clear
            self.distance_to_obstacle = self.radar_length

    def draw(self, screen):
        # 1. Draw the Car
        pygame.draw.rect(screen, self.color, self.rect)

        # 2. Draw the Sensor Beam
        # Green if clear, Red if close (< 60px)
        sensor_color = (0, 255, 0) if self.distance_to_obstacle > 60 else (255, 0, 0)

        start_pos = self.rect.center
        end_pos = list(start_pos)

        if self.direction == "EAST": end_pos[0] += (self.distance_to_obstacle + 20)
        elif self.direction == "WEST": end_pos[0] -= (self.distance_to_obstacle + 20)
        elif self.direction == "NORTH": end_pos[1] -= (self.distance_to_obstacle + 20)
        elif self.direction == "SOUTH": end_pos[1] += (self.distance_to_obstacle + 20)

        pygame.draw.line(screen, sensor_color, start_pos, end_pos, 2)