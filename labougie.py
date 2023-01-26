import pygame
import time
import sys
import pickle as pkl
import time


class Candle:

    def __init__(self, name, burn_time, color):

        assert type(color) == tuple or type(color) == str or type(
            color) == None

        self.color = color
        self.burn_time = burn_time
        self.e_time = 0.0
        self.name = name
        self.creation_date = time.time()

    def save_candle(self, path):

        with open(path, "wb") as f:
            pkl.dump(
                {
                    'color': self.color,
                    'burn_time': self.burn_time,
                    'elapsed_time': self.e_time,
                    'name': self.name,
                    'created': self.creation_date
                }, f)

    def load_candle(self, path):

        with open(path, "rb") as f:
            d = pkl.load(f)

            self.color = d['color']
            self.burn_time = d['burn_time']
            self.e_time = d['elapsed_time']
            self.name = d['name']
            self.creation_date = d['created']


pygame.init()

clock = pygame.time.Clock()


def run():
    X = 300
    Y = 300
    screen = pygame.display.set_mode((X, Y))
    font = pygame.font.SysFont('monospace', 15)

    candle = Candle("test_candle", 1.0 * 60.0, (255, 255, 0))

    pygame.display.set_caption('LaBougie')
    st = time.time()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

        screen.fill((255, 255, 255))

        s = time.time() - st
        candle.e_time = s

        if s >= candle.burn_time:
            running = False
            sys.exit()

        percentage = s / candle.burn_time
        text = f"{percentage*100:.2f}%"

        tl = font.render(text, 1, (0, 0, 0))
        screen.blit(tl, (X - 100, Y - 100))

        candle_rectangle = pygame.Rect(0, 0, 30, 150 * (1.0 - percentage))
        candle_rectangle.midbottom = (X // 2, (Y // 4) * 3)

        wick_rectangle = pygame.Rect(0, 0, 5, 10)
        wick_rectangle.midbottom = candle_rectangle.midtop
        wick_rectangle.centery += 2
      
        pygame.draw.rect(screen, candle.color, candle_rectangle)
        pygame.draw.rect(screen, (0, 0, 0), wick_rectangle)
        pygame.display.flip()
        clock.tick(60)


run()