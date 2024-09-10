import pygame
from pygame import Surface
import pygame.sprite
import pygame.transform

class Monster(pygame.sprite.Sprite):
    def __init__(self,screen:Surface, filename:str,x:int, y:int):
        pygame.sprite.Sprite.__init__(self)
            
        self.screen = screen        
        img = pygame.image.load(f'{filename}').convert_alpha()
        self.image = pygame.transform.scale(img,(40,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.delay_counter = 0

    def update(self):
        self.rect.x += self.direction
        self.delay_counter += 1
        if abs(self.delay_counter) > 25:
            self.direction *= -1
            self.delay_counter *= -1