import pygame
from Game.Entity.Projectile import EnemyProjectile
from Game.Game_Graphics.Graphics_Loader import (iterateFrames, bunny_run_left_frames, bunny_run_right_frames,
                                                bunny_idle_left_frames, bunny_idle_right_frames, mc_run_left_frames,
                                                mc_run_right_frames, mc_idle_left_frames, mc_idle_right_frames)


# Enemy viselkedés
# Az összes ellenfélnek az alapja mind öröklődik innen

class Enemy:
    def __init__(self, x: int, y: int, width: int, height: int):
        if not isinstance(x, int) or not isinstance(y, int) or not isinstance(width, int) or not isinstance(height, int):
            raise TypeError('Invalid argument type for Enemy init')
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._vel = 5
        self._health = 1
        self._canShoot = False
        self._canMove = True
        self._idleFrameCount = 0
        self._movingFrameCount = 0
        self._shootingFrameCount = 0
        self._isShooting = False
        self._isAlive = True
        self._canBeJumped = True
        self._isIdle = True
        self._facingLeft = True
        self._facingRight = False
        self._isMoving = False
        self._hitbox = pygame.Rect(self.x, self.y, 30, 40)

    # <editor-fold desc="Property-k és setterek">
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
    def vel(self):
        return self._vel

    @property
    def health(self):
        return self._health

    @property
    def idleFrameCount(self):
        return self._idleFrameCount

    @property
    def movingFrameCount(self):
        return self._movingFrameCount

    @property
    def canShoot(self):
        return self._canShoot

    @property
    def canMove(self):
        return self._canMove

    @property
    def canBeJumped(self):
        return self._canBeJumped

    @property
    def isIdle(self):
        return self._isIdle

    @property
    def shootingFrameCount(self):
        return self._shootingFrameCount

    @property
    def isShooting(self):
        return self._isShooting

    @property
    def isAlive(self):
        return self._isAlive

    @property
    def facingLeft(self):
        return self._facingLeft

    @property
    def facingRight(self):
        return self._facingRight

    @property
    def isMoving(self):
        return self._isMoving

    @property
    def hitbox(self):
        return self._hitbox

    @x.setter
    def x(self, x: int or float):
        if not isinstance(x, (int, float)):
            raise TypeError("x must be an integer of float")
        self._x = x

    @y.setter
    def y(self, y: int or float):
        if not isinstance(y, (int, float)):
            raise TypeError("y must be an integer or float")
        self._y = y

    @width.setter
    def width(self, width: int):
        if not isinstance(width, int):
            raise TypeError("width must be an integer")
        self._width = width

    @height.setter
    def height(self, height: int):
        if not isinstance(height, int):
            raise TypeError("height must be an integer")
        self._height = height

    @health.setter
    def health(self, health: int):
        if not isinstance(health, int):
            raise TypeError("health must be an integer")
        self._health = health

    @idleFrameCount.setter
    def idleFrameCount(self, idleFrameCount: int):
        if not isinstance(idleFrameCount, int):
            raise TypeError("idleFrameCount must be an integer")
        self._idleFrameCount = idleFrameCount

    @movingFrameCount.setter
    def movingFrameCount(self, movingFrameCount: int):
        if not isinstance(movingFrameCount, int):
            raise TypeError("movingFrameCount must be an integer")
        self._movingFrameCount = movingFrameCount

    @shootingFrameCount.setter
    def shootingFrameCount(self, shootingFrameCount: int):
        if not isinstance(shootingFrameCount, int):
            raise TypeError("shootingFrameCount must be an integer")
        self._shootingFrameCount = shootingFrameCount

    @isShooting.setter
    def isShooting(self, isShooting: bool):
        if not isinstance(isShooting, bool):
            raise TypeError("isShooting must be a bool")
        self._isShooting = isShooting

    @isAlive.setter
    def isAlive(self, isAlive: bool):
        if not isinstance(isAlive, bool):
            raise TypeError("isAlive must be a bool")
        self._isAlive = isAlive

    @facingLeft.setter
    def facingLeft(self, facingLeft: bool):
        if not isinstance(facingLeft, bool):
            raise TypeError("facingLeft must be a bool")
        self._facingLeft = facingLeft

    @facingRight.setter
    def facingRight(self, facingRight: bool):
        if not isinstance(facingRight, bool):
            raise TypeError("facingRight must be a bool")
        self._facingRight = facingRight

    @isIdle.setter
    def isIdle(self, isIdle: bool):
        if not isinstance(isIdle, bool):
            raise TypeError("isIdle must be a bool")
        self._isIdle = isIdle

    @isMoving.setter
    def isMoving(self, isMoving: bool):
        if not isinstance(isMoving, bool):
            raise TypeError("isMoving must be a bool")
        self._isMoving = isMoving

    @hitbox.setter
    def hitbox(self, hitbox: pygame.Rect):
        if not isinstance(hitbox, pygame.Rect):
            raise TypeError("hitbox must be a pygame.Rect object")
        self._hitbox = hitbox

    @canShoot.setter
    def canShoot(self, canShoot: bool):
        if not isinstance(canShoot, bool):
            raise TypeError("canShoot must be a bool")
        self._canShoot = canShoot

    @canMove.setter
    def canMove(self, canMove: bool):
        if not isinstance(canMove, bool):
            raise TypeError("canMove must be a bool")
        self._canMove = canMove

    # </editor-fold>

    # Ez lesz a default Enemy animáció, a Főszereplő, de csak akkor ha nincs implementálva sajátja,
    # soha nem lesz hívva ha minden jól alakul
    def drawEnemy(self, window: pygame.Surface):
        if isinstance(window, pygame.Surface):
            if self.isAlive:
                if self.isMoving:
                    if self.facingRight:
                        self.movingFrameCount = iterateFrames(self, window, mc_run_right_frames, self.movingFrameCount,
                                                              12)
                    else:
                        self.movingFrameCount = iterateFrames(self, window, mc_run_left_frames, self.movingFrameCount,
                                                              12)
                elif self.isIdle:
                    if self.facingRight:
                        self.idleFrameCount = iterateFrames(self, window, mc_idle_right_frames, self.idleFrameCount, 11)
                    else:
                        self.idleFrameCount = iterateFrames(self, window, mc_idle_left_frames, self.idleFrameCount, 11)
                self.hitbox = pygame.Rect(self.x, self.y, 30, 40)
                pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)
        else:
            raise TypeError('Invalid window argument for drawEnemy')

    def hit(self):
        self.health = self.health - 1
        if self.health == 0:
            self.isAlive = False

    def shoot(self, direction: int):
        if direction == 1 or direction == -1:
            if self.canShoot:
                EnemyProjectile(round(self.x + self.width // 2), round(self.y + self.height // 2), direction)
        else:
            raise ValueError('Invalid direction argument for Enemy shoot')

    def move(self, direction: str):
        if direction == 'left':
            self.isIdle = False
            self.facingLeft = True
            self.facingRight = False
            self.isMoving = True
            self.x -= self.vel
        elif direction == 'right':
            self.isIdle = False
            self.facingLeft = False
            self.facingRight = True
            self.isMoving = True
            self.x += self.vel
        else:
            raise ValueError('Invalid direction argument for Enemy move')


# A goomba féle ellenfél aki nem csinál semmit csak oda vissza járkál
class BunnyEnemy(Enemy):
    def __init__(self, x: int or float, y: int or float, width: int, height: int):
        super().__init__(x, y, width, height)
        self.canShoot = False
        self.canMove = True

    # Kell egy megoldás arra, hogy ezt egységesíteni lehessen
    def drawEnemy(self, window: pygame.Surface):
        if isinstance(window, pygame.Surface):
            if self.isAlive:
                if self.isMoving:
                    if self.facingRight:
                        self.movingFrameCount = iterateFrames(self, window, bunny_run_right_frames,
                                                              self.movingFrameCount, 12)
                    else:
                        self.movingFrameCount = iterateFrames(self, window, bunny_run_left_frames,
                                                              self.movingFrameCount, 12)
                elif self.isIdle:
                    if self.facingRight:
                        self.idleFrameCount = iterateFrames(self, window, bunny_idle_right_frames,
                                                            self.idleFrameCount, 8)
                    else:
                        self.idleFrameCount = iterateFrames(self, window, bunny_idle_left_frames,
                                                            self.idleFrameCount, 8)
                self.hitbox = pygame.Rect(self.x, self.y, 30, 40)
                pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)
        else:
            raise TypeError('Invalid window argument Bunny drawEnemy')

    def move(self, direction: str):
        super().move(direction)

    def hit(self):
        super().hit()
        print("Enemy hit")


# Az egyhelyben álló folyamatosan lövő ellenfél
class PlantEnemy(Enemy):
    def __init__(self, x: int or float, y: int or float, width: int, height: int):
        super().__init__(x, y, width, height)
        self.canShoot = True
        self.canMove = False
        self.shootCooldown = 0

    def drawEnemy(self, window: pygame.Surface):
        super().drawEnemy(window)

    def hit(self):
        super().hit()

    # Hogy garantálom, hogy az animáció lejátszódjon mielőtt lő és utánna viszamegy idle-be?
    # self.shootingFrameCount = iterateFrames(self, window, plane_attack_left_frames, self.shootingFrameCount, 8)
    def shoot(self, direction: int):
        if self.shootCooldown == 0:
            self.isShooting = True
            super().shoot(direction)
        self.shootCooldown = 90
