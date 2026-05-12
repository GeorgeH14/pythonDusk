"""
Improved AI Snake Trainer with PyTorch + Pygame
-----------------------------------------------

Upgrades included:
- Better exploration strategy
- Distance-based rewards
- Survival reward
- Larger neural network
- Faster training
- Better frame limit
- Improved learning stability

Install:
    pip install pygame torch numpy

Run:
    python snake_ai_improved.py
"""

import pygame
import random
import numpy as np
from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim

# =========================================================
# SETTINGS
# =========================================================

BLOCK_SIZE = 20
WIDTH = 640
HEIGHT = 480

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

# =========================================================
# PYGAME SETUP
# =========================================================

pygame.init()
font = pygame.font.SysFont("arial", 25)

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

# =========================================================
# GAME
# =========================================================

class Direction:
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class SnakeGameAI:

    def __init__(self, w=WIDTH, h=HEIGHT):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Improved AI Snake")
        self.reset()

    def reset(self):

        self.direction = Direction.RIGHT

        self.head = Point(self.w // 2, self.h // 2)

        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)
        ]

        self.score = 0
        self.food = None
        self.frame_iteration = 0

        self._place_food()

    def _place_food(self):

        x = random.randint(
            0,
            (self.w - BLOCK_SIZE) // BLOCK_SIZE
        ) * BLOCK_SIZE

        y = random.randint(
            0,
            (self.h - BLOCK_SIZE) // BLOCK_SIZE
        ) * BLOCK_SIZE

        self.food = Point(x, y)

        if any(p.x == x and p.y == y for p in self.snake):
            self._place_food()

    def play_step(self, action):

        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # -----------------------------------------
        # OLD DISTANCE TO FOOD
        # -----------------------------------------

        old_distance = (
            abs(self.head.x - self.food.x) +
            abs(self.head.y - self.food.y)
        )

        # -----------------------------------------
        # MOVE
        # -----------------------------------------

        self._move(action)
        self.snake.insert(0, self.head)

        reward = 0
        game_over = False

        # -----------------------------------------
        # NEW DISTANCE TO FOOD
        # -----------------------------------------

        new_distance = (
            abs(self.head.x - self.food.x) +
            abs(self.head.y - self.food.y)
        )

        # reward moving toward food
        if new_distance < old_distance:
            reward += 0.3
        else:
            reward -= 0.3

        # small survival reward
        reward += 0.05

        # -----------------------------------------
        # COLLISION
        # -----------------------------------------

        if (
            self.is_collision() or
            self.frame_iteration > 250 * len(self.snake)
        ):
            game_over = True
            reward = -5
            return reward, game_over, self.score

        # -----------------------------------------
        # FOOD
        # -----------------------------------------

        if self.head.x == self.food.x and self.head.y == self.food.y:
            self.score += 1
            reward = 15
            self._place_food()
        else:
            self.snake.pop()

        self._update_ui()

        # Faster training speed
        clock.tick(30)

        return reward, game_over, self.score

    def is_collision(self, pt=None):

        if pt is None:
            pt = self.head

        if pt.x > self.w - BLOCK_SIZE or pt.x < 0:
            return True

        if pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True

        if any(p.x == pt.x and p.y == pt.y for p in self.snake[1:]):
            return True

        return False

    def _update_ui(self):

        self.display.fill(BLACK)

        for pt in self.snake:

            pygame.draw.rect(
                self.display,
                BLUE1,
                pygame.Rect(
                    pt.x,
                    pt.y,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
            )

            pygame.draw.rect(
                self.display,
                BLUE2,
                pygame.Rect(
                    pt.x + 4,
                    pt.y + 4,
                    12,
                    12
                )
            )

        pygame.draw.rect(
            self.display,
            RED,
            pygame.Rect(
                self.food.x,
                self.food.y,
                BLOCK_SIZE,
                BLOCK_SIZE
            )
        )

        text = font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )

        self.display.blit(text, [0, 0])

        pygame.display.flip()

    def _move(self, action):

        """
        action:
            [1,0,0] -> straight
            [0,1,0] -> right turn
            [0,0,1] -> left turn
        """

        clockwise = [
            Direction.RIGHT,
            Direction.DOWN,
            Direction.LEFT,
            Direction.UP
        ]

        idx = clockwise.index(self.direction)

        # straight
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clockwise[idx]

        # right turn
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clockwise[next_idx]

        # left turn
        else:
            next_idx = (idx - 1) % 4
            new_dir = clockwise[next_idx]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

# =========================================================
# NEURAL NETWORK
# =========================================================

class LinearQNet(nn.Module):

    def __init__(self, input_size, hidden_size, output_size):

        super().__init__()

        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        self.linear3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):

        x = torch.relu(self.linear1(x))
        x = torch.relu(self.linear2(x))
        x = self.linear3(x)

        return x

    def save(self, file_name="snake_model.pth"):
        torch.save(self.state_dict(), file_name)

# =========================================================
# TRAINER
# =========================================================

class QTrainer:

    def __init__(self, model, lr, gamma):

        self.lr = lr
        self.gamma = gamma
        self.model = model

        self.optimizer = optim.Adam(
            model.parameters(),
            lr=self.lr
        )

        self.criterion = nn.MSELoss()

    def train_step(
        self,
        state,
        action,
        reward,
        next_state,
        done
    ):

        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:

            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)

            done = (done,)

        pred = self.model(state)

        target = pred.clone()

        for idx in range(len(done)):

            Q_new = reward[idx]

            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(
                    self.model(next_state[idx])
                )

            target[idx][torch.argmax(action[idx]).item()] = Q_new

        self.optimizer.zero_grad()

        loss = self.criterion(target, pred)

        loss.backward()

        self.optimizer.step()

# =========================================================
# AGENT
# =========================================================

class Agent:

    def __init__(self):

        self.n_games = 0
        self.gamma = 0.9

        self.memory = deque(maxlen=MAX_MEMORY)

        # Better network
        self.model = LinearQNet(13, 512, 3)

        self.trainer = QTrainer(
            self.model,
            lr=LR,
            gamma=self.gamma
        )

    def get_state(self, game):

        head = game.snake[0]

        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [

            # danger straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            # danger right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            # danger left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            # movement direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # food location
            game.food.x < game.head.x,
            game.food.x > game.head.x,
            game.food.y < game.head.y,
            game.food.y > game.head.y,

            # normalized food vector
            (game.food.x - game.head.x) / game.w,
            (game.food.y - game.head.y) / game.h
        ]

        return np.array(state, dtype=float)

    def remember(
        self,
        state,
        action,
        reward,
        next_state,
        done
    ):

        self.memory.append(
            (
                state,
                action,
                reward,
                next_state,
                done
            )
        )

    def train_long_memory(self):

        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(
                self.memory,
                BATCH_SIZE
            )
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)

        self.trainer.train_step(
            states,
            actions,
            rewards,
            next_states,
            dones
        )

    def train_short_memory(
        self,
        state,
        action,
        reward,
        next_state,
        done
    ):

        self.trainer.train_step(
            state,
            action,
            reward,
            next_state,
            done
        )

    def get_action(self, state):

        # better exploration strategy
        epsilon = max(80 - self.n_games, 5)

        final_move = [0, 0, 0]

        if random.randint(0, 200) < epsilon:
            move = random.randint(0, 2)

        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()

        final_move[move] = 1

        return final_move

# =========================================================
# TRAIN LOOP
# =========================================================

def train():

    record = 0

    agent = Agent()
    game = SnakeGameAI()

    while True:

        # current state
        state_old = agent.get_state(game)

        # move
        final_move = agent.get_action(state_old)

        # perform move
        reward, done, score = game.play_step(final_move)

        # new state
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(
            state_old,
            final_move,
            reward,
            state_new,
            done
        )

        # remember
        agent.remember(
            state_old,
            final_move,
            reward,
            state_new,
            done
        )

        # game over
        if done:

            game.reset()

            agent.n_games += 1

            # train long memory
            agent.train_long_memory()

            # save best model
            if score > record:
                record = score
                agent.model.save()

            print(
                f"Game: {agent.n_games} | "
                f"Score: {score} | "
                f"Record: {record} | "
            )

# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    train()