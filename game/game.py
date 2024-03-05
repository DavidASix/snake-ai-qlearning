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

    def check_game_over(self):
        if (self.snake.snake[0][0] < 0 or self.snake.snake[0][0] >= c.WINDOW_WIDTH or
            self.snake.snake[0][1] < 0 or self.snake.snake[0][1] >= c.WINDOW_HEIGHT or
            self.snake.snake[0] in self.snake.snake[1:]):
            print("Game over")
            return True
        else:
            return False
    
    # QLearning Functions
    def get_state(self):
        snake_head = self.snake[0]
        snake_body = self.snake[1:-1]
        snake_tail = self.snake[-1]
        food_position = self.food.food
        snake_direction = self.snake.direction
        current_score = self.score.score
        collided = self.check_game_over()
        ate_food = self.food.check_collision(self.snake)
        return np.array([snake_head, snake_body, snake_tail, food_position, snake_direction, current_score, collided, ate_food])
    
    def get_possible_actions(self):
        # List out the possible key presses from the current position
        available_moves = self.snake.get_available_moves()
        available_moves.append('no_change')
        return available_moves

    def reset(self):
        self.snake = Snake()
        self.food = Food(self.snake)
        self.score = Score()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
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

            if self.check_game_over():
                break

            self.display.fill(c.DARK_GREY)
            for coord in self.snake.snake:
                pygame.draw.rect(self.display, c.WHITE, pygame.Rect(coord[0], coord[1], c.PIXEL_SIZE, c.PIXEL_SIZE), 1)
            pygame.draw.rect(self.display, c.RED, pygame.Rect(self.food.food[0], self.food.food[1], c.PIXEL_SIZE, c.PIXEL_SIZE))


            self.score.draw(self.display)
            pygame.display.update()
            self.clock.tick(10)
            