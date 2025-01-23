import pygame
from Button.Button import Button
from Game.Game_Graphics.Graphics_Loader import level1_bg, level3_bg, level2_bg

pygame.init()

# 20 FPS-re cappelt óra
clock = pygame.time.Clock()
FPS = 20

# A screen-hez tartozó változók
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 640
BOTTOM_MARGIN = 140
RIGHT_MARGIN = 300

window = pygame.display.set_mode((WINDOW_WIDTH + RIGHT_MARGIN, WINDOW_HEIGHT + BOTTOM_MARGIN))
pygame.display.set_caption('Level Editor')

# Játékhoz használt változók
ROWS = 16
MAX_COLS = 150
TILE_SIZE = WINDOW_HEIGHT // ROWS

scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1


# Rajzoló metódusok és hozzájuk tartózó változók

tiles_across = WINDOW_WIDTH * 5 // level1_bg.get_width()
tiles_down = WINDOW_HEIGHT // level1_bg.get_height()
MAP_WIDTH = level1_bg.get_width() * tiles_across


# Hogy változtassuk meg a háttéret? ötlet: listába beletesszük az összes képet és gombra változtatjuk
def draw_bg():
    window.fill((144, 201, 120))
    for row in range(tiles_down):
        for col in range(tiles_across):
            x_pos = col * level1_bg.get_width()
            y_pos = row * level1_bg.get_height()
            window.blit(level1_bg, (x_pos - scroll, y_pos))


def draw_grid():
    # v mint vertical
    for v in range(MAX_COLS + 1):
        pygame.draw.line(window, (255, 255, 255), (v * TILE_SIZE - scroll, 0),
                         (v * TILE_SIZE - scroll, WINDOW_HEIGHT), 2)
    # h mint horizontal
    for h in range(ROWS + 1):
        pygame.draw.line(window, (255, 255, 255), (0, h * TILE_SIZE), (WINDOW_WIDTH, h * TILE_SIZE), 2)


run = True
while run:
    clock.tick(FPS)
    draw_bg()
    draw_grid()

    # kamera mozgás
    if scroll_left and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < MAP_WIDTH - WINDOW_WIDTH:
        scroll += 5 * scroll_speed

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

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()
