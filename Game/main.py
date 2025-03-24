import sys

import pygame
from Button.Button import Button
from Game_Graphics.Graphics_Loader import (create_btn_pic, play_btn_pic, quit_btn_pic, muted_btn_pic, unmuted_btn_pic,
                                           level1_bg, leaderboard_btn_pic, back_btn_pic, left_btn_pic, right_btn_pic,
                                           up_btn_pic, down_btn_pic, start_btn_pic, health_head_pic, lvl1_preview_pic,
                                           lvl2_preview_pic, lvl3_preview_pic, lvl4_preview_pic)
from Game.Level_Editor.level_editor import level_edit
from pygame import mixer
from Game.Game_loop.game_loop import game_loop
from DAO.DAO_sqlite import SQLiteDAO
pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MAX_LEVEL = 4
WHITE = (255, 255, 255)
LEVEL_PICTURES = [
    lvl1_preview_pic,
    lvl2_preview_pic,
    lvl3_preview_pic,
    lvl4_preview_pic
]

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pink Guy's Adventures - Main Menu")
pygame.display.set_icon(health_head_pic)

# Háttérzenék

menu_background_music = mixer.Sound('./Audio/Menu_theme.mp3')
menu_background_music.set_volume(0.05)

game_music = mixer.Sound('./Audio/Game_theme.mp3')
game_music.set_volume(0.05)

level_editor_music = mixer.Sound('./Audio/Level_Editor_theme.mp3')
level_editor_music.set_volume(0.05)

menu_background_music.play(-1)

DAO = SQLiteDAO('./Database/leaderboard.db')

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
            menu_background_music.stop()
            audio = False
            wait = 2
    else:
        if muted_btn.draw(window) and wait == 0:
            menu_background_music.play(-1)
            audio = True
            wait = 2

    # Szükséges a zene némító és hangosító gombokra hogy 1 kattintásra ne egyszerre mindkettő nyomódjon meg

    if wait != 0:
        wait -= 1


def show_leaderboard():
    """
    Megrajzolja a Toplista ablakot
    """
    def draw_leaderboard_entries_window():
        """
        Megrajzolja magát a toplistát
        """

        lb_surface = pygame.Rect(WINDOW_WIDTH//8, WINDOW_HEIGHT//6, LB_WIDTH, LB_HEIGHT)
        pygame.draw.rect(window, (255, 0, 0), lb_surface, -1)

        for i in range(scroll_offset, min(scroll_offset + max_visible_scores, len(lb_entries))):
            name, score = lb_entries[i]
            text = font.render(f"{i+1}. {name}: {score}", True, WHITE)
            window.blit(text, (lb_surface.x + LB_WIDTH//3, lb_surface.y + 15 + (i - scroll_offset) * 30))

    r = True

    level = 1
    left_pressed = False
    right_pressed = False
    up_pressed = False
    down_pressed = False

    with DAO:
        lb_entries = DAO.get_all(level)

    LB_WIDTH = 600
    LB_HEIGHT = 400
    max_visible_scores = LB_HEIGHT // 31
    scroll_offset = 0

    back_btn = Button(WINDOW_WIDTH-150, WINDOW_HEIGHT-90, back_btn_pic, 1)
    left_btn = Button(80 - left_btn_pic.get_width(), WINDOW_HEIGHT - 325, left_btn_pic, 1)
    right_btn = Button(WINDOW_WIDTH-80, WINDOW_HEIGHT - 325, right_btn_pic, 1)
    up_btn = Button(WINDOW_WIDTH - 200, WINDOW_HEIGHT - 490, up_btn_pic, 1)
    down_btn = Button(WINDOW_WIDTH - 200, WINDOW_HEIGHT - 150, down_btn_pic, 1)

    while r:
        leaderboard_level_txt = font.render(f"Our top performers for level: {level}", True, WHITE)

        draw_background()
        draw_leaderboard_entries_window()
        window.blit(leaderboard_level_txt, (150, 60))

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if back_btn.draw(window) or keys[pygame.K_ESCAPE]:
            r = False

        if left_btn.draw(window) or keys[pygame.K_LEFT]:
            if level > 1 and not left_pressed:
                level -= 1
                with DAO:
                    lb_entries = DAO.get_all(level)
                left_pressed = True

        if right_btn.draw(window) or keys[pygame.K_RIGHT]:
            if level < MAX_LEVEL and not right_pressed:
                level += 1
                with DAO:
                    lb_entries = DAO.get_all(level)
                right_pressed = True

        if up_btn.draw(window) or keys[pygame.K_UP]:
            if scroll_offset > 0 and not up_pressed:
                scroll_offset -= 1
                up_pressed = True
        if down_btn.draw(window) or keys[pygame.K_DOWN]:
            if scroll_offset + max_visible_scores < len(lb_entries) and not down_pressed:
                scroll_offset += 1
                down_pressed = True

        if not keys[pygame.K_LEFT]:
            left_pressed = False

        if not keys[pygame.K_RIGHT]:
            right_pressed = False

        if not keys[pygame.K_UP]:
            up_pressed = False

        if not keys[pygame.K_DOWN]:
            down_pressed = False

        draw_audio_toggle()
        pygame.display.update()


def show_level_selection():
    """
    Megrajzólja a pálya szelekciós ablakot
    """
    def draw_level_picture(lvl: int):
        """
        Megrajzolja a pálya előnézet képét
        :param lvl: a pálya amelyiket jelenleg kiválasztott a játékos
        """
        LS_WIDTH = 402
        LS_HEIGHT = 252

        ls_surface = pygame.Rect(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 3, LS_WIDTH, LS_HEIGHT)
        pygame.draw.rect(window, (0, 255, 0), ls_surface, 1)
        window.blit(LEVEL_PICTURES[level-1], (ls_surface.x + 1, ls_surface.y + 1))

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
        draw_level_picture(level)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if back_btn.draw(window) or keys[pygame.K_ESCAPE]:
            r = False

        if start_btn.draw(window):
            menu_background_music.stop()
            if audio:
                game_music.play(-1)
            game_loop(level)
            if audio:
                game_music.stop()
                menu_background_music.play(-1)
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
        menu_background_music.stop()
        if audio:
            level_editor_music.play(-1)
        level_edit()
        if audio:
            level_editor_music.stop()
            menu_background_music.play(-1)

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
