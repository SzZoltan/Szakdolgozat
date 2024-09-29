import pygame
# Enemy viselkedés
# Az összes ellenfélnek az alapja mind öröklődik innen


class Enemy:
    def __init__(self, x, y, width, height, canmove, canshoot):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.health = 1
        self.canShoot = canshoot
        self.canMove = canmove
        self.idleFrameCount = 0
        self.isIdle = True
        self.hitbox = pygame.Rect(self.x, self.y, 30, 40)

    def drawEnemy(self, window):
        self.hitbox = pygame.Rect(self.x, self.y, 30, 40)
        pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)


# A goomba féle ellenfél aki nem csinál semmit csak oda vissza járkál
class BunnyEnemy(Enemy):
    def __init__(self, x, y, width, height, canmove, canshoot):
        super().__init__(x, y, width, height, canmove, canshoot)
        self.canShoot = False
        self.canMove = True

    def drawEnemy(self, window):
        super().drawEnemy(window)


# Az egyhelyben álló folyamatosan lövő ellenfél
class PlantEnemy(Enemy):
    def __init__(self, x, y, width, height, canmove, canshoot):
        super().__init__(x, y, width, height, canmove, canshoot)
        self.canShoot = True
        self.canMove = False
        self.shootCooldown = 0

    def drawEnemy(self, window):
        super().drawEnemy(window)
