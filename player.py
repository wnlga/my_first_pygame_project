from pygame.sprite import Sprite, collide_mask
from pygame import Surface
from pygame import init as niga
from pygame.mask import from_surface
from pygame.image import load
from pygame import mixer
import pyganim

mixer.pre_init(44100, -8, 1, 14000)
niga()
atsound = mixer.Sound('sounds/punch.ogg')
aatsound = mixer.Sound('sounds/punchb.ogg')
MOVE_SPEED = 30
GRAVITY = 0.56
ANIATT = [('images/hero/heroattach0.png', 100),
          ('images/hero/heroattach1.png', 200)]
ANIATTR = [('images/hero/heroattach2.png', 100),
           ('images/hero/heroattach31.png', 200)]
HERDIE = [('images/hero/herodie0.png', 500),
          ('images/hero/herodie1.png', 500), ('images/hero/herodie1.png', 20000)]
HERDIEL = [('images/hero/herodie3.png', 500),
           ('images/hero/herodie4.png', 500), ('images/hero/herodie4.png', 20000)]


class Player(Sprite):
    def __init__(self, x, y, sr):
        Sprite.__init__(self)
        self.idie = False
        self.idiee = False
        self.sr = sr
        self.nxt = False
        self.next_lvl = False
        self.image = Surface((100, 49))
        self.rect = self.image.get_rect()
        self.mask = from_surface(self.image)
        self.rect.x = x
        self.xvel = 0
        self.rect.y = y
        self.yvel = 0
        self.count_attach = 0
        self.ccount_attach = 0
        self.onGround = False
        self.boltAniatt = pyganim.PygAnimation(ANIATT)
        self.boltAniattr = pyganim.PygAnimation(ANIATTR)
        self.boltAnidie = pyganim.PygAnimation(HERDIE)
        self.boltAnidiel = pyganim.PygAnimation(HERDIEL)
        self.enc = [0, 0, 0]
        self.ats = False

    def update(self, left, right, attach, up, platforms, lr, enemies):
        if self.count_attach >= 10:
            self.image = load('images/empty.png')
            self.idie = True
            if self.lr:
                self.boltAnidie.blit(self.image, (0, 0))
                self.boltAnidie.play()
            else:
                self.boltAnidiel.blit(self.image, (0, 0))
                self.boltAnidiel.play()
            if (self.boltAnidie.currentFrameNum == 2 or self.boltAnidiel.currentFrameNum == 2):
                self.idiee = True
        if not self.idie:
            self.lr = lr
            if isinstance(enemies, list):
                for enemy in enemies:
                    en_x = enemy.rect.x
                    en_y = enemy.rect.y
                    if abs(self.rect.x - en_x) < 50 and enemy.attach:
                        if (enemy.boltAniatt.currentFrameNum == 1 or enemy.boltAniattr.currentFrameNum == 1):
                            self.count_attach += 1
                            enemy.attach = False

                        if attach:
                            self.xvel = 0
                            right = left = False
                            self.image = load('images/empty.png')
                            if self.lr:
                                self.boltAniattr.play()
                                self.boltAniattr.blit(self.image, (0, 0))
                                if self.rect.x - en_x < 0 and self.rect.x - en_x > -50:
                                    if self.boltAniattr.currentFrameNum == 1:
                                        atsound.play()
                                        if self.rect.y - 26 == en_y:
                                            self.ccount_attach += 1
                                            self.enc[enemies.index(enemy)] += 1
                            if not self.lr:
                                self.boltAniatt.play()
                                self.boltAniatt.blit(self.image, (0, 0))
                                if self.rect.x - en_x > 0 and self.rect.x - en_x < 40:
                                    if self.boltAniatt.currentFrameNum == 1:
                                        atsound.play()
                                        if self.rect.y - 26 == en_y:
                                            self.ccount_attach += 1
                                            self.enc[enemies.index(enemy)] += 1
            else:
                enemy = enemies
                en_x = enemies.rect.x
                en_y = enemies.rect.y
                if self.rect.x - en_x >= -20:
                    if enemy.boltAniatt.currentFrameNum == 1:
                        self.count_attach += 1
                        if not self.ats:
                            aatsound.play()
                            self.ats = True
                    else:
                        self.ats = False
                if attach:
                    self.xvel = 0
                    right = left = False
                    self.image = load('images/empty.png')
                    if self.lr:
                        self.boltAniattr.play()
                        self.boltAniattr.blit(self.image, (0, 0))
                        if self.rect.x - en_x > -10:
                            if self.boltAniattr.currentFrameNum == 1:
                                atsound.play()
                                if self.rect.y - en_y > -1:
                                    self.ccount_attach += 1
                    if not self.lr:
                        self.boltAniatt.play()
                        self.boltAniatt.blit(self.image, (0, 0))
                        if self.rect.x - en_x > -10:
                            if self.boltAniatt.currentFrameNum == 1:
                                atsound.play()
                                if self.rect.y - en_y > -1:
                                    self.ccount_attach += 1

            if left:
                self.boltAniatt.stop()
                self.boltAniattr.stop()
                if self.rect.x >= 885:
                    self.rect.x -= 10
                self.xvel = -MOVE_SPEED
                self.image = load('images/hero/herostand.png')
                self.mask = from_surface(self.image)

            if right:
                attach = False
                self.boltAniatt.stop()
                self.boltAniattr.stop()
                if self.rect.x <= 80:
                    self.rect.x += 9
                self.xvel = MOVE_SPEED
                self.image = load('images/hero/herostandr.png')
                self.mask = from_surface(self.image)

            elif not (right or left):
                self.xvel = 0
                if not attach:
                    if self.lr:
                        self.image = load('images/hero/heroattach2.png')
                    elif not self.lr:
                        self.image = load('images/hero/heroattach0.png')
                    self.mask = from_surface(self.image)

            if up:
                if self.onGround:
                    self.yvel -= MOVE_SPEED - 10

            if not self.onGround:
                self.yvel += 3 * GRAVITY
            self.onGround = False
            self.rect.x += self.xvel
            self.collide(self.xvel, 0, platforms)
            self.rect.y += self.yvel
            self.collide(0, self.yvel, platforms)

    def is_die(self):
        return self.idiee

    def nextlvl(self, nl):
        self.next_lvl = nl

    def get_pose_p(self):
        return self.rect.x, self.rect.y

    def get_enc(self):
        return self.enc

    def getca(self):
        return self.ccount_attach

    def setenc(self, enc):
        self.enc = enc
        return self.count_attach

    def next(self):
        return self.nxt

    def collide(self, xvel, yvel, platforms):
        if not self.next_lvl:
            if self.rect.x > self.sr.right - 60:
                self.rect.x = self.sr.right - 60
        else:
            if self.rect.x > self.sr.right:
                self.nxt = True
        if self.rect.x < self.sr.left - 40:
            self.rect.x = self.sr.left - 40
        for pl in platforms:
            if collide_mask(self, pl):
                if xvel > 0:
                    if not self.next_lvl:
                        if self.rect.x >= 80:
                            self.rect.right = pl.rect.left + 37
                if xvel < 0:
                    if self.rect.x <= 800:
                        self.rect.left = pl.rect.right - 35
                if yvel > 0:
                    self.rect.bottom = pl.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = pl.rect.bottom
                    self.yvel = 0
