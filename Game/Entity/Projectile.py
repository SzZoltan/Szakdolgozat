import pygame


# Projectile-ok alapja öröklődés baráti és ellenséges projectile
class Projectile:
    def __init__(self, x: int, y: int, direction: int):
        self._x = x
        self._y = y
        self._dir = direction
        self._hitbox = pygame.Rect(self.x - 5, self.y - 5, 10, 10)
        # self._lifespan = 100
        self._color = pygame.Color('blue')
        self._vel = 10 * direction
        self._isFriendly = None

    # <editor-fold desc="Property-k és setterek">
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def dir(self):
        return self._dir

    @property
    def hitbox(self):
        return self._hitbox

    @property
    def color(self):
        return self._color

    @property
    def isFriendly(self):
        return self._isFriendly

    @property
    def vel(self):
        return self._vel

    @x.setter
    def x(self, x):
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        self._x = x

    @y.setter
    def y(self, y):
        if not isinstance(y, int):
            raise TypeError("y must be an integer")
        self._y = y

    @hitbox.setter
    def hitbox(self, hitbox):
        if not isinstance(hitbox, pygame.Rect):
            raise TypeError("hitbox must be a pygame.Rect object")
        self._hitbox = hitbox

    @isFriendly.setter
    def isFriendly(self, isFriendly):
        if not isinstance(isFriendly, bool):
            raise TypeError("isFriendly must be a boolean")
        self._isFriendly = isFriendly

    @color.setter
    def color(self, color):
        if not isinstance(color, pygame.Color):
            raise TypeError("color must be a pygame.Color object")
        self._color = color

    # </editor-fold>

    def draw(self, window):
        if isinstance(window, pygame.Surface):
            self.hitbox = pygame.Rect(self.x - 5, self.y - 5, 10, 10)
            pygame.draw.circle(window, self.color, (self.x, self.y), 5)
            # pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)
        else:
            raise TypeError('Invalid draw arguments for Projectile')


class FriendlyProjectile(Projectile):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.color = pygame.Color(0, 255, 0)
        self.isFriendly = True

    def draw(self, window):
        super().draw(window)


class EnemyProjectile(Projectile):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.color = pygame.Color(255, 0, 0)
        self.isFriendly = False

    def draw(self, window):
        super().draw(window)
