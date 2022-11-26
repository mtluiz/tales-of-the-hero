import pygame
from settings import *
from player import *
from tile import *
from debug import debug
from utils.import_csv_layout import *
import random
from os import walk
from weapon import *
from ui import *

def import_folder(path):
  surface_list = []
  for _, __, img_files in walk(path):
    for image in sorted(img_files):
      full_path = path + '/' + image
      image_surf = pygame.image.load(full_path).convert_alpha()
      surface_list.append(image_surf)
  return surface_list 
class Level:
  def __init__(self):
    self.surface = pygame.display.get_surface()

    self.visible_sprites = YSortCameraGroup()
    self.obstacles_sprites = pygame.sprite.Group()

    self.ui = UI()

    self.current_attack = None
    
    self.create_map()

  def create_map(self):
    layouts = {
      'boundary' : import_csv_layout('assets/map/map_FloorBlocks.csv'),
      'grass': import_csv_layout('assets/map/map_Grass.csv'),
      'object': import_csv_layout('assets/map/map_Objects.csv'),
    }

    graphics = {
      'objects': import_folder("assets/graphics/objects")
    }

    for style, layout in layouts.items():
      for i, row in enumerate(layout):
        for j, col in enumerate(row):
          if col != '-1':
            y = i * TILESIZE
            x = j * TILESIZE
            if style == 'boundary':
              Tile((x,y), [ self.obstacles_sprites], 'invisible')
            if style == 'grass':
              Tile((x,y), [ self.visible_sprites], 'grass', pygame.image.load("assets/graphics/grass/grass_"+ str(random.randint(1,3)) +".png"))
            if style == 'object':
              surface = graphics['objects'][int(col)]
              Tile((x,y), [self.obstacles_sprites, self.visible_sprites], 'object', surface)

    self.player = Player((2000, 1430), [self.visible_sprites], self.obstacles_sprites, self.create_attack, self.destroy_weapon)

    # for i, row in enumerate(WORLD_MAP):
    #   for j, col in enumerate(row):
    #     y = i * TILESIZE
    #     x = j * TILESIZE
    #     if col == "x": 
    #       Tile((x, y), [self.visible_sprites, self.obstacles_sprites])          
    #     elif col == "p":
    #       self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites)
  def destroy_weapon(self):
      if self.current_attack:
          self.current_attack.kill()

  def create_attack(self):
    self.current_attack = Weapon(self.player, [self.visible_sprites])

  def run(self):
    self.visible_sprites.custom_draw(self.player)
    self.visible_sprites.update()
    self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
  def __init__(self):
    
    super().__init__()
    self.surface = pygame.display.get_surface()
    self.half_width = self.surface.get_size()[0] // 2
    self.half_height = self.surface.get_size()[1] // 2
    self.offset = pygame.math.Vector2(100, 100)
    print(self.sprites())

    # creating floor
    self.floor_surface = pygame.image.load('assets/graphics/tilemap/ground.png').convert()
    self.floor_rect = self.floor_surface.get_rect(topleft=(0,0))

  def custom_draw(self, player):
    self.offset.x = player.rect.centerx - self.half_width
    self.offset.y = player.rect.centery - self.half_height

    #drawing floor
    floor_offset_pos = self.floor_rect.topleft - self.offset
    self.surface.blit(self.floor_surface, floor_offset_pos)
    
    for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
      offset_rect = sprite.rect.topleft - self.offset
      self.surface.blit(sprite.image, offset_rect)
      
