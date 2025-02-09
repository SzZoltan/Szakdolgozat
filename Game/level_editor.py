import pygame
import pickle
from Button.Button import Button
from Game.Game_Graphics.Graphics_Loader import (level1_bg, level3_bg, level2_bg, map_editor_tile_list,
                                                save_btn_pic, load_btn_pic, ok_btn_pic, back_btn_pic)
def level_edit():
    pygame.init()

    # 20 FPS-re cappelt óra
    clock = pygame.time.Clock()
    FPS = 20

    # A screen-hez tartozó változók
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 640
    BOTTOM_MARGIN = 140
    RIGHT_MARGIN = 300

    GREEN = (144, 201, 120)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)

    window = pygame.display.set_mode((WINDOW_WIDTH + RIGHT_MARGIN, WINDOW_HEIGHT + BOTTOM_MARGIN))
    pygame.display.set_caption('Level Editor')

    # Játékhoz használt változók
    ROWS = 16
    MAX_COLS = 150
    TILE_SIZE = WINDOW_HEIGHT // ROWS
    font = pygame.font.SysFont('Futura', 30)
    level = 0
    background_id = 1

    scroll_left = False
    scroll_right = False
    scroll = 0
    scroll_speed = 1
    mcx_position = 0
    mcy_position = ROWS - 2
    endtilex_position = 9
    endtiley_position = ROWS - 2


    # Rajzoló metódusok és hozzájuk tartózó változók

    tiles_across = WINDOW_WIDTH * 5 // level1_bg.get_width()
    tiles_down = WINDOW_HEIGHT // level1_bg.get_height()
    MAP_WIDTH = level1_bg.get_width() * tiles_across
    current_tile = 0


    # Pálya elmentése listába

    world_data = []
    for row in range(ROWS):
        r = [-1] * MAX_COLS
        world_data.append(r)

    map_data = {
        'world_data': world_data,
        'background': background_id
    }
    # Ezzel egy alap földet generálunk

    for tile in range(0, MAX_COLS):
        world_data[ROWS-1][tile] = 0
    world_data[ROWS-2][0] = 6
    world_data[ROWS-2][9] = 10

    # Szöveg kiírására szolgáló metódus


    def draw_txt(text, font, text_color, x, y, surface):
        img = font.render(text, True, text_color)
        surface.blit(img, (x, y))


    # Csinál egy új felületet amibe kiírja az error üzenetet és egy gomb megnyomásával el lehet tüntetni a felületet

    def error_popup(text):
        popup_width = 500
        popup_height = 200
        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.fill(RED)

        draw_txt(text, font, WHITE, popup_width // 2 - 100, popup_height // 2 - 50, popup_surface)

        ok_btn = Button((WINDOW_WIDTH+RIGHT_MARGIN) // 2 - 40, (WINDOW_HEIGHT+BOTTOM_MARGIN) // 2 + 50, ok_btn_pic, 1)

        window.fill(BLACK)
        window.blit(popup_surface, ((WINDOW_WIDTH + RIGHT_MARGIN)//2 - popup_width // 2,
                                    (WINDOW_HEIGHT + BOTTOM_MARGIN) // 2 - popup_height // 2))
        pygame.display.flip()
        waiting = True

        wait = 200
        waitcountdown = False

        while waiting:
            if waitcountdown:
                wait -= 1
            if wait == 0:
                waiting = False

            if ok_btn.draw(window):
                waitcountdown = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.update()


    def draw_bg():
        window.fill(GREEN)
        if background_id == 1:
            for rows in range(tiles_down):
                for col in range(tiles_across):
                    x_pos = col * level1_bg.get_width()
                    y_pos = rows * level1_bg.get_height()
                    window.blit(level1_bg, (x_pos - scroll, y_pos))
        elif background_id == 2:
            for rows in range(tiles_down):
                for col in range(tiles_across):
                    x_pos = col * level2_bg.get_width()
                    y_pos = rows * level2_bg.get_height()
                    window.blit(level2_bg, (x_pos - scroll, y_pos))
        else:
            for rows in range(tiles_down):
                for col in range(tiles_across):
                    x_pos = col * level3_bg.get_width()
                    y_pos = rows * level3_bg.get_height()
                    window.blit(level3_bg, (x_pos - scroll, y_pos))


    def draw_grid():

        # v mint vertical

        for v in range(MAX_COLS + 1):
            pygame.draw.line(window, WHITE, (v * TILE_SIZE - scroll, 0),
                             (v * TILE_SIZE - scroll, WINDOW_HEIGHT), 2)

        # h mint horizontal

        for h in range(ROWS + 1):
            pygame.draw.line(window, WHITE, (0, h * TILE_SIZE), (WINDOW_WIDTH, h * TILE_SIZE), 2)


    def draw_world():
        for y, rows in enumerate(world_data):
            for x, t in enumerate(rows):
                if t >= 0:
                    window.blit(map_editor_tile_list[t], (x * TILE_SIZE - scroll, y * TILE_SIZE))


    def load_map():
        filler_data = {
            'world_data': world_data,
            'background': background_id
        }
        try:
            with open(f'Maps/level_{level}_data', 'rb') as pickle_in:
                data = pickle.load(pickle_in)
                return data
        except FileNotFoundError:
            error_popup('Map not found error')
            return filler_data
        except pickle.UnpicklingError:
            error_popup('Map unpickling error')
            return filler_data
        except Exception as e:
            error_popup(f'Something went wrong: {e}')
            return filler_data


    def save_map():
        try:
            map_data['world_data'] = world_data
            map_data['background'] = background_id
            with open(f'Maps/level_{level}_data', 'wb') as pickle_out:
                pickle.dump(map_data, pickle_out)
        except FileNotFoundError:
            error_popup("Directory doesn't exist")
        except pickle.PickleError:
            error_popup("The Map can't be saved")
        except Exception as e:
            error_popup(f'Something went wrong: {e}')
        finally:
            pickle_out.close()


    #   Megnézi hogy van-e pontosan 1 Főszereplő és pontosan 1 záró block

    def check_map_validity():
        mc_count = 0
        endtile_count = 0
        error_builder = ''
        for r in world_data:
            for col in r:
                if col == 6:
                    mc_count += 1
                if col == 10:
                    endtile_count += 1
        if mc_count == 0:
            error_builder = 'There is no main character'
        if mc_count > 1:
            error_builder = 'There is more than one main character'
        if endtile_count == 0:
            error_builder = 'There is no end tile'
        if endtile_count > 1:
            error_builder = 'There is more than one end tile'
        if mc_count != 1 or endtile_count != 1:
            error_popup(error_builder)
            return False
        else:
            return True


    # Gombok létrehozása

    button_list = []
    button_col = 0
    button_row = 0

    save_btn = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT + BOTTOM_MARGIN - 50, save_btn_pic, 1)
    load_btn = Button(WINDOW_WIDTH // 2 + 200, WINDOW_HEIGHT + BOTTOM_MARGIN - 50, load_btn_pic, 1)
    back_btn = Button(WINDOW_WIDTH // 2 + 500, WINDOW_HEIGHT + BOTTOM_MARGIN - 50, back_btn_pic, 1)

    # Skálázuk egy kicsit a map_editor_tile_list képeit és utána a gombra tesszük és utána eltoljuk 75 pixel + 50-el

    for i in range(len(map_editor_tile_list)):
        img = pygame.transform.scale(map_editor_tile_list[i], (TILE_SIZE, TILE_SIZE))
        tile_button = Button(WINDOW_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img, 1)
        button_list.append(tile_button)
        button_col += 1
        if button_col == 3:
            button_row += 1
            button_col = 0


    run = True
    while run:
        clock.tick(FPS)
        draw_bg()
        draw_grid()
        draw_world()

        draw_txt(f'Level: {level}', font, WHITE, 10, WINDOW_HEIGHT + BOTTOM_MARGIN - 100, window)
        draw_txt('Press UP or DOWN arrows to change level and 1,2,3 to change background', font, WHITE, 10,
                 WINDOW_HEIGHT + BOTTOM_MARGIN - 70, window)

        pygame.draw.rect(window, GREEN, (WINDOW_WIDTH, 0, RIGHT_MARGIN, WINDOW_HEIGHT))

        if back_btn.draw(window):
            run = False

        # Pálya mentése

        if save_btn.draw(window):
            if check_map_validity():
                save_map()

        # Pálya betöltés

        if load_btn.draw(window):
            scroll = 0
            load = load_map()
            world_data = load['world_data']
            background_id = load['background']

        button_count = 0
        for button_count, i in enumerate(button_list):
            if i.draw(window):
                current_tile = button_count

        pygame.draw.rect(window, BLUE, (button_list[current_tile]), 3)

        # Kamera mozgás

        if scroll_left and scroll > 0:
            scroll -= 5 * scroll_speed
        if scroll_right and scroll < MAP_WIDTH - WINDOW_WIDTH:
            scroll += 5 * scroll_speed

        # Új tile hozzáadaása a képhez

        pos = pygame.mouse.get_pos()
        x = (pos[0] + scroll) // TILE_SIZE
        y = pos[1] // TILE_SIZE

        if pos[0] < WINDOW_WIDTH and pos[1] < WINDOW_HEIGHT:
            if pygame.mouse.get_pressed()[0] == 1:
                if world_data[y][x] != current_tile:
                    if current_tile == 6:
                        if world_data[mcy_position][mcx_position] == 6:
                            world_data[mcy_position][mcx_position] = -1
                        world_data[y][x] = current_tile
                        mcx_position = x
                        mcy_position = y
                    elif current_tile == 10:
                        if world_data[endtiley_position][endtilex_position] == 10:
                            world_data[endtiley_position][endtilex_position] = -1
                        world_data[y][x] = current_tile
                        endtilex_position = x
                        endtiley_position = y
                    else:
                        if world_data[y][x] != 6 or world_data[y][x] != 10:
                            world_data[y][x] = current_tile

            if pygame.mouse.get_pressed()[2] == 1:
                world_data[y][x] = -1

        # pygame event-ek kezelője

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    scroll_left = True
                if event.key == pygame.K_RIGHT:
                    scroll_right = True
                if event.key == pygame.K_RSHIFT:
                    scroll_speed = 5
                if event.key == pygame.K_UP:
                    level += 1
                if event.key == pygame.K_DOWN and level > 0:
                    level -= 1
                if event.key == pygame.K_1:
                    background_id = 1
                if event.key == pygame.K_2:
                    background_id = 2
                if event.key == pygame.K_3:
                    background_id = 3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    scroll_left = False
                if event.key == pygame.K_RIGHT:
                    scroll_right = False
                if event.key == pygame.K_RSHIFT:
                    scroll_speed = 1

        pygame.display.update()

