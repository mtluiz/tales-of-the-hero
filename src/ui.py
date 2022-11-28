import pygame
from settings import *

class UI:
  def __init__(self):
    self.surface = pygame.display.get_surface()
    self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

    # bar setup
    self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
    self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

  def show_bar(self, current, max_amount, bg_rect, color):
    pygame.draw.rect(self.surface, UI_BG_COLOR, bg_rect)

    ratio = current / max_amount
    current_width = bg_rect.width * ratio
    current_rect = bg_rect.copy()
    current_rect.width = current_width
    
    pygame.draw.rect(self.surface, color, current_rect)
    pygame.draw.rect(self.surface, UI_BORDER_COLOR, bg_rect, 3)

  def show_exp(self, exp):
    text_surface = self.font.render(str(int(exp)), False, TEXT_COLOR)
    x = self.surface.get_size()[0] - 20
    y = self.surface.get_size()[1] - 20
    text_rect = text_surface.get_rect(bottomright = (x, y))
    pygame.draw.rect(self.surface, UI_BORDER_COLOR, text_rect.inflate(20,20))
    self.surface.blit(text_surface, text_rect)
    pygame.draw.rect(self.surface, UI_BORDER_COLOR, text_rect.inflate(20,20), 3)

  def weapon_box(self, left, top, weapon_index):
    selection_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
    weapon_items = list(weapon_data.values())

    weapon_graphic = pygame.image.load(weapon_items[weapon_index]['graphic']).convert_alpha()
    pygame.draw.rect(self.surface, UI_BG_COLOR, selection_rect.get_rect(center=(0,0)))
    pygame.draw.rect(self.surface, UI_BORDER_COLOR, selection_rect,3)
    self.surface.blit(weapon_graphic, weapon_graphic)

  def magic_box(self, left, top, magic_index):
    selection_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
    pygame.draw.rect(self.surface, UI_BG_COLOR, selection_rect)
    pygame.draw.rect(self.surface, UI_BORDER_COLOR, selection_rect,3)

  def display(self, player):
    self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
    self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

    self.show_exp(player.exp)
    self.weapon_box(100, 600, player.weapon_index)
    self.magic_box(10, 600, 0)
    