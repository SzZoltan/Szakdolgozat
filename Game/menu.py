import sys

import pygame
from Button.Button import Button
from Game_Graphics.Graphics_Loader import (create_btn_pic, play_btn_pic, quit_btn_pic, muted_btn_pic, unmuted_btn_pic,
                                           level1_bg, leaderboard_btn_pic, back_btn_pic, left_btn_pic, right_btn_pic,
                                           start_btn_pic)
from level_editor import level_edit
from main import game_loop
from DAO.DAO_sqlite import SQLiteDAO
pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MAX_LEVEL = 3
WHITE = (255, 255, 255)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pink Guy's Adventures - Main Menu")

DAO = SQLiteDAO('leaderboard.db')

audio = True
wait = 0
font = pygame.font.SysFont(None, 50)

tiles_across = WINDOW_WIDTH // level1_bg.get_width() + 1
tiles_down = WINDOW_HEIGHT // level1_bg.get_height() + 1


def remake_main_menu():
    """
    Újraméretezi a Főmenü ablakot és beállítja a nevét
    """
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pink Guy's Adventures - Main Menu")


def draw_background():
    """
    Megrajzólja a Főmenü hátterét
    """
    for row in range(tiles_down):
        for col in range(tiles_across):
            x_pos = col * level1_bg.get_width()
            y_pos = row * level1_bg.get_height()
            window.blit(level1_bg, (x_pos, y_pos))


def draw_audio_toggle():
    """
    Megrajzolja az audio némító és hangosító gombokat, itt változik az audio érték is
    """
    global audio, wait

    if audio:
        if unmuted_btn.draw(window) and wait == 0:
            audio = False
            wait = 2
    else:
        if muted_btn.draw(window) and wait == 0:
            audio = True
            wait = 2

    # Szükséges a zene némító és hangosító gombokra hogy 1 kattintásra ne egyszerre mindkettő nyomódjon meg

    if wait != 0:
        wait -= 1


def show_leaderboard():
    """
    Megrajzolja a Toplista ablakot
    """
    r = True

    LB_WIDTH = 600
    LB_HEIGHT = 400

    level = 1
    left_pressed = False
    right_pressed = False

    leaderboard_level_txt = font.render(f"Our top performers for level: ", True, WHITE)

    lb_surface = pygame.Surface((LB_WIDTH, LB_HEIGHT))
    lb_surface.fill((255, 0, 0))

    back_btn = Button(WINDOW_WIDTH-150, WINDOW_HEIGHT-90, back_btn_pic, 1)
    left_btn = Button(80 - left_btn_pic.get_width(), WINDOW_HEIGHT-325, left_btn_pic, 1)
    right_btn = Button(WINDOW_WIDTH-80, WINDOW_HEIGHT-325, right_btn_pic, 1)

    while r:
        lvl_txt = font.render(f"{level}", True, WHITE)

        draw_background()
        window.blit(lb_surface, (100, 100))
        window.blit(leaderboard_level_txt, (150, 60))
        window.blit(lvl_txt, (WINDOW_WIDTH - 170, 60))

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if back_btn.draw(window) or keys[pygame.K_ESCAPE]:
            r = False

        if left_btn.draw(window) or keys[pygame.K_LEFT]:
            if level > 1 and not left_pressed:
                level -= 1
                left_pressed = True

        if right_btn.draw(window) or keys[pygame.K_RIGHT]:
            if level < MAX_LEVEL and not right_pressed:
                level += 1
                right_pressed = True

        if not keys[pygame.K_LEFT]:
            left_pressed = False

        if not keys[pygame.K_RIGHT]:
            right_pressed = False

        draw_audio_toggle()
        pygame.display.update()


def show_level_selection():
    """
    Megrajzólja a pálya szelekciós ablakot
    """
    r = True

    level = 1
    left_pressed = False
    right_pressed = False

    choose_level_txt = font.render(f"Choose the level you wish to play: ", True, WHITE)

    back_btn = Button(WINDOW_WIDTH-150, WINDOW_HEIGHT-90, back_btn_pic, 1)
    start_btn = Button(WINDOW_WIDTH // 2 - start_btn_pic.get_width() // 2, WINDOW_HEIGHT-90, start_btn_pic, 1)
    left_btn = Button(150 - left_btn_pic.get_width(), WINDOW_HEIGHT-325, left_btn_pic, 1)
    right_btn = Button(WINDOW_WIDTH-150, WINDOW_HEIGHT-325, right_btn_pic, 1)

    while r:
        lvl_txt = font.render(f"Level: {level}", True, WHITE)

        draw_background()
        window.blit(choose_level_txt, (120, 70))
        window.blit(lvl_txt, (WINDOW_WIDTH // 2 - 70, 130))

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if back_btn.draw(window) or keys[pygame.K_ESCAPE]:
            r = False

        if start_btn.draw(window):
            game_loop(level)
            r = False

        if left_btn.draw(window) or keys[pygame.K_LEFT]:
            if level > 1 and not left_pressed:
                level -= 1
                left_pressed = True

        if right_btn.draw(window) or keys[pygame.K_RIGHT]:
            if level < MAX_LEVEL and not right_pressed:
                level += 1
                right_pressed = True

        if not keys[pygame.K_LEFT]:
            left_pressed = False

        if not keys[pygame.K_RIGHT]:
            right_pressed = False

        draw_audio_toggle()
        pygame.display.update()


# Gombok definiálása

play_btn = Button(700 // 2, 250, play_btn_pic, 1)
create_btn = Button(660 // 2, 300, create_btn_pic, 1)
quit_btn = Button(700 // 2, 400, quit_btn_pic, 1)
muted_btn = Button(50, WINDOW_HEIGHT-90, muted_btn_pic, 1)
unmuted_btn = Button(50, WINDOW_HEIGHT-90, unmuted_btn_pic, 1)
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
        pygame.time.delay(100)
        level_edit()
        remake_main_menu()

    if play_btn.draw(window):
        pygame.time.delay(100)
        show_level_selection()
        remake_main_menu()

    if leaderboard_btn.draw(window):
        pygame.time.delay(100)
        show_leaderboard()

    if quit_btn.draw(window):
        run = False

    draw_audio_toggle()
    pygame.display.update()


pygame.quit()
sys.exit()
