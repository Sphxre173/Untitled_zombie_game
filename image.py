from utils import load_image, create_surface, resize, SCREEN_WIDTH, SCREEN_HEIGHT, half_size_resize, load_alpha
logo_src = resize(load_image(r"ASSETS\IMAGE\PROFILE\PFP.png"), 0.40)

lobby_src = load_image(r"ASSETS\IMAGE\BG_LOBBY\BG\Artboard 1.png")
play_button = load_image(r"ASSETS\IMAGE\BG_LOBBY\BUTTON\PLAY BUTTON.png")
endless_button = load_image(r"ASSETS\IMAGE\BG_LOBBY\BUTTON\ENDLESS.png")
setting_button = load_image(r"ASSETS\IMAGE\BG_LOBBY\BUTTON\SETTING.png")
shop_button = load_image(r"ASSETS\IMAGE\BG_LOBBY\BUTTON\SHOP.png")
quit_button = load_image(r"ASSETS\IMAGE\BG_LOBBY\BUTTON\QUIT.png")
awaken_frame = resize(load_image(r"ASSETS\In_game_assets\Awakening bar\with shadow.png"),0.37)
ifie33 = create_surface(SCREEN_WIDTH, SCREEN_HEIGHT, '#1f1e33')
bullet_img = create_surface(30, 15, "#FF4800")
bullet_icon_color = load_image(r'ASSETS\IMAGE\BULLET\bullet_colored.png')
bullet_icon_bw = load_image(r"ASSETS\IMAGE\BULLET\bullet_bw.png")
pause_screen_ui = load_image(r"ASSETS\IMAGE\PAUSE_UI'\Paused_screen.png")
glock_base = load_image(r"ASSETS\IMAGE\SHOP_ASSETS\GLOCK 17.png")
ak_base = load_image(r"ASSETS\IMAGE\SHOP_ASSETS\AK_47.png")
buy_button = load_image(r"ASSETS\IMAGE\SHOP_ASSETS\BUY.png")
equip_button = load_image(r"ASSETS\IMAGE\SHOP_ASSETS\Equip.png")
unequip_button = load_image(r"ASSETS\IMAGE\SHOP_ASSETS\UNEQUIP.png")
ui_bar = half_size_resize(load_image(r"ASSETS\IMAGE\UI\bar.png"))
in_game_bg = load_image(r"ASSETS\In_game_assets\BG\in_game_bg.png")
vignette_awakening = load_alpha(r"ASSETS\In_game_assets\Awakening bar\vignette_downscaled.png")

#TEMPORARY STUFF
temp_battle_field = create_surface(SCREEN_WIDTH, SCREEN_HEIGHT, '#333333')
temp_shop_screen = create_surface(SCREEN_WIDTH, SCREEN_HEIGHT, "#823131")
temp_pause_screen = create_surface(SCREEN_WIDTH, SCREEN_HEIGHT, "#000000")



#ITEM_LOADER
medicine = [resize(load_image(rf"ASSETS\In_game_assets\Item\MEDKIT\0{i}_item animations -medkit.png"), 4)
                   for i in range(0, 7)]
coin_box = [resize(load_image(rf"ASSETS\In_game_assets\Item\CHEST\0{i}_item animations -MetalChest.png"), 4)
                   for i in range(0, 7)]
bullet_box = [resize(load_image(rf"ASSETS\In_game_assets\Item\AMMO\0{i}_item animations -ammo-rifle.png"), 4)
                   for i in range(0, 7)]


#picture\player_blue\run\
PLAYER_RUN_AK_SPRITE= [resize(load_image(rf"ASSETS\IMAGE\PLAYER_ANIM\AK_ANIM\char_ak_running_fixed_shadow\file_name_{i}.png"), 0.9)
                   for i in range(1, 41)]
PLAYER_IDLE_AK_SPRITE = [resize(load_image(rf"ASSETS\IMAGE\PLAYER_ANIM\AK_ANIM\char_ak_idle_shadow_fix\file_name_{i}.png"), 0.9)
                   for i in range(1, 41)]
PLAYER_RUN_GLOCK_SPRITE= [resize(load_image(rf"ASSETS\IMAGE\PLAYER_ANIM\GLOCK\Char_pistol_running\file_name_{i}.png"), 0.9)
                   for i in range(1, 36)]
PLAYER_IDLE_GLOCK_SPRITE = [resize(load_image(rf"ASSETS\IMAGE\PLAYER_ANIM\GLOCK\char_pistol_idle\file_name_{i}.png"), 0.9)
                   for i in range(1, 37)]
PLAYER_DEAD_SPRITE = [resize(load_image(rf"ASSETS\IMAGE\PLAYER_ANIM\char_dead_anim\file_name_{i}.png"), 1.05)
                      for i in range(0, 57)]



ZOMBIE_LVL1_SPRITE_RUN = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_lv1\RUN\0{i}_Zombie_run.png"), 3)
                      for i in range(0, 8)]

ZOMBIE_LVL1_SPRITE_HIT = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_lv1\HIT\0{i}_Zombie_Hit.png"), 3)
                      for i in range(0, 3)]

ZOMBIE_LVL1_SPRITE_KNOCKED = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_lv1\KNOCKED\0{i}_Zombie_knocked .png"), 3)
                      for i in range(0, 6)]

ZOMBIE_LVL1_SPRITE_DEAD = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_lv1\DEAD\0{i}_Zombie_Death 1.png"), 3)
                      for i in range(0, 8)]



ZOMBIE_LVL2_SPRITE_RUN = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_lv2\RUN\0{i}_Zombie 2_Run.png"), 3)
                      for i in range(0, 8)]

ZOMBIE_LVL2_SPRITE_HIT = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_lv2\HIT\0{i}_Zombie 2_Hit.png"), 3)
                      for i in range(0, 3)]

ZOMBIE_LVL2_SPRITE_KNOCKED = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_lv2\KNOCKED\0{i}_Zombie 2_knocked.png"), 3)
                      for i in range(0, 6)]

ZOMBIE_LVL2_SPRITE_DEAD = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_lv2\DEAD\0{i}_Zombie 2_Death 1 .png"), 3)
                      for i in range(0, 8)]



ZOMBIE_LVL3_SPRITE_RUN = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_lv3\RUN\0{i}_Zombie 3_run.png"), 3)
                      for i in range(0, 8)]

ZOMBIE_LVL3_SPRITE_HIT = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_lv3\HIT\0{i}_Zombie 4_hit.png"), 3)
                      for i in range(0, 3)]

ZOMBIE_LVL3_SPRITE_KNOCKED = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_lv3\KNOCKED\0{i}_Zombie 4_knocked .png"), 3)
                      for i in range(0, 6)]

ZOMBIE_LVL3_SPRITE_DEAD = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_lv3\DEAD\0{i}_Zombie 4_death 4.png"), 3)
                      for i in range(0, 8)]



ZOMBIE_BOSS_SPRITE_RUN = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_BOSS\RUN\0{i}_Zombie 3_run .png"), 3)
                      for i in range(0, 8)]

ZOMBIE_BOSS_SPRITE_HIT = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_BOSS\HIT\0{i}_Zombie 3_Hit .png"), 3)
                      for i in range(0, 3)]

ZOMBIE_BOSS_SPRITE_KNOCKED = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_BOSS\KNOCKED\0{i}_Zombie 3_knocked .png"), 3)
                      for i in range(0, 6)]

ZOMBIE_BOSS_SPRITE_DEAD = [resize(load_image(rf"ASSETS\In_game_assets\Zombie\zombie_BOSS\DEAD\0{i}_Zombie 3_death.png"), 3)
                      for i in range(0, 8)]





BG_SPRITE = [load_image(rf"lobby_renamed\file_name_{i}.png")
             for i in range(0, 601)]

SHOP_SPRITE_CURTAIN_ON = [load_image(rf"SHOP_ANIM\file_name_{i}.png")
             for i in range(0, 300)]

SHOP_SPRITE_IDLE = [load_image(rf"SHOP_ANIM_IDLE\file_name_{i}.png")
             for i in range(0, 552)]