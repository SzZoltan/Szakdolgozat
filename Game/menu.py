import sys

import pygame
from Button.Button import Button
from Game_Graphics.Graphics_Loader import (create_btn_pic, play_btn_pic, quit_btn_pic, muted_btn_pic, unmuted_btn_pic,
                                           level1_bg, leaderboard_btn_pic, back_btn_pic)
from level_editor import level_edit
from main import game_loop
pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pink Guy's Adventures - Main Menu")

audio = True
wait = 0

tiles_across = WINDOW_WIDTH // level1_bg.get_width() + 1
tiles_down = WINDOW_HEIGHT // level1_bg.get_height() + 1


def remake_main_menu():
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pink Guy's Adventures - Main Menu")


def draw_background():
    for row in range(tiles_down):
        for col in range(tiles_across):
            x_pos = col * level1_bg.get_width()
            y_pos = row * level1_bg.get_height()
            window.blit(level1_bg, (x_pos, y_pos))


def draw_audio_toggle():
    global audio, wait
    if audio:
        if unmuted_btn.draw(window) and wait == 0:
            print('muted')
            audio = False
            wait = 2
    else:
        if muted_btn.draw(window) and wait == 0:
            print('unmuted')
            audio = True
            wait = 2

    # Szükséges a zene némító és hangosító gombokra hogy 1 kattintásra ne egyszerre mindkettő nyomódjon meg

    if wait != 0:
        wait -= 1


def show_leaderboard():
    r = True

    LB_WIDTH = 600
    LB_HEIGHT = 400
    lb_surface = pygame.Surface((LB_WIDTH, LB_HEIGHT))
    lb_surface.fill((255, 0, 0))

    back_btn = Button(WINDOW_WIDTH-150, WINDOW_HEIGHT-90, back_btn_pic, 1)

    while r:
        draw_background()
        window.blit(lb_surface, (100, 100))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if back_btn.draw(window):
            r = False

        draw_audio_toggle()
        pygame.display.update()


# Gombok definiálása

play_btn = Button(700 // 2, 250, play_btn_pic, 1)
create_btn = Button(660 // 2, 300, create_btn_pic, 1)
quit_btn = Button(700 // 2, 400, quit_btn_pic, 1)
muted_btn = Button(50, 550, muted_btn_pic, 1)
unmuted_btn = Button(50, 550, unmuted_btn_pic, 1)
leaderboard_btn = Button(590 // 2, 350, leaderboard_btn_pic, 1)

run = True
while run:
    draw_background()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # ==================Gombok==================

    if create_btn.draw(window):
        level_edit()
        remake_main_menu()

    if play_btn.draw(window):
        game_loop()
        remake_main_menu()

    if leaderboard_btn.draw(window):
        show_leaderboard()

    if quit_btn.draw(window):
        run = False

    draw_audio_toggle()
    pygame.display.update()


pygame.quit()
sys.exit()
