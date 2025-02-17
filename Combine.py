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
    def __init__(self, pos, groups, obstacles, enemies, buskets):
        super().__init__(groups)
        self.image = pygame.image.load('/Users/ivan/PycharmProjects/super-mario/resources/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(0, 0)
        self.obstacles = obstacles
        self.enemies = enemies
        self.coins = buskets
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
        if keys[pygame.K_SPACE] and self.on_ground():
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
        collisions = pygame.sprite.spritecollide(self, self.obstacles, False)
        for sprite in collisions:
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
        if self.rect.top > 720 or pygame.sprite.spritecollideany(self, self.enemies):
            lives_left -= 1
            self.pos = pygame.math.Vector2(reset_pos)
            self.rect.topleft = reset_pos
            self.vel = pygame.math.Vector2(0, 0)

    def coin_checker(self):
        global coin_bank
        collected_coins = pygame.sprite.spritecollide(self, self.coins, True)
        coin_bank += len(collected_coins)

    def update(self, reset_pos):
        self.apply_gravity()
        self.handle_input()
        self.move()
        self.lives_checker(reset_pos)
        self.coin_checker()

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

tmx_data = load_pygame('resources/pygame03_map.tmx')

all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
buskets = pygame.sprite.Group()

for layer in tmx_data.visible_layers:
    if hasattr(layer, 'data'):
        for x, y, surf in layer.tiles():
            pos = (x * 32, y * 32)
            Tile(pos=pos, surf=surf, groups=[all_sprites, obstacles])

for obj in tmx_data.objects:
    pos = obj.x, obj.y
    if obj.image:
        Tile(pos=pos, surf=obj.image, groups=[all_sprites])

player_start_pos = (100, 100)
player = Player(pos=player_start_pos, groups=all_sprites, obstacles=obstacles, enemies=enemies, buskets=buskets)

enemy_positions = [(200, 550), (600, 260), (750, 325)]
for pos in enemy_positions:
    Enemy(pos=pos, groups=[all_sprites, enemies])

coin_positions = [(200, 500), (600, 170), (750,200)]
for pos in coin_positions:
    Coin(pos=pos, groups=[all_sprites, buskets])

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

    screen.fill('White')
    all_sprites.draw(screen)

    lives_text = font.render(f'Lives: {lives_left}', True, (0, 0, 0))
    coin_text = font.render(f'Buskets: {coin_bank}', True, (0, 0, 0))
    screen.blit(lives_text, (10, 10))
    screen.blit(coin_text, (10, 40))

    pygame.display.update()
    clock.tick(60)
