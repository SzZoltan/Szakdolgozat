import pygame

MAP_EDITOR_TILE_TYPES = 11
GRAPHICS_LOCATION = 'Graphics'


def getSprite(sheet: pygame.Surface, f_width: int, f_height: int, x: int, y: int):
    """
    A spritesheetből kiszed 1 frame-et és visszadja
    :param sheet: pygame.Surface, a Spritesheet
    :param f_width: int, frame szélessége
    :param f_height: int, fram magassága
    :param x: int, a frame kezdő x koordinátája
    :param y: int, a frame kezdő y koordinátája
    :return: pygame.Surface, a frame amit kivágott a spritesheetből
    """

    if (not isinstance(sheet, pygame.Surface) or not isinstance(f_width, int) or
            not isinstance(f_height, int) or not isinstance(x, int) or not isinstance(y, int)):
        raise TypeError('Invalid Argument type for getSprite')

    frame = pygame.Surface((f_width, f_height), pygame.SRCALPHA)
    frame.blit(sheet, (0, 0), (x * f_width, y * f_height, f_width, f_height))
    return frame


# Kiszedjük a frame-eket egy listába:
def frameToList(width: int, height: int, rows: int, collums: int, spritesheet: pygame.Surface):
    """
    Készít egy listát a beolvasott spritesheetből
    :param width: int, az egyes frame-ek szélessége
    :param height: int, az egyes frame-ek magassága
    :param rows: int, a spritesheet sorainak száma
    :param collums: int, a spritesheet oszlopainak száma
    :param spritesheet: pygame.Surface, a sprite sheet
    :return: pygame.Surface list, a különböző frame-ekből álló lista
    """
    if (not isinstance(width, int) or not isinstance(height, int) or not isinstance(rows, int) or
            not isinstance(collums, int) or not isinstance(spritesheet, pygame.Surface)):
        raise TypeError('Invalid Argument type for frameToList')
    frames = []
    for row in range(rows):
        for col in range(collums):
            frame = getSprite(spritesheet, width, height, col, row)
            frames.append(frame)
    return frames


# Frame iteráló
def iterateFrames(self, window: pygame.Surface, frames: list, f_count: int, m_frames: int):
    """
    Végigiterál egy frame-ek listáján ez rajzól mindent a képernyőre

    :param self: maga az objektum ami alkalmazni fogja ezt a metódust
    :param window: pygame.Surface, a felület amire felrajzolják
    :param frames: pygame.Surface list, a lista amin iterálunk
    :param f_count: int, a jelenlegi frame mutatója
    :param m_frames: int, a maximális frame-ek száma a listában

    :return: f_count, a mutató
    """
    if (not isinstance(window, pygame.Surface) or not isinstance(frames, list) or
            not isinstance(f_count, int) or not isinstance(m_frames, int)):
        raise TypeError('Invalid Argument type for iterateFrames')
    for frame in frames:
        if not isinstance(frame, pygame.Surface):
            raise TypeError("The frames list must contain only pygame.Surface objects")
    if f_count < m_frames:
        window.blit(frames[f_count], (self.x, self.y))
        f_count += 1
    else:
        f_count = 0
        window.blit(frames[f_count], (self.x, self.y))
    return f_count


# ====================================================User Interface====================================================

half_heart_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/User Interface/Half_Heart.png')
full_heart_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/User Interface/Full_Heart.png')
empty_heart_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/User Interface/Empty_Heart.png')
health_head_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/User Interface/Health_Head.png')
pause_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/User Interface/pause.png')
unpause_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/User Interface/unpause.png')
cherries_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/User Interface/Cherries.png')

# ====================================================Map Previews======================================================

lvl1_preview_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Map_previews/Lvl1_preview.png')
lvl2_preview_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Map_previews/Lvl2_preview.png')
lvl3_preview_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Map_previews/Lvl3_preview.png')
lvl4_preview_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Map_previews/Lvl4_preview.png')

# =======================================================Gombok=========================================================

save_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/save_btn.png')
load_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/load_btn.png')
ok_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/ok_btn.png')
back_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/back_btn.png')
muted_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/muted_btn.png')
unmuted_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/unmuted_btn.png')
no_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/no_btn.png')
yes_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/yes_btn.png')
play_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/play_btn.png')
quit_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/quit_btn.png')
create_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/create_btn.png')
leaderboard_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/leaderboard_btn.png')
left_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/left_btn.png')
right_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/right_btn.png')
up_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/up_btn.png')
down_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/down_btn.png')
start_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/start_btn.png')
again_btn_pic = pygame.image.load(f'{GRAPHICS_LOCATION}/Buttons/again_btn.png')

# =======================================================Spriteok=======================================================

# Főszereplő

mc_running_right_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Main Characters/Pink Man/Run (32x32).png')
mc_running_left_sprite = pygame.transform.flip(mc_running_right_sprite, True, False)
mc_idle_right_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Main Characters/Pink Man/Idle (32x32).png')
mc_idle_left_sprite = pygame.transform.flip(mc_idle_right_sprite, True, False)
mc_jump_right_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Main Characters/Pink Man/Jump (32x32).png')
mc_jump_left_sprite = pygame.transform.flip(mc_jump_right_sprite, True, False)

# Pálya háttér

level1_bg = pygame.image.load(f'{GRAPHICS_LOCATION}/Background/Brown.png')
level2_bg = pygame.image.load(f'{GRAPHICS_LOCATION}/Background/Purple.png')
level3_bg = pygame.image.load(f'{GRAPHICS_LOCATION}/Background/Blue.png')

# Power Upok

apple_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Items/Fruits/Apple.png')
pineapple_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Items/Fruits/Pineapple.png')
cherry_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Items/Fruits/Cherries.png')
strawberry_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Items/Fruits/Strawberry.png')

# Finish kupa

end_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Items/Checkpoints/End/End (Idle).png')

# Bunny ellenfél

bunny_run_left_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Enemies/Bunny/Run (34x44).png')
bunny_run_right_sprite = pygame.transform.flip(bunny_run_left_sprite, True, False)
bunny_idle_left_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Enemies/Bunny/Idle (34x44).png')
bunny_idle_right_sprite = pygame.transform.flip(bunny_idle_left_sprite, True, False)

# Plant ellenfél

plant_idle_left_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Enemies/Plant/Idle (44x42).png')
plant_idle_right_sprite = pygame.transform.flip(plant_idle_left_sprite, True, False)
plant_attack_left_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Enemies/Plant/Attack (44x42).png')
plant_attack_right_sprite = pygame.transform.flip(plant_attack_left_sprite, True, False)

# Turtle ellenfél

turtle_idle_spiked_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Enemies/Turtle/Idle 1 (44x26).png')
turtle_idle_unspiked_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Enemies/Turtle/Idle 2 (44x26).png')
turtle_spikes_in_sprites = pygame.image.load(f'{GRAPHICS_LOCATION}/Enemies/Turtle/Spikes in (44x26).png')
turtle_spikes_out_sprites = pygame.image.load(f'{GRAPHICS_LOCATION}/Enemies/Turtle/Spikes out (44x26).png')

# Block sprite

brick_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Terrain/brick.png')
steel_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Terrain/steel.png')
gold_sprite = pygame.image.load(f'{GRAPHICS_LOCATION}/Terrain/gold.png')

# Map Editor képek

map_editor_tile_list = []
for x in range(MAP_EDITOR_TILE_TYPES):
    img = pygame.image.load(f'{GRAPHICS_LOCATION}/Editor Tiles/{x}.png')
    map_editor_tile_list.append(img)

# ======================================================Frame-ek========================================================

# Főszereplő

mc_run_right_frames = frameToList(32, 32, 1, 12, mc_running_right_sprite)
mc_run_left_frames = frameToList(32, 32, 1, 12, mc_running_left_sprite)
mc_idle_right_frames = frameToList(32, 32, 1, 11, mc_idle_right_sprite)
mc_idle_left_frames = frameToList(32, 32, 1, 11, mc_idle_left_sprite)
mc_jump_right_frames = frameToList(32, 32, 1, 1, mc_jump_right_sprite)
mc_jump_left_frames = frameToList(32, 32, 1, 1, mc_jump_left_sprite)

# Power Up

apple_frames = frameToList(32, 32, 1, 17, apple_sprite)
pineapple_frames = frameToList(32, 32, 1, 17, pineapple_sprite)
cherry_frames = frameToList(32, 32, 1, 17, cherry_sprite)
strawberry_frames = frameToList(32, 32, 1, 17, strawberry_sprite)

# Finish kupa

end_frame = frameToList(64, 64, 1, 1, end_sprite)

# Bunny Ellenfél

bunny_run_left_frames = frameToList(34, 44, 1, 12, bunny_run_left_sprite)
bunny_run_right_frames = frameToList(34, 44, 1, 12, bunny_run_right_sprite)
bunny_idle_left_frames = frameToList(34, 44, 1, 8, bunny_idle_left_sprite)
bunny_idle_right_frames = frameToList(34, 44, 1, 8, bunny_idle_right_sprite)

# Plant Ellenfél

plant_idle_left_frames = frameToList(44, 42, 1, 11, plant_idle_left_sprite)
plant_idle_right_frames = frameToList(44, 42, 1, 11, plant_idle_right_sprite)
plant_attack_left_frames = frameToList(44, 42, 1, 8, plant_attack_left_sprite)
plant_attack_right_frames = frameToList(44, 42, 1, 8, plant_attack_right_sprite)

# Turtle Ellenfél

turtle_idle_spiked_frames = frameToList(44, 42, 1, 14, turtle_idle_spiked_sprite)
turtle_idle_unspiked_frames = frameToList(44, 42, 1, 14, turtle_idle_unspiked_sprite)
turtle_spikes_in_frames = frameToList(44, 42, 1, 8, turtle_spikes_in_sprites)
turtle_spikes_out_frames = frameToList(44, 42, 1, 8, turtle_spikes_out_sprites)

# Block

brick_frame = frameToList(40, 40, 1, 1, brick_sprite)
steel_frame = frameToList(40, 40, 1, 1, steel_sprite)
gold_frame = frameToList(40, 40, 1, 1, gold_sprite)

