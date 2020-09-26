import pygame
import time
from pygame.locals import *

pygame.mixer.pre_init(48000, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(16)


class Sounds:
    def __init__(self):
        self.sounds = {
            "Power_up": pygame.mixer.Sound("assets/Sounds/Powerup.ogg"),
            "Portal-transport": pygame.mixer.Sound("assets/Sounds/Portal_transport.ogg"),
            "Walking": pygame.mixer.Sound("assets/Sounds/Walking.ogg"),
            "Item-pickup": pygame.mixer.Sound("assets/Sounds/ItemPickup.ogg"),
            "explosion": pygame.mixer.Sound("assets/Sounds/explosion.ogg"),
            "Opener": pygame.mixer.Sound("assets/Sounds/Opener.ogg"),
            "Click": pygame.mixer.Sound("assets/Sounds/Click.ogg"),
            "EnginePickup": pygame.mixer.Sound("assets/Sounds/EnginePickup.ogg")
        }
