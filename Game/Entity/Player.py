from Game.Entity.Projectile import FriendlyProjectile
from Game.Game_Graphics.Graphics_Loader import *


# Player visekedésének definálása
class Player:
    def __init__(self, x, y, width, height):
        self.hp = 1
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.lives = 3
        self.hitbox = pygame.Rect(self.x, self.y, 30, 40)
        self.vel = 5
        self.jumpCount = 10
        self.idleFrameCount = 0
        self.runningFrameCount = 0
        self.iFrames = 0
        self.isInvincible = False
        self.canShoot = False
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
                self.runningFrameCount = iterateFrames(self, window, mc_run_right_frames, self.runningFrameCount, 12)
            else:
                self.runningFrameCount = iterateFrames(self, window, mc_run_left_frames, self.runningFrameCount, 12)
        elif self.isIdle:
            if self.facingRight:
                self.idleFrameCount = iterateFrames(self, window, mc_idle_right_frames, self.idleFrameCount, 11)
            else:
                self.idleFrameCount = iterateFrames(self, window, mc_idle_left_frames, self.idleFrameCount, 11)
        self.hitbox = pygame.Rect(self.x, self.y, 30, 40)
        pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)

    def move(self, direction):
        if direction == 'left':
            self.isIdle = False
            self.facingLeft = True
            self.facingRight = False
            self.isRunning = True
            self.x -= self.vel
        if direction == 'right':
            self.isIdle = False
            self.facingLeft = False
            self.facingRight = True
            self.isRunning = True
            self.x += self.vel

    def jump(self):
        if self.jumpCount >= -10:
            neg = 0.7
            if self.jumpCount < 0:
                neg = -0.7
            self.y -= (self.jumpCount ** 2) * 0.5 * neg
            self.jumpCount -= 1
        else:
            self.isJump = False
            self.jumpCount = 10

    def hit(self):
        if not self.isInvincible:
            self.hp = self.hp - 1
            print("Player hit")
            self.iFrames = 60

    def shoot(self, direction):
        return FriendlyProjectile(round(self.x + self.width // 2), round(self.y + self.height // 2), direction)
