import pygame
import time
import sys
from modules import Candle

pygame.init()

clock = pygame.time.Clock()

def run():
    X = 300
    Y = 300
    screen = pygame.display.set_mode((X, Y))
    font = pygame.font.SysFont('monospace', 15)

    candle = Candle("test_candle", 1.0*60.0, (255, 0, 0))

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
        
        percentage = s/candle.burn_time
        text = f"{percentage*100:.2f}%"

        tl = font.render(text, 1, (0,0,0))
        screen.blit(tl, (X-200, Y-200))

        rectangle = pygame.Rect(30, 30, 30*(1.0-percentage), 30*(1.0-percentage))
        pygame.draw.rect(screen, candle.color, rectangle)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run()