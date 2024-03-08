import pygame
from player import Player
from enemies import Enemy
from boss import Boss
from map import levels
from platforms import Platform
from menu import Menu
from fps import FPSCounter

level = levels[0]
cl = 0
playm = False
slss = 'sounds/obbck.mp3'
slbs ='sounds/bossbck.mp3'
cenemy = 10
font = pygame.font.Font(None, 36)
black = (255, 255, 255)
health = 0
go = False
SIZE = [1000, 600]
sr = pygame.display.get_surface().get_rect()
while True:
    if not go:
        ng = Menu.menu(True if level == levels[0] else False)
    if ng:
        level = levels[0]
        cenemy = 10

    if level != levels[0]:
        if levels.index(level) % 2 == 0:
            cenemy += 2
        else:
            cenemy += 3
    ncl = False
    screen = pygame.display.set_mode(SIZE)
    sr = screen.get_rect()
    window = pygame.Surface(SIZE)
    enc = [0, 0, 0]
    window = pygame.image.load('images/oboi.jpg')
    sprite_group = pygame.sprite.Group()
    if level != levels[-1]:
        if level == levels[0]:
            pygame.mixer.music.load('sounds/obbck.mp3')
        enemy = Enemy()
        enemy1 = Enemy()
        enemy2 = Enemy()
        allen = 3
        sprite_group.add(enemy)
        sprite_group.add(enemy1)
        sprite_group.add(enemy2)
    else:
        pygame.mixer.music.load('sounds/bossbck.mp3')
        boss = Boss()
        playm = False
        sprite_group.add(boss)
        en = boss
    pygame.mixer.music.set_volume(1)
    if level == levels[0]:
        hero = Player(16, 510, sr)
    else:
        hero = Player(-23, 510, sr)
    sprite_group.add(hero)

    count_attach = 0
    platforms = []
    y = 0
    x = 0
    for row in level:
        for col in row:
            if col == '-':
                pl = Platform(x, y)
                sprite_group.add(pl)
                platforms.append(pl)
            x += 40
        y += 40
        x = 0

    left = right = up = attach = False
    lr = True
    done = True
    timer = pygame.time.Clock()
    fps_counter = FPSCounter(screen, font, timer, health)
    if not playm:
        pygame.mixer.music.play(-1, 10)
        playm = True
    while done:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.mixer.music.stop()
                playm = False
                done = False
                go = False

            if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:
                attach = True
            if i.type == pygame.MOUSEBUTTONUP and i.button == 1:
                attach = False
                count_attach += 1

            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_a:
                    lr = False
                    left = True
                if i.key == pygame.K_e:
                    shoot = True
                if i.key == pygame.K_d:
                    lr = True
                    right = True
                if i.key == pygame.K_w or i.key == pygame.K_SPACE:
                    up = True

            if i.type == pygame.KEYUP:
                if i.key == pygame.K_a:
                    left = False
                if i.key == pygame.K_e:
                    shoot = False
                if i.key == pygame.K_d:
                    right = False
                if i.key == pygame.K_w or i.key == pygame.K_SPACE:
                    up = False

        screen.blit(window, (0, 0))
        sprite_group.draw(screen)
        if level != levels[-1]:
            en = [enemy, enemy1, enemy2]
        hero.update(left, right, attach, up, platforms, lr, en)
        enc = hero.get_enc()
        if level != levels[-1]:
            enemy.update(hero, attach, lr)
            enemy.getca(enc[0])
            enemy1.update(hero, attach, lr)
            enemy1.getca(enc[1])
            enemy2.update(hero, attach, lr)
            enemy2.getca(enc[2])
            if enemy.is_die():
                sprite_group.remove(enemy)
                enc[0] = 0
                if allen < cenemy:
                    enemy = Enemy()
                    allen += 1
                    sprite_group.add(enemy)
            if enemy1.is_die():
                sprite_group.remove(enemy1)
                enc[1] = 0
                if allen < cenemy:
                    enemy1 = Enemy()
                    allen += 1
                    sprite_group.add(enemy1)
            if enemy2.is_die():
                enc[2] = 0
                sprite_group.remove(enemy2)
                if allen < cenemy:
                    enemy2 = Enemy()
                    allen += 1
                    sprite_group.add(enemy2)
        else:
            ca = hero.getca()
            boss.update(hero, attach)
            boss.getca(ca)
            if boss.is_die():
                pygame.mixer.music.stop()
                playm = False
                go = False
                done = False
        health = hero.setenc(enc)
        fps_counter.reheal(health)
        fps_counter.render()
        fps_counter.update()
        pygame.display.flip()
        timer.tick(20)
        if level != levels[-1]:
            if allen >= cenemy:
                if enemy.is_die() and enemy1.is_die() and enemy2.is_die():
                    hero.nextlvl(True)
                    ng = False
                    if not ncl:
                        cl += 1
                    ncl = True
                    if cl > 5:
                        cl = 0
                    if hero.next():
                        go = True
                        level = levels[cl]
                        break

        if hero.is_die():
            pygame.mixer.music.stop()
            playm = False
            done = False
            go = False
