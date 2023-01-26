import pygame
import time
import sys
import pickle as pkl
import time
import os
import random



pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d, %d' % (150, 50)

clock = pygame.time.Clock()

X = 300
Y = 300
screen = pygame.display.set_mode((X, Y))
font = pygame.font.SysFont('monospace', 15)

class FlameParticle:
    alpha_layer_qty = 2
    alpha_glow_difference_constant = 2

    def __init__(self, x=X // 2, y=Y // 2, r=5):
        self.x = x
        self.y = y
        self.r = r
        self.original_r = r
        self.alpha_layers = FlameParticle.alpha_layer_qty
        self.alpha_glow = FlameParticle.alpha_glow_difference_constant
        max_surf_size = 2 * self.r * self.alpha_layers * self.alpha_layers * self.alpha_glow
        self.surf = pygame.Surface((max_surf_size, max_surf_size), pygame.SRCALPHA)
        self.burn_rate = 0.1 * random.randint(1, 4)

    def update(self):
        self.y -= 7 - self.r
        self.x += random.randint(-self.r, self.r)
        self.original_r -= self.burn_rate
        self.r = int(self.original_r)
        if self.r <= 0:
            self.r = 1

    def draw(self):
        max_surf_size = 2 * self.r * self.alpha_layers * self.alpha_layers * self.alpha_glow
        self.surf = pygame.Surface((max_surf_size, max_surf_size), pygame.SRCALPHA)
        for i in range(self.alpha_layers, -1, -1):
            alpha = 255 - i * (255 // self.alpha_layers - 5)
            if alpha <= 0:
                alpha = 0
            radius = self.r * i * i * self.alpha_glow
            if self.r == 4 or self.r == 3:
                r, g, b = (255, 0, 0)
            elif self.r == 2:
                r, g, b = (255, 150, 0)
            else:
                r, g, b = (50, 50, 50)
            # r, g, b = (0, 0, 255)  # uncomment this to make the flame blue
            color = (r, g, b, alpha)
            pygame.draw.circle(self.surf, color, (self.surf.get_width() // 2, self.surf.get_height() // 2), radius/5)
        screen.blit(self.surf, self.surf.get_rect(center=(self.x, self.y)))


class Flame:
    def __init__(self, x=X // 2, y=Y // 2):
        self.x = x
        self.y = y
        self.flame_intensity = 2
        self.flame_particles = []
        for i in range(self.flame_intensity * 25):
            self.flame_particles.append(FlameParticle(self.x + random.randint(-5, 5), self.y, random.randint(1, 5)))

    def draw_flame(self):
        for i in self.flame_particles:
            if i.original_r <= 0:
                self.flame_particles.remove(i)
                self.flame_particles.append(FlameParticle(self.x + random.randint(-5, 5), self.y, random.randint(1, 5)))
                del i
                continue
            i.update()
            i.draw()

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


def run():
    candle = Candle("test_candle", 1.0 * 60.0, (255, 255, 0))
    pygame.display.set_caption('LaBougie')
    st = time.time()
    running = True

    flame = Flame()
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

        flame.x, flame.y = wick_rectangle.midtop
        pygame.draw.rect(screen, candle.color, candle_rectangle)
        pygame.draw.rect(screen, (0, 0, 0), wick_rectangle)

        flame.draw_flame()
        pygame.display.flip()
        clock.tick(60)


run()