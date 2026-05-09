from image import SHOP_SPRITE_CURTAIN_ON, SHOP_SPRITE_IDLE
import pygame

class Animated_Shop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame = SHOP_SPRITE_CURTAIN_ON
        self.animation_index = 0
        self.animation_speed = 1
        self.image = self.frame[self.animation_index]
        self.rect = self.image.get_rect()
    def update(self):
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.frame):
            self.animation_index = 0
            self.frame = SHOP_SPRITE_IDLE
            #insert loop animation here
        self.image = self.frame[int(self.animation_index)]