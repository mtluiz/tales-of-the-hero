import pygame

class Weapon(pygame.sprite.Sprite):
  def __init__(self, player, groups):
    super().__init__(groups)

    direction = player.status.split('_')[0]

    #graphic 
    self.image = pygame.Surface((40, 40))

    #placement
    if direction == 'right':
      self.rect = self.image.get_rect(midleft = player.rect.center)