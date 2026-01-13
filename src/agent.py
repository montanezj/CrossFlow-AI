import torch
import random
import numpy as np
from collections import deque # Data structure to store memory
from network import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001 # Learning Rate

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # Randomness
        self.gamma = 0.9 # Discount rate (value of future rewards)
        self.memory = deque(maxlen=MAX_MEMORY) # popleft() if max len reached

        # Inputs: [Speed, Obstacle_Dist] = 2
        # Hidden: 256 nodes
        # Outputs: [Slower, Same, Faster] = 3
        self.model = Linear_QNet(2, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, car):
        """Helper to get the state from the car instance"""
        return car.get_state()

    def remember(self, state, action, reward, next_state, done):
        """Store the experience in memory"""
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        """Train on a batch of past experiences (Replay Buffer)"""
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # Random sample
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        """Train on the immediate step that just happened"""
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        """
        Epsilon-Greedy Strategy:
        - Initially, take random moves to explore.
        - Over time, rely more on the Model's prediction.
        """
        # Random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games # Decrease randomness as games increase
        final_move = [0,0,0]

        if random.randint(0, 200) < self.epsilon:
            # Random Move
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            # AI Prediction
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move