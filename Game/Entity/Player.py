from Game.Entity.Projectile import FriendlyProjectile
from Game.Game_Graphics.Graphics_Loader import *


# Player visekedésének definálása
class Player:
    def __init__(self, x: int, y: int, width: int, height: int):
        self._hp = 1
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._lives = 3
        self._hitbox = pygame.Rect(self.x, self.y, 30, 40)
        self._vel = 5
        self._jumpCount = 10
        self._idleFrameCount = 0
        self._runningFrameCount = 0
        self._iFrames = 0
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

    # Setters
    @hp.setter
    def hp(self, value):
        if not isinstance(value, int):
            raise ValueError("hp attribute must be an integer.")
        self._hp = value

    @x.setter
    def x(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise ValueError("X coordinate must be an integer or float.")
        self._x = value

    @y.setter
    def y(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise ValueError("Y coordinate must be an integer or float.")
        self._y = value

    @width.setter
    def width(self, value):
        if not isinstance(value, int):
            raise ValueError("Width attribute must be an integer.")
        self._width = value

    @height.setter
    def height(self, value):
        if not isinstance(value, int):
            raise ValueError("Height attribute must be an integer.")
        self._height = value

    @lives.setter
    def lives(self, value):
        if not isinstance(value, int):
            raise ValueError("Lives attribute must be an integer.")
        self._lives = value

    @hitbox.setter
    def hitbox(self, value):
        if not isinstance(value, pygame.Rect):
            raise ValueError("Hitbox attribute must be an pygame.Rect.")
        self._hitbox = value

    @jumpCount.setter
    def jumpCount(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise ValueError("Jump count attribute must be an integer or float.")
        self._jumpCount = value

    @idleFrameCount.setter
    def idleFrameCount(self, value):
        if not isinstance(value, int):
            raise ValueError("Idle frame count attribute must be an integer.")
        self._idleFrameCount = value

    @runningFrameCount.setter
    def runningFrameCount(self, value):
        if not isinstance(value, int):
            raise ValueError("Running frame count attribute must be an integer.")
        self._runningFrameCount = value

    @iFrames.setter
    def iFrames(self, value):
        if not isinstance(value, int):
            raise ValueError("iFrames attribute must be an integer.")
        self._iFrames = value

    @isInvincible.setter
    def isInvincible(self, value):
        if not isinstance(value, bool):
            raise ValueError("isInvincible attribute must be an boolean.")
        self._isInvincible = value

    @canShoot.setter
    def canShoot(self, value):
        if not isinstance(value, bool):
            raise ValueError("canShoot attribute must be an boolean.")
        self._canShoot = value

    @isFalling.setter
    def isFalling(self, value):
        if not isinstance(value, bool):
            raise ValueError("isFalling attribute must be an boolean.")
        self._isFalling = value

    @isJump.setter
    def isJump(self, value):
        if not isinstance(value, bool):
            raise ValueError("isJump attribute must be an boolean.")
        self._isJump = value

    @isIdle.setter
    def isIdle(self, value):
        if not isinstance(value, bool):
            raise ValueError("isIdle attribute must be an boolean.")
        self._isIdle = value

    @facingLeft.setter
    def facingLeft(self, value):
        if not isinstance(value, bool):
            raise ValueError("facingLeft attribute must be an boolean.")
        self._facingLeft = value

    @facingRight.setter
    def facingRight(self, value):
        if not isinstance(value, bool):
            raise ValueError("facingRight attribute must be an boolean.")
        self._facingRight = value

    @isRunning.setter
    def isRunning(self, value):
        if not isinstance(value, bool):
            raise ValueError("isRunning attribute must be an boolean.")
        self._isRunning = value

    # </editor-fold>

    # Játékos animációiért felelős függvény
    def drawPlayer(self, window: pygame.Surface):
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
        self.hitbox = pygame.Rect(self.x, self.y, 30, 40)
        pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)

    def move(self, direction):
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
        if direction == 1 or direction == -1:
            return FriendlyProjectile(round(self.x + self.width // 2), round(self.y + self.height // 2), direction)
        else:
            raise ValueError('Invalid direction for Player shoot')
