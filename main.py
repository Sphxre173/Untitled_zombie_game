import pygame

#<---------------------------CONSTANT VALUE----------------------------->
pygame.init()
from config import *
from utils import *
from Sprite.Player import Player
from ui.Button import *
from ui.BG import Animated_BG
from image import *
from sound import *
from Sprite.Game_UI import *
from Sprite.Zombie import *
from Sprite.Item import *
from ui.SHOP import Animated_Shop
from ui.SHOP_BUTTON import Shop_Button
import GAME_STAT

def main():
    global clock, is_play, shop_sound_playing
    global player1, player_group, bullet_group, zombie_group, item_group, game_ui_class
    global level, boss_spawned_count
    # GAME LOOP VARIABLE
    awakening_sound_debouncer = False
    vignette_opacity = 0

    #INIT CLOCK
    clock = pygame.time.Clock()

    #check if json file is exist
    check_data_file()
    data = load_data()
    money = data["money"]
    gun_unlocked = data["gun_unlocked"]
    gun_equip = data["gun_equip"]

    #OBJECT
    player1 = Player()
    play_button_class = Button(play_button, 250, is_play_button)
    shop_button_class = Button(shop_button, 350, is_shop)
    quit_button_class = Button(quit_button, 450, is_quit)
    
    anim_bg = Animated_BG()
    shop_anim = Animated_Shop()
    game_ui_class = UI(player1)
    
    #init shop button
    if gun_unlocked["Glock"] == True:
        if gun_equip["Glock"] == True:
            shop_button_1 = Shop_Button(unequip_button, 257, equip_glock)
            GAME_STAT.current_bullet = 10
            GAME_STAT.max_current_bullet = 10
            player1.current_gun = "Glock"
            player1.update_gun()
        else:
            shop_button_1 = Shop_Button(equip_button, 257, equip_glock)

    if gun_unlocked["ak_47"] == True:
        if gun_equip["ak_47"] == True:
            shop_button_2 = Shop_Button(unequip_button, 520, equip_ak)
            GAME_STAT.current_bullet = 30
            GAME_STAT.max_current_bullet = 30
            player1.current_gun = "ak_47"
            player1.update_gun()
        else:
            shop_button_2 = Shop_Button(equip_button, 520, equip_ak)
    else:
        shop_button_2 = Shop_Button(buy_button, 520, equip_ak)
        
    #GROUP
    player_group = pygame.sprite.Group()
    button_group = pygame.sprite.Group()
    shop_button_group = pygame.sprite.Group(shop_button_1, shop_button_2)
    anim_bg_group = pygame.sprite.Group(anim_bg)
    shop_anim_group = pygame.sprite.Group(shop_anim)
    bullet_group = pygame.sprite.Group()
    zombie_group = pygame.sprite.Group()
    item_group = pygame.sprite.Group()

    player_group.add(player1)
    button_group.add(play_button_class, shop_button_class, quit_button_class)

    #VAR
    opacity = 0
    is_play = False
    is_game_over = False
    shop_sound_playing = False
    shop_base_x = -500
    was_mouse_pressed = False

    max_zombie = 5
    zombie_spawn_cooldown = 3000
    last_zombie_spawn_time = 0
    level = 1
    boss_spawned_count = 0

    #REVAMP YOUR CODE
    global state, anim_init_debouncer
    game_loop = True
    is_play_pause = False
    anim_init_debouncer = False
    is_soundtrack_play = False
    is_gameover_soundtrack = False
    state = "credit"

    #CREATE CREDIT 
    while game_loop:
        clock.tick(FPS_IN_GAME)
        tick = pygame.time.get_ticks()
        #event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    ####### CHECK PAUSE #######
                    if state == "play" and not is_game_over:
                        state = "pause"
                        player1.play_sound("stop")
                        anim_init_debouncer = False
                    elif state == "pause" and not is_game_over:
                        is_play_pause = False
                        state = "play"
                    ##### CHECK SHOP EXIT #####
                    if state == "shop":
                        to_lobby()
                        
                if event.key == pygame.K_f and state == "play" and not is_game_over:
                    if GAME_STAT.awakening_gauge >= GAME_STAT.awakening_max:
                        if not awakening_sound_debouncer:
                            awakening_toggle_sound.play()
                            awakening_sound_debouncer = True

                        GAME_STAT.is_awakening = True
                        GAME_STAT.awakening_start_time = pygame.time.get_ticks()
                #RELOAD KEYBIND
                if event.key == pygame.K_r and state == "play":
                    if GAME_STAT.total_bullet > 0:
                        bullet_need = GAME_STAT.max_current_bullet - GAME_STAT.current_bullet
                        if GAME_STAT.total_bullet >= bullet_need:
                            GAME_STAT.current_bullet += bullet_need
                            GAME_STAT.total_bullet -= bullet_need
                        else:
                            GAME_STAT.current_bullet += GAME_STAT.total_bullet
                            GAME_STAT.total_bullet = 0
                        was_mouse_pressed = False
                        reload_sound.play()
                #RESTART KEYBIND ESC
                if event.key == pygame.K_r and state == "pause":
                    #RESTART COMMAND HERE
                    reset_game()
                    state = "play"
                    is_play_pause = False
                    print("RESETTED")
                #QUIT TO LOBBY ESC
                if event.key == pygame.K_q and state == "pause":
                    #RESTART COMMAND HERE
                    reset_game()
                    is_play_pause = False
                    in_game_soundtrack.fadeout(3000)
                    is_soundtrack_play = False
                    to_lobby()
                    print("TO LOBBY")

                #RESTART KEYBIND GAMEOVER
                if event.key == pygame.K_r and state == "play" and is_game_over == True:
                    #RESTART COMMAND HERE
                    reset_game()
                    is_game_over = False
                    if not anim_init_debouncer:
                        if data["gun_equip"]["Glock"]:
                            player1.current_gun = "Glock"
                            player1.update_gun()
                        elif data["gun_equip"]["ak_47"]:
                            player1.current_gun = "ak_47"
                            player1.update_gun()
                        anim_init_debouncer = True
                    GAME_STAT.play_dead_animation = True
                    game_over_soundtrack.stop()
                    is_gameover_soundtrack = False
                    opacity = 0
                    print("RESETTED")
                #QUIT TO LOBBY GAMEOVER
                if event.key == pygame.K_q and state == "play" and is_game_over == True:
                    #RESTART COMMAND HERE
                    reset_game()
                    in_game_soundtrack.fadeout(3000)
                    is_soundtrack_play = False
                    opacity = 0
                    GAME_STAT.play_dead_animation = True
                    game_over_soundtrack.fadeout(2000)
                    is_gameover_soundtrack = False
                    to_lobby()
                    print("TO LOBBY")
        #first screen
        if state == "credit":
            if opacity <= 255:
                opacity += 1.3
                draw_bg(screen, ifie33, opacity)
                draw_game_logo(screen, logo_src, FONT, opacity)
                if opacity >= 255:
                    opacity = 0
                    #transition to lobby
                    state = "lobby"
        elif state == "lobby":
            data = load_data()
            money = data["money"]
            if not is_play:
                lobby_sound.set_volume(0.4)
                lobby_sound.play(-1)
                is_play = True
            draw_bg(screen, lobby_src, 255)
            anim_bg_group.update()
            button_group.update()
            anim_bg_group.draw(screen)
            display_money(money)
            button_group.draw(screen)
        elif state == "shop":
            #play shop soundtrack
            if not shop_sound_playing:
                shop_bell.play().set_volume(0.7)
                shop_sound.play(-1, 0, 2000).set_volume(0.1)
                shop_sound_playing = True
            shop_anim_group.update()
            shop_anim_group.draw(screen)
            target_x = 0
            shop_base_x += (target_x - shop_base_x) * 0.1

            data = load_data()
            gun_unlocked = data["gun_unlocked"]
            gun_equip = data["gun_equip"]
            if gun_unlocked["Glock"]:
                if gun_equip["Glock"]:
                    shop_button_1 = Shop_Button(unequip_button, 257, equip_glock)
                else:
                    shop_button_1 = Shop_Button(equip_button, 257, equip_glock)

            if gun_unlocked["ak_47"]:
                if gun_equip["ak_47"]:
                    shop_button_2 = Shop_Button(unequip_button, 520, equip_ak)
                else:
                    shop_button_2 = Shop_Button(equip_button, 520, equip_ak)
            else:
                shop_button_2 = Shop_Button(buy_button, 520, equip_ak)

            shop_button_group = pygame.sprite.Group(shop_button_1, shop_button_2)
            
            shop_button_group.update(shop_base_x)
            draw_shop_assets(screen, shop_base_x)
            shop_button_group.draw(screen)

        elif state == "play":
            current_time = pygame.time.get_ticks()
            is_game_over = player1.is_dead()
            data = load_data()

            if not anim_init_debouncer:
                if data["gun_equip"]["Glock"]:
                    player1.current_gun = "Glock"
                    player1.update_gun()

                elif data["gun_equip"]["ak_47"]:
                    player1.current_gun = "ak_47"
                    player1.update_gun()
                anim_init_debouncer = True
            print(anim_init_debouncer)
            
            if not is_game_over:
                if not GAME_STAT.is_awakening:
                    awakening_sound_debouncer = False

                if not is_soundtrack_play:
                    in_game_soundtrack.set_volume(0.2)
                    in_game_soundtrack.play(-1)
                    is_soundtrack_play = True
                #spawn the zombie
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0]:
                    if GAME_STAT.is_awakening:
                        fired = player1.shoot(bullet_group)
                        if fired:
                            shoot_sound.play()
                    else:
                        if GAME_STAT.current_bullet > 0:
                            fired = player1.shoot(bullet_group)
                            if fired:
                                GAME_STAT.current_bullet -= 1
                                shoot_sound.play()
                        else:
                            if not was_mouse_pressed:
                                empty_sound.play()

                    was_mouse_pressed = True
                else:
                    was_mouse_pressed = False

                if GAME_STAT.zombie_killed >= 5 and level == 1:
                    level = 2
                    max_zombie = 8
                    zombie_spawn_cooldown = 1500
                elif GAME_STAT.zombie_killed >= 30 and level == 2:
                    level = 3
                    max_zombie = 15
                    zombie_spawn_cooldown = 1000
                if current_time - last_zombie_spawn_time > zombie_spawn_cooldown:
                    for _ in range(2):
                        if len(zombie_group) < max_zombie:
                            spawn_zombie(player1, zombie_group, level)
                    last_zombie_spawn_time = current_time
                if GAME_STAT.zombie_killed >= (boss_spawned_count + 1) * 50:
                    boss_spawned_count += 1
                    x = SCREEN_WIDTH + 50
                    y = random.randint(400, SCREEN_HEIGHT-30)
                    boss = Zombie(
                        player1,
                        spawn_pos=(x, y),
                        hp=50 + boss_spawned_count * 10,
                        reward=500,
                        attack_power= 20 + boss_spawned_count * 5,
                        speed=1.2,
                        sprite_pics={
                            "walk": ZOMBIE_BOSS_SPRITE_RUN,
                            "hit": ZOMBIE_BOSS_SPRITE_HIT,
                            "death": ZOMBIE_BOSS_SPRITE_DEAD
                        }
                    )
                    boss.is_boss = True
                    zombie_group.add(boss)

                    print(f"🔥 BOSS ROUND {boss_spawned_count}")
                draw_bg(screen, in_game_bg, 255)
                
                ############################## CHECK COLIDE #######################################
                # BULLET COLIDE CHECKssss
                is_bullet_hit = pygame.sprite.groupcollide(bullet_group, zombie_group, True, False)
                # if bullet is hit
                if is_bullet_hit:
                    #check which zombie is hit and - hp of zombie
                    for bullet, hit_list in is_bullet_hit.items():
                        for zombie in hit_list:
                            if zombie.state == "death":
                                continue  
                            damage = bullet.damage
                            if GAME_STAT.is_awakening:
                                damage *= 2
                            destroy = zombie.take_damage(damage)
                            if not GAME_STAT.is_awakening:
                                GAME_STAT.awakening_gauge += 2
                            if GAME_STAT.awakening_gauge > GAME_STAT.awakening_max:
                                GAME_STAT.awakening_gauge = GAME_STAT.awakening_max
                        if destroy:
                            if random.random() < 0.3:
                                item_type = random.choice(["medicine", "ammo_box", "coin_box"])
                                item = Item(item_type, (zombie.rect.centerx, zombie.rect.centery),current_time)
                                item_group.add(item)
                            GAME_STAT.zombie_killed += 1
                            data = load_data()
                            data["money"] += zombie.money_reward
                            data["zombie_killed"] += 1
                            save_data(data)
                player1.check_collision(zombie_group, tick)
                # PLAYER COLIDE ITEM CHECK
                item_hit = pygame.sprite.groupcollide(item_group, player_group, True, False)
                if item_hit:
                    for item_check in item_hit:
                        if item_check.item_type == "ammo_box":
                            GAME_STAT.total_bullet += 20
                            bullet_box_sound.set_volume(1.2)
                            bullet_box_sound.play()
                        elif item_check.item_type == "medicine":
                            player1.hp = min(player1.hp + 10, 100)
                            medkit_sound.play()
                        elif item_check.item_type == "coin_box":
                            data = load_data()
                            data["money"] += 50
                            save_data(data)
                        item_check.kill()
                if GAME_STAT.is_awakening:
                    current_time = pygame.time.get_ticks()
                    elapsed = current_time - GAME_STAT.awakening_start_time

                    if elapsed >= GAME_STAT.awakening_duration:
                        GAME_STAT.is_awakening = False
                        GAME_STAT.awakening_gauge = 0
                        print("หมดร่างทอง")
                    else:
                        ratio = 1 - (elapsed / GAME_STAT.awakening_duration)
                        ratio = max(0, ratio)
                        GAME_STAT.awakening_gauge = GAME_STAT.awakening_max * ratio
                #UPDATE AND DISPLAY
                player_group.update()
                bullet_group.update()
                zombie_group.update(zombie_group)
                item_group.update()
                item_group.draw(screen)
                zombie_group.draw(screen)
                bullet_group.draw(screen)
                player_group.draw(screen)
                
                ratio = GAME_STAT.awakening_gauge / GAME_STAT.awakening_max

                ratio = ratio ** 2

                target_opacity = int(ratio * 200)

                if GAME_STAT.awakening_gauge >= GAME_STAT.awakening_max and not GAME_STAT.is_awakening:
                    target_opacity = 200
                    vignette_opacity += (target_opacity - vignette_opacity) * 0.25
                else:
                    vignette_opacity += (target_opacity - vignette_opacity) * 0.1

                vignette_awakening.set_alpha(int(vignette_opacity))
                screen.blit(vignette_awakening, (0, 0))
                game_ui_class.draw_all()
            else:
                #stop soundtrack
                in_game_soundtrack.fadeout(1500)
                is_soundtrack_play = False
                if not is_gameover_soundtrack:
                    game_over_soundtrack.set_volume(0.2)
                    game_over_soundtrack.play(-1)
                    is_gameover_soundtrack = True
                draw_bg(screen, in_game_bg, 255)
                if opacity <= 155:
                    opacity += 1
                show_death_animation(GAME_STAT.play_dead_animation, opacity)
                player1.play_sound("stop")
        elif state == "pause":
            if not is_play_pause:
                print("is pause")
                draw_bg(screen, temp_pause_screen, 125)
                toggle_pause_ui()
                is_play_pause = True
        pygame.display.flip()

def reset_game():

    global player1, player_group, bullet_group, zombie_group, item_group
    global max_zombie, zombie_spawn_cooldown, last_zombie_spawn_time, game_ui_class
    global is_game_over, level, boss_spawned_count,vignette_opacity

    player1 = Player()
    game_ui_class = UI(player1)

    data = load_data()
    if data["gun_equip"]["Glock"]:
        player1.current_gun = "Glock"
    elif data["gun_equip"]["ak_47"]:
        player1.current_gun = "ak_47"

    player1.update_gun()

    # RESET PLAYER

    player_group.empty()
    bullet_group.empty()
    zombie_group.empty()
    item_group.empty()

    player_group.add(player1)
    # RESET GROUP

    # RESET GAME STAT
    gun_equip = data["gun_equip"]
    if gun_equip["Glock"]:
        GAME_STAT.current_bullet = 10
        GAME_STAT.max_current_bullet = 10
    elif gun_equip["ak_47"]:
        GAME_STAT.current_bullet = 30
        GAME_STAT.max_current_bullet = 30
    
    GAME_STAT.total_bullet = 100
    GAME_STAT.zombie_killed = 0
    
    GAME_STAT.awakening_max = 100
    GAME_STAT.is_awakening = False
    GAME_STAT.awakening_duration = 10000
    GAME_STAT.awakening_start_time = 0
    GAME_STAT.awakening_gauge = 0
    # RESET LEVEL SYSTEM
    level = 1
    max_zombie = 5
    zombie_spawn_cooldown = 3000
    boss_spawned_count = 0
    vignette_opacity = 0
    last_zombie_spawn_time = pygame.time.get_ticks()

    # RESET GAME STATE
    is_game_over = False

def is_play_button():
    global state, is_play, anim_init_debouncer
    fade(screen, clock, fade_in=False, speed=2)
    lobby_sound.stop()
    is_play = False
    anim_init_debouncer = False
    state = "play"
    fade(screen, clock, fade_in=True)

def to_lobby():
    global state, is_play, shop_sound_playing, anim_init_debouncer
    fade(screen, clock, fade_in=False, speed=2)
    lobby_sound.stop()
    shop_sound.fadeout(500)
    state = "lobby"
    is_play = False
    anim_init_debouncer = False
    shop_sound_playing = False
    fade(screen, clock, fade_in=True)

def equip_glock():
    data = load_data()
    for gun in data["gun_equip"]:
        data["gun_equip"][gun] = False

    data["gun_equip"]["Glock"] = True

    save_data(data)
    GAME_STAT.current_bullet = 10
    GAME_STAT.max_current_bullet = 10
    state = "shop"  # reload state

def equip_ak():
    data = load_data()
    if data["money"] >= 4700 and not data["gun_unlocked"]["ak_47"]:
        data["gun_unlocked"]["ak_47"] = True
        data["money"] -= 4700
        print("Unlocked")
    else:
        print("not enough cash")

    if data["gun_unlocked"]["ak_47"] == True:
        for gun in data["gun_equip"]:
            data["gun_equip"][gun] = False
        data["gun_equip"]["ak_47"] = True
        save_data(data)
        GAME_STAT.current_bullet = 30
        GAME_STAT.max_current_bullet = 30
    state = "shop"  # reload state


def is_shop():
    global state                     
    fade(screen, clock, fade_in=False, speed=2)
    lobby_sound.stop()
    state = "shop"
    fade(screen, clock, fade_in=True)

def is_quit():
    pygame.quit()

main()

                ### TASK ###

# MAIN SYSTEM 
# - make restart feature            #COMPLETED
# - make shop usable (slowest)      #COMPLETED
# - make game over screen (restart) #COMPLETED
# - make better player ui           #COMPLETED

# FRONTEND
# - draw bg                         #COMPLETED
# - make pause ui                   #COMPLETED
# - make character animation        #COMPLETED
# - make zombie animation           #COMPLETED
# - make shop illustrator           #COMPLETED
# - make gun illustrator            #COMPLETED

#               YAYYYYYYYYYYY

# EXTRA (DO THIS AFTER MAIN GAME AND FRONT END IS FINISHED)
# MAKE A THROWABLE STUFF LIKE MOLOTOV FLASH GRENADE OR SMTH 

#### fix a health bar by using if health <= 0: health bar x = 0####