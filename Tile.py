import pygame_sdl2 as pygame
from helpers import load_image


class Tile(pygame.sprite.Sprite):

    def __init__(self, src_rect=None, dest_rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('puzzle1.jpg', -1)

        if dest_rect is not None:
            self.rect = dest_rect

        self.surface = pygame.Surface((self.rect.width, self.rect.height))

        # Optional cropping
        if src_rect is not None:
            self.surface.blit(self.image, (0, 0), src_rect)
