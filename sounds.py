import pygame

pygame.mixer.pre_init(48000, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(16)


class Sounds:
    def __init__(self):
        self.sounds = {
            "Power_up": pygame.mixer.Sound("assets/Sounds/Powerup.wav"),
            "Portal-transport": pygame.mixer.Sound("assets/Sounds/Portal_transport.wav"),
            "Walking": pygame.mixer.Sound("assets/Sounds/Walking.wav"),
            "Item-pickup": pygame.mixer.Sound("assets/Sounds/ItemPickup.wav"),
            "explosion": pygame.mixer.Sound("assets/Sounds/explosion.wav"),
            "Opener": pygame.mixer.Sound("assets/Sounds/Opener.wav"),
            "Click": pygame.mixer.Sound("assets/Sounds/Click.wav"),
            "EnginePickup": pygame.mixer.Sound("assets/Sounds/EnginePickup.wav"),
            "Door": pygame.mixer.Sound("assets/Sounds/door_opening.wav")
        }
