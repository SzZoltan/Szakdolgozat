import pygame

def getSprite(sheet: pygame.Surface, f_width: int, f_height: int, x: int, y: int):
    # kiszed 1 frame-et a sprite-sheetből
    # f_width: frame széle
    # f_height: frame hossza
    # x: x kezdő koordináta a frame-en
    # y: y kezdő koordináta a frame-en

    if (not isinstance(sheet, pygame.Surface) or not isinstance(f_width, int) or
            not isinstance(f_height, int) or not isinstance(x, int) or not isinstance(y, int)):
        raise TypeError('Invalid Argument type for getSprite')

    frame = pygame.Surface((f_width, f_height), pygame.SRCALPHA)
    frame.blit(sheet, (0, 0), (x * f_width, y * f_height, f_width, f_height))
    return frame


# Kiszedjük a frame-eket egy listába:
def frameToList(width: int, height: int, rows: int, collums: int, spritesheet: pygame.Surface):
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


# Java doc szerű doksit létrehozni, ha létezik
# Property fájlba kiszedni ezeket
# Főszereplő
mc_running_right_sprite = pygame.image.load(f'Graphics/Main Characters/Pink Man/Run (32x32).png')
mc_running_left_sprite = pygame.transform.flip(mc_running_right_sprite, True, False)
mc_idle_right_sprite = pygame.image.load(f'Graphics/Main Characters/Pink Man/Idle (32x32).png')
mc_idle_left_sprite = pygame.transform.flip(mc_idle_right_sprite, True, False)
mc_jump_right_sprite = pygame.image.load(f'Graphics/Main Characters/Pink Man/Jump (32x32).png')
mc_jump_left_sprite = pygame.transform.flip(mc_jump_right_sprite, True, False)
# Pálya háttér
level1_bg = pygame.image.load(f'Graphics/Background/Brown.png')
# Power Upok
apple_sprite = pygame.image.load(f'Graphics/Items/Fruits/Apple.png')
pineapple_sprite = pygame.image.load(f'Graphics/Items/Fruits/Pineapple.png')
cherry_sprite = pygame.image.load(f'Graphics/Items/Fruits/Cherries.png')
strawberry_sprite = pygame.image.load(f'Graphics/Items/Fruits/Strawberry.png')
# Bunny ellenfél
bunny_run_left_sprite = pygame.image.load(f'Graphics/Enemies/Bunny/Run (34x44).png')
bunny_run_right_sprite = pygame.transform.flip(bunny_run_left_sprite, True, False)
bunny_idle_left_sprite = pygame.image.load(f'Graphics/Enemies/Bunny/Idle (34x44).png')
bunny_idle_right_sprite = pygame.transform.flip(bunny_idle_left_sprite, True, False)
# Plant ellenfél
plant_idle_left_sprite = pygame.image.load(f'Graphics/Enemies/Plant/Idle (44x42).png')
plant_idle_right_sprite = pygame.transform.flip(plant_idle_left_sprite, True, False)
plant_attack_left_sprite = pygame.image.load(f'Graphics/Enemies/Plant/Attack (44x42).png')
plant_attack_right_sprite = pygame.transform.flip(plant_attack_left_sprite, True, False)
# Block sprite
brick_sprite = pygame.image.load(f'Graphics/Terrain/brick.png')
steel_sprite = pygame.image.load(f'Graphics/Terrain/steel.png')
gold_sprite = pygame.image.load(f'Graphics/Terrain/gold.png')

# Frame-ek
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
# Bunny Ellenfél
bunny_run_left_frames = frameToList(34, 44, 1, 12, bunny_run_left_sprite)
bunny_run_right_frames = frameToList(34, 44, 1, 12, bunny_run_right_sprite)
bunny_idle_left_frames = frameToList(34, 44, 1, 8, bunny_idle_left_sprite)
bunny_idle_right_frames = frameToList(34, 44, 1, 8, bunny_idle_right_sprite)
# Plant Ellenfél
plane_idle_left_frames = frameToList(44, 42, 1, 11, plant_idle_left_sprite)
plane_idle_right_frames = frameToList(44, 42, 1, 11, plant_idle_right_sprite)
plane_attack_left_frames = frameToList(44, 42, 1, 8, plant_attack_left_sprite)
plane_attack_right_frames = frameToList(44, 42, 1, 8, plant_attack_right_sprite)
# Block
brick_frame = frameToList(40, 40, 1, 1, brick_sprite)
steel_frame = frameToList(40, 40, 1, 1, steel_sprite)
gold_frame = frameToList(40, 40, 1, 1, gold_sprite)
