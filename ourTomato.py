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

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
time_ticks, t = pygame.USEREVENT + 1, 1000
pygame.time.set_timer(time_ticks, t)

PAUSE_IMG = [ pygame.image.load(os.path.join("icon", "pause.png")), pygame.image.load(os.path.join("icon", "pause_hover.png"))]
PLAY_IMG = [pygame.image.load(os.path.join("icon", "play.png")), pygame.image.load(os.path.join("icon", "play_hover.png"))]
STOP_IMG = [pygame.image.load(os.path.join("icon", "stop.png")), pygame.image.load(os.path.join("icon", "stop_hover.png"))]
PROGRESS_IMG = [pygame.image.load(os.path.join("progress", "my_tomato_time_{}.png".format(i))) for i in range(37)]

img_rect = PLAY_IMG[0].get_rect()
LEFT_BUTTON_RECT = (10, SCREEN_HEIGHT - img_rect.height - 10, img_rect.width, img_rect.height)
RIGHT_BUTTON_RECT = (SCREEN_WIDTH - 10 - img_rect.width, SCREEN_HEIGHT - img_rect.height - 10, img_rect.width, img_rect.height)

print(LEFT_BUTTON_RECT, RIGHT_BUTTON_RECT)

is_start = False
is_work_time = True

work_time = 25
rest_time = 5

total_work_sec = total_rest_sec = 0
work_sec = rest_sec = 0

is_left_hover = 0
is_right_hover = 0

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

def mouse_hover(event):
    global is_left_hover, is_right_hover
    if (LEFT_BUTTON_RECT[0] < event.pos[0] < LEFT_BUTTON_RECT[0] + LEFT_BUTTON_RECT[2]
        and LEFT_BUTTON_RECT[1] < event.pos[1] < LEFT_BUTTON_RECT[1] + LEFT_BUTTON_RECT[3]):
        is_left_hover = 1
    else:
        is_left_hover = 0
    if (RIGHT_BUTTON_RECT[0] < event.pos[0] < RIGHT_BUTTON_RECT[0] + RIGHT_BUTTON_RECT[2]
        and RIGHT_BUTTON_RECT[1] < event.pos[1] < RIGHT_BUTTON_RECT[1] + RIGHT_BUTTON_RECT[3]):
        is_right_hover = 1
    else:
        is_right_hover = 0

def mouse_click(event):
    global is_start, is_work_time, work_time , rest_time, work_sec, rest_sec, total_work_sec, total_rest_sec

    if (LEFT_BUTTON_RECT[0] < event.pos[0] < LEFT_BUTTON_RECT[0] + LEFT_BUTTON_RECT[2]
            and LEFT_BUTTON_RECT[1] < event.pos[1] < LEFT_BUTTON_RECT[1] + LEFT_BUTTON_RECT[3]):
        if is_start:
            is_start = False
        else:
            is_start = True
            total_work_sec = work_sec = work_time * 60
            total_rest_sec = rest_sec = rest_time * 60
            is_work_time = True


def draw_circle(percent, win):

    idx = - int(percent // 2.7)
    win.blit(PROGRESS_IMG[idx], (0, 0))



def convert_to_time(sec):
    mins, secs = divmod(sec, 60)
    timeformat = '{:0>2d}:{:0>2d}'.format(mins, secs)
    return timeformat


def render_win(win):
    win.fill(BG_COLOR)
    percent = 0
    show_text_input(win, work_time, rest_time)
    if not is_start:
        show_text_countdown(win, '00:00')
    else:
        if is_work_time:
            show_text_countdown(win, convert_to_time(work_sec))
            percent = int(work_sec/total_work_sec * 100)
        else:
            show_text_countdown(win, convert_to_time(rest_sec))
            percent = int(rest_sec/total_rest_sec * 100)
    draw_circle(percent, win)

    if not is_start:
        win.blit(PLAY_IMG[is_left_hover], LEFT_BUTTON_RECT[:2])
    else:
        win.blit(STOP_IMG[is_left_hover], LEFT_BUTTON_RECT[:2])

    win.blit(PAUSE_IMG[is_right_hover], RIGHT_BUTTON_RECT[:2])

    pygame.display.update()


run = True
while run:
    clock.tick(30)
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            mouse_hover(event)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                # do button check
                mouse_click(event)
            elif event.button == 4 and not is_start:
                change_time(event.pos, True)
            elif event.button == 5 and not is_start:
                change_time(event.pos, False)
        if event.type == time_ticks:
            if is_start:
                if is_work_time:
                    work_sec -= 1
                    if work_sec == 0:
                        # alert
                        work_time = False
                else:
                    rest_sec -= 1
                    if rest_sec == 0:
                        work_time = True
    render_win(win)

pygame.quit()
