from pygame.sprite import Sprite
from pygame import Surface
from pygame.mask import from_surface
from pygame.image import load
import pyganim
import random

MOVE_SPEED = 3
ANILIVED = [('images/enemy/29413.png', 200), ('images/enemy/29409.png', 200),
            ('images/enemy/29410.png', 200), ('images/enemy/29411.png', 200), ('images/enemy/29411.png', 200)]
ANILIVE = [('images/enemy/29411.png', 200), ('images/enemy/29410.png', 200),
           ('images/enemy/29409.png', 200), ('images/enemy/29413.png', 200), ('images/enemy/29413.png', 200)]
ANIATT = [('images/enemy/skelatt0.png', 400),
          ('images/enemy/skelatt1.png', 400)]
ANIATTR = [('images/enemy/skelatt2.png', 400),
           ('images/enemy/skelatt3.png', 400)]
ANIWALKR = [('images/enemy/walk1.png', 200), ('images/enemy/walk2.png', 200),
            ('images/enemy/walk5.png', 200), ('images/enemy/walk3.png', 100), ('images/enemy/walk4.png', 200)]
ANIWALK = [('images/enemy/walk1l.png', 200), ('images/enemy/walk2l.png', 200),
           ('images/enemy/walk5l.png', 200), ('images/enemy/walk3l.png', 100), ('images/enemy/walk4l.png', 200)]
lr = True


class Enemy(Sprite):
    def __init__(self):
        self.die = False
        self.is_live = False
        Sprite.__init__(self)
        self.count_attach = 0
        self.lr = lr
        self.image = Surface((85, 75))
        self.rect = self.image.get_rect()
        self.mask = from_surface(self.image)
        self.rect.x = random.randint(40, 900)
        self.xvel = 0
        self.rect.y = 485
        self.yvel = 0
        self.onGround = False
        self.boltAnilive = pyganim.PygAnimation(ANILIVED, loop=False)
        self.boltAniatt = pyganim.PygAnimation(ANIATT, loop=False)
        self.boltAniattr = pyganim.PygAnimation(ANIATTR, loop=False)
        self.boltAniwalr = pyganim.PygAnimation(ANIWALKR)
        self.boltAniwalk = pyganim.PygAnimation(ANIWALK)
        self.boltAnilive.blit(self.image, (0, 0))
        self.attach = False
        self.image = load('images/empty.png')
        self.boltAnilived = pyganim.PygAnimation(ANILIVE, loop=False)

    def is_die(self):
        return self.die

    def getca(self, ca):
        self.count_attach = ca

    def update(self, hero, attach, lr):
        self.image = load('images/empty.png')
        self.boltAnilived.play()
        self.boltAnilived.blit(self.image, (0, 0))
        if self.boltAnilived.currentFrameNum == 4:
            self.is_live = True
            self.boltAnilived.stop()
        if not self.die and self.is_live:
            self.lr = lr
            if self.count_attach < 3:
                player_x, player_y = hero.rect.x, hero.rect.y
                if self.rect.x - player_x > 0:
                    self.image = load('images/empty.png')
                    self.boltAniwalk.play()
                    self.boltAniwalk.blit(self.image, (0, 0))
                    if self.rect.x - player_x > 40:
                        self.boltAniatt.stop()
                        self.boltAniattr.stop()
                        self.xvel = -MOVE_SPEED
                        self.attach = False
                    else:
                        self.xvel = 0
                        self.image = load('images/enemy/29412.png')
                        if self.rect.y + 26 == player_y:
                            if attach:
                                if lr:
                                    self.count_attach += 1
                            self.image = load('images/empty.png')
                            if (self.boltAniattr.isFinished()):
                                self.attach = True
                            if self.boltAniattr.state != "playing":
                                self.attach = True
                                self.boltAniattr.play()
                            self.boltAniattr.play()
                            self.boltAniattr.blit(self.image, (0, 0))
                        else:
                            self.boltAniatt.stop()
                            self.boltAniattr.stop()

                elif self.rect.x - player_x < 0:
                    self.image = load('images/empty.png')
                    self.boltAniwalr.play()
                    self.boltAniwalr.blit(self.image, (0, 0))
                    if self.rect.x - player_x < -30:
                        self.boltAniatt.stop()
                        self.boltAniattr.stop()
                        self.xvel = MOVE_SPEED
                        self.attach = False
                    else:
                        self.xvel = 0
                        self.image = load('images/enemy/29413.png')
                        if self.rect.y + 26 == player_y:
                            if attach:
                                if not lr:
                                    self.count_attach += 1
                            self.image = load('images/empty.png')
                            if self.boltAniatt.isFinished():
                                self.attach = True
                            if self.boltAniatt.state != "playing":
                                self.attach = True
                                self.boltAniatt.play()
                            self.boltAniatt.play()
                            self.boltAniatt.blit(self.image, (0, 0))
                        else:
                            self.boltAniatt.stop()
                            self.boltAniattr.stop()
                self.rect.x += self.xvel
            else:
                self.boltAniatt.stop()
                self.boltAniattr.stop()
                self.image = load('images/empty.png')
                self.boltAnilive.play()
                self.boltAnilive.blit(self.image, (0, 0))
                if self.boltAnilive.currentFrameNum == 4:
                    self.rect.x = -100
                    self.die = True
