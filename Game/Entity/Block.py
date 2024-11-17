# Öröklődés különleges block-okból: ? blokk, törhetetlen
from Game.Entity.PowerUp import Powerup, Apple, Pineapple, Cherry, Strawberry
from enum import Enum
import pygame

# Enum az inside powerupokra


class Inside(Enum):
    APPLE = Apple
    PINEAPPLE = Pineapple
    CHERRY = Cherry
    STRAWBERRY = Strawberry
    NOTHING = None


class Block:
    # Az Inside-ot hogyan oldjam meg, string, maga az PowerUp?
    def __init__(self, x: int or float, y: int or float, inside=Inside.NOTHING):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.hitbox = pygame.Rect(self._x, self._y, self.width, self.height)
        self.isBreakable = True
        self.isContainer = False
        self.inside = inside
        self.isVisible = True

    # <editor-fold desc="Porperty-k és Setterek">
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def hitbox(self):
        return self._hitbox

    @property
    def inside(self):
        return self._inside

    @property
    def isVisible(self):
        return self._isVisible

    @property
    def isBreakable(self):
        return self._isBreakable

    @property
    def isContainer(self):
        return self._isContainer

    @x.setter
    def x(self, x: int or float):
        if isinstance(x, (int, float)):
            self._x = x
        else:
            raise TypeError("x must be an int or float")

    @y.setter
    def y(self, y: int or float):
        if isinstance(y, (int, float)):
            self._y = y
        else:
            raise TypeError("y must be an int or float")

    @hitbox.setter
    def hitbox(self, hitbox: pygame.Rect):
        if isinstance(hitbox, pygame.Rect):
            self._hitbox = hitbox
        else:
            raise TypeError("hitbox must be pygame.Rect type")

    @inside.setter
    def inside(self, inside: Inside):
        if isinstance(inside, Inside):
            self._inside = inside
        else:
            raise TypeError("inside must be Inside enum type")

    @isContainer.setter
    def isContainer(self, isContainer: bool):
        if isinstance(isContainer, bool):
            self._isContainer = isContainer
        else:
            raise TypeError("isContainer must be bool")

    @isBreakable.setter
    def isBreakable(self, isBreakable: bool):
        if isinstance(isBreakable, bool):
            self._isBreakable = isBreakable
        else:
            raise TypeError("isBreakable must be bool")

    @isVisible.setter
    def isVisible(self, isVisible: bool):
        if isinstance(isVisible, bool):
            self._isVisible = isVisible
        else:
            raise TypeError("isVisible must be bool")
    # </editor-fold>

    def destroy(self):
        if self.isBreakable:
            self.isVisible = False
            if self.isContainer:
                if self.inside == Inside.APPLE:
                    return Apple(self.x, self.y, 32, 32)
                elif self.inside == Inside.PINEAPPLE:
                    return Pineapple(self.x, self.y, 32, 32)
                elif self.inside == Inside.CHERRY:
                    return Cherry(self.x, self.y, 32, 32)
                elif self.inside == Inside.STRAWBERRY:
                    return Strawberry(self.x, self.y, 32, 32)
                elif self.inside == Inside.NOTHING:
                    return None
            else:
                return None

    def draw(self, window: pygame.Surface):
        if self.isVisible:
            self.hitbox = pygame.Rect(self.x, self.y, 40, 40)
            pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)