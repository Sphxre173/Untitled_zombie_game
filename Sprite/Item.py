from image import *
import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, item_type, spawn_pos_xy:tuple, creation_time):
        super().__init__()

        item_images = {
            "medicine": medicine,
            "ammo_box": bullet_box,
            "coin_box": coin_box
        }

        self.item_type = item_type
        self.frames = item_images[self.item_type]   # ✅ เก็บ list ของภาพ
        self.animation_index = 0
        self.animation_speed = 0.1

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = spawn_pos_xy

        self.creation_time = creation_time
        self.lifetime = 5000

    def update(self):
        self.animation_index += self.animation_speed

        if self.animation_index >= len(self.frames):
            self.animation_index = 0

        self.image = self.frames[int(self.animation_index)]

        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time > self.lifetime:
            self.kill()