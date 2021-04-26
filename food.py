import pygame
import random


class Food():
    def __init__(self):
        self.food_position = []  # xy coords for food
        self.square_size = 10
        self.rows = 50
        self.columns = 50

    def new_food(self, snake_pos):
        new_pos = [random.randint(0, self.columns-1)*self.square_size,
                   random.randint(0, self.rows-1)*self.square_size]
        while any(new_pos == body for body in snake_pos):
            new_pos = [random.randint(
                0, self.columns) * self.square_size, random.randint(0, self.rows) * self.square_size]
        self.food_position = new_pos

    def draw_on_display(self, display):
        display.blit(pygame.image.load("images/apple.png").convert(),
                     (self.food_position[0], self.food_position[1]))

    @property
    def get_pos(self):
        return self.food_position
