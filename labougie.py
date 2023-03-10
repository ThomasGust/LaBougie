import pygame
import time
import sys
import pickle as pkl
import time
import os
import random
import math
import colorsys


pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d, %d' % (150, 50)

clock = pygame.time.Clock()

X = 600
Y = 600
screen = pygame.display.set_mode((X, Y))
font = pygame.font.SysFont('monospace', 15)
title_font = pygame.font.SysFont('monospace', 25)

##############################################################################
#### THANKS TO https://github.com/tank-king for most of the flame effect! ####
##############################################################################

class FlameParticle:
    alpha_layer_qty = 2
    alpha_glow_difference_constant = 2

    def __init__(self, x=X // 2, y=Y // 2, r=25):
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
    def __init__(self, x=X // 2, y=Y // 2, fi=2, speed = 25.0):
        self.x = x
        self.y = y
        self.flame_intensity = fi
        self.flame_particles = []
        for i in range(self.flame_intensity * speed):
            self.flame_particles.append(FlameParticle(self.x + random.randint(-5, 5), self.y, random.randint(1, 7)))

    def draw_flame(self):
        for i in self.flame_particles:
            if i.original_r <= 0:
                self.flame_particles.remove(i)
                self.flame_particles.append(FlameParticle(self.x + random.randint(-5, 5), self.y, random.randint(1, 7)))
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

class ColorPicker:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface((w, h))
        self.image.fill((255, 255, 255))
        self.rad = h//2
        self.pwidth = w-self.rad*2
        self.color = pygame.Color(0)
        for i in range(self.pwidth):
            self.color.hsla = (int(360*i/self.pwidth), 100, 50, 100)
            pygame.draw.rect(self.image, self.color, (i+self.rad, h//3, 1, h-2*h//3))
        self.p = 0

    def get_color(self):
        color = pygame.Color(0)
        color.hsla = (int(self.p * self.pwidth), 100, 50, 100)
        return color

    def update(self):
        moude_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if moude_buttons[0] and self.rect.collidepoint(mouse_pos):
            self.p = (mouse_pos[0] - self.rect.left - self.rad) / self.pwidth
            self.p = (max(0, min(self.p, 1)))

    def draw(self, surf):
        surf.blit(self.image, self.rect)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pygame.draw.circle(surf, self.get_color(), center, self.rect.height // 3)

def run():
    done = False
    candle = Candle("test_candle", 3.0 * 10.0, (255, 255, 0))
    pygame.display.set_caption('LaBougie')
    st = time.time()
    running = True

    flame = Flame(fi=20, speed=25)
    color_picker = ColorPicker(50, 50, 400, 60)
    user_text = ''
    title_rect = pygame.Rect(X//2, 0, 120, 60)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if title_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
                
                candle.name = user_text

        screen.fill((255, 255, 255))
        title = title_font.render(user_text, 1, (0, 0, 0))
        s = time.time() - st
        candle.e_time = s

        if s >= candle.burn_time:
            done = True
            print('COMPLETED CANDLE!!!')
        percentage = s / candle.burn_time
        text = f"{percentage*100:.2f}%"
        if not done:

            candle_rectangle = pygame.Rect(0, 0, 60, 300 * (1.0 - percentage))
            candle_rectangle.midbottom = (X // 2, (Y // 20) * 18)

            wick_rectangle = pygame.Rect(0, 0, 10, 20)
            wick_rectangle.midbottom = candle_rectangle.midtop
            wick_rectangle.centery += 1

            color_picker.rect.centerx = candle_rectangle.centerx

            flame.x, flame.y = wick_rectangle.midbottom
            pygame.draw.rect(screen, candle.color, candle_rectangle)
            pygame.draw.rect(screen, (0, 0, 0), wick_rectangle)

            color_picker.update()
            color_picker.draw(screen)

            flame.draw_flame()

        title_rect.midbottom = color_picker.rect.center
        screen.blit(title, title_rect)

        percentage = font.render(text, 1, (0, 0, 0))
        percentage_rect = pygame.Rect(0, 0, 60, 30)
        percentage_rect.midtop = candle_rectangle.midbottom
        screen.blit(percentage, percentage_rect)

        candle.color = color_picker.get_color()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__": 
    run()