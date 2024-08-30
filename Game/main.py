import pygame
pygame.init()

# Az animációk 20 FPS-re vannak megcsinálva
clock = pygame.time.Clock()


mc_running_right_sprite = pygame.image.load('Graphics/Main Characters/Pink Man/Run (32x32).png')
mc_running_left_sprite = pygame.transform.flip(mc_running_right_sprite, True, False)
mc_idle_right_sprite = pygame.image.load('Graphics/Main Characters/Pink Man/Idle (32x32).png')
mc_idle_left_sprite = pygame.transform.flip(mc_idle_right_sprite, True, False)
mc_jump_right_sprite = pygame.image.load('Graphics/Main Characters/Pink Man/Jump (32x32).png')
mc_jump_left_sprite = pygame.transform.flip(mc_jump_right_sprite, True, False)
level1_bg = pygame.image.load('Graphics/Background/Brown.png')


def redrawGameWindow():
    # A háttér
    # len(mc_run_right_frames) a hosszért
    win.fill((0, 0, 0))
    for row in range(tiles_down):
        for col in range(tiles_across):
            x_pos = col * level1_bg.get_width()
            y_pos = row * level1_bg.get_height()
            win.blit(level1_bg, (x_pos, y_pos))
    mc.drawPlayer(win)
    pygame.display.update()


def getSprite(sheet, f_width, f_height, x, y):
    """
    kiszed 1 frame-et a sprite-sheetből
    f_width: frame széle
    f_height: frame hossza
    x: x kezdő koordináta a frame-en
    y: y kezdő koordináta a frame-en
    """
    frame = pygame.Surface((f_width, f_height), pygame.SRCALPHA)
    frame.blit(sheet, (0, 0), (x*f_width, y*f_height, f_width, f_height))
    return frame


def frameToList(width, height, rows, collums, spritesheet):
    # Kiszedjük a frame-eket egy listába:
    frames = []
    for row in range(rows):
        for col in range(collums):
            frame = getSprite(spritesheet, width, height, col, row)
            frames.append(frame)
    return frames


# Frame-ek

mc_run_right_frames = frameToList(32, 32, 1, 12, mc_running_right_sprite)
mc_run_left_frames = frameToList(32, 32, 1, 12, mc_running_left_sprite)
mc_idle_right_frames = frameToList(32, 32, 1, 11, mc_idle_right_sprite)
mc_idle_left_frames = frameToList(32, 32, 1, 11, mc_idle_left_sprite)
mc_jump_right_frames = frameToList(32, 32, 1, 1, mc_jump_right_sprite)
mc_jump_left_frames = frameToList(32, 32, 1, 1, mc_jump_left_sprite)

""" 
Terv: Az alapokat kifejelszteni: player, block, projectile,powerup, enemy, block alapú map editor elkészítése és
miután ez megvan: pályák ,egy főmenü, score system, leaderboard 
"""


window_width = 500
window_height = 500
tiles_across = window_width // level1_bg.get_width()+1
tiles_down = window_height // level1_bg.get_height()+1

win = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption('MyGame')


class Player:
    # Player visekedésének definálása
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, 30, 40)
        self.vel = 5
        self.jumpCount = 10
        self.idleFrameCount = 0
        self.runningFrameCount = 0
        self.isFalling = False
        self.isJump = False
        self.isIdle = True
        self.isFalling = False
        self.facingLeft = False
        self.facingRight = True
        self.isRunning = False

    def drawPlayer(self, window):
        # Játékos animációiért felelős
        if self.isJump:
            if self.facingRight:
                window.blit(mc_jump_right_frames[0], (self.x, self.y))
            else:
                window.blit(mc_jump_left_frames[0], (self.x, self.y))
        elif self.isRunning:
            if self.facingRight:
                if self.runningFrameCount < 12:
                    window.blit(mc_run_right_frames[self.runningFrameCount], (self.x, self.y))
                    self.runningFrameCount += 1
                else:
                    self.runningFrameCount = 0
                    window.blit(mc_run_right_frames[self.runningFrameCount], (self.x, self.y))
            else:
                if self.runningFrameCount < 12:
                    window.blit(mc_run_left_frames[self.runningFrameCount], (self.x, self.y))
                    self.runningFrameCount += 1
                else:
                    self.runningFrameCount = 0
                    window.blit(mc_run_left_frames[self.runningFrameCount], (self.x, self.y))
        elif self.isIdle:
            if self.facingRight:
                if self.idleFrameCount < 11:
                    window.blit(mc_idle_right_frames[self.idleFrameCount], (self.x, self.y))
                    self.idleFrameCount += 1
                else:
                    self.idleFrameCount = 0
                    window.blit(mc_idle_right_frames[self.idleFrameCount], (self.x, self.y))
            elif self.facingLeft:
                if self.idleFrameCount < 11:
                    window.blit(mc_idle_left_frames[self.idleFrameCount], (self.x, self.y))
                    self.idleFrameCount += 1
                else:
                    self.idleFrameCount = 0
                    window.blit(mc_idle_left_frames[self.idleFrameCount], (self.x, self.y))
        self.hitbox = (self.x, self.y, 30, 40)
        pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)


class Projectile:
    # Projectile-ok alapja öröklődés baráti és ellenséges projectile
    pass


class Block:
    # Öröklődés különleges block-okból: ? blokk, törhetetlen
    pass


class Enemy:
    # Az összes ellenfélnek az alapja mind öröklődik innen
    pass


class Powerup:
    # A PowerUp-oknak alapja ebből öröklődik az összes
    pass


mc = Player(255, 255, 20, 20)
run = True

# Mainloop
while run:
    clock.tick(20)

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not any(keys):
        mc.isRunning = False
        mc.isIdle = True
    else:
        mc.isIdle = False

    if keys[pygame.K_LEFT]:
        mc.facingLeft = True
        mc.facingRight = False
        mc.isRunning = True
        mc.x -= mc.vel
    if keys[pygame.K_RIGHT]:
        mc.facingLeft = False
        mc.facingRight = True
        mc.isRunning = True
        mc.x += mc.vel

    # Ugrás viselkedés: Parabola megoldás
    # Később a fel nyílra átteni az ugrást és a le nyílt törölni
    if not mc.isJump:
        if keys[pygame.K_UP]:
            mc.y -= mc.vel
        if keys[pygame.K_DOWN]:
            mc.y += mc.vel
        if keys[pygame.K_SPACE]:
            mc.isJump = True
    else:
        if mc.jumpCount >= -10:
            neg = 1
            if mc.jumpCount < 0:
                neg = -1
            mc.y -= (mc.jumpCount ** 2) * 0.5 * neg
            mc.jumpCount -= 1
        else:
            mc.isJump = False
            mc.jumpCount = 10

    redrawGameWindow()

pygame.quit()
