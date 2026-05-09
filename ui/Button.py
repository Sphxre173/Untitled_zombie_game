import pygame
from utils import load_sound

class Button(pygame.sprite.Sprite):
    def __init__(self, image, y_point, pointer_function):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.y = y_point
        self.rect.x = -50
        self.target_function = pointer_function
        self.is_pressed = False
        self.click_sound = load_sound(r"ASSETS\IMAGE\BG_LOBBY\BUTTON\SOUND\47313572-ui-sounds-pack-5-19-359747.mp3")
        self.hover_sound = load_sound(r"ASSETS\IMAGE\BG_LOBBY\BUTTON\SOUND\hover.mp3")
        self.debouncer_hover = False
    def update(self):
        
        #get mouse position
        get_mouse_pos = pygame.mouse.get_pos()
        #get mouse press
        get_mouse_pressed = pygame.mouse.get_pressed()
        
        if self.rect.collidepoint(get_mouse_pos):
            print("hovering")
            #play animation
            if not self.debouncer_hover:
                self.hover_sound.play()
                self.debouncer_hover = True
            if self.rect.x <= -20:
                self.rect.x += 3
            if get_mouse_pressed[0] and not self.is_pressed:
                self.click_sound.play()
                self.target_function()
                self.is_pressed = True
        else:
            if self.rect.x >= -50:
                self.rect.x -= 3
            self.debouncer_hover = False
            self.is_pressed = False