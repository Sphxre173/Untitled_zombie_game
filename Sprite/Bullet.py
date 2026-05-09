import pygame
from config import screen

class Bullet(pygame.sprite.Sprite):

    def __init__(self, pos, direction, damage):
        super().__init__()

        self.radius = 5
        self.color = (255, 220, 0)

        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)

        pygame.draw.circle(
            self.image,
            self.color,
            (self.radius, self.radius),
            self.radius
        )

        self.rect = self.image.get_rect(center=pos)

        self.direction = direction
        self.speed = 30
        self.damage = damage
    def update(self):

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        if not screen.get_rect().colliderect(self.rect):
            self.kill()