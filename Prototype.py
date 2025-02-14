import sys

import pygame
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)


pygame.init()
screen = pygame.display.set_mode((1280,720))
tmx_data = load_pygame('resources/pygame03_map.tmx')
sprite_group = pygame.sprite.Group()


for layer in tmx_data.visible_layers:
    if hasattr(layer,'data'):
        for x,y,surf in layer.tiles():
            pos = (x * 32, y * 32)
            Tile(pos=pos, surf=surf, groups=sprite_group)

for obj in tmx_data.objects:
    pos = obj.x, obj.y
    if obj.image:
        Tile(pos=pos, surf=obj.image, groups=sprite_group)


sprite_group.draw(screen)
pygame.display.update()
screen.fill('White')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
