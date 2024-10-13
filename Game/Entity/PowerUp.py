from Game.Entity.Player import *


# A PowerUp-oknak alapja ebből öröklődik az összes


class Powerup:
    def __init__(self, x: int, y: int, width: int, height: int, frames: list):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._frameCount = 0
        self._isVisible = True
        self._hitbox = pygame.Rect(self.x + 5, self.y + 5, 20, 20)
        for frame in frames:
            if not isinstance(frame, pygame.Surface):
                raise TypeError("The frames list must contain pygame.Surface objects")
        self._frames = frames

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
    def x(self, x):
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        self._x = x

    @y.setter
    def y(self, y):
        if not isinstance(y, int):
            raise TypeError("y must be an integer")
        self._y = y

    @width.setter
    def width(self, width):
        if not isinstance(width, int):
            raise TypeError("width must be an integer")
        self._width = width

    @height.setter
    def height(self, height):
        if not isinstance(height, int):
            raise TypeError("height must be an integer")
        self._height = height

    @frameCount.setter
    def frameCount(self, frameCount):
        if not isinstance(frameCount, int):
            raise TypeError("frameCount must be an integer")
        self._frameCount = frameCount

    @hitbox.setter
    def hitbox(self, hitbox):
        if not isinstance(hitbox, pygame.Rect):
            raise TypeError("hitbox must be an pygame.Rect object")
        self._hitbox = hitbox

    @isVisible.setter
    def isVisible(self, isVisible):
        if not isinstance(isVisible, bool):
            raise TypeError("isVisible must be bool")
        self._isVisible = isVisible

    # </editor-fold>

    def drawPowerup(self, window):
        if isinstance(window, pygame.Surface):
            if self.isVisible:
                self.hitbox = pygame.Rect(self.x + 5, self.y + 5, 20, 20)
                self.frameCount = iterateFrames(self, window, self.frames, self.frameCount, 17)
                # pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)
        else:
            raise TypeError("Invalid Window argument for drawPowerup")

    def pickUp(self, player):
        if isinstance(player, Player):
            if self.isVisible:
                print('Item picked up')
                self.isVisible = False
        else:
            raise TypeError("Invalid player argument for pickUp")


# Megnöveli 1-el az életerejét a karakternek
class Apple(Powerup):
    def __init__(self, x, y, width, height, frames):
        super().__init__(x, y, width, height, frames)

    def drawApple(self, window):
        super().drawPowerup(window)

    def pickUp(self, player):
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
    def __init__(self, x, y, width, height, frames):
        super().__init__(x, y, width, height, frames)

    def drawCherry(self, window):
        super().drawPowerup(window)

    def pickUp(self, player):
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
    def __init__(self, x, y, width, height, frames):
        super().__init__(x, y, width, height, frames)

    def drawPineapple(self, window):
        super().drawPowerup(window)

    def pickUp(self, player):
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
    def __init__(self, x, y, width, height, frames):
        super().__init__(x, y, width, height, frames)

    def drawStrawberry(self, window):
        super().drawPowerup(window)

    def pickUp(self, player):
        if isinstance(player, Player):
            if self.isVisible:
                self.isVisible = False
                player.isInvincible = True
                print('Strawberry picked up, invinciblity for 10 seconds')
        else:
            raise TypeError("Invalid player argument for pickUp")
