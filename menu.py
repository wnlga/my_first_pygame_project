import sys
import pygame
import pyganim

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Меню")

font = pygame.font.Font(None, 72)

BACKGROUND = pyganim.PygAnimation([('images/background/0001.jpg', 75),
                                  ('images/background/0002.jpg', 75),
                                  ('images/background/0003.jpg', 75),
                                  ('images/background/0004.jpg', 75),
                                  ('images/background/0005.jpg', 75),
                                  ('images/background/0006.jpg', 75),
                                  ('images/background/0007.jpg', 75),
                                  ('images/background/0008.jpg', 75),
                                  ('images/background/0009.jpg', 75),
                                  ('images/background/0010.jpg', 75),
                                  ('images/background/0011.jpg', 75),
                                  ('images/background/0012.jpg', 75),
                                  ('images/background/0013.jpg', 75),
                                  ('images/background/0014.jpg', 75),
                                  ('images/background/0015.jpg', 75),
                                  ('images/background/0016.jpg', 75),
                                  ('images/background/0017.jpg', 75),
                                  ('images/background/0018.jpg', 75)])

BACKGROUND.scale((SCREEN_WIDTH + 392, SCREEN_HEIGHT + 210))
BACKGROUND.play()

text_new_game = font.render("Начать игру", True, WHITE)
text_continue = font.render("Продолжить", True, WHITE)
text_exit = font.render("Выйти из игры", True, WHITE)

button_spacing = 60

text_rect_new_game = text_new_game.get_rect(
    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.1))
text_rect_exit = text_exit.get_rect(
    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.1 + button_spacing))
text_rect_cont = text_continue.get_rect(
    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.1 - button_spacing))


class Menu():
    def __init__(self):
        self.menu()

    def menu(cont):
        stop = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if text_rect_exit.collidepoint(event.pos):
                        pygame.quit()
                        exit()
                    if text_rect_new_game.collidepoint(event.pos):
                        stop = False
                        poi = True
                        break

                    if not cont:
                        if text_rect_cont.collidepoint(event.pos):
                            stop = False
                            poi = False
                            break
            if not stop:
                break
            screen.fill(BLACK)
            BACKGROUND.blit(screen, (0, -80))

            if text_rect_new_game.collidepoint(pygame.mouse.get_pos()):
                text_new_game.set_alpha(128)
            else:
                text_new_game.set_alpha(255)
            if text_rect_exit.collidepoint(pygame.mouse.get_pos()):
                text_exit.set_alpha(128)
            else:
                text_exit.set_alpha(255)
            if not cont:
                if text_rect_cont.collidepoint(pygame.mouse.get_pos()):
                    text_continue.set_alpha(128)
                else:
                    text_continue.set_alpha(255)
            else:
                text_continue.set_alpha(50)

            screen.blit(text_new_game, text_rect_new_game)
            screen.blit(text_exit, text_rect_exit)
            screen.blit(text_continue, text_rect_cont)

            pygame.display.flip()
        return poi
