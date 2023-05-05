#!/usr/bin/python3
import time
from datetime import datetime
from math import cos, sin, radians

import pygame

WIDTH = 1824
HEIGHT = 984


DISPLAY_TIME = 0
DISPLAY_TIMER = 1
TRANSITION = 2
WAITING_FOR_TIMER = 3

TRANSITION_SPEED = 3

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

background = pygame.image.load("higher_quality/bg-removebg.png")
big_needle_image = pygame.image.load("higher_quality/big_needle.png")
big_needle_pivot_point = (62-big_needle_image.get_width()/2, 839-big_needle_image.get_height()/2)
small_needle_image = pygame.image.load("higher_quality/small_needle.png")
small_needle_pivot_point = (72-small_needle_image.get_width()/2, 646-small_needle_image.get_height()/2)
tens_needle_image = pygame.image.load("higher_quality/tens_needle.png")
tens_needle_pivot_point = (31-tens_needle_image.get_width()/2, 242-tens_needle_image.get_height()/2)

#new_big_needle_image = pygame.Surface((big_needle_image.get_width() * 1.6167664670658684, big_needle_image.get_height() * 1.6167664670658684)).convert_alpha()
#new_big_needle_image.fill((0, 0, 0, 0))
#pygame.transform.scale_by(big_needle_image, 1.6167664670658684, new_big_needle_image)
#big_needle_image = new_big_needle_image

surface = pygame.surface.Surface(background.get_size())

timer_started_at = datetime.utcfromtimestamp(0)
# Used for the transition
needles_pos = (0, 0, 0)

mode = DISPLAY_TIME


def rotate(image, angle, pivot):
    rotated = pygame.transform.rotate(image, angle)
    cos_angle = cos(radians(angle))
    sin_angle = sin(radians(angle))
    new_base = ((cos_angle, sin_angle), (-sin_angle, cos_angle))
    new_pivot = (pivot[0] * new_base[0][0] + pivot[1] * new_base[0][1],
                 pivot[0] * new_base[1][0] + pivot[1] * new_base[1][1])
    return rotated, rotated.get_rect(center=(0, 0)).move(-new_pivot[0], -new_pivot[1])


def display_clock(small_needle_rotation, big_needle_rotation, tens_needle_rotation):
    surface.blit(background, (0, 0))
    small_needle_transformed, rect = rotate(small_needle_image, -small_needle_rotation, small_needle_pivot_point)
    surface.blit(small_needle_transformed, rect.move(1085, 2000))
    big_needle_transformed, rect = rotate(big_needle_image, -big_needle_rotation, big_needle_pivot_point)
    surface.blit(big_needle_transformed, rect.move(1085, 2000))
    tens_needle_transformed, rect = rotate(tens_needle_image, -tens_needle_rotation, tens_needle_pivot_point)
    surface.blit(tens_needle_transformed, rect.move(1082, 2494))


def display_current_time():
    global needles_pos
    time = datetime.now()
    seconds_angle = time.second / 60 * 360
    minutes_angle = time.minute / 60 * 360
    hour_angle = time.hour / 12 * 360
    needles_pos = (hour_angle, minutes_angle, seconds_angle)
    display_clock(hour_angle, minutes_angle, seconds_angle)


def display_timer():
    time = datetime.now() - timer_started_at
    seconds = time.seconds % 60
    minutes = (time.seconds - seconds) / 60
    tens_angle = time.microseconds / 1000000 * 360
    seconds_angle = seconds / 60 * 360
    minutes_angle = minutes / 60 * 360
    display_clock(minutes_angle, seconds_angle, tens_angle)


def display_transition():
    global needles_pos, mode, timer_started_at
    if mode == WAITING_FOR_TIMER:
        display_clock(0, 0, 0)
        if time.time() - timer_started_at.timestamp() > 3:
            mode = DISPLAY_TIMER
            timer_started_at = datetime.now()
        return
    if needles_pos[0] != 0:
        needles_pos = (needles_pos[0] - TRANSITION_SPEED if needles_pos[0] < 180 else needles_pos[0] + TRANSITION_SPEED, needles_pos[1], needles_pos[2])
    if needles_pos[1] != 0:
        needles_pos = (needles_pos[0], needles_pos[1] - TRANSITION_SPEED if needles_pos[1] < 180 else needles_pos[1] + TRANSITION_SPEED, needles_pos[2])
    if needles_pos[2] != 0:
        needles_pos = (needles_pos[0], needles_pos[1], needles_pos[2] - TRANSITION_SPEED if needles_pos[2] < 180 else needles_pos[2] + TRANSITION_SPEED)
    if needles_pos[0] % 360 < TRANSITION_SPEED:
        needles_pos = (0, needles_pos[1], needles_pos[2])
    if needles_pos[1] % 360 < TRANSITION_SPEED:
        needles_pos = (needles_pos[0], 0, needles_pos[2])
    if needles_pos[2] % 360 < TRANSITION_SPEED:
        needles_pos = (needles_pos[0], needles_pos[1], 0)
    if needles_pos == (0, 0, 0):
        mode = WAITING_FOR_TIMER
        timer_started_at = datetime.now()
    display_clock(*needles_pos)


clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                exit()
            elif event.key == pygame.K_SPACE and mode == DISPLAY_TIME:
                mode = TRANSITION
    screen.fill((0, 0, 0))
    surface.fill((0, 0, 0))
    if mode == DISPLAY_TIME:
        display_current_time()
    elif mode == DISPLAY_TIMER:
        display_timer()
    elif mode == TRANSITION or WAITING_FOR_TIMER:
        display_transition()
    scale_factor = HEIGHT / background.get_height()
    print(clock.get_fps())
    #print("-----")
    #print(background.get_width())
    #print(1920/2 - background.get_width()/2)
    #print(pygame.mouse.get_pos())
    pygame.transform.smoothscale(surface, (int(background.get_width()*scale_factor), HEIGHT), screen.subsurface((WIDTH/2 - background.get_width()*scale_factor/2, 0, background.get_width()*scale_factor, HEIGHT)))
    pygame.display.flip()


