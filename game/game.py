import pygame
import sys
import numpy as np
import game.constants as c
from game.snake import Snake
from game.food import Food
from game.score import Score

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food(self.snake)
        self.score = Score()
        self.game_over = False
        self.ate_food = False

    def check_game_over(self):
        if (self.snake.snake[0][0] < 0 or self.snake.snake[0][0] >= c.WINDOW_WIDTH or
            self.snake.snake[0][1] < 0 or self.snake.snake[0][1] >= c.WINDOW_HEIGHT or
            self.snake.snake[0] in self.snake.snake[1:]):
            return True
        else:
            return False
    
    # QLearning Functions
    def get_state(self):
        state = (
            self.snake.snake[0],
            #tuple(self.snake.snake[1:-1]),
            self.snake.snake[-1],
            self.food.food,
            self.snake.direction,
            #self.score.score,
            #self.game_over,
            #self.ate_food
        )
        return state
    
    def get_possible_actions(self):
        # List out the possible key presses from the current position
        available_moves = self.snake.get_available_moves()
        available_moves.append('no_change')
        return available_moves

    def reset(self):
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food(self.snake)
        self.score = Score()
        self.game_over = False

    def calculate_reward(self, current_state, previous_state):
        reward = 0
        reward += 60 if self.ate_food else 0
        reward -= 25 if self.game_over else 0
        if reward == 0:
            # Penalize direction switch
            reward -= 20 if current_state[3] != previous_state[3] else 0
            reward += 20 if current_state[3] == 'no_change' else 0
            # Calculate if the snake is moving towards the food in general
            head = current_state[0]
            food = current_state[2]
            current_dist = tuple(abs(x1 - x2) for x1, x2 in zip(head, food))
            head = previous_state[0]
            food = previous_state[2]
            previous_dist = tuple(abs(x1 - x2) for x1, x2 in zip(head, food))
            # Determine negative or positive trajectory
            #dist_diff = tuple(x1 - x2 for x1, x2 in zip(previous_dist, current_dist))
            #total_diff = sum(dist_diff)
            # Calculate approx closeness to food
            closeness = 1 - ( (sum(current_dist) / 2) / (sum(self.display.get_size()) / 2) )
            # Penalize moving further from the food
            # If it's moving towards it, reward else punish
            # Add a number between -10 and 10
            reward += (20 * closeness) - 10 
        return round(reward, 3)

    def step(self, action, episode, slow=False):
        previous_state = self.get_state()
        self.game_loop(action, episode)
        game_state = self.get_state()
        done = self.game_over
        reward = self.calculate_reward(game_state, previous_state)
        if (slow):
            self.clock.tick(10)
        return game_state, reward, done, self.score.score

    def run(self):
        while True:
            previous_state = self.get_state()
            self.game_loop()
            game_state = self.get_state()
            reward = self.calculate_reward(game_state, previous_state)
            print(f'Reward: {reward}')
            if self.game_over:
                break
            self.clock.tick(5)

    def render_episode(self, episode):
        font = pygame.font.SysFont('Arial', 20)
        text = font.render(f'Episode: {episode}', True, c.WHITE)
        self.display.blit(text, (c.WINDOW_WIDTH - text.get_width(), 0))
    
    def game_loop(self, action='no_change', episode=None):
        if action != 'no_change':
            key_event = pygame.event.Event(pygame.KEYDOWN, key=int(action))
            pygame.event.post(key_event)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    self.reset()
                # Set new direction to first pressed key
                # After first key is selected
                self.snake.change_direction(event)

        # New direction has been established, disable changing direction
        self.snake.changing_direction = False
        self.snake.move()
        if self.food.check_collision(self.snake):
            self.score.increase_score()
            self.ate_food = True
        else:
            self.ate_food = False

        if self.check_game_over():
            self.game_over = True

        self.display.fill(c.DARK_GREY)
        for coord in self.snake.snake:
            pygame.draw.rect(self.display, c.WHITE, pygame.Rect(coord[0], coord[1], c.PIXEL_SIZE, c.PIXEL_SIZE), 1)
        pygame.draw.rect(self.display, c.RED, pygame.Rect(self.food.food[0], self.food.food[1], c.PIXEL_SIZE, c.PIXEL_SIZE))

        self.score.draw(self.display)
        if episode is not None:
            self.render_episode(episode)

        pygame.display.update()