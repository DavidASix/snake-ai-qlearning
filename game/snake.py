import pygame
import game.constants as c

class Snake:
    def __init__(self):
        self.direction = c.LEFT
        self.changing_direction = False
        self.snake = [(200, 200), (220, 200), (240, 200)]

    def change_direction(self, event):
        # If a direction has been set this tick, do not set a new direction
        if self.changing_direction:
            return
        # Snake cannot turn in the direction its coming from
        if (event.key == pygame.K_UP and self.direction == c.DOWN 
            or event.key == pygame.K_DOWN and self.direction == c.UP
            or event.key == pygame.K_LEFT and self.direction == c.RIGHT
            or event.key == pygame.K_RIGHT and self.direction == c.LEFT):
            return
        # direction has been set
        self.changing_direction = True
        keys = {pygame.K_UP: c.UP, pygame.K_DOWN: c.DOWN, pygame.K_LEFT: c.LEFT, pygame.K_RIGHT: c.RIGHT}
        self.direction = keys[event.key]

    def move(self):
        head = self.snake[0]
        if self.direction == c.UP:
            new_head = (head[0], head[1] - c.PIXEL_SIZE)
        elif self.direction == c.DOWN:
            new_head = (head[0], head[1] + c.PIXEL_SIZE)
        elif self.direction == c.LEFT:
            new_head = (head[0] - c.PIXEL_SIZE, head[1])
        elif self.direction == c.RIGHT:
            new_head = (head[0] + c.PIXEL_SIZE, head[1])

        if new_head != self.snake[0]:
            self.snake.insert(0, new_head)