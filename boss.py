from pygame.sprite import Sprite
from pygame import Surface
from pygame import init
from pygame import mixer
from pygame.mask import from_surface
from pygame.image import load
import pyganim

MOVE_SPEED = 3
ANILIVE = [('images/enemy/bossst0.png', 1000),
           ('images/enemy/bossst1.png', 1000)]
ANILIVED = [('images/enemy/dieboss.png', 500),
            ('images/enemy/die2.png', 500), ('images/enemy/die2.png', 200)]
ANIATT = [('images/enemy/bossat1.png', 400), ('images/enemy/bossat2.png', 400)]
lr = True


class Boss(Sprite):
    def __init__(self):
        self.die = False
        Sprite.__init__(self)
        self.count_attach = 0
        self.lr = lr
        self.image = Surface((150, 109))
        self.rect = self.image.get_rect()
        self.mask = from_surface(self.image)
        self.rect.x = 810
        self.xvel = 0
        self.rect.y = 450
        self.yvel = 0
        self.boltAnilive = pyganim.PygAnimation(ANILIVE)
        self.boltAnilived = pyganim.PygAnimation(ANILIVED, loop=False)
        self.boltAniatt = pyganim.PygAnimation(ANIATT)
        self.image = load('images/empty.png')
        self.boltAnilive.play()
        self.boltAnilive.blit(self.image, (0, 0))

    def is_die(self):
        return self.die

    def getca(self, ca):
        self.count_attach = ca

    def update(self, hero, attach):
        self.image = load('images/empty.png')
        self.boltAnilive.play()
        self.boltAnilive.blit(self.image, (0, 0))
        if self.count_attach < 100:
            player_x, player_y = hero.rect.x, hero.rect.y
            if self.rect.x - player_x <= 10:
                if self.rect.y - player_y <= 0:
                    if attach:
                        self.count_attach += 1
                    self.image = load('images/empty.png')
                    self.boltAnilive.stop()
                    self.boltAniatt.play()
                    self.boltAniatt.blit(self.image, (0, 0))
                else:
                    self.boltAniatt.stop()
        else:
            self.boltAniatt.stop()
            self.image = load('images/empty.png')
            self.boltAnilived.play()
            self.boltAnilived.blit(self.image, (0, 0))
            if self.boltAnilived.currentFrameNum == 2:
                self.die = True
