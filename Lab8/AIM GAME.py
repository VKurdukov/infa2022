import pygame
from pygame.draw import *
from random import randint

pygame.init()

pygame.mouse.set_visible(False)

FPS = 576
screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("BALLS 2")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, YELLOW, GREEN, MAGENTA]

font = pygame.font.SysFont("Arial Black", 25)

lose = font.render('U LOSE! [click to play again]', 0, (0, 0, 0))
loserect = [0, 0, 0, 0]
win = font.render('U SURVIVED! [click to play again]', 0, (0, 0, 0))
winrect = [0, 0, 0, 0]


def new_ball():
    '''рисует новый шарик '''
    x = randint(200, 1000)
    y = randint(200, 700)
    r = randint(10, 100)
    color = COLORS[randint(0, 3)]
    vx = 0
    vy = 0
    circle(screen, color, (x, y), r)
    circle(screen, BLACK, (x, y), r, 5)
    objs.append([(x, y), r, color, (vx, vy)])
    return [(x, y), r, color, (vx, vy)]


def rvec_sq(mp, xy):
    a = (mp[0] - xy[0]) ** 2 + (mp[1] - xy[1]) ** 2
    return a


def distance(mp, objs, hited):
    '''проверяет, куда попадает мышка и обновляет shoted'''
    hited = []
    for i in range(len(objs)):
        if rvec_sq(mp, objs[i][0]) <= objs[i][1] ** 2:
            hited.append(i)
    return hited


def prin(objs, mousepos, score):
    '''рисует окно и выводит на экран все объекты'''
    rect(screen, BLUE, (100, 100, 1000, 700))
    for i in objs:
        circle(screen, i[2], i[0], i[1])
        circle(screen, BLACK, i[0], i[1], 5)
    for i in range(len(mousetrail) - 1):
        circle(screen, CYAN, mousetrail[i], 12)
    circle(screen, WHITE, mousepos, 17)
    circle(screen, BLUE, mousepos, 16)
    scoresurf = screen.blit(font.render('Score: ' + str(score), 1, GREEN), (0, 0))
    combosurf = screen.blit(font.render(str(combo) + 'X', 0, GREEN), (0, 870))


score = 0
objs = []
mousetrail = [(5000, 5000)] * (FPS // 10)
print(mousetrail)
tickcounter = 0
hited = []

pygame.display.update()
clock = pygame.time.Clock()
funny = True
pause = 0
combo = 0
mp = (600, 450)

while funny:

    clock.tick(FPS)

    del mousetrail[0]
    mousetrail.append(mp)

    if pause == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                funny = False
            if event.type == pygame.MOUSEMOTION:
                mp = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                hited = distance(mp, objs, hited)
                if len(hited) > 0:
                    combo += 1
                    score += combo
                    del objs[hited[-1]]
                else:
                    combo = 0

    tickcounter += 1
    if tickcounter == 3 * FPS // 4:
        tickcounter = 0
        a = new_ball()
    prin(objs, pygame.mouse.get_pos(), score)

    if len(objs) > 7:
        funny = False

    # new_ball()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()