import pygame
import math
from utils import *
from config import *
from image import *
from Sprite.Bullet import *
from sound import *
import GAME_STAT

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 6
        self.is_moving = False
        self.frame = 0 #frame is for like indicate location of each picture
        self.animation_speed = 0.5
        self.is_facing_right = True
        self.run_playing = False
        self.hp = 60
        self.last_hit_time = 0
        self.cooldown = 1000
        self.player_idle_sprite = PLAYER_IDLE_GLOCK_SPRITE
        self.player_run_sprite = PLAYER_RUN_GLOCK_SPRITE
        self.animation_index = 0
        self.current_gun = "Glock"
        
        self.image = PLAYER_IDLE_GLOCK_SPRITE[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = SCREEN_WIDTH//2, SCREEN_HEIGHT//2

        self.hitbox = pygame.Rect(0, 0, 30, 40)  # ปรับขนาดได้
        self.hitbox.center = self.rect.center

        self.gun_data = {
            "Glock": {
                "damage": 1,
                "fire_rate": 400  # ms
            },
            "ak_47": {
                "damage": 2,
                "fire_rate": 120
            }
        }

        self.last_shot_time = 0
        self.player_run_sound = load_sound(r"picture\Sound\Running.wav")
        self.hurt_sound = zombie_attack_sound
    def update_gun(self):
        set_image = {
            "Glock" : (PLAYER_RUN_GLOCK_SPRITE, PLAYER_IDLE_GLOCK_SPRITE),
            "ak_47" : (PLAYER_RUN_AK_SPRITE, PLAYER_IDLE_AK_SPRITE)
        }
        self.player_run_sprite, self.player_idle_sprite = set_image[self.current_gun]
        self.animation_index = 0
    def update(self):
        self.is_moving = False
        key_captured = pygame.key.get_pressed()
        if key_captured[pygame.K_w]:
            if self.hitbox.top <= 380:
                self.hitbox.top = 380
            else:
                self.hitbox.y -= self.speed
                self.is_moving = True
        if key_captured[pygame.K_s]:
            if self.hitbox.bottom >= SCREEN_HEIGHT:
                self.hitbox.bottom = SCREEN_HEIGHT
            else:
                self.hitbox.y += self.speed
                self.is_moving = True
        if key_captured[pygame.K_a]:
            if self.hitbox.left <= 0:
                self.hitbox.left = 0
            else:
                self.hitbox.x -= self.speed
                self.is_moving = True
            self.is_facing_right = False
        if key_captured[pygame.K_d]:
            if self.hitbox.right >= SCREEN_WIDTH:
                self.hitbox.right = SCREEN_WIDTH
            else:
                self.hitbox.x += self.speed
                self.is_moving = True
            self.is_facing_right = True
        
        if self.is_moving:
            self.frame = self.player_run_sprite
            self.play_sound("run")
        else:
            self.frame = self.player_idle_sprite
            self.play_sound("stop")
        self.animate()
        self.rect.center = self.hitbox.center
        """ print(self.is_facing_right)
 """
    def play_sound(self, command:str):
        if command == "run" and not self.run_playing:
            self.player_run_sound.play(-1)
            self.run_playing = True
        elif command == "stop":
            self.player_run_sound.stop()
            self.run_playing = False
        elif command == "hurt":
            self.hurt_sound.set_volume(0.5)
            self.hurt_sound.play()



    def animate(self):
        #add speed to change frame value by 0.3 each loop
        self.animation_index += self.animation_speed
        #chack if animation index have more than length of self.frame that currently on
        if self.animation_index >= len(self.frame):
            self.animation_index = 0
        self.image = self.frame[int(self.animation_index)]
        
        #check if turn status is not from original place
        if not self.is_facing_right:
            #flip the image
            self.image = pygame.transform.flip(self.image, True, False)

    def check_collision(self, zombies, current_time):
        hit = False
        for z in zombies:
            if self.hitbox.colliderect(z.rect):
                if current_time - self.last_hit_time > self.cooldown:
                    print("hit!")
                    hit = True
                    self.hp -= z.attack_power
                    self.play_sound("hurt")
        if hit:
            self.last_hit_time = current_time
            
    def shoot(self, bullet_group):
        now = pygame.time.get_ticks()
        gun = self.gun_data[self.current_gun]

        if now - self.last_shot_time < gun["fire_rate"]:
            return False

        self.last_shot_time = now

        mouse_pos = pygame.mouse.get_pos()
        player_pos = self.rect.center

        direction = pygame.Vector2(mouse_pos) - pygame.Vector2(player_pos)

        if direction.length() == 0:
            return False

        direction = direction.normalize()

        bullet = Bullet(player_pos, direction, gun["damage"])
        bullet_group.add(bullet)

        return True
    
    def is_dead(self):
        return not self.hp > 0