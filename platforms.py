from pygame.image import load
from pygame.sprite import Sprite


class Platform(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = load('images/platforms/platform.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
