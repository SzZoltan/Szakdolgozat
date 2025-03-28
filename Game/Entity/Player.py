import pygame
from Game.Entity.Projectile import FriendlyProjectile
from Game.Game_Graphics.Graphics_Loader import (iterateFrames, mc_jump_left_frames, mc_jump_right_frames,
                                                mc_run_right_frames, mc_run_left_frames, mc_idle_left_frames,
                                                mc_idle_right_frames)


# Player visekedésének definálása
class Player:
    """
    A játékos objektum
    """
    def __init__(self, x: int or float, y: int or float):
        """
        A Player objektumot innicializálja
        :param x: int vagy float, x koordináta
        :param y: int vagy float, y koordináta
        """
        self._hp = 1
        self._x = x
        self._y = y
        self._width = 32
        self._height = 32
        self._lives = 3
        self._hitbox = pygame.Rect(self.x, self.y, 30, 35)
        self._vel = 7
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
        """
        Visszadja a Player életerejét
        :return: int, életerő
        """
        return self._hp

    @property
    def x(self):
        """
        Visszadja a Player x koordinátáját
        :return: int vagy float, x koordináta
        """
        return self._x

    @property
    def y(self):
        """
        Visszadja a Player y koordinátáját
        :return: int vagy float, y koordináta
        """
        return self._y

    @property
    def width(self):
        """
        Visszadja a Player szélességét
        :return: int, szélesség
        """
        return self._width

    @property
    def height(self):
        """
        Visszadja a Player magasságát
        :return: int, magasság
        """
        return self._height

    @property
    def lives(self):
        """
        Visszadja a Player életeinek számát
        :return: int, életek száma
        """
        return self._lives

    @property
    def hitbox(self):
        """
        Visszadja a Player hitboxát
        :return: pygame.Rect, a hitbox
        """
        return self._hitbox

    @property
    def vel(self):
        """
        Visszadja a Player sebességét
        :return: int, sebesség
        """
        return self._vel

    @property
    def jumpCount(self):
        """
        Visszadja a Player ugrásszámlálóját, szükésges az ugrás metódushoz
        :return: int, ugrásszámláló
        """
        return self._jumpCount

    @property
    def idleFrameCount(self):
        """
        Visszadja a Player tétlen képkockáinak mutatóját
        :return: int, mutató
        """
        return self._idleFrameCount

    @property
    def runningFrameCount(self):
        """
        Visszadja a Player futó képkockáinak mutatóját
        :return: int, mutató
        """
        return self._runningFrameCount

    @property
    def iFrames(self):
        """
        Visszadja a Player iFrame-einek jelenlegi számát
        :return: int
        """
        return self._iFrames

    @property
    def isInvincible(self):
        """
        Visszadja a Player jelenleg sebezhetetlen-e
        :return: bool, True ha sebezhetetlen, False ha nem
        """
        return self._isInvincible

    @property
    def canShoot(self):
        """
        Visszadja a Player jelenleg tud-e lőni
        :return: bool, True ha tud lőni, False ha nem
        """
        return self._canShoot

    @property
    def isFalling(self):
        """
        Visszadja a Player jelenleg esik le
        :return: bool, True ha esik, False ha nem
        """
        return self._isFalling

    @property
    def isJump(self):
        """
        Visszadja a Player jelenleg ugrik-e
        :return: bool, True ha ugrik, False ha nem
        """
        return self._isJump

    @property
    def isIdle(self):
        """
        Visszadja a Player jelenleg tétlen-e
        :return: bool, True ha tétlen, False ha nem
        """
        return self._isIdle

    @property
    def facingLeft(self):
        """
        Visszadja a Player jelenleg balra néz-e
        :return: bool, True ha balra néz, False ha nem
        """
        return self._facingLeft

    @property
    def facingRight(self):
        """
        Visszadja a Player jelenleg jobbra néz-e
        :return: bool, True ha jobbra néz, False ha nem
        """
        return self._facingRight

    @property
    def isRunning(self):
        """
        Visszadja a Player jelenleg fut-e
        :return: bool, True ha fut, False ha nem
        """
        return self._isRunning

    @property
    def isAlive(self):
        """
        Visszadja a Player jelenleg él-e
        :return: bool, True ha él, False ha nem
        """
        return self._isAlive

    # Setters
    @hp.setter
    def hp(self, value: int):
        """
        Beállítja a Player-nek az életerejét, 2-nél nem lehet nagyobb értéket adni neki
        :param value: int, az új életerő
        """
        if not isinstance(value, int):
            raise TypeError("hp attribute must be an integer.")
        if value < 0:
            self._hp = 0
        elif value > 2:
            self._hp = 2
        else:
            self._hp = value

    @x.setter
    def x(self, value: int or float):
        """
        Beállítja a Player-nek az x koordinátáját
        :param value: int vagy float, az új x koordináta
        """
        if not isinstance(value, (int, float)):
            raise TypeError("X coordinate must be an integer or float.")
        self._x = value

    @y.setter
    def y(self, value: int or float):
        """
        Beállítja a Player-nek az y koordinátáját
        :param value: int vagy float, az új y koordináta
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Y coordinate must be an integer or float.")
        self._y = value

    @width.setter
    def width(self, value: int):
        """
        Beállítja a Player-nek a szélességét
        :param value: int, az új szélesség
        """
        if not isinstance(value, int):
            raise TypeError("Width attribute must be an integer.")
        self._width = value

    @height.setter
    def height(self, value: int):
        """
        Beállítja a Player-nek a magasságát
        :param value: int, az új magasságát
        """
        if not isinstance(value, int):
            raise TypeError("Height attribute must be an integer.")
        self._height = value

    @lives.setter
    def lives(self, value: int):
        """
        Beállítja a Player életeinek számát
        :param value: int, az új életek száma
        """
        if not isinstance(value, int):
            raise TypeError("Lives attribute must be an integer.")
        self._lives = value

    @hitbox.setter
    def hitbox(self, value: pygame.Rect):
        """
        Beállítja a Player-nek a hitboxát
        :param value: pygame.Rect, az új hitbox
        """
        if not isinstance(value, pygame.Rect):
            raise TypeError("Hitbox attribute must be an pygame.Rect.")
        self._hitbox = value

    @jumpCount.setter
    def jumpCount(self, value: int or float):
        """
        Beállítja a Player-nek az ugrásszámlálóját
        :param value: int vagy flaot, az új számláló
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Jump count attribute must be an integer or float.")
        self._jumpCount = value

    @idleFrameCount.setter
    def idleFrameCount(self, value: int):
        """
        Beállítja a Player-nek a tétlen képkocka mutatóját
        :param value: int, az új mutató
        """
        if not isinstance(value, int):
            raise TypeError("Idle frame count attribute must be an integer.")
        self._idleFrameCount = value

    @runningFrameCount.setter
    def runningFrameCount(self, value: int):
        """
        Beállítja a Player-nek a futó képkocka mutatóját
        :param value: int, az új mutató
        """
        if not isinstance(value, int):
            raise TypeError("Running frame count attribute must be an integer.")
        self._runningFrameCount = value

    @iFrames.setter
    def iFrames(self, value: int):
        """
        Beállítja a Player-nek az iFrame változót
        :param value: int, az új változó
        """
        if not isinstance(value, int):
            raise TypeError("iFrames attribute must be an integer.")
        self._iFrames = value

    @isInvincible.setter
    def isInvincible(self, value: bool):
        """
        Beállítja hogy a Player jelenleg sebezhetetlen-e
        :param value: bool, True ha sebezhetetlen, False ha nem
        """
        if not isinstance(value, bool):
            raise TypeError("isInvincible attribute must be an boolean.")
        self._isInvincible = value

    @canShoot.setter
    def canShoot(self, value: bool):
        """
        Beállítja hogy a Player jelenleg lőni tud-e
        :param value: bool, True ha tud lőni, False ha nem
        """
        if not isinstance(value, bool):
            raise TypeError("canShoot attribute must be an boolean.")
        self._canShoot = value

    @isFalling.setter
    def isFalling(self, value: bool):
        """
        Beállítja hogy a Player jelenleg esik-e
        :param value: bool, True ha esik, False ha nem
        """
        if not isinstance(value, bool):
            raise TypeError("isFalling attribute must be an boolean.")
        if not self.isJump:
            self._isFalling = value

    @isJump.setter
    def isJump(self, value: bool):
        """
        Beállítja hogy a Player jelenleg ugrik-e
        :param value: bool, True ha ugrik, False ha nem
        """
        if not isinstance(value, bool):
            raise TypeError("isJump attribute must be an boolean.")
        self._isJump = value

    @isIdle.setter
    def isIdle(self, value: bool):
        """
        Beállítja hogy a Player jelenleg tétlen-e
        :param value: bool, True ha tétlen, False ha nem
        """
        if not isinstance(value, bool):
            raise TypeError("isIdle attribute must be an boolean.")
        self._isIdle = value

    @facingLeft.setter
    def facingLeft(self, value: bool):
        """
        Beállítja hogy a Player balra néz-e
        :param value: bool, True ha balra néz, False ha nem
        """
        if not isinstance(value, bool):
            raise TypeError("facingLeft attribute must be an boolean.")
        self._facingLeft = value

    @facingRight.setter
    def facingRight(self, value: bool):
        """
        Beállítja hogy a Player jobbra néz-e
        :param value: bool, True ha jobbra néz, False ha nem
        """
        if not isinstance(value, bool):
            raise TypeError("facingRight attribute must be an boolean.")
        self._facingRight = value

    @isRunning.setter
    def isRunning(self, value: bool):
        """
        Beállítja hogy a Player jelenleg fut-e
        :param value: bool, True ha fut, False ha nem
        """
        if not isinstance(value, bool):
            raise TypeError("isRunning attribute must be an boolean.")
        self._isRunning = value

    @isAlive.setter
    def isAlive(self, value: bool):
        """
        Beállítja hogy a Player jelenleg él-e
        :param value: bool, True ha él, False ha nem
        """
        if not isinstance(value, bool):
            raise TypeError("isAlive attribute must be an boolean.")
        self._isAlive = value
    # </editor-fold>

    def drawPlayer(self, window: pygame.Surface):
        """
        Felrajzólja a játékost a képernyőre, minden különböző állapotában
        :param window: pygame.Surface, a felület amire felrajzolja
        """
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

    def move(self, direction: str):
        """
        A játékos mozgását valósítsa meg
        :param direction: string, 'left' ha balra mozdul, 'right', ha jobbra
        """
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
        """
        Megvalósítsa a játékos ugrás viselkedését, félparabola módon ugrik fel és amikor már nem ugrik akkor
         gravitáció átveszi
        """
        if not self.isFalling and self.isJump:
            if self.jumpCount >= 0:
                self.y -= int((self.jumpCount ** 2) * 0.5 * 0.7)
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.isFalling = True
                self.jumpCount = 10

    def bounce(self):
        """
        Ha a Játékos esik és ráugrik egy ellenfél fejére akkor egy kisebb ugrást fog csinálni
        """
        if self.isFalling:
            self.jumpCount = 7
            self.isFalling = False
            self.isJump = True
            self.jump()

    def interruptJump(self):
        """
        Megszakítja a Játékos ugrását, ha jelenleg ugrik csak akkor működik
        """
        if self.isJump:
            self.isJump = False
            self.isFalling = True
            self.jumpCount = 10

    def hit(self):
        """
        Ha a Játékos nem sebezhetetlen és nincsenek iFrame-jei akkor levon 1-et az életerejéből
        """
        if not self.isInvincible and self.iFrames == 0:
            if self.canShoot:
                self.canShoot = False
            else:
                self.hp = self.hp - 1
            self.iFrames = 30

    def kill(self):
        """
        Azonnal 0-ra állítja a Játékos életerejét, ha leesik akkor használatos a hit() helyett
        """
        self.hp = 0

    def shoot(self, direction: int):
        """
        A Játékos lő egyett ha megvan neki a PowerUp
        :param direction: 0 balra vagy 1 jobbra lőjje a lövedéket
        :return: FriendlyProjectile, a lövedék
        """
        if direction == 1 or direction == -1:
            if self.canShoot:
                return FriendlyProjectile(round(self.x + self.width // 2), round(self.y + self.height // 2), direction)
        else:
            raise ValueError('Invalid direction for Player shoot')

    def iFrame(self):
        """
        A Játékos iFrame-eiből von le 1-et
        """
        if self.iFrames > 0:
            self.iFrames -= 1

    def clear_effects(self):
        """
        A Játékost "alapértelmezett" állapotba állítja vissza, akkor használatos, amikor újraéled a Játékos
        """
        self.iFrames = 0
        self.jumpCount = 10
        self.isAlive = True
        self.isInvincible = False
        self.canShoot = False
        self.isFalling = False
        self.isJump = False
        self.isIdle = True
        self.facingLeft = False
        self.facingRight = True
        self.isRunning = False
