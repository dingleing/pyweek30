import pygame
from pygame import mixer

#Background music
mixer.music.load("background.wav")
mixer.music.play(-1)

#Starting music
OpenSound = mixer.Sound("Opener.wav")
OpenSound.play()

# copy paste the below codes where you have written the codes of explosion and notation 1-6 respectively.
explosionSound = mixer.Sound("explosion.wav")
explosionSound.play()

#1
click_sound = mixer.Sound("ButtonClick.wav")
click_sound.play()

#2
engine_pickup_sound = mixer.Sound("EnginePickup.wav")
engine_pickup_sound.play()

#3
item_pickup_sound = mixer.Sound("ItemPickup.wav")
item_pickup_sound.play()

#4
portal_sound = mixer.Sound("Portal.wav")
portal_sound.play()

#5
powerup_sound = mixer.Sound("Powerup.wav")
powerup_sound.play()

#6
walking_sound = mixer.Sound("Walking.wav")
walking_sound.play()



#Turyam