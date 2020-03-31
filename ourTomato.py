import pygame
import os
import math
from pygame.locals import *

from roundrects import round_rect

pygame.init()

pygame.display.set_caption('Our Tomato')

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
BG_COLOR = (50, 74, 92)

EMPTY_COLOR = (99, 100, 101)
FILL_COLOR = (172, 222, 216)

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
MOVEEVENT, t = pygame.USEREVENT+1, 1000
pygame.time.set_timer(MOVEEVENT, t)

PAUSE_IMG = pygame.image.load(os.path.join("icon", "pause.png"))
PAUSE_IMG_HOVER = pygame.image.load(os.path.join("icon", "pause_hover.png"))
PLAY_IMG = pygame.image.load(os.path.join("icon", "play.png"))
PLAY_IMG_HOVER = pygame.image.load(os.path.join("icon", "play_hover.png"))
STOP_IMG = pygame.image.load(os.path.join("icon", "stop.png"))
STOP_IMG_HOVER = pygame.image.load(os.path.join("icon", "stop_hover.png"))


def show_text(text, x, y, size, color, win):
    my_font = pygame.font.SysFont("arial", size)
    text = my_font.render(text, True, color)
    win.blit(text, (x, y))

def show_text_input( win):
    round_rect(win,(10,10,30,20), (255,255,255), 3)

def draw_circle(angle, radius, width, x, y, color, win):
    pass
    # degree = 0
    # while degree < angle:
    #     new_x = int(x + radius * math.cos(math.pi/2 -degree))
    #     new_y = int(y - radius * math.sin(math.pi/2 - degree))
    #     pygame.draw.circle(win, color, (new_x, new_y), width)
    #     degree += math.pi/100


rundown_sec = 25*60

def convert_to_time(sec):
    mins, secs = divmod(sec, 60)
    timeformat = '{:0>2d}:{:0>2d}'.format(mins, secs)
    return timeformat


def render_win(win):

    win.fill(BG_COLOR)

    show_text(convert_to_time(rundown_sec), 90, 100, 60, (255, 255, 255), win)
    show_text_input(win)
    show_text('25', 18, 10, 15, BG_COLOR, win)
    draw_circle(6.28, 100, 3, 150, 150, EMPTY_COLOR, win)
    draw_circle(3.14, 100, 3, 150, 150, FILL_COLOR, win)

    win.blit(PAUSE_IMG, (20, 250))
    win.blit(PAUSE_IMG_HOVER, (60, 250))
    win.blit(PLAY_IMG, (100, 250))
    win.blit(PLAY_IMG_HOVER, (140, 250))
    win.blit(STOP_IMG, (180, 250))
    win.blit(STOP_IMG_HOVER, (220, 250))
    pygame.display.update()


run = True
while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print('start count')
        if event.type == MOVEEVENT:
            rundown_sec -= 1
    render_win(win)


pygame.quit()
