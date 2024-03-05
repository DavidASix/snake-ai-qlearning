import pygame
import game.constants as c

class Snake:
    def __init__(self):
        self.direction = pygame.K_LEFT
        self.changing_direction = False
        self.snake = [(200, 200), (220, 200), (240, 200)]

    def get_available_moves(self):
        all_actions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        opposite_direction = {pygame.K_UP: pygame.K_DOWN, pygame.K_DOWN: pygame.K_UP, pygame.K_LEFT: pygame.K_RIGHT, pygame.K_RIGHT: pygame.K_LEFT}
        possible_actions = [action for action in all_actions if action != self.direction and action != opposite_direction[self.direction]]
        return possible_actions

    def change_direction(self, event):
        # If a direction has been set this tick, do not set a new direction
        if self.changing_direction:
            return
        # Snake cannot turn in the direction its coming from
        if event.key not in self.get_available_moves():
            return
        # direction has been set
        self.changing_direction = True
        self.direction = event.key

    def move(self):
        head = self.snake[0]
        if self.direction == pygame.K_UP:
            new_head = (head[0], head[1] - c.PIXEL_SIZE)
        elif self.direction == pygame.K_DOWN:
            new_head = (head[0], head[1] + c.PIXEL_SIZE)
        elif self.direction == pygame.K_LEFT:
            new_head = (head[0] - c.PIXEL_SIZE, head[1])
        elif self.direction == pygame.K_RIGHT:
            new_head = (head[0] + c.PIXEL_SIZE, head[1])

        if new_head != self.snake[0]:
            self.snake.insert(0, new_head)