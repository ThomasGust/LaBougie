
import pygame
import time
import sys

pygame.init()

clock = pygame.time.Clock()

X = 300
Y = 300
screen = pygame.display.set_mode((X, Y))
font = pygame.font.SysFont('monospace', 15)

stop = 1.0*60.0*60.0
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

    if s >= stop:
        running = False
        sys.exit()
    text = f"{(s/stop)*100}%"
    tl = font.render(text, 1, (0,0,0))
    screen.blit(tl, (X-200, Y-200))

    pygame.display.update()
    clock.tick(60)