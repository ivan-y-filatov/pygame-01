import sys
import pygame
from pytmx.util_pygame import load_pygame

lives_left = 3
coin_bank = 0

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('/Users/ivan/PycharmProjects/super-mario/resources/enemy.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('/Users/ivan/PycharmProjects/super-mario/resources/KFC.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles, enemies, coins):
        super().__init__(groups)
        #self.image = pygame.image.load('/Users/ivan/PycharmProjects/super-mario/resources/player.png').convert_alpha()
        self.sprites = []
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(0, 0)
        self.obstacles = obstacles
        self.enemies = enemies
        self.coins = coins
        self.gravity = 0.5
        self.jump_strength = -9
        self.speed = 5

    def apply_gravity(self):
        self.vel.y += self.gravity

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel.x = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.vel.x = self.speed
        else:
            self.vel.x = 0
        if keys[pygame.K_UP] and self.on_ground():
            self.vel.y = self.jump_strength

    def on_ground(self):
        self.rect.y += 1
        collision = pygame.sprite.spritecollide(self, self.obstacles, False)
        self.rect.y -= 1
        return bool(collision)

    def move(self):
        self.pos.x += self.vel.x
        self.rect.x = int(self.pos.x)
        self.handle_collisions('horizontal')

        self.pos.y += self.vel.y
        self.rect.y = int(self.pos.y)
        self.handle_collisions('vertical')

    def handle_collisions(self, direction):
        for sprite in pygame.sprite.spritecollide(self, self.obstacles, False):
            if direction == 'horizontal':
                if self.vel.x > 0:
                    self.rect.right = sprite.rect.left
                elif self.vel.x < 0:
                    self.rect.left = sprite.rect.right
                self.pos.x = self.rect.x
            elif direction == 'vertical':
                if self.vel.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.vel.y = 0
                elif self.vel.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.vel.y = 0
                self.pos.y = self.rect.y

    def lives_checker(self, reset_pos):
        global lives_left
        if self.rect.top > 900 or pygame.sprite.spritecollideany(self, self.enemies):
            lives_left -= 1
            self.pos = pygame.math.Vector2(reset_pos)
            self.rect.topleft = reset_pos
            self.vel = pygame.math.Vector2(0, 0)

    def coin_checker(self):
        global coin_bank
        collected = pygame.sprite.spritecollide(self, self.coins, True)
        coin_bank += len(collected)

    def update(self, reset_pos):
        self.apply_gravity()
        self.handle_input()
        self.move()
        self.lives_checker(reset_pos)
        self.coin_checker()

def camera_offset(player, width, height):
    offset_x = -(player.rect.centerx - width // 2)
    offset_y = -(player.rect.centery - height // 2)
    return offset_x, offset_y

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

tmx_data = load_pygame('resources/test.tmx')

all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()

for layer in tmx_data.visible_layers:
    if hasattr(layer, 'data'):
        for x, y, surf in layer.tiles():
            Tile((x * 32, y * 32), surf, [all_sprites, obstacles])

for obj in tmx_data.objects:
    if obj.image:
        Tile((obj.x, obj.y), obj.image, [all_sprites])

player_start_pos = (100, 100)
player = Player(player_start_pos, all_sprites, obstacles, enemies, coins)

for pos in [(200, 550), (750, 515), (750, 325)]:
    Enemy(pos, [all_sprites, enemies])

for pos in [(200, 500), (300, 832), (750, 200)]:
    Coin(pos, [all_sprites, coins])

font = pygame.font.Font(None, 36)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    all_sprites.update(player_start_pos)

    if lives_left <= 0:
        print("Game Over!")
        pygame.quit()
        sys.exit()

    screen.fill('white')
    offset_x, offset_y = camera_offset(player, 1280, 720)

    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))

    coordinates_text = font.render(f'`Coords: {player.pos}', True, (0,0,0))
    lives_text = font.render(f'Lives: {lives_left}', True, (0, 0, 0))
    coin_text = font.render(f'Coins: {coin_bank}', True, (0, 0, 0))
    screen.blit(lives_text, (10, 10))
    screen.blit(coin_text, (10, 40))
    screen.blit(coordinates_text, (10, 70))

    pygame.display.update()
    clock.tick(60)
