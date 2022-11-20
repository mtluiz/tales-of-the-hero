import pygame
from settings import *
from player import *
from tile import *
from debug import debug

class Level:
  def __init__(self):
    self.surface = pygame.display.get_surface()
    self.visible_sprites = pygame.sprite.Group()
    self.obstacles_sprites = pygame.sprite.Group()

    self.create_map()

  def create_map(self):
    for i, row in enumerate(WORLD_MAP):
      for j, col in enumerate(row):
        y = i * TILESIZE
        x = j * TILESIZE
        if col == "x": 
          Tile((x, y), [self.visible_sprites])          
        elif col == "p":
          self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites)

  def run(self):
    self.visible_sprites.draw(self.surface)
    self.visible_sprites.update()
    debug(self.player.direction)