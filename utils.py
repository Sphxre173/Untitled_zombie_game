import pygame
from config import *
import os
import json
import random
import GAME_STAT

def create_surface(w, h, color):
    surface = pygame.surface.Surface((w, h))
    surface.fill(color)
    return surface

def resize(image, size:float):
    return pygame.transform.smoothscale(
        image, (image.get_rect().width * size, image.get_rect().height * size)
    )

def half_size_resize(image):
    return pygame.transform.scale(
        image, (image.get_rect().width//2.3, image.get_rect().height//2.3)
    )

def load_image(image) -> pygame.image:
    return pygame.image.load(image)

def load_alpha(img):
    return pygame.image.load(img).convert_alpha()

def load_sound(sound_path:str)->pygame.mixer.Sound:
    return pygame.mixer.Sound(sound_path)

def draw_bg(screen, img_src, opacity=0):
    img_src.set_alpha(opacity)
    screen.blit(img_src, (0, 0))


def draw_game_logo(screen, logo_src, font, opacity):
    get_time = pygame.time.get_ticks()
    rendered = font.render("Maded by", True, WHITE)
    rendered.set_alpha(opacity)
    logo_src.set_alpha(opacity)
    screen.blit(logo_src, (SCREEN_WIDTH//2 - logo_src.get_rect().width//2,
                          SCREEN_HEIGHT//2 - logo_src.get_rect().height//2))
    screen.blit(rendered, (SCREEN_WIDTH//2 - rendered.get_rect().width//2,
                          (SCREEN_HEIGHT//2 - rendered.get_rect().height//2) - 90))
    
def fade(screen, clock, fade_in=True, speed=3):
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0,0,0))
    if fade_in:
        alpha_range = range(255, -1, -speed)
    else:
        alpha_range = range(0, 256, speed)

    for alpha in alpha_range:
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0,0))
        pygame.display.update()
        clock.tick(FPS)

def display_money(money):
    money_y = 20
    money_render = FONT.render(f"Money : {money}", True, WHITE)
    money_x = (SCREEN_WIDTH-money_render.get_width())-20
    screen.blit(money_render, (money_x, money_y))

def check_data_file()->dict|None:
    check_file = os.listdir(r"USER_DATA")
    if "Player_data.json" in check_file:
        with open(os.path.join("USER_DATA", "Player_data.json"), "r") as file:
            dat = json.load(file)
            return dat["money"]
    else:
        data = {
            "money" : 0,
            "zombie_killed" : 0,
            "gun_unlocked" : {
                "Glock" : True,
                "ak_47" : False
            },
            "gun_equip" : {
                "Glock" : True,
                "ak_47" : False
            }
        }

        with open(os.path.join("USER_DATA", "Player_data.json"), "w") as file:
            dat = json.dumps(data, indent=4)
            file.write(dat)

def load_data():
    with open(os.path.join("USER_DATA", "Player_data.json"), "r") as f:
        return json.load(f)

def save_data(data):
    with open(os.path.join("USER_DATA", "Player_data.json"), "w") as f:
        json.dump(data, f, indent=4)

""" def update_json(money:bool=False, money_amount:int=0, gun_unlock:bool=False, gun_name:str=None):
    if money:
        with open(os.path.join("USER_DATA", "Player_data.json"), "r") as file:
            dat = json.load(file)
            dat["money"] += money_amount
            dat["zombie_killed"] += 1
        with open(os.path.join("USER_DATA", "Player_data.json"), "w") as file:
            dat = json.dumps(dat)
            print("saved")
            file.write(dat)
    if gun_unlock:
        if gun_name == "ak_47":
            with open(os.path.join("USER_DATA", "Player_data.json"), "r") as file:
                dat = json.load(file)
                dat["gun_unlocked"]["ak_47"] = True
                dat["gun_equip"]["ak_47"] = True
            with open(os.path.join("USER_DATA", "Player_data.json"), "w") as file:
                dat = json.dumps(dat)
                print("saved")
                file.write(dat) """

def spawn_zombie(target, zombie_group, player_level):
    from Sprite.Zombie import Zombie
    from image import ZOMBIE_LVL1_SPRITE_HIT, ZOMBIE_LVL1_SPRITE_DEAD, ZOMBIE_LVL1_SPRITE_KNOCKED, ZOMBIE_LVL1_SPRITE_RUN, ZOMBIE_LVL2_SPRITE_DEAD, ZOMBIE_LVL2_SPRITE_KNOCKED, ZOMBIE_LVL2_SPRITE_HIT, ZOMBIE_LVL2_SPRITE_RUN, ZOMBIE_LVL3_SPRITE_DEAD, ZOMBIE_LVL3_SPRITE_HIT, ZOMBIE_LVL3_SPRITE_KNOCKED, ZOMBIE_LVL3_SPRITE_RUN
    side = random.choice(["left", "right"])
    hp = 0
    reward = 0
    attack_power = 0
    speed = 0
    
    #random zombie
    if player_level >= 3 and random.randint(1, 8) == 1:
        hp = 5
        reward = 10
        attack_power = 5
        speed = 3
        current_sprite = {
                            "walk": ZOMBIE_LVL3_SPRITE_RUN,
                            "hit": ZOMBIE_LVL3_SPRITE_HIT,
                            "death": ZOMBIE_LVL3_SPRITE_DEAD
                        }    
    elif player_level >= 2 and random.randint(1, 4) == 1:
        hp = 3
        reward = 5
        attack_power = 3
        speed = 2
        current_sprite = {
                            "walk": ZOMBIE_LVL2_SPRITE_RUN,
                            "hit": ZOMBIE_LVL2_SPRITE_HIT,
                            "death": ZOMBIE_LVL2_SPRITE_DEAD
                        }    
    else:
        hp = 1
        reward = 3
        attack_power = 1
        speed = 1
        current_sprite = current_sprite = {
                            "walk": ZOMBIE_LVL1_SPRITE_RUN,
                            "hit": ZOMBIE_LVL1_SPRITE_HIT,
                            "death": ZOMBIE_LVL1_SPRITE_DEAD
                        }    
            
    if side == "top":
        x = random.randint(0, SCREEN_WIDTH)
        y = -50
    elif side == "bottom":
        x = random.randint(0, SCREEN_WIDTH)
        y = SCREEN_HEIGHT + 50
    elif side == "left":
        x = -50
        y = random.randint(400, SCREEN_HEIGHT-30)
    else:
        x = SCREEN_WIDTH + 50
        y = random.randint(400, SCREEN_HEIGHT-30)
    zombie = Zombie(target, (x, y), hp, reward, attack_power, speed, current_sprite)
    zombie_group.add(zombie)

def draw_shop_assets(screen, base_x):
    from image import glock_base, ak_base
    glock_y = 110
    ak_y = 370
    screen.blit(glock_base, (base_x, glock_y))
    screen.blit(ak_base, (base_x, ak_y))

def toggle_pause_ui():
    from image import pause_screen_ui
    rect = pause_screen_ui.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(pause_screen_ui, rect)

def show_death_animation(play_animate, opacity):
    from image import PLAYER_DEAD_SPRITE, in_game_bg, temp_pause_screen
    import GAME_STAT
    if play_animate:
        GAME_STAT.play_dead_animation = False
        for i, frame in enumerate(PLAYER_DEAD_SPRITE):
            screen.blit(in_game_bg, (0,0))
            screen.blit(frame, (SCREEN_WIDTH//2 - frame.get_width()//2, 
                               (SCREEN_HEIGHT//2 - frame.get_height()//2)+100))
            pygame.display.flip()
            pygame.time.wait(10)
            if i == len(PLAYER_DEAD_SPRITE) - 1:
                break
    else:
        special_game_over = pygame.font.SysFont("DB Adman X", 130, False)
        special_guide = pygame.font.SysFont("DB Adman X", 55, False)
        game_over_font = special_game_over.render("GAME OVER!", True, WHITE)
        stat_font = special_guide.render(f"Zombie killed : {GAME_STAT.zombie_killed}", True, WHITE)
        guide_font = special_guide.render(f"Press R to retry | Q to lobby", True, WHITE)

        temp_pause_screen.set_alpha(opacity)
        screen.blit(temp_pause_screen, (0, 0))
        screen.blit(game_over_font, (SCREEN_WIDTH//2 - game_over_font.get_width()//2,
                                     (SCREEN_HEIGHT//2 - game_over_font.get_height()//2)-250))
        screen.blit(stat_font, (SCREEN_WIDTH//2 - stat_font.get_width()//2,
                                (SCREEN_HEIGHT//2 - stat_font.get_height()//2)-170))
        screen.blit(guide_font, (SCREEN_WIDTH//2 - guide_font.get_width()//2,
                                (SCREEN_HEIGHT//2 - guide_font.get_height()//2)-110))
        
        screen.blit(PLAYER_DEAD_SPRITE[55], (SCREEN_WIDTH//2 - PLAYER_DEAD_SPRITE[55].get_width()//2, 
                                    (SCREEN_HEIGHT//2 - PLAYER_DEAD_SPRITE[55].get_height()//2)+100))

#FIX SHOW DEATH ANIM AFTER LUNCH