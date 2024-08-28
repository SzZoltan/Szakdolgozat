import pygame
pygame.init()

clock = pygame.time.Clock()


mc_running_right_sprite = pygame.image.load('Graphics/Main Characters/Pink Man/Run (32x32).png')


class Player:
    # Player visekedésének definálása
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.isFalling = False
        self.hitbox = (self.x + 20, self.y, 28, 60)

    def drawPlayer(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height))
        self.hitbox = (self.x - 5, self.y-10, 30, 40)
        pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)


class Projectile:
    # Projectile-ok alapja öröklődés baráti és ellenséges projectile
    pass


class Block:
    # Öröklődés kükönleges block-okból: ? blokk, törhetetlen
    pass


class Enemy:
    # Az összes ellenfélnek az alapja mind öröklődik innen
    pass


class Powerup:
    # A PowerUp-oknak alapja ebből öröklődik az összes
    pass


def redrawGameWindow():
    # Ezt majd javítani a háttérre
    # len(mc_run_right_frames) a hosszért
    win.fill("black")
    mc.drawPlayer(win)
    win.blit(mc_run_right_frames[11], mc_running_right_sprite.get_rect())
    pygame.display.update()


def getSprite(sheet, f_width, f_height, x, y):
    """
    kiszed 1 frame-et a sprite-sheetből
    f_width: frame széle
    f_height: frame hossza
    x: x koordináta a frame-en
    y: y koordináta a frame-en
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

""" 
Terv: Az alapokat kifejelszteni: player, block, projectile,powerup, enemy, block alapú map editor elkészítése és
miután ez megvan: pályák ,egy főmenü, score system, leaderboard 
"""

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption('MyGame')

mc = Player(255, 255, 20, 20)
run = True

# Mainloop
while run:
    clock.tick(20)
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        mc.x -= mc.vel
    if keys[pygame.K_RIGHT]:
        mc.x += mc.vel
    if keys[pygame.K_UP]:
        mc.y -= mc.vel
    if keys[pygame.K_DOWN]:
        mc.y += mc.vel

    redrawGameWindow()

pygame.quit()
