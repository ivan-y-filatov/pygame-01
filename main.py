import pygame
from pytmx.util_pygame import load_pygame
pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400



WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
PLAYER_SPEED = 3
JUMP_HEIGHT = -10

GRAVITY = 0.6

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")
tmx_data = load_pygame('resources/pygame01_map.tmx')
print(tmx_data.layers)
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
        self.velocity_y = 0
        self.on_ground = False

    def update(self, platforms, spikes):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = JUMP_HEIGHT

        for spike in spikes:
            if self.rect.colliderect(spike.rect):
                self.rect.x = 50
                self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
                self.velocity_y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

player = Player() # Just test comment
platforms = pygame.sprite.Group()
spikes = pygame.sprite.Group()

platforms.add(Platform(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10))
platforms.add(Platform(150, 300, 100, 10))
platforms.add(Platform(350, 200, 100, 10))

spikes.add(Spike(250, SCREEN_HEIGHT - 20, 30, 10))
spikes.add(Spike(400, 190, 30, 10))

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(platforms, spikes)
    platforms.draw(screen)
    spikes.draw(screen)
    screen.blit(player.image, player.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
