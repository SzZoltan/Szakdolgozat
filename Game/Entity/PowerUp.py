import pygame
from Game.Game_Graphics.Graphics_Loader import (iterateFrames, apple_frames, pineapple_frames, cherry_frames,
                                                strawberry_frames, end_frame)
from Game.Entity.Player import Player


class Powerup:
    """
    A PowerUp-oknak alapja ebből öröklődik az összes
    """
    def __init__(self, x: int or float, y: int or float, width: int, height: int):
        """
        Inicializálja a PowerUp-ot
        :param x: int vagy float, x koordináta
        :param y: int vagy float, y koordináta
        :param width: int, szélesség
        :param height: int, magasság
        """
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
        """
        Visszadja a PowerUp x koordinátáját
        :return: int vagy float, x koordináta
        """
        return self._x

    @property
    def y(self):
        """
        Visszadja a PowerUp y koordinátáját
        :return: int vagy float, y koordináta
        """
        return self._y

    @property
    def width(self):
        """
        Visszadja a PowerUp szélességét
        :return: int, szélesség
        """
        return self._width

    @property
    def height(self):
        """
        Visszadja a PowerUp magasságát
        :return: int, magasság
        """
        return self._height

    @property
    def frameCount(self):
        """
        Visszadja a PowerUp képkockáinak mutatóját
        :return: int, a mutató
        """
        return self._frameCount

    @property
    def frames(self):
        """
        Visszadja a PowerUp képkockáinak listáját
        :return: pygame.Surface list, a képkockákból álló lista
        """
        return self._frames

    @property
    def isVisible(self):
        """
        Visszadja a PowerUp jelenleg látható-e
        :return: bool, True ha látható, False ha nem
        """
        return self._isVisible

    @property
    def hitbox(self):
        """
        Visszadja a PowerUp hitboxát
        :return: pygame.Rect, a hitbox
        """
        return self._hitbox

    @x.setter
    def x(self, x: int or float):
        """
        Beállítja, a PowerUp x koordinátáját
        :param x: int vagy float, az új koordináta
        """
        if not isinstance(x, (int, float)):
            raise TypeError("x must be an integer or float")
        self._x = x

    @y.setter
    def y(self, y: int or float):
        """
        Beállítja, a PowerUp y koordinátáját
        :param y: int vagy float, az új koordináta
        """
        if not isinstance(y, (int, float)):
            raise TypeError("y must be an integer or float")
        self._y = y

    @width.setter
    def width(self, width: int):
        """
        Beállítja, a PowerUp szélességét
        :param width: int, az új szélesség
        """
        if not isinstance(width, int):
            raise TypeError("width must be an integer")
        self._width = width

    @height.setter
    def height(self, height: int):
        """
        Beállítja, a PowerUp magasságát
        :param height: int, az új magasságát
        """
        if not isinstance(height, int):
            raise TypeError("height must be an integer")
        self._height = height

    @frameCount.setter
    def frameCount(self, frameCount: int):
        """
        Beállítja, a PowerUp képkockáinak mutatóját
        :param frameCount: int, a mutató új értéke
        """
        if not isinstance(frameCount, int):
            raise TypeError("frameCount must be an integer")
        self._frameCount = frameCount

    @hitbox.setter
    def hitbox(self, hitbox: pygame.Rect):
        """
        Beállítja, a PowerUp hitboxának egy új értékét
        :param hitbox: pygame.Rect, a hitbox új értéke
        """
        if not isinstance(hitbox, pygame.Rect):
            raise TypeError("hitbox must be an pygame.Rect object")
        self._hitbox = hitbox

    @isVisible.setter
    def isVisible(self, isVisible: bool):
        """
        Beállítja, hogy a PowerUp látható-e
        :param isVisible: bool, True ha látható, False ha nem
        """
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
        """
        Felrajzolja a PowerUp metódust a megadott felületre
        :param window: pygame.Surface, a felület amire rajzolunk
        """
        if isinstance(window, pygame.Surface):
            if self.isVisible:
                self.frameCount = iterateFrames(self, window, self.frames, self.frameCount, self.maxframes)
        else:
            raise TypeError("Invalid Window argument for drawPowerup")

    def pickUp(self, player: Player):
        """
        Felveszi az PowerUp-ot, nem láthatóvá teszi
        :param player: Player, a játékos aki felveszi
        """
        if isinstance(player, Player):
            if self.isVisible:
                self.isVisible = False
        else:
            raise TypeError("Invalid player argument for pickUp")


class Apple(Powerup):
    """
    Megnöveli 1-el az életerejét a Játékosnak, PowerUp-ból származik
    """
    def __init__(self, x: int, y: int, width: int = 32, height: int = 32):
        """
        Innicializálja az Apple PowerUp-ot, az ősét hívja meg, és hozzárendeli a megfelelő képlistát
        :param x: int, az x koordináta
        :param y: int, az y koordináta
        :param width: int, az Apple szélessége, alapértelmezetten 32
        :param height: int, az Apple magassága, alapértelmezetten 32
        """
        super().__init__(x, y, width, height)
        self.frames = apple_frames

    def drawPowerup(self, window: pygame.Surface):
        """
        Felrajzolja az Apple PowerUp-ot a megadott felületre, az Ősét hívja meg
        :param window: pygame.Surface, a felület amire rajzolunk
        """
        self.hitbox = pygame.Rect(self.x + 5, self.y + 5, 20, 20)
        super().drawPowerup(window)

    def pickUp(self, player: Player):
        """
        Megnöveli a játékos életerejét 1-el, és eltünteti az Apple-t
        :param player: Player, a játékos aki felveszi az Apple-t
        """
        if isinstance(player, Player):
            if self.isVisible:
                self.isVisible = False
                player.hp = player.hp + 1
        else:
            raise TypeError("Invalid player argument for pickUp")


class Cherry(Powerup):
    """
    Elérhetővé teszi a lövés képességet a karakterünknek, elveszik miután eltalálják vagy meghal, PowerUp-ból öröklődik
    """
    def __init__(self, x: int, y: int, width: int = 32, height: int = 32):
        """
        Innicializálja a Cherry PowerUp-ot, az ősét hívja meg, és hozzárendeli a megfelelő képlistát
        :param x: int, az x koordináta
        :param y: int, az y koordináta
        :param width: int, a Cherry szélessége, alapértelmezetten 32
        :param height: int, a Cherry magassága, alapértelmezetten 32
        """
        super().__init__(x, y, width, height)
        self.frames = cherry_frames

    def drawPowerup(self, window: pygame.Surface):
        """
        Felrajzolja a Cherry PowerUp-ot a megadott felületre, az Ősét hívja meg
        :param window: pygame.Surface, a felület amire rajzolunk
        """
        self.hitbox = pygame.Rect(self.x + 5, self.y + 5, 20, 20)
        super().drawPowerup(window)

    def pickUp(self, player: Player):
        """
        Elérhetővé teszi a lövés képességet a Játékosnak, és eltünteti a Cherry-t
        :param player: Player, a játékos aki felveszi az Cherry-t
        """
        if isinstance(player, Player):
            if self.isVisible:
                self.isVisible = False
                player.canShoot = True
        else:
            raise TypeError("Invalid player argument for pickUp")


class Pineapple(Powerup):
    """
    Megnöveli az életek/újrapróbálkozások számát a Játékosnak
    """
    def __init__(self, x: int, y: int, width: int = 32, height: int = 32):
        """
        Innicializálja a Pineapple PowerUp-ot, az ősét hívja meg, és hozzárendeli a megfelelő képlistát
        :param x: int, az x koordináta
        :param y: int, az y koordináta
        :param width: int, a Pineapple szélessége, alapértelmezetten 32
        :param height: int, a Pineapple magassága, alapértelmezetten 32
        """
        super().__init__(x, y, width, height)
        self.frames = pineapple_frames

    def drawPowerup(self, window: pygame.Surface):
        """
        Felrajzolja a Pineapple PowerUp-ot a megadott felületre, az Ősét hívja meg
        :param window: pygame.Surface, a felület amire rajzolunk
        """
        self.hitbox = pygame.Rect(self.x + 5, self.y + 5, 20, 20)
        super().drawPowerup(window)

    def pickUp(self, player: Player):
        """
        Megnöveli az életek számát a játékosnak, és eltünteti a Pineapple-t
        :param player: Player, a játékos aki felveszi az Pineapple-t
        """
        if isinstance(player, Player):
            if self.isVisible:
                self.isVisible = False
                player.lives = player.lives + 1
        else:
            raise TypeError("Invalid player argument for pickUp")


class Strawberry(Powerup):
    """
    Sebezhetetlenné teszi a Játékost egy ideig és míg sebezhetetlen át tud menni különböző ellenfeleken
    """
    def __init__(self, x: int, y: int, width: int = 32, height: int = 32):
        """
        Innicializálja a Strawberry PowerUp-ot, az ősét hívja meg, és hozzárendeli a megfelelő képlistát
        :param x: int, az x koordináta
        :param y: int, az y koordináta
        :param width: int, a Strawberry szélessége, alapértelmezetten 32
        :param height: int, a Strawberry magassága, alapértelmezetten 32
        """
        super().__init__(x, y, width, height)
        self.frames = strawberry_frames

    def drawPowerup(self, window: pygame.Surface):
        """
        Felrajzolja a Strawberry PowerUp-ot a megadott felületre, az Ősét hívja meg
        :param window: pygame.Surface, a felület amire rajzolunk
        """
        self.hitbox = pygame.Rect(self.x + 5, self.y + 5, 20, 20)
        super().drawPowerup(window)

    def pickUp(self, player: Player):
        """
        Sebezhetelenné teszi a játékost, és eltünteti a Strawberry-t
        :param player: Player, a játékos aki felveszi a Strawberry-t
        """
        if isinstance(player, Player):
            if self.isVisible:
                self.isVisible = False
                player.isInvincible = True
                player.iFrames = 100
        else:
            raise TypeError("Invalid player argument for pickUp")


class Finish(Powerup):
    """
    Egy különleges Powerup amit csak a pálya végén lehet megtalálni, ezzel zárúl le a játék
    """
    def __init__(self, x: int, y: int, width: int = 32, height: int = 32):
        """
        Innicializálja a Finish PowerUp-ot, az ősét hívja meg, és hozzárendeli a megfelelő képlistát
        :param x: int, az x koordináta
        :param y: int, az y koordináta
        :param width: int, a Finish szélessége, alapértelmezetten 32
        :param height: int, a Finish magassága, alapértelmezetten 32
        """
        super().__init__(x, y, width, height)
        self.frames = end_frame
        self.hitbox = pygame.Rect(self.x + 5, self.y + 10, 53, 55)
        self.maxframes = 1

    def drawPowerup(self, window: pygame.Surface):
        """
        Felrajzolja a Finish PowerUp-ot a megadott felületre, az Ősét hívja meg
        :param window: pygame.Surface, a felület amire rajzolunk
        """
        self.hitbox = pygame.Rect(self.x + 5, self.y + 10, 53, 55)
        super().drawPowerup(window)

    def pickUp(self, player: Player):
        """
        Ha ezt felveszik a játék véget ér és a játékos győz, és eltünteti a Finish-t
        :param player: Player, a játékos aki felveszi a Finish-t
        """
        if isinstance(player, Player):
            if self.isVisible:
                self.isVisible = False
                pass
        else:
            raise TypeError("Invalid player argument for pickUp")
