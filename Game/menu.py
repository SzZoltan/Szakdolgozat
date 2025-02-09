import pygame
from Button.Button import Button
from Game_Graphics.Graphics_Loader import create_btn_pic
from level_editor import level_edit
pygame.init()

window = pygame.display.set_mode((800, 600))

create_btn = Button(800 // 2, 300, create_btn_pic, 1)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if create_btn.draw(window):
        level_edit()
        window = pygame.display.set_mode((800, 600))

    pygame.display.update()

pygame.quit()

