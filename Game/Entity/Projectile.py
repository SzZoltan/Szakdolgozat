import pygame


# Projectile-ok alapja öröklődés baráti és ellenséges projectile
class Projectile:
    def __init__(self, x, y, direction):
        if isinstance(x, int) and isinstance(y, int) and isinstance(direction, int):
            self.x = x
            self.y = y
            self.dir = direction
            self.hitbox = pygame.Rect(self.x - 5, self.y - 5, 10, 10)
            # self.lifespan = 100
            self.vel = 10 * direction
            self.isFriendly = None
        else:
            raise TypeError('Invalid innit arguments for Projectile')

    def draw(self, window, color):
        if isinstance(window, pygame.Surface) and isinstance(color, pygame.Color):
            self.hitbox = pygame.Rect(self.x - 5, self.y - 5, 10, 10)
            pygame.draw.circle(window, color, (self.x, self.y), 5)
            # pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)
        else:
            raise TypeError('Invalid draw arguments for Projectile')


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