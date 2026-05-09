import pygame
from image import BG_SPRITE 
from config import screen

class Animated_BG(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame = BG_SPRITE
        self.frame_index = 0
        self.animation_speed = 1.1
        self.image = self.frame[self.frame_index]
        self.rect = self.image.get_rect(topleft=(0,0))
    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frame):
            self.frame_index = 0
        self.image = self.frame[int(self.frame_index)]