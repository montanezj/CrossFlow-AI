import pygame
import math
import numpy as np

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
        self.speed = speed
        self.max_speed = 8  # Cap speed so AI doesn't fly off screen
        self.crashed = False

        # Sensor Data
        self.radar_length = 200
        self.distance_to_obstacle = 200

        # Initialize Position
        self.reset_position()

    def reset_position(self):
        """Resets car to starting position (used after crashes)"""
        self.crashed = False
        self.speed = 2 # Reset speed

        if self.direction == "WEST":
            self.x, self.y = WIDTH, CENTER - LANE_OFFSET - (CAR_WIDTH // 2)
            self.color = (0, 100, 255)
            self.dx, self.dy = -1, 0
            self.rect = pygame.Rect(self.x, self.y, CAR_LENGTH, CAR_WIDTH)

        elif self.direction == "EAST":
            self.x, self.y = -CAR_LENGTH, CENTER + LANE_OFFSET - (CAR_WIDTH // 2)
            self.color = (255, 50, 50)
            self.dx, self.dy = 1, 0
            self.rect = pygame.Rect(self.x, self.y, CAR_LENGTH, CAR_WIDTH)

        elif self.direction == "NORTH":
            self.x, self.y = CENTER + LANE_OFFSET - (CAR_WIDTH // 2), HEIGHT
            self.color = (255, 215, 0)
            self.dx, self.dy = 0, -1
            self.rect = pygame.Rect(self.x, self.y, CAR_WIDTH, CAR_LENGTH)

        elif self.direction == "SOUTH":
            self.x, self.y = CENTER - LANE_OFFSET - (CAR_WIDTH // 2), -CAR_LENGTH
            self.color = (160, 32, 240)
            self.dx, self.dy = 0, 1
            self.rect = pygame.Rect(self.x, self.y, CAR_WIDTH, CAR_LENGTH)

    def get_state(self):
        """
        Returns the inputs for the Neural Network:
        [Normalized Speed, Normalized Radar Distance]
        """
        # We normalize values to be between 0 and 1 for better AI performance
        norm_speed = self.speed / self.max_speed
        norm_dist = self.distance_to_obstacle / self.radar_length

        return np.array([norm_speed, norm_dist], dtype=np.float32)

    def move(self, action=None):
        """
        Action is an integer from the AI:
        0 = Decelerate
        1 = Maintain Speed
        2 = Accelerate
        """
        if not self.crashed:
            # AI Control
            if action is not None:
                if action == 0:   # Brake
                    self.speed -= 0.2
                elif action == 2: # Gas
                    self.speed += 0.2

                # Clamp Speed (Don't stop completely, don't speed too much)
                self.speed = max(1, min(self.speed, self.max_speed))

            # Apply Movement
            self.x += self.dx * self.speed
            self.y += self.dy * self.speed

            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

    def check_radar(self, cars):
        start_x, start_y = self.rect.center

        for d in range(0, self.radar_length, 10):
            if self.direction == "EAST": check_x, check_y = start_x + (CAR_LENGTH/2) + d, start_y
            elif self.direction == "WEST": check_x, check_y = start_x - (CAR_LENGTH/2) - d, start_y
            elif self.direction == "NORTH": check_x, check_y = start_x, start_y - (CAR_LENGTH/2) - d
            elif self.direction == "SOUTH": check_x, check_y = start_x, start_y + (CAR_LENGTH/2) + d

            hit = False
            for car in cars:
                if car != self and car.rect.collidepoint(check_x, check_y):
                    self.distance_to_obstacle = d
                    hit = True
                    break
            if hit: break
        else:
            self.distance_to_obstacle = self.radar_length

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        # Visualize Radar
        sensor_color = (0, 255, 0) if self.distance_to_obstacle > 60 else (255, 0, 0)
        start_pos = self.rect.center
        end_pos = list(start_pos)

        if self.direction == "EAST": end_pos[0] += (self.distance_to_obstacle + 20)
        elif self.direction == "WEST": end_pos[0] -= (self.distance_to_obstacle + 20)
        elif self.direction == "NORTH": end_pos[1] -= (self.distance_to_obstacle + 20)
        elif self.direction == "SOUTH": end_pos[1] += (self.distance_to_obstacle + 20)

        pygame.draw.line(screen, sensor_color, start_pos, end_pos, 2)