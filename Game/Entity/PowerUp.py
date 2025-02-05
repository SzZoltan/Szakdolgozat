import pygame
from Game.Game_Graphics.Graphics_Loader import (iterateFrames, apple_frames, pineapple_frames, cherry_frames,
                                                strawberry_frames, end_frame)
from Game.Entity.Player import Player


# A PowerUp-oknak alapja ebből öröklődik az összes


class Powerup:
    def __init__(self, x: int or float, y: int or float, width: int, height: int):
        self._x = x
        self.y = y
        self.width = width
        self.height = height
        self.frameCount = 0
        self.isVisible = True
        self.hitbox = pygame.Rect(self.x + 5, self.y + 5, 20, 20)
        self.frames = apple_frames
        self.maxframes = 17

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
    def frameCount(self):
        return self._frameCount

    @property
    def frames(self):
        return self._frames

    @property
    def isVisible(self):
        return self._isVisible

    @property
    def hitbox(self):
        return self._hitbox

    @x.setter
    def x(self, x: int or float):
        if not isinstance(x, (int, float)):
            raise TypeError("x must be an integer or float")
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

    @frameCount.setter
    def frameCount(self, frameCount: int):
        if not isinstance(frameCount, int):
            raise TypeError("frameCount must be an integer")
        self._frameCount = frameCount

    @hitbox.setter
    def hitbox(self, hitbox: int):
        if not isinstance(hitbox, pygame.Rect):
            raise TypeError("hitbox must be an pygame.Rect object")
        self._hitbox = hitbox

    @isVisible.setter
    def isVisible(self, isVisible: bool):
        if not isinstance(isVisible, bool):
            raise TypeError("isVisible must be bool")
        self._isVisible = isVisible

    @frames.setter
    def frames(self, frames: list):
        for frame in frames:
            if not isinstance(frame, pygame.Surface):
                raise TypeError("frames must be a list containing pygame.Surface objects")
        self._frames = frames

    # </editor-fold>

    def drawPowerup(self, window: pygame.Surface):
        if isinstance(window, pygame.Surface):
            if self.isVisible:
                self.frameCount = iterateFrames(self, window, self.frames, self.frameCount, self.maxframes)
        else:
            raise TypeError("Invalid Window argument for drawPowerup")

    def pickUp(self, player: Player):
        if isinstance(player, Player):
            if self.isVisible:
                print('Item picked up')
                self.isVisible = False
        else:
            raise TypeError("Invalid player argument for pickUp")


# Megnöveli 1-el az életerejét a karakternek
class Apple(Powerup):
    def __init__(self, x: int, y: int, width: int = 32, height: int = 32):
        super().__init__(x, y, width, height)
        self.frames = apple_frames

    def drawPowerup(self, window: pygame.Surface):
        self.hitbox = pygame.Rect(self.x + 5, self.y + 5, 20, 20)
        super().drawPowerup(window)

    def pickUp(self, player: Player):
        if isinstance(player, Player):
            if self.isVisible:
                self.isVisible = False
                print('Apple picked up, health increased')
                print(f'current: {player.hp} hp')
                player.hp = player.hp + 1
                print(f'current: {player.hp} hp')
        else:
            raise TypeError("Invalid player argument for pickUp")


# Elérhetővé teszi a lövés képességet a karakterünknek, elveszik miután eltalálják vagy meghal
class Cherry(Powerup):
    def __init__(self, x: int, y: int, width: int = 32, height: int = 32):
        super().__init__(x, y, width, height)
        self.frames = cherry_frames

    def drawPowerup(self, window: pygame.Surface):
        self.hitbox = pygame.Rect(self.x + 5, self.y + 5, 20, 20)
        super().drawPowerup(window)

    def pickUp(self, player: Player):
        if isinstance(player, Player):
            if self.isVisible:
                self.isVisible = False
                print('Cherry picked up, shooting unlocked')
                print(f'current: {player.canShoot} ')
                player.canShoot = True
                print(f'current: {player.canShoot} ')
        else:
            raise TypeError("Invalid player argument for pickUp")


# Megnöveli az életek/újrapróbálkozások számát a Játékosnak
class Pineapple(Powerup):
    def __init__(self, x: int, y: int, width: int = 32, height: int = 32):
        super().__init__(x, y, width, height)
        self.frames = pineapple_frames

    def drawPowerup(self, window: pygame.Surface):
        self.hitbox = pygame.Rect(self.x + 5, self.y + 5, 20, 20)
        super().drawPowerup(window)

    def pickUp(self, player: Player):
        if isinstance(player, Player):
            if self.isVisible:
                self.isVisible = False
                print('Pineapple picked up, number of lives increased')
                print(f'current: {player.lives} lives')
                player.lives = player.lives + 1
                print(f'current: {player.lives} lives')
        else:
            raise TypeError("Invalid player argument for pickUp")


# Halhatatlanná teszi a karaktert egy ideig és míg halhatatlan át tud menni különböző ellenfeleken
class Strawberry(Powerup):
    def __init__(self, x: int, y: int, width: int = 32, height: int = 32):
        super().__init__(x, y, width, height)
        self.frames = strawberry_frames

    def drawPowerup(self, window: pygame.Surface):
        self.hitbox = pygame.Rect(self.x + 5, self.y + 5, 20, 20)
        super().drawPowerup(window)

    def pickUp(self, player: Player):
        if isinstance(player, Player):
            if self.isVisible:
                self.isVisible = False
                player.isInvincible = True
                print('Strawberry picked up, invinciblity for 10 seconds')
        else:
            raise TypeError("Invalid player argument for pickUp")


class Finish(Powerup):
    def __init__(self, x: int, y: int, width: int = 32, height: int = 32):
        super().__init__(x, y, width, height)
        self.frames = end_frame
        self.hitbox = pygame.Rect(self.x + 5, self.y + 10, 53, 55)
        self.maxframes = 1

    def drawPowerup(self, window: pygame.Surface):
        self.hitbox = pygame.Rect(self.x + 5, self.y + 10, 53, 55)
        super().drawPowerup(window)

    def pickUp(self, player: Player):
        if isinstance(player, Player):
            if self.isVisible:
                print('Trophy picked up, Game Won!')
        else:
            raise TypeError("Invalid player argument for pickUp")