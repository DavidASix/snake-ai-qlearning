import pygame
import random
import game.constants as c

class Food:
    def __init__(self, snake):
        self.food = self.generate_food_location(snake)
    
    def generate_food_location(self, snake):
        # TODO: This code is not at all efficient
        food = (random.randint(0, c.WINDOW_WIDTH / c.PIXEL_SIZE - 1) * c.PIXEL_SIZE,
                random.randint(0, c.WINDOW_HEIGHT / c.PIXEL_SIZE - 1) * c.PIXEL_SIZE)
        while food in snake.snake:
            food = (random.randint(0, c.WINDOW_WIDTH / c.PIXEL_SIZE - 1) * c.PIXEL_SIZE,
                    random.randint(0, c.WINDOW_HEIGHT / c.PIXEL_SIZE - 1) * c.PIXEL_SIZE)
        return food
    
    def check_collision(self, snake):
        if snake.snake[0] == self.food:
            self.food = self.generate_food_location(snake)
            return True
        else:
            snake.snake.pop()
            return False