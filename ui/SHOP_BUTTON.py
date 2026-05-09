import pygame

class Shop_Button(pygame.sprite.Sprite):
    def __init__(self, image:pygame.image, y:int, fuction_action):
        super().__init__()
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = y
        self.func = fuction_action
        self.scale = 1
        self.target_scale = 1
        self.clicked = False
    def update(self, shop_base_x):
    # position
        self.rect.x = shop_base_x + 350
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # hover check
        if self.rect.collidepoint(mouse_pos):
            self.target_scale = 1.1

            if mouse_pressed[0] and not self.clicked:
                self.func()
                self.clicked = True
        else:
            self.target_scale = 1
        
        if not mouse_pressed[0]:
            self.clicked = False

        # smooth scale (ease)
        self.scale += (self.target_scale - self.scale) * 0.2

        # apply scale
        new_w = int(self.original_image.get_width() * self.scale)
        new_h = int(self.original_image.get_height() * self.scale)

        center = self.rect.center

        self.image = pygame.transform.smoothscale(self.original_image, (new_w, new_h))
        self.rect = self.image.get_rect(center=center)