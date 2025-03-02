import pygame


class Projectile:
    """
    Projectile-ok alapja ebből öröklődik a baráti és ellenséges projectile
    """
    def __init__(self, x: int or float, y: int or float, direction: int):
        """
        Inicializálja a Projectile-t
        :param x: int vagy float, x koordináta
        :param y: int vagy float, y koordináta
        :param direction: 1 jobbra vagy -1 blara
        """
        self.x = x
        self.y = y
        self.dir = direction
        self.hitbox = pygame.Rect(self.x - 5, self.y - 5, 10, 10)
        self.color = pygame.Color('blue')
        self._vel = 10 * direction
        self._isFriendly = None

    # <editor-fold desc="Property-k és setterek">
    @property
    def x(self):
        """
        Visszadja az x koordinátát
        :return: int, x koordináta
        """
        return self._x

    @property
    def y(self):
        """
        Visszadja az y koordinátát
        :return: int, y koordináta
        """
        return self._y

    @property
    def dir(self):
        """
        Visszadja az irányt
        :return: 1 vagy -1
        """
        return self._dir

    @property
    def hitbox(self):
        """
        Visszadja a hitboxot
        :return: pygame.Rect, a hitbox
        """
        return self._hitbox

    @property
    def color(self):
        """
        Visszadja a színét a Projectile-nak
        :return: pygame.Color, a szín
        """
        return self._color

    @property
    def isFriendly(self):
        """
        Visszadja, hogy barátságos vagy ellenséges-e a Projectile
        :return: bool, baráti vagy ellenséges
        """
        return self._isFriendly

    @property
    def vel(self):
        """
        Visszadja a sebességét a Projectile-nak
        :return: int, a sebesség
        """
        return self._vel

    @x.setter
    def x(self, x: int or float):
        """
        Beállítja a Projectile x koordinátáját
        :param x: int vagy float, az új x koordináta
        """
        if not isinstance(x, (int, float)):
            raise TypeError("x must be an integer or float")
        self._x = x

    @y.setter
    def y(self, y: int or float):
        """
        Beállítja a Projectile y koordinátáját
        :param y: int vagy float, az új y koordináta
        """
        if not isinstance(y, (int, float)):
            raise TypeError("y must be an integer or float")
        self._y = y

    @hitbox.setter
    def hitbox(self, hitbox: pygame.Rect):
        """
        Beállítja a Projectile hitboxát
        :param hitbox: pygame.Rect, az új hitbox
        """
        if not isinstance(hitbox, pygame.Rect):
            raise TypeError("hitbox must be a pygame.Rect object")
        self._hitbox = hitbox

    @isFriendly.setter
    def isFriendly(self, isFriendly: bool):
        """
        Beállítja hogy a Projectile baráti-e vagy nem
        :param isFriendly: bool, hogy baráti-e vagy nem
        """
        if not isinstance(isFriendly, bool):
            raise TypeError("isFriendly must be a boolean")
        self._isFriendly = isFriendly

    @color.setter
    def color(self, color: pygame.Color):
        """
        Beállítja a Projectile színét
        :param color: pygame.Color, a Projectile színe
        """
        if not isinstance(color, pygame.Color):
            raise TypeError("color must be a pygame.Color object")
        self._color = color

    @dir.setter
    def dir(self, direc: int):
        """
        Beállítja hogy a Projectile melyik irányba megy
        :param direc: 1 jobbra vagy -1 balra
        """
        if isinstance(direc, int):
            if direc == 1 or direc == -1:
                self._dir = direc
            else:
                raise TypeError("dir must be an integer that is 1 or -1")
        else:
            raise TypeError("dir must be an integer that is 1 or -1")

    # </editor-fold>

    def draw(self, window: pygame.Surface):
        """
        Megrajzolja a Projectile-t a megadott felszínre
        :param window: pygame.Surface, a felszín amire rajzolunk
        """
        if isinstance(window, pygame.Surface):
            self.hitbox = pygame.Rect(self.x - 5, self.y - 5, 10, 10)
            pygame.draw.circle(window, self.color, (self.x, self.y), 5)
        else:
            raise TypeError('Invalid draw arguments for Projectile')


class FriendlyProjectile(Projectile):
    """
    Egy Projectile ami barátságos
    """
    def __init__(self, x: int or float, y: int or float, direction: int):
        """
        A FriendlyProjectile-t innicializálja, az őst hívja meg
        :param x: int vagy float, x koordináta
        :param y: int vagy float, y koordináta
        :param direction: 1 jobbra vagy -1 blara
        """
        super().__init__(x, y, direction)
        self.color = pygame.Color(0, 255, 0)
        self.isFriendly = True

    def draw(self, window: pygame.Surface):
        """
        Felrajzolja a FriendlyProjectile-t a megadott felszínre, az őst hívja meg
        :param window: pygame.Surface, a felszín amire rajzolunk
        """
        super().draw(window)


class EnemyProjectile(Projectile):
    """
    Az Ellenséges Projectile
    """
    def __init__(self, x: int or float, y: int or float, direction: int):
        """
        Az EnemyProjectile-t innicializálja, az őst hívja meg
        :param x: int vagy float, x koordináta
        :param y: int vagy float, y koordináta
        :param direction: 1 jobbra vagy -1 blara
        """
        super().__init__(x, y, direction)
        self.color = pygame.Color(255, 0, 0)
        self.isFriendly = False

    def draw(self, window:pygame.Surface):
        """
        Felrajzolja az EnemyProjectile-t a megadott felszínre, az őst hívja meg
        :param window: pygame.Surface, a felszín amire rajzolunk
        """
        super().draw(window)
