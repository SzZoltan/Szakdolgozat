# Öröklődés különleges block-okból: ? blokk, törhetetlen
from Game.Entity.PowerUp import Apple, Pineapple, Cherry, Strawberry
from Game.Game_Graphics.Graphics_Loader import (brick_frame, steel_frame, gold_frame)
from enum import Enum
import pygame


class Inside(Enum):
    """
    Egy enum ami megmondja mi van a blockokban
    """
    APPLE = Apple
    PINEAPPLE = Pineapple
    CHERRY = Cherry
    STRAWBERRY = Strawberry
    NOTHING = None


class Block:
    """
    A Block-oknak az Őse, ebből öröklődik az összes létező Block
    """
    def __init__(self, x: int or float, y: int or float, inside=Inside.NOTHING):
        """
        A Block-ot inicializálja
        :param x: int vagy float, x koordináta
        :param y: int vagy float, y koordináta
        :param inside: Inside enum egyik tagja, alapértelmezetten üres
        """
        if not isinstance(x, (int or float)) or not isinstance(y, (int or float)) or not isinstance(inside, Inside):
            raise TypeError("Invalid innit attributes: x and y must be int or float and inside has "
                            "to be of the Inside enum")
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
        """
        Visszaadja a Block x koordinátáját
        :return: int vagy float, x koordináta
        """
        return self._x

    @property
    def y(self):
        """
        Visszaadja a Block y koordinátáját
        :return: int vagy float, y koordináta
        """
        return self._y

    @property
    def hitbox(self):
        """
        Visszaadja a Block hitbox-át
        :return: pygame.Rect, hitbox
        """
        return self._hitbox

    @property
    def inside(self):
        """
        Visszaadja mi van a Block-ban
        :return: Inside enum egyik értéke
        """
        return self._inside

    @property
    def isVisible(self):
        """
        Visszadja, hogy a Block látható-e
        :return: bool, hogy látható-e vagy sem
        """
        return self._isVisible

    @property
    def isBreakable(self):
        """
        Visszaadja hogy a Block törhető-e
        :return: bool, törhető vagy sem
        """
        return self._isBreakable

    @property
    def isContainer(self):
        """
        Visszadja, hogy a Block egy tároló-e
        :return: bool, tároló vagy nem
        """
        return self._isContainer

    @x.setter
    def x(self, x: int or float):
        """
        Beállítja az x koordináta értékét
        :param x: int vagy float, az új koordináta értéke
        """
        if isinstance(x, (int, float)):
            self._x = x
        else:
            raise TypeError("x must be an int or float")

    @y.setter
    def y(self, y: int or float):
        """
        Beállítja az y koordináta értékét
        :param y: int vagy float, az új koordináta értéke
        """
        if isinstance(y, (int, float)):
            self._y = y
        else:
            raise TypeError("y must be an int or float")

    @hitbox.setter
    def hitbox(self, hitbox: pygame.Rect):
        """
        Beállítja a hitbox értéken
        :param hitbox: pygame.Rect, az új hitbox értéke
        """
        if isinstance(hitbox, pygame.Rect):
            self._hitbox = hitbox
        else:
            raise TypeError("hitbox must be pygame.Rect type")

    @inside.setter
    def inside(self, inside: Inside):
        """
        Beállítja, hogy mi legyen a Block-ban
        :param inside: Inside enum egyik értéke, az amit tárol a Block
        """
        if isinstance(inside, Inside):
            self._inside = inside
        else:
            raise TypeError("inside must be Inside enum type")

    @isContainer.setter
    def isContainer(self, isContainer: bool):
        """
        Beállítja, hogy Tároló-e a Block
        :param isContainer: bool, tároló vagy nem
        """
        if isinstance(isContainer, bool):
            self._isContainer = isContainer
        else:
            raise TypeError("isContainer must be bool")

    @isBreakable.setter
    def isBreakable(self, isBreakable: bool):
        """
        Beállítja, hogy törhető-e a Block
        :param isBreakable: bool, törhető vagy nem
        """
        if isinstance(isBreakable, bool):
            self._isBreakable = isBreakable
        else:
            raise TypeError("isBreakable must be bool")

    @isVisible.setter
    def isVisible(self, isVisible: bool):
        """
        Beállítja, hogy látható-e a Block
        :param isVisible: bool, látható vagy nem
        """
        if isinstance(isVisible, bool):
            self._isVisible = isVisible
        else:
            raise TypeError("isVisible must be bool")
    # </editor-fold>

    def destroy(self):
        """
        Elpusztítja a Block-ot
        :return: None, ha üres volt, különben az egyik PowerUp-ot ami az Inside enum-ba van
        """
        if self.isBreakable:
            self.isVisible = False
            if self.isContainer:
                if self.inside == Inside.APPLE:
                    return Apple(self.x+5, self.y-15, 32, 32)
                elif self.inside == Inside.PINEAPPLE:
                    return Pineapple(self.x+5, self.y-15, 32, 32)
                elif self.inside == Inside.CHERRY:
                    return Cherry(self.x+5, self.y-15, 32, 32)
                elif self.inside == Inside.STRAWBERRY:
                    return Strawberry(self.x+5, self.y-15, 32, 32)
                elif self.inside == Inside.NOTHING:
                    return None
            else:
                return None

    def draw(self, window: pygame.Surface):
        """
        Megrajzolja a Block-ot, ha látható
        :param window: pygame.Surface, a képernyő amire rajzoljuk
        """
        if not isinstance(window, pygame.Surface):
            raise TypeError("window must be pygame.Surface")
        if self.isVisible:
            self.hitbox = pygame.Rect(self.x, self.y, 40, 40)
            window.blit(brick_frame[0], (self.x, self.y))


class BrickBlock(Block):
    """
    Átalgos tégla, törhető, de nincs benne semmi
    """
    def __init__(self, x: int or float, y: int or float):
        """
        A Brick-et inicializálja, az ősét hívja meg
        :param x: int vagy float, x koordináta
        :param y: int vagy float, y koordináta
        """
        super().__init__(x, y)
        self.isBreakable = True
        self.isContainer = False
        self.inside = Inside.NOTHING
        self.isVisible = True

    def destroy(self):
        """
        Elpusztítja a Brick-et, az őst hívja meg
        :return: None
        """
        return super().destroy()

    def draw(self, window: pygame.Surface):
        """
        Felrajzolja a megadott felületre a Brick-et
        :param window: pygame.Surface, amire rajzoljuk
        """
        if not isinstance(window, pygame.Surface):
            raise TypeError("window must be pygame.Surface")
        if self.isVisible:
            self.hitbox = pygame.Rect(self.x, self.y, 40, 40)
            window.blit(brick_frame[0], (self.x, self.y))


class SteelBlock(Block):
    """
    Vasblock, törhetetlen, nincs benne semmi
    """
    def __init__(self, x: int or float, y: int or float):
        """
        SteelBlock-ot inicializálja, az Őst hívja meg
        :param x: int vagy float, x koordináta
        :param y: int vagy float, y koordináta
        """
        super().__init__(x, y)
        self.isBreakable = False
        self.isContainer = False
        self.inside = Inside.NOTHING
        self.isVisible = True

    def destroy(self):
        """
        Nem csinál semmit mivel nem pusztítható el ez a Block
        :return: None
        """
        return super().destroy()

    def draw(self, window: pygame.Surface):
        """
        Felrajzolja a megadott felületre a SteelBlock-ot
        :param window: pygame.Surface, amire rajzoljuk
        """
        if not isinstance(window, pygame.Surface):
            raise TypeError("window must be pygame.Surface")
        if self.isVisible:
            self.hitbox = pygame.Rect(self.x, self.y, 40, 40)
            window.blit(steel_frame[0], (self.x, self.y))


class GoldBlock(Block):
    """
    Aranyblock, törhető és van benne PowerUp
    """
    def __init__(self, x: int or float, y: int or float, inside):
        """
        Inicializálja a GoldBlock-ot, Őst hívja meg
        :param x: int vagy float, x koordinita
        :param y: int vagy float, y koordinita
        :param inside: az Inside enum egyik változója amelyik PowerUp benne van
        """
        super().__init__(x, y)
        self.isBreakable = True
        self.isContainer = True
        self.inside = inside
        self.isVisible = True

    def destroy(self):
        """
        Elpusztítja a GoldBlock-ot
        :return: A PowerUp ami benne volt
        """
        return super().destroy()

    def draw(self, window: pygame.Surface):
        """
        Felrajzolja a GoldBlock-ot a felületre
        :param window: pygame.Surface, a felület amire rajzoljuk
        """
        if not isinstance(window, pygame.Surface):
            raise TypeError("window must be pygame.Surface")
        if self.isVisible:
            self.hitbox = pygame.Rect(self.x, self.y, 40, 40)
            window.blit(gold_frame[0], (self.x, self.y))
