import pygame
import sys
import numpy as np
from car import Car
from agent import Agent

# --- Configuration ---
WIDTH, HEIGHT = 800, 800
FPS = 60 # Speed up FPS if you want to train faster (e.g., 120 or 0 for max speed)
BG_COLOR = (30, 30, 30)
ROAD_COLOR = (50, 50, 50)
LINE_COLOR = (255, 215, 0)
ROAD_WIDTH = 120
CENTER = WIDTH // 2
ROAD_START = CENTER - (ROAD_WIDTH // 2)
ROAD_END = CENTER + (ROAD_WIDTH // 2)

def draw_env(screen):
    screen.fill(BG_COLOR)
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
    cars = []
    # Spawn cars with random speeds to vary the scenarios
    cars.append(Car("WEST", speed=4))
    cars.append(Car("EAST", speed=3))
    cars.append(Car("NORTH", speed=5))
    cars.append(Car("SOUTH", speed=3))
    return cars

def check_collisions(cars):
    # If any car hits another, return True
    for i, car_a in enumerate(cars):
        for j, car_b in enumerate(cars):
            if i != j:
                if car_a.rect.colliderect(car_b.rect):
                    return True
    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CrossFlow AI - Training Mode")
    clock = pygame.time.Clock()

    # 1. Initialize the Brain
    # We use one shared "Agent" for all cars.
    # This speeds up learning (4x experience per frame).
    agent = Agent()

    cars = reset_simulation()
    score = 0
    record = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                agent.model.save() # Save progress on quit

        # --- AI DECISION LOOP ---
        game_over = False

        # We loop through every car and let the AI control it individually
        for car in cars:
            # 1. Get Old State
            state_old = agent.get_state(car)

            # 2. Get Move (Action)
            # action is a list [1,0,0] -> We need index for car.move()
            final_move = agent.get_action(state_old)
            move_index = np.argmax(final_move).item() # 0=Brake, 1=Same, 2=Gas

            # 3. Perform Move
            car.move(move_index)
            car.check_radar(cars) # Update sensors

            # 4. Check Result (Collision)
            # Note: We check if *this specific move* caused a global crash
            crash = check_collisions(cars)

            # 5. Calculate Reward
            reward = 0
            if crash:
                reward = -10
                game_over = True
                car.crashed = True
            else:
                # Reward for speed (0.1 to 1.0)
                reward = (car.speed / car.max_speed)
                # Optional: Extra penalty for being stopped (prevent camping)
                if car.speed < 2:
                    reward -= 0.5

            # 6. Get New State
            state_new = agent.get_state(car)

            # 7. Train Short Term Memory (The immediate lesson)
            agent.train_short_memory(state_old, final_move, reward, state_new, crash)

            # 8. Store in Long Term Memory
            agent.remember(state_old, final_move, reward, state_new, crash)

            if crash: break # Stop processing other cars if simulation died

        # --- HANDLING RESETS ---
        if game_over:
            agent.n_games += 1
            agent.train_long_memory() # Replay and learn from mistakes

            if score > record:
                record = score
                agent.model.save() # Save best brain

            print(f"Game: {agent.n_games} | Score: {int(score)} | Record: {int(record)}")

            score = 0
            cars = reset_simulation()
        else:
            score += 1 # Score increases every frame you survive

        # --- DRAWING ---
        draw_env(screen)
        for car in cars:
            car.draw(screen)

        # Draw Stats
        font = pygame.font.Font(None, 36)
        text = font.render(f"Gen: {agent.n_games} Record: {int(record)}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()