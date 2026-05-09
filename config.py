import pygame

FPS = 60
FPS_IN_GAME = 90
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800
FONT_FAMILY = "ShopeeFont Rounded"
FONT = pygame.font.SysFont(FONT_FAMILY, 30)
FONT_BOLD = pygame.font.SysFont(FONT_FAMILY, 50, True)

#color value
WHITE = (255, 255, 255)
RED = (230, 0, 0)
GREEN = (0, 233, 0)

#INIT SCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#UTIL VAR
center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)