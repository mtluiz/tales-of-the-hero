import pygame
from settings import *
from player import *
from tile import *
from debug import debug

class Level:
  def __init__(self):
    self.surface = pygame.display.get_surface()

    self.visible_sprites = YSortCameraGroup()
    self.obstacles_sprites = pygame.sprite.Group()

    self.create_map()

  def create_map(self):
    for i, row in enumerate(WORLD_MAP):
      for j, col in enumerate(row):
        y = i * TILESIZE
        x = j * TILESIZE
        if col == "x": 
          Tile((x, y), [self.visible_sprites, self.obstacles_sprites])          
        elif col == "p":
          self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites)

  def run(self):
    self.visible_sprites.custom_draw(self.player)
    self.visible_sprites.update()
    debug(self.player.direction)


class YSortCameraGroup(pygame.sprite.Group):
  def __init__(self):
    
    super().__init__()
    self.surface = pygame.display.get_surface()
    self.half_width = self.surface.get_size()[0] // 2
    self.half_height = self.surface.get_size()[1] // 2
    self.offset = pygame.math.Vector2(100, 100)

  def custom_draw(self, player):
    self.offset.x = player.rect.centerx - self.half_width
    self.offset.y = player.rect.centery - self.half_height

    for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
      offset_rect = sprite.rect.topleft - self.offset
      self.surface.blit(sprite.image, offset_rect)
      print(sprite.rect)
