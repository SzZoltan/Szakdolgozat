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
apple_sprite = pygame.image.load('Graphics/Items/Fruits/Apple.png')
pineapple_sprite = pygame.image.load('Graphics/Items/Fruits/Pineapple.png')
cherry_sprite = pygame.image.load('Graphics/Items/Fruits/Cherries.png')
strawberry_sprite = pygame.image.load('Graphics/Items/Fruits/Strawberry.png')


# A háttér
# len(mc_run_right_frames) a hosszért
def redrawGameWindow():
    win.fill((0, 0, 0))
    for row in range(tiles_down):
        for col in range(tiles_across):
            x_pos = col * level1_bg.get_width()
            y_pos = row * level1_bg.get_height()
            win.blit(level1_bg, (x_pos, y_pos))
    mc.drawPlayer(win)
    apple.drawApple(win)
    pineapple.drawPineapple(win)
    cherry.drawCherry(win)
    strawberry.drawStrawberry(win)
    for fproj in friendlyProjectiles:
        fproj.draw(win, (0, 255, 0))
    pygame.display.update()


def getSprite(sheet, f_width, f_height, x, y):
    # kiszed 1 frame-et a sprite-sheetből
    # f_width: frame széle
    # f_height: frame hossza
    # x: x kezdő koordináta a frame-en
    # y: y kezdő koordináta a frame-en

    frame = pygame.Surface((f_width, f_height), pygame.SRCALPHA)
    frame.blit(sheet, (0, 0), (x*f_width, y*f_height, f_width, f_height))
    return frame


# Kiszedjük a frame-eket egy listába:
def frameToList(width, height, rows, collums, spritesheet):
    frames = []
    for row in range(rows):
        for col in range(collums):
            frame = getSprite(spritesheet, width, height, col, row)
            frames.append(frame)
    return frames


# Frame iteráló
def iterateFrames(self, window, frames, f_count, m_frames):
    if f_count < m_frames:
        window.blit(frames[f_count], (self.x, self.y))
        f_count += 1
    else:
        f_count = 0
        window.blit(frames[f_count], (self.x, self.y))
    return f_count


# Frame-ek

mc_run_right_frames = frameToList(32, 32, 1, 12, mc_running_right_sprite)
mc_run_left_frames = frameToList(32, 32, 1, 12, mc_running_left_sprite)
mc_idle_right_frames = frameToList(32, 32, 1, 11, mc_idle_right_sprite)
mc_idle_left_frames = frameToList(32, 32, 1, 11, mc_idle_left_sprite)
mc_jump_right_frames = frameToList(32, 32, 1, 1, mc_jump_right_sprite)
mc_jump_left_frames = frameToList(32, 32, 1, 1, mc_jump_left_sprite)
apple_frames = frameToList(32, 32, 1, 17, apple_sprite)
pineapple_frames = frameToList(32, 32, 1, 17, pineapple_sprite)
cherry_frames = frameToList(32, 32, 1, 17, cherry_sprite)
strawberry_frames = frameToList(32, 32, 1, 17, strawberry_sprite)


# Terv: Az alapokat kifejelszteni: player, block, projectile,powerup, enemy, block alapú map editor elkészítése és
# miután ez megvan: pályák ,egy főmenü, score system, leaderboard


window_width = 500
window_height = 500
tiles_across = window_width // level1_bg.get_width()+1
tiles_down = window_height // level1_bg.get_height()+1

win = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption('MyGame')


# Player visekedésének definálása
class Player:
    def __init__(self, x, y, width, height):
        self.hp = 1
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.lifes = 3
        self.hitbox = (self.x, self.y, 30, 40)
        self.vel = 5
        self.jumpCount = 10
        self.idleFrameCount = 0
        self.runningFrameCount = 0
        self.canShoot = True
        self.isFalling = False
        self.isJump = False
        self.isIdle = True
        self.isFalling = False
        self.facingLeft = False
        self.facingRight = True
        self.isRunning = False

    # Játékos animációiért felelős függvény
    def drawPlayer(self, window):
        if self.isJump:
            if self.facingRight:
                window.blit(mc_jump_right_frames[0], (self.x, self.y))
            else:
                window.blit(mc_jump_left_frames[0], (self.x, self.y))
        elif self.isRunning:
            if self.facingRight:
                self.runningFrameCount = iterateFrames(self, win, mc_run_right_frames, self.runningFrameCount, 12)
            else:
                self.runningFrameCount = iterateFrames(self, win, mc_run_left_frames, self.runningFrameCount, 12)
        elif self.isIdle:
            if self.facingRight:
                self.idleFrameCount = iterateFrames(self, win, mc_idle_right_frames, self.idleFrameCount, 11)
            else:
                self.idleFrameCount = iterateFrames(self, win, mc_idle_left_frames, self.idleFrameCount, 11)
        self.hitbox = (self.x, self.y, 30, 40)
        pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)


# Projectile-ok alapja öröklődés baráti és ellenséges projectile
class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.dir = direction
        self.hitbox = (self.x - 5, self.y - 5, 10, 10)
        # self.lifespan = 100
        self.vel = 10 * direction
        self.isFriendly = None

    def draw(self, window, color):
        self.hitbox = (self.x - 5, self.y - 5, 10, 10)
        pygame.draw.circle(window, color, (self.x, self.y), 5)
        # pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)


class FriendlyProjectile(Projectile):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.isFriendly = True

    def draw(self, window, color):
        super().draw(window, color)


class EnemyProjectile(Projectile):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.isFriendly = False

    def draw(self, window, color):
        super().draw(window, color)


# Öröklődés különleges block-okból: ? blokk, törhetetlen
class Block:
    pass


# Az összes ellenfélnek az alapja mind öröklődik innen
class Enemy:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.health = 1
        self.canShoot = True
        self.canMove = True
        self.hitbox = (self.x, self.y, 30, 40)

    def drawEnemy(self, window):
        self.hitbox = (self.x, self.y, 30, 40)
        pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)


# A goomba féle ellenfél aki nem csinál semmit csak oda vissza járkál
class BunnyEnemy(Enemy):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.canShoot = False
        self.canMove = True

    def drawEnemy(self, window):
        super().drawEnemy(window)


# Az egyhelyben álló folyamatosan lövő ellenfél
class PlantEnemy(Enemy):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.canShoot = True
        self.canMove = False
        self.shootCooldown = 0

    def drawEnemy(self, window):
        super().drawEnemy(window)


# A PowerUp-oknak alapja ebből öröklődik az összes
class Powerup:
    def __init__(self, x, y, width, height, frames):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.frameCount = 0
        self.frames = frames
        self.hitbox = (self.x+5, self.y+5, 20, 20)

    def drawPowerup(self, window):
        self.hitbox = (self.x+5, self.y+5, 20, 20)
        self.frameCount = iterateFrames(self, window, self.frames, self.frameCount, 17)
        pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)


# Megnöveli 1-el az életerejét a karakternek
class Apple(Powerup):
    def __init__(self, x, y, width, height, frames):
        super().__init__(x, y, width, height, frames)

    def drawApple(self, window):
        super().drawPowerup(window)


# Elérhetővé teszi a lövés képességet a karakterünknek, elveszik miután eltalálják vagy meghal
class Cherry(Powerup):
    def __init__(self, x, y, width, height, frames):
        super().__init__(x, y, width, height, frames)

    def drawCherry(self, window):
        super().drawPowerup(window)


# Megnöveli az életek/újrapróbálkozások számát a Játékosnak
class Pineapple(Powerup):
    def __init__(self, x, y, width, height, frames):
        super().__init__(x, y, width, height, frames)

    def drawPineapple(self, window):
        super().drawPowerup(window)


# Halhatatlanná teszi a karaktert egy ideig és míg halhatatlan át tud menni különböző ellenfeleken
class Strawberry(Powerup):
    def __init__(self, x, y, width, height, frames):
        super().__init__(x, y, width, height, frames)

    def drawStrawberry(self, window):
        super().drawPowerup(window)


mc = Player(0, 255, 32, 32)
apple = Apple(200, 255, 32, 32, apple_frames)
cherry = Cherry(250, 255, 32, 32, cherry_frames)
pineapple = Pineapple(150, 255, 32, 32, pineapple_frames)
strawberry = Strawberry(300, 255, 32, 32, strawberry_frames)
friendlyProjectiles = []
enemyProjectiles = []

# shootLimit azért hogy legyen egy kis delay a lövések között
shootLimit = 0
run = True

# Mainloop
while run:
    clock.tick(20)

    keys = pygame.key.get_pressed()

    for proj in friendlyProjectiles:
        if window_width > proj.x > 0:
            proj.x += proj.vel
            # hit check ide jön majd kell majd projectile hit method
        else:
            friendlyProjectiles.pop(friendlyProjectiles.index(proj))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not any(keys):
        mc.isRunning = False
        mc.isIdle = True

    if keys[pygame.K_LEFT]:
        mc.isIdle = False
        mc.facingLeft = True
        mc.facingRight = False
        mc.isRunning = True
        mc.x -= mc.vel

    if keys[pygame.K_RIGHT]:
        mc.isIdle = False
        mc.facingLeft = False
        mc.facingRight = True
        mc.isRunning = True
        mc.x += mc.vel

    if shootLimit > 0:
        shootLimit += 1
    if shootLimit > 3:
        shootLimit = 0

    if keys[pygame.K_SPACE]:
        mc.isIdle = True
        if mc.canShoot and shootLimit == 0:
            if len(friendlyProjectiles) < 5:
                if mc.facingRight:
                    friendlyProjectiles.append(FriendlyProjectile(round(mc.x + mc.width//2),
                                                                  round(mc.y + mc.height//2), 1))
                else:
                    friendlyProjectiles.append(FriendlyProjectile(round(mc.x + mc.width//2),
                                                                  round(mc.y + mc.height//2), -1))
                shootLimit = 1
    # Ugrás viselkedés: Parabola megoldás
    if not mc.isJump:
        if keys[pygame.K_UP]:
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
