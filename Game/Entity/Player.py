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
        self.isInvincible = False
        self.hitbox = pygame.Rect(self.x, self.y, 30, 40)
        self.vel = 5
        self.jumpCount = 10
        self.idleFrameCount = 0
        self.runningFrameCount = 0
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

    def Move(self, direction):
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

    def Jump(self):
        if self.jumpCount >= -10:
            neg = 1
            if self.jumpCount < 0:
                neg = -1
            self.y -= (self.jumpCount ** 2) * 0.5 * neg
            self.jumpCount -= 1
        else:
            self.isJump = False
            self.jumpCount = 10
