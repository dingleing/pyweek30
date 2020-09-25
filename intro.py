import pygame
import random
import sys
import math
from pygame.locals import *


# basic config


class Planet:
    planets = []

    def __init__(self, display, cords=None, acceleration=0.02):
        if cords is None:
            cords = [0, 0, 0]
        self.display = display
        self.cords = cords
        self.surface_parameters = (600, 450)
        self.center = [400.01, 225.01]
        self.speed = 1.4

        self.direction = self.find_angle([self.cords[0], self.cords[1]])

        self.x_dir = math.cos(self.direction)
        self.y_dir = math.sin(self.direction)
        self.color = (random.randint(0, 255), 0, 0)
        self.acceleration = acceleration

    @staticmethod
    def distances(cords1, cords2):
        return [abs(cords1[0] - cords2[0]), abs(cords1[1] - cords2[1])]

    def find_angle(self, point):
        dists = self.distances(self.center,
                               point)
        angle = math.atan(dists[1] / dists[0])

        if point[0] < self.center[0]:
            if point[1] < self.center[1]:
                return angle + math.pi
            else:
                return (math.pi / 2 - angle) + (math.pi / 2)
        else:
            if point[1] < self.center[1]:
                return (math.pi / 2 - angle) + 3 * (math.pi / 2)
            else:
                return angle

    def move(self):

        pygame.draw.circle(self.display, self.color, [self.cords[0], self.cords[1]],
                           int(self.cords[2]), int(self.cords[2]))

        self.cords[2] += 0.1 * self.speed
        self.cords[1] += self.y_dir * self.speed
        self.cords[0] += self.x_dir * self.speed

        if self.cords[0] < -200 or self.cords[0] > self.surface_parameters[0] + 200 or \
                self.cords[1] < -200 or self.cords[1] > self.surface_parameters[1] + 200:
            self.planets.remove(self)

        self.speed += self.acceleration

    @classmethod
    def create_planets(cls, how_many, display):
        cls.planets = [Planet(display,
                              [random.randint(0, 600), random.randint(0, 450), random.randint(0, 20)])
                       for _ in range(how_many)]

    @classmethod
    def move_all(cls):
        for planet in cls.planets:
            planet.move()


def intro(screenX, display, Window_size, fs=False):

    clock = pygame.time.Clock()

    # gg

    planets = Planet
    planets.create_planets(200, display)

    speeder = 0.02

    game_management = {
        "planet": pygame.image.load("assets/textures/intro/planet.png").convert(),
        "spaceship": pygame.image.load("assets/textures/intro/spaceship.png").convert(),
        "spaceship_cords": [100, 280],
        "explosion": pygame.image.load("assets/textures/intro/explosion.png").convert(),
        "uhm": pygame.image.load("assets/textures/intro/uhmmmm.png").convert(),
        "not_working": pygame.image.load("assets/textures/intro/problem.png").convert(),
        "help": pygame.image.load("assets/textures/intro/help.png").convert(),
        "loading": pygame.image.load("assets/textures/intro/loading.png").convert(),
        "end": pygame.image.load("assets/textures/intro/end.png").convert(),
        "message_cords": [400, 350]
    }
    game_management["spaceship"].set_colorkey((0, 0, 0))
    game_management["planet"].set_colorkey((0, 0, 0))
    game_management["explosion"].set_colorkey((0, 0, 0))

    back_to_menu = False

    alive = True
    while alive:
        display.fill((0, 0, 0))

        # planets

        planets.move_all()

        if speeder < 2:
            planets.planets.append(Planet(display,
                                          [random.randint(350, 450), random.randint(175, 275), random.randint(0, 10)],
                                          speeder))

            if speeder > 1.8:
                for _ in range(10):
                    planets.planets.append(Planet(display,
                                                  [random.randint(350, 450), random.randint(175, 275),
                                                   random.randint(0, 10)],
                                                  speeder))

            display.blit(game_management["spaceship"], game_management["spaceship_cords"])
            game_management["spaceship_cords"][0] += 0.05
            game_management["spaceship_cords"][1] -= 0.025

            # bonus stuff

            if speeder < 0.8:
                display.blit(game_management["uhm"], game_management["message_cords"])
            elif speeder < 1.5:
                display.blit(game_management["not_working"], game_management["message_cords"])
            else:
                display.blit(game_management["help"], game_management["message_cords"])

        elif speeder > 2.05:
            if 2.1 > speeder:
                game_management["spaceship_cords"] = [0, 250]
                display.fill((255, 255, 255))
            else:
                display.blit(game_management["planet"], [400, 50])

            if speeder > 2.2 and game_management["spaceship_cords"][0] < 300:
                display.blit(game_management["spaceship"], game_management["spaceship_cords"])
                game_management["spaceship_cords"][0] += 20
                game_management["spaceship_cords"][1] -= 8
            elif speeder > 2.2:
                display.blit(game_management["explosion"], [325, 100])

            if speeder > 2.4:
                display.blit(game_management["end"], [0, 0])

        if speeder > 2.6:
            file = open("assets/save.txt", "w")
            file.write("cave_level")
            file.close()
            display.blit(game_management["loading"], [0, 0])
            alive = False

        speeder += 0.001
        speeder = round(speeder, 3)

        # event loop

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    display.blit(game_management["loading"], [0, 0])
                    back_to_menu = True
                    alive = False

                elif event.key == K_f:
                    # remember fs = fullscreen
                    fs = not fs
                    if fs is False:
                        screenX = pygame.display.set_mode(Window_size)
                    else:
                        screenX = pygame.display.set_mode(Window_size, pygame.FULLSCREEN)

        # basic loop config

        screenX.blit(pygame.transform.scale(display, Window_size), (0, 0))
        pygame.display.update()
        clock.tick(60)

    display.blit(game_management["loading"], [0, 0])
    if back_to_menu:
        return False
    return True
