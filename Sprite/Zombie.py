import pygame
from image import *

class Zombie(pygame.sprite.Sprite):
    def __init__(self, target,spawn_pos:tuple, hp, reward, attack_power, speed, sprite_pics:dict):
        super().__init__()
        self.animations = sprite_pics
        #CHANGE THIS TO SPRITE_PIC PARAM LATER    
        self.state = "walk"
        self.animation_index = 0
        self.image = self.animations[self.state][0]
        self.animation_speed = 0.3
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = spawn_pos
        self.player = target
        self.should_flip = False
        self.hp = hp
        self.money_reward = reward
        self.attack_power = attack_power
        self.speed = speed
    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.animation_index = 0
    def animation(self):
        frames = self.animations[self.state]

        self.animation_index += self.animation_speed

        if self.animation_index >= len(frames):
            if self.state == "death":
                self.kill()
                return
            elif self.state == "hit":
                self.set_state("walk")

            self.animation_index = 0

        self.image = frames[int(self.animation_index)]

        if not self.should_flip:
            self.image = pygame.transform.flip(self.image, True, False)
    def update(self, zombies:list):

        self.animation()
        if self.state == "death":
            return

        inflated_self = self.rect.inflate(-20, -20)
        for other_zombies in zombies:
            if self != other_zombies and inflated_self.colliderect(other_zombies.rect):
                if self.rect.centerx < other_zombies.rect.centerx:
                    self.rect.x -= 1
                else:
                    self.rect.x += 1
                if self.rect.centery < other_zombies.rect.centery:
                    self.rect.y -= 1
                else:
                    self.rect.y += 1
        
        player_pos = self.player.rect.center
        zombie_pos = self.rect.center

        direction = pygame.Vector2(player_pos) - pygame.Vector2(zombie_pos)

        if direction.length() != 0:
            direction = direction.normalize()

        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

        self.should_flip = direction.x < 0

    def take_damage(self, damage):
        if self.state == "death":
            return False
        self.hp -= damage

        if self.hp > 0:
            self.set_state("hit")
            return False
        else:
            self.set_state("death")
            return True