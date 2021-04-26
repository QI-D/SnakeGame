import pygame

class Window():

    def __init__(self, size:int=500, rows:int=20):
        self.rows = rows
        self.size = size
        self.window = pygame.display.set_mode((self.size, self.size))

    def draw(self):
        lines = self.size // self.rows

        x = 0
        y = 0
        for line in range(self.rows):
            x += lines
            y += lines

            pygame.draw.line(self.window, (255, 255, 255), (x, 0), (x, self.size))
            pygame.draw.line(self.window, (255, 255, 255), (0, y), (self.size, y))

    def redraw(self):
        self.window.fill((0,0,0))
        pygame.time.delay(50)
        pygame.time.Clock().tick(10)
        self.draw()
        pygame.display.update()