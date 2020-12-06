import pygame
import random
import sys
import math
from sounds import *
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

        pygame.draw.circle(self.display, self.color, [int(self.cords[0]), int(self.cords[1])],
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


def ending(screenX, display, Window_size, fs=False):
    clock = pygame.time.Clock()

    # gg

    planets = Planet
    planets.create_planets(200, display)
    ss = Sounds()

    speeder = 0.02

    spaceship_before = pygame.image.load("assets/textures/end/spaceship.png").convert_alpha()
    spaceship_after = pygame.transform.rotate(spaceship_before, 45)

    spaceship_rect = spaceship_after.get_rect()
    new_width = 200
    new_height = new_width * spaceship_rect[3] / spaceship_rect[2]
    spaceship_after = pygame.transform.scale(spaceship_after, [new_width, int(new_height)])

    game_management = {
        "planet": pygame.image.load("assets/textures/intro/planet.png").convert(),
        "spaceship": spaceship_after,
        "spaceship_cords": [350, 200],
        "spaceship_width": 150,
        "loading": pygame.image.load("assets/textures/intro/loading.png").convert(),
        "word01": pygame.image.load("assets/textures/end/word_01.png").convert_alpha(),
        "word02": pygame.image.load("assets/textures/end/word_02.png").convert_alpha(),
        "word03": pygame.image.load("assets/textures/end/word_03.png").convert_alpha(),
        "word04": pygame.image.load("assets/textures/end/word_04.png").convert_alpha(),
        "word05": pygame.image.load("assets/textures/end/word_05.png").convert_alpha(),
        "word06": pygame.image.load("assets/textures/end/word_06.png").convert_alpha(),
        "dotdot": pygame.image.load("assets/textures/end/dotdot.png").convert_alpha(),
        "message_cords": [10, 50]
    }

    alive = True

    while alive:
        display.fill((0, 0, 0))
        display.blit(game_management["planet"], [400, 250])

        display.blit(game_management["spaceship"], game_management["spaceship_cords"])
        game_management["spaceship_cords"][0] -= 0.05
        game_management["spaceship_cords"][1] -= 0.025

        #     # bonus stuff

        if speeder == 0.02:
            ss.sounds["EnginePickup"].play()

        if speeder < 0.3:
            planets.move_all()
            planets.planets.append(Planet(display,
                                          [random.randint(350, 450), random.randint(175, 275), random.randint(0, 10)],
                                          speeder))
            display.blit(game_management["word01"], game_management["message_cords"])
        elif speeder < 0.7:
            display.blit(game_management["word02"], game_management["message_cords"])
        elif speeder < 1.1:
            display.blit(game_management["dotdot"], game_management["message_cords"])
        elif speeder < 1.4:
            display.blit(game_management["word03"], game_management["message_cords"])
        elif speeder < 1.8:
            display.blit(game_management["word04"], game_management["message_cords"])
        elif speeder < 1.9:
            display.blit(game_management["word05"], game_management["message_cords"])
        else:
            display.blit(game_management["word06"], game_management["message_cords"])

        if speeder == 2.1:
            display.blit(game_management["loading"], [0, 0])
            file = open("assets/save.txt", "w")
            file.write("intro")
            file.close()
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

    return False, fs
