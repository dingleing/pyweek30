from ray_cast import *
from cave_level_engine import *

import pygame
from pygame.locals import *

import random
import sys
import math
from pathlib import Path


def cave_level(screenX, display, Window_size, fs=False):
    pygame.mixer.pre_init(48000, -16, 2, 512)
    pygame.init()
    pygame.mixer.set_num_channels(16)

    clock = pygame.time.Clock()

    back_to_menu = False

    # !!!!!creating objects to control game
    loading = pygame.image.load("assets/textures/intro/loading.png").convert()

    game = Game()
    game.fs = fs

    objects = Objects()

    objects.values["water"] = 0
    objects.values["add_water"] = False
    objects.values["dead"] = False
    objects.values["lava_level"] = 0
    objects.values["tutorial_timer"] = 0
    objects.values["won"] = False

    ids = Id()

    # !!!!!creating player

    # never set direction to 0
    Player = Object("player", game.custom_id_giver, [500, 500], [0, 0], 0.01, True, [8, 8])
    Player.move.collisions = True  # enables collisions for player
    Player.move.speed = 8 # increasing speed so ur not super slow
    Player.move.angle_speed = Player.move.speed/160
    Player.move.offset = 30  # were creating 120 rays with 0.5 angle difference and we need player offset 30 angles
    # don't try to understand the comment above its just 30 it just is

    # simulating movement so u dont start at speed 0
    Player.dir_movement = Player.move.set_start_dir_movement(Player.direction, Player.dir_movement)

    # sorts player
    sort(Player, objects)
    # moves to next id
    game.custom_id_giver += 1

    # !!!!!creating rays

    rays = Rays(Player.direction, 200, display)

    # !!!!!creating map

    game_map = load_map("assets/maps/bungs_map")

    # !!!!! loading objects

    load_objects(game_map, 32, 32, objects, game)

    lava_wall = Object("deadly", game.custom_id_giver, [-32, 0], [0, 0], 0, False, [3200, 32])
    sort(lava_wall, objects)
    game.custom_id_giver += 1

    # !!!!! getting the dictionary for ray_casting
    # it contains textures for different blocks, numbers in map

    ray_dictionary = get_ray_dictionary()

    # timers for animations

    timer = Timers()
    timer.add_timer(40, True, "ray_lava_animation")
    timer.add_timer(20, True, "lava_rise")

    # !!!!!game loop

    while game.alive:
        # deleting objects

        game_map = objects.del_pos_in_map(game_map)
        objects.take_out_trash(ids)
        ids.remove_by_id(objects)

        # bg

        display.fill((0, 0, 0))

        # floor

        pygame.draw.rect(display, (186, 154, 88), (0, 330, 600, 120))
        pygame.draw.rect(display, (168, 136, 70), (0, 275, 600, 80))
        pygame.draw.rect(display, (145, 117, 60), (0, 245, 600, 30))
        pygame.draw.rect(display, (131, 106, 54), (0, 225, 600, 20))

        # celling

        pygame.draw.rect(display, (186, 154, 88), (0, 0, 600, 120))
        pygame.draw.rect(display, (168, 136, 70), (0, 120, 600, 80))
        pygame.draw.rect(display, (145, 117, 60), (0, 200, 600, 30))
        pygame.draw.rect(display, (131, 106, 54), (0, 230, 600, 20))

        # doing player movement

        Player.movement = Player.move.move(Player.dir_movement)
        Player.direction, Player.dir_movement = Player.move.change_dir(Player.direction, Player.dir_movement,
                                                                       Player.move.angle_speed)
        # second parameter is speed of rotation

        # adding additional conditions

        if objects.values["add_water"]:
            objects.values["water"] += 1
            objects.values["add_water"] = False

        game_map = rise_lava(game_map, objects.values["lava_level"], objects, lava_wall)

        # collisions

        objects.do_collisions(objects)

        # casting rays

        player_mid = [Player.object_pos[0] + (Player.size[0] / 2), Player.object_pos[1] + (Player.size[0] / 2)]
        rays.cast_rays(200, Player.direction, player_mid,
                       game_map, Player.direction + (Player.move.offset * Player.move.degree), ray_dictionary)
        # for Player_mid argument we must give middle of player

        # running animations

        timer.add_time(ray_dictionary, objects)

        # event loop

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # key_down

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    objects.values["dead"] = True
                    game.alive = False
                    back_to_menu = True

                elif event.key == K_f:
                    # remember fs = fullscreen
                    game.fs = not game.fs
                    if game.fs is False:
                        screenX = pygame.display.set_mode(Window_size)
                    else:
                        screenX = pygame.display.set_mode(Window_size, pygame.FULLSCREEN)

                elif event.key == K_d:
                    Player.move.right = True
                elif event.key == K_a:
                    Player.move.left = True
                elif event.key == K_w:
                    Player.move.forward = True
                elif event.key == K_s:
                    Player.move.backwards = True

            # key_up

            elif event.type == KEYUP:
                if event.key == K_d:
                    Player.move.right = False
                elif event.key == K_a:
                    Player.move.left = False
                elif event.key == K_w:
                    Player.move.forward = False
                elif event.key == K_s:
                    Player.move.backwards = False

        # tutorial

        if objects.values["tutorial_timer"] < 80:
            display.blit(pygame.image.load("assets/textures/intro/objective0.png"), [0, 0])
        elif objects.values["tutorial_timer"] < 160:
            display.blit(pygame.image.load("assets/textures/intro/objective1.png"), [0, 0])
        elif objects.values["tutorial_timer"] < 200:
            display.blit(pygame.image.load("assets/textures/intro/fullscreen_tutorial.png"), [0, 0])

        objects.values["tutorial_timer"] += 1

        # checking if dead or won

        if objects.values["dead"]:
            display.blit(loading, [0, 0])
            screenX.blit(pygame.transform.scale(display, Window_size), (0, 0))
            pygame.display.update()
            game.alive = False

        if objects.values["won"]:
            display.blit(loading, [0, 0])
            screenX.blit(pygame.transform.scale(display, Window_size), (0, 0))
            pygame.display.update()
            game.alive = False
            file = open("assets/save.txt", "w")
            file.write("onto_the_forest")
            file.close()

        # basic loop config

        screenX.blit(pygame.transform.scale(display, Window_size), (0, 0))
        pygame.display.update()
        clock.tick(40)

    if back_to_menu:
        return False, fs
    return True, fs


def rise_lava(game_map, line, objects, lava_wall):
    index = 0
    for num in game_map[line]:
        if num == "0":
            game_map[line][index] = "5"
        index += 1
    lava_wall.change_pos([0, line * 32])

    objects.do_inplace_col(objects)

    return game_map
