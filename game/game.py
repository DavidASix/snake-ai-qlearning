import pygame
import sys
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

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
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
            