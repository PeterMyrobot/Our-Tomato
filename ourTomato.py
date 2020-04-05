import pygame
import os
from pygame.locals import *

from roundrects import round_rect

pygame.init()

pygame.display.set_caption('Our Tomato')

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
BG_COLOR = (50, 74, 92)

EMPTY_COLOR = (99, 100, 101)
FILL_COLOR = (172, 222, 216)

MINS_RECT = (10, 10, 30, 20)
SECS_RECT = (52, 10, 30, 20)
DASH_RECT = (40, 10, 12, 20)
LEFTBUTTON_RECT = (10,300-42,)


win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
MOVEEVENT, t = pygame.USEREVENT + 1, 1000
pygame.time.set_timer(MOVEEVENT, t)

PAUSE_IMG = [ pygame.image.load(os.path.join("icon", "pause.png")), pygame.image.load(os.path.join("icon", "pause_hover.png"))]
PLAY_IMG = [pygame.image.load(os.path.join("icon", "play.png")), pygame.image.load(os.path.join("icon", "play_hover.png"))]
STOP_IMG = [pygame.image.load(os.path.join("icon", "stop.png")), pygame.image.load(os.path.join("icon", "stop_hover.png"))]
PROGRESS_IMG = [pygame.image.load(os.path.join("progress", "my_tomato_time_{}.png".format(i))) for i in range(37)]


def show_text_rect(text, size, rect, color,  win):
    my_font = pygame.font.Font("alien.ttf", size)
    text = my_font.render(text, True, color)

    x = rect[0] + (rect[2] - text.get_rect().width)//2
    y = rect[1] + (rect[3] - text.get_rect().height)//2
    win.blit(text, (x, y))


def show_text_input(win, work, rest):
    round_rect(win, MINS_RECT, (255, 255, 255), 3)
    round_rect(win, SECS_RECT, (255, 255, 255), 3)

    show_text_rect('-',  15, DASH_RECT, (255, 255, 255), win)
    show_text_rect(str(work), 15, MINS_RECT, BG_COLOR, win)
    show_text_rect(str(rest), 15, SECS_RECT, BG_COLOR, win)


def show_text_countdown(win, time):
    my_font = pygame.font.Font("alien.ttf", 46)
    my_font2 = pygame.font.Font("Roboto-Thin.ttf", 13)
    text = my_font.render(time, True, (255, 255, 255))
    till_text = my_font2.render('Till 00 : 00', True, (255, 255, 255))

    x1 = 50 + (200 - text.get_rect().width)//2
    y1 = 50 + 74

    x2 = 50 + (200 - till_text.get_rect().width)//2
    y2 = y1 + text.get_rect().height + 15

    win.blit(text, (x1, y1))
    win.blit(till_text, (x2, y2))


work_time = 25
rest_time = 5

total_sec = 25*60
rundown_sec = 25*60

is_left_hover = 0
is_right_hover = 0


def change_time(pos, is_add):
    global work_time, rest_time
    if 10 < pos[0] < 40 and 10 < pos[1] < 30:
        if is_add:
            work_time += 1
        else:
            work_time -= 1
    elif 52 < pos[0] < 82 and 10 < pos[1] <30:
        if is_add:
            rest_time += 1
        else:
            rest_time -= 1

def draw_circle(percent, win):

    idx = - int(percent // 2.7)
    win.blit(PROGRESS_IMG[idx], (0, 0))



def convert_to_time(sec):
    mins, secs = divmod(sec, 60)
    timeformat = '{:0>2d}:{:0>2d}'.format(mins, secs)
    return timeformat


def render_win(win):
    win.fill(BG_COLOR)

    show_text_input(win, work_time, rest_time)
    show_text_countdown(win, convert_to_time(rundown_sec))

    percent = int(rundown_sec/total_sec * 100)
    draw_circle(percent, win)

    win.blit(PLAY_IMG[is_left_hover], (10, 300-42))
    win.blit(PAUSE_IMG[is_right_hover], (300-42, 300-42))
    pygame.display.update()


run = True
while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                # do button check
                print("button press?")
                pass
            elif event.button == 4:
                change_time(event.pos, True)
            elif event.button == 5:
                change_time(event.pos, False)
        if event.type == MOVEEVENT:
            rundown_sec -= 1
    render_win(win)

pygame.quit()
