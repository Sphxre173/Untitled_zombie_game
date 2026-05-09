import GAME_STAT
from config import *
from image import *
from utils import create_surface, check_data_file, display_money

class UI:
    def __init__(self, player):
        self.player = player
    def draw_ui(self):
        screen.blit(ui_bar, (30, 30))
    def draw_rect(self):
        width = 320
        height = 35
        ratio = self.player.hp / 100
        if self.player.hp<=0:
            hp_bar = 0
        else:
            hp_bar = width * ratio
        x, y = 292/2, 40
        bar = create_surface(hp_bar, height, "#0aff74")
        screen.blit(bar, (x, y))
    def draw_red_rect(self):
        width = 320
        height = 35
        x, y = 292/2, 40
        bar = create_surface(width, height, "#ff0a3f")
        screen.blit(bar, (x, y))

    def draw_bullet_bar(self):
        x = 215
        y = 85
        current_bullet = FONT.render(f"x{GAME_STAT.current_bullet}", True, WHITE)
        screen.blit(current_bullet, (x, y))
        
    def display_total_bullet(self):
        total_bullet = GAME_STAT.total_bullet
        y = 85
        x = 350
        total_bullet_rendered = FONT.render(f"x{total_bullet}", True, WHITE)
        screen.blit(total_bullet_rendered, (x, y))

    def draw_stat(self):
        money = check_data_file()
        display_money(money)

    def draw_awakening(self):
        ratio = GAME_STAT.awakening_gauge / GAME_STAT.awakening_max

        bar_width = 265
        bar_height = 35

        x = (SCREEN_WIDTH // 2) - (bar_width // 2)
        y = SCREEN_HEIGHT - 70

        # 🟫 background (เทา)
        pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))

        # 🟨 gauge (เหลือง)
        pygame.draw.rect(screen, (255, 215, 0), (x, y, bar_width * ratio, bar_height))

        screen.blit(awaken_frame, (x,y-30))

    def draw_all(self):
        """ self.draw_rect()
        self.draw_bullet_bar()
        self.display_total_bullet()"""
        self.draw_stat()
        self.draw_red_rect()
        self.draw_rect()
        self.draw_ui()
        self.display_total_bullet()
        self.draw_bullet_bar()
        self.draw_awakening()