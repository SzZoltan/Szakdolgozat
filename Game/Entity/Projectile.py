import pygame


# Projectile-ok alapja öröklődés baráti és ellenséges projectile
class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.dir = direction
        self.hitbox = pygame.Rect(self.x - 5, self.y - 5, 10, 10)
        # self.lifespan = 100
        self.vel = 10 * direction
        self.isFriendly = None

    def draw(self, window, color):
        self.hitbox = pygame.Rect(self.x - 5, self.y - 5, 10, 10)
        pygame.draw.circle(window, color, (self.x, self.y), 5)
        # pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)


class FriendlyProjectile(Projectile):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.isFriendly = True

    def draw(self, window, color):
        super().draw(window, color)


class EnemyProjectile(Projectile):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.isFriendly = False

    def draw(self, window, color):
        super().draw(window, color)