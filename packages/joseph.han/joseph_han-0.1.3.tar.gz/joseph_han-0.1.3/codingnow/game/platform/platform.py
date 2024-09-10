import pygame
import pygame.sprite

from codingnow.game.platform.player import *
from codingnow.game.platform.block import *
from codingnow.game.platform.coin import *
from codingnow.game.platform.monster import *
from codingnow.game.platform.lava import *
from codingnow.game.platform.bullet import *

class Platform():
    player:Player = None
    def __init__(self,screen:Surface) -> None:
        self.screen = screen
        self.group_block = pygame.sprite.Group()
        self.group_coin = pygame.sprite.Group()
        self.group_lava = pygame.sprite.Group()
        self.group_monster = pygame.sprite.Group()
        self.group_bullet = pygame.sprite.Group()
        self.coin_list = []
        self.monster_list = []
    
    def game_reset(self):
        self.group_bullet.empty()
        self.group_coin.empty()
        self.group_monster.empty()
        for coin in self.coin_list:
            self.group_coin.add(Coin(self.screen,coin[0],coin[1],coin[2]))
        for mon in self.monster_list:
            self.group_monster.add(Monster(self.screen,mon[0],mon[1],mon[2]))
            
    def add_player(self,filename:str, width:int, height:int):
        self.player = Player(self,self.screen,filename,width,height)
        return self.player
        
    def add_block(self,filename:str, x:int, y:int,move_x:int=0,move_y:int=0):
        self.group_block.add(Block(self.screen,filename,x,y,move_x,move_y))
        
    def add_coin(self,filename:str, x:int, y:int):
        self.group_coin.add(Coin(self.screen,filename,x,y))
        self.coin_list.append((filename,x,y))
        
        
    def add_monster(self,filename:str, x:int, y:int):
        self.group_monster.add(Monster(self.screen,filename,x,y))
        self.monster_list.append((filename,x,y))
        
    def add_lava(self,filename:str, x:int, y:int, num:int):
        for i in range(num):
            self.group_lava.add(Lava(self.screen,filename,x+30*i,y))
        
    def add_bullet(self,filename:str):
        self.group_bullet.add(Bullet(self.screen,filename,self.player))
        
    def draw(self):
        if self.player is not None:            
            self.player.draw()
            
        for bullet in self.group_bullet:
            if pygame.sprite.spritecollide(bullet, self.group_monster, True):
                bullet.kill()
                self.player.score += 20
                if self.player.snd_dic['monster'] is not None:
                    self.player.snd_dic['monster'].play()
        
        self.group_block.update()
        self.group_coin.update()
        self.group_monster.update()
        self.group_lava.update()
        self.group_bullet.update()
        
        self.group_block.draw(self.screen)
        self.group_coin.draw(self.screen)
        self.group_monster.draw(self.screen)
        self.group_lava.draw(self.screen)
        self.group_bullet.draw(self.screen)