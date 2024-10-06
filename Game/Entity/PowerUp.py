from Game.Entity.Player import *
# A PowerUp-oknak alapja ebből öröklődik az összes


class Powerup:
    def __init__(self, x, y, width, height, frames):
        if (isinstance(x, int) and isinstance(y, int) and isinstance(width, int) and isinstance(height, int) and
                isinstance(frames, list) and isinstance(frames[0], pygame.Surface)):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.frameCount = 0
            self.frames = frames
            self.isVisible = True
            self.hitbox = pygame.Rect(self.x+5, self.y+5, 20, 20)
        else:
            raise TypeError("Invalid innit arguments for Powerup")

    def drawPowerup(self, window):
        if isinstance(window, pygame.Surface):
            if self.isVisible:
                self.hitbox = pygame.Rect(self.x+5, self.y+5, 20, 20)
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
