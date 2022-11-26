import pygame
from settings import *
from os import walk
from debug import *
from ui import *

def import_folder(path):
  surface_list = []
  for _, __, img_files in walk(path):
    for image in sorted(img_files):
      full_path = path + '/' + image
      image_surf = pygame.image.load(full_path).convert_alpha()
      surface_list.append(image_surf)
  return surface_list 

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_weapon):
        super().__init__(groups)
        self.image = pygame.image.load("assets/graphics/test/realplayer2.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -26)

        #setup animations
        self.import_player_assets()

        #status
        self.status = 'down'

        self.frame_index = 0
        self.animation_speed = 0.15
        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # weapon change
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}

        self.health = self.stats["health"] * 0.5
        self.energy = self.stats["energy"]
        self.speed = self.stats["speed"]
        self.exp = 123

        #weapon
        self.create_attack = create_attack
        self.destroy_weapon = destroy_weapon
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        print(self.weapon)
        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = 'assets/graphics/player/'
        self.animations = {
            'up' : [],
            'down' : [],
            'left': [],
            'right': [],
            'right_idle': [],
            'left_idle': [],
            'up_idle': [],
            'down_idle': [],
            'right_attack': [],
            'left_attack': [],
            'up_attack': [],
            'down_attack': [],
        }
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(character_path + animation)


    def colision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = +1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = +1
                self.status = 'right'
            else:
                self.direction.x = 0

            if keys[pygame.K_SPACE] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            if keys[pygame.K_LCTRL] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print("magic")
            
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_index = (self.weapon_index + 1) % 5
                self.weapon = list(weapon_data.keys())[self.weapon_index]

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

        if not self.attacking:
            self.destroy_weapon()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)


    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
            pass
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')

        if not self.attacking:
                self.status = self.status.replace('_attack', '_idle')

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.colision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.colision('vertical')
        self.rect.center = self.hitbox.center

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        debug(self.status)
        self.move(self.speed)
