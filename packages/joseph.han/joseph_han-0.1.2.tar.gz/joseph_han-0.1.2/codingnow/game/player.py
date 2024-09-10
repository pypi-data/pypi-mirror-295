import pygame
from pygame import Surface

class Player():
    speed = 1
    def __init__(self,screen:Surface,img) -> None:
        self.screen = screen        
        # img = pygame.image.load('images/player_warrior.png')
        self.image = pygame.transform.scale(img,(60,60))
        self.rect = self.image.get_rect()
    
    def key_pressed(self):
        key_press = pygame.key.get_pressed()
        
        if key_press[pygame.K_UP]:
            self.rect.centery -= self.speed

        if key_press[pygame.K_DOWN]:
            self.rect.centery += self.speed
            
        if key_press[pygame.K_LEFT]:
            self.rect.centerx -= self.speed
            
        if key_press[pygame.K_RIGHT]:
            self.rect.centerx += self.speed
            
    def update(self):
        self.key_pressed()
        
    def draw(self):
        self.update()
        self.screen.blit(self.image, self.rect)