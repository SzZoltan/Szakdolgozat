import pygame
from Game.Entity.Projectile import FriendlyProjectile
from Game.Game_Graphics.Graphics_Loader import (iterateFrames, mc_jump_left_frames, mc_jump_right_frames,
                                                mc_run_right_frames, mc_run_left_frames, mc_idle_left_frames,
                                                mc_idle_right_frames)


# Player visekedésének definálása
class Player:
    def __init__(self, x: int or float, y: int or float):
        self._hp = 1
        self._x = x
        self._y = y
        self._width = 32
        self._height = 32
        self._lives = 3
        self._hitbox = pygame.Rect(self.x, self.y, 30, 35)
        self._vel = 5
        self._jumpCount = 10
        self._idleFrameCount = 0
        self._runningFrameCount = 0
        self._iFrames = 0
        self._isAlive = True
        self._isInvincible = False
        self._canShoot = False
        self._isFalling = False
        self._isJump = False
        self._isIdle = True
        self._facingLeft = False
        self._facingRight = True
        self._isRunning = False

    # <editor-fold desc="Property-k és setterek">
    @property
    def hp(self):
        return self._hp

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def lives(self):
        return self._lives

    @property
    def hitbox(self):
        return self._hitbox

    @property
    def vel(self):
        return self._vel

    @property
    def jumpCount(self):
        return self._jumpCount

    @property
    def idleFrameCount(self):
        return self._idleFrameCount

    @property
    def runningFrameCount(self):
        return self._runningFrameCount

    @property
    def iFrames(self):
        return self._iFrames

    @property
    def isInvincible(self):
        return self._isInvincible

    @property
    def canShoot(self):
        return self._canShoot

    @property
    def isFalling(self):
        return self._isFalling

    @property
    def isJump(self):
        return self._isJump

    @property
    def isIdle(self):
        return self._isIdle

    @property
    def facingLeft(self):
        return self._facingLeft

    @property
    def facingRight(self):
        return self._facingRight

    @property
    def isRunning(self):
        return self._isRunning
    @property
    def isAlive(self):
        return self._isAlive

    # Setters
    @hp.setter
    def hp(self, value):
        if not isinstance(value, int):
            raise TypeError("hp attribute must be an integer.")
        if value < 0:
            self._hp = 0
        else:
            self._hp = value

    @x.setter
    def x(self, value: int or float):
        if not isinstance(value, (int, float)):
            raise TypeError("X coordinate must be an integer or float.")
        self._x = value

    @y.setter
    def y(self, value: int or float):
        if not isinstance(value, (int, float)):
            raise TypeError("Y coordinate must be an integer or float.")
        self._y = value

    @width.setter
    def width(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Width attribute must be an integer.")
        self._width = value

    @height.setter
    def height(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Height attribute must be an integer.")
        self._height = value

    @lives.setter
    def lives(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Lives attribute must be an integer.")
        self._lives = value

    @hitbox.setter
    def hitbox(self, value: pygame.Rect):
        if not isinstance(value, pygame.Rect):
            raise TypeError("Hitbox attribute must be an pygame.Rect.")
        self._hitbox = value

    @jumpCount.setter
    def jumpCount(self, value: int or float):
        if not isinstance(value, (int, float)):
            raise TypeError("Jump count attribute must be an integer or float.")
        self._jumpCount = value

    @idleFrameCount.setter
    def idleFrameCount(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Idle frame count attribute must be an integer.")
        self._idleFrameCount = value

    @runningFrameCount.setter
    def runningFrameCount(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Running frame count attribute must be an integer.")
        self._runningFrameCount = value

    @iFrames.setter
    def iFrames(self, value: int):
        if not isinstance(value, int):
            raise TypeError("iFrames attribute must be an integer.")
        self._iFrames = value

    @isInvincible.setter
    def isInvincible(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("isInvincible attribute must be an boolean.")
        self._isInvincible = value

    @canShoot.setter
    def canShoot(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("canShoot attribute must be an boolean.")
        self._canShoot = value

    @isFalling.setter
    def isFalling(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("isFalling attribute must be an boolean.")
        if not self.isJump:
            self._isFalling = value

    @isJump.setter
    def isJump(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("isJump attribute must be an boolean.")
        self._isJump = value

    @isIdle.setter
    def isIdle(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("isIdle attribute must be an boolean.")
        self._isIdle = value

    @facingLeft.setter
    def facingLeft(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("facingLeft attribute must be an boolean.")
        self._facingLeft = value

    @facingRight.setter
    def facingRight(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("facingRight attribute must be an boolean.")
        self._facingRight = value

    @isRunning.setter
    def isRunning(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("isRunning attribute must be an boolean.")
        self._isRunning = value

    @isAlive.setter
    def isAlive(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("isAlive attribute must be an boolean.")
        self._isAlive = value
    # </editor-fold>

    # Játékos animációiért felelős függvény
    def drawPlayer(self, window: pygame.Surface):
        if not isinstance(window, pygame.Surface):
            raise TypeError('Invalid window argument')
        if self.iFrames % 2 == 0:
            if self.isJump:
                if self.facingRight:
                    window.blit(mc_jump_right_frames[0], (self.x, self.y))
                else:
                    window.blit(mc_jump_left_frames[0], (self.x, self.y))
            elif self.isRunning:
                if self.facingRight:
                    self.runningFrameCount = iterateFrames(self, window, mc_run_right_frames, self.runningFrameCount,
                                                           12)
                else:
                    self.runningFrameCount = iterateFrames(self, window, mc_run_left_frames, self.runningFrameCount, 12)
            elif self.isIdle:
                if self.facingRight:
                    self.idleFrameCount = iterateFrames(self, window, mc_idle_right_frames, self.idleFrameCount, 11)
                else:
                    self.idleFrameCount = iterateFrames(self, window, mc_idle_left_frames, self.idleFrameCount, 11)
        self.hitbox = pygame.Rect(self.x, self.y, 30, 35)
        pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)

    def move(self, direction: str):
        if direction == 'left':
            self.isIdle = False
            self.facingLeft = True
            self.facingRight = False
            self.isRunning = True
            self.x -= self.vel
        elif direction == 'right':
            self.isIdle = False
            self.facingLeft = False
            self.facingRight = True
            self.isRunning = True
            self.x += self.vel
        else:
            raise ValueError('Invalid direction for Player move')

    def jump(self):
        if not self.isFalling and self.isJump:
            if self.jumpCount >= 0:
                self.y -= int((self.jumpCount ** 2) * 0.5 * 0.7)
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.isFalling = True
                self.jumpCount = 10

    def bounce(self):
        if self.isFalling:
            self.jumpCount = 7
            self.isFalling = False
            self.isJump = True
            self.jump()

    def interruptJump(self):
        if self.isJump:
            self.isJump = False
            self.isFalling = True
            self.jumpCount = 10

    def hit(self):
        if not self.isInvincible and self.iFrames == 0:
            self.hp = self.hp - 1
            print("Player hit")
            self.iFrames = 30

    def shoot(self, direction: int):
        if direction == 1 or direction == -1:
            if self.canShoot:
                return FriendlyProjectile(round(self.x + self.width // 2), round(self.y + self.height // 2), direction)
        else:
            raise ValueError('Invalid direction for Player shoot')

    def iFrame(self):
        if self.iFrames > 0:
            self.iFrames -= 1

            #print(self.iFrames)
