from Game.Entity.Projectile import EnemyProjectile
from Game.Game_Graphics.Graphics_Loader import *


# Enemy viselkedés


# Az összes ellenfélnek az alapja mind öröklődik innen
class Enemy:
    def __init__(self, x, y, width, height):
        if isinstance(x, int) and isinstance(y, int) and isinstance(width, int) and isinstance(height, int):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = 5
            self.health = 1
            self.canShoot = False
            self.canMove = True
            self.idleFrameCount = 0
            self.movingFrameCount = 0
            self.shootingFrameCount = 0
            self.isShooting = False
            self.isAlive = True
            self.canBeJumped = True
            self.isIdle = True
            self.facingLeft = True
            self.facingRight = False
            self.isMoving = False
            self.hitbox = pygame.Rect(self.x, self.y, 30, 40)
        else:
            raise TypeError('Invalid innit arguments for Enemy')

    # Ez lesz a default Enemy animáció, a Főszereplő, de csak akkor ha nincs implementálva sajátja,
    # soha nem lesz hívva ha minden jól alakul
    def drawEnemy(self, window):
        if isinstance(window, pygame.Surface):
            if self.isAlive:
                if self.isMoving:
                    if self.facingRight:
                        self.movingFrameCount = iterateFrames(self, window, mc_run_left_frames, self.movingFrameCount, 12)
                    else:
                        self.movingFrameCount = iterateFrames(self, window, mc_run_left_frames, self.movingFrameCount, 12)
                elif self.isIdle:
                    if self.facingRight:
                        self.idleFrameCount = iterateFrames(self, window, mc_idle_right_frames, self.idleFrameCount, 11)
                    else:
                        self.idleFrameCount = iterateFrames(self, window, mc_idle_left_frames, self.idleFrameCount, 11)
                self.hitbox = pygame.Rect(self.x, self.y, 30, 40)
                pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)
        else:
            raise TypeError('Invalid window argument for drawEnemy')

    def hit(self):
        self.health = self.health - 1
        if self.health == 0:
            self.isAlive = False

    def shoot(self, direction):
        if direction == 1 or direction == -1:
            if self.canShoot:
                EnemyProjectile(round(self.x + self.width // 2), round(self.y + self.height // 2), direction)
        else:
            raise ValueError('Invalid direction argument for Enemy shoot')

    def move(self, direction):
        if direction == 'left':
            self.isIdle = False
            self.facingLeft = True
            self.facingRight = False
            self.isMoving = True
            self.x -= self.vel
        elif direction == 'right':
            self.isIdle = False
            self.facingLeft = False
            self.facingRight = True
            self.isMoving = True
            self.x += self.vel
        else:
            raise ValueError('Invalid direction argument for Enemy move')


# A goomba féle ellenfél aki nem csinál semmit csak oda vissza járkál
class BunnyEnemy(Enemy):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.canShoot = False
        self.canMove = True

    # Kell egy megoldás arra, hogy ezt egységesíteni lehessen
    def drawEnemy(self, window):
        if isinstance(window, pygame.Surface):
            if self.isAlive:
                if self.isMoving:
                    if self.facingRight:
                        self.movingFrameCount = iterateFrames(self, window, bunny_run_right_frames,
                                                              self.movingFrameCount, 12)
                    else:
                        self.movingFrameCount = iterateFrames(self, window, bunny_run_left_frames,
                                                              self.movingFrameCount, 12)
                elif self.isIdle:
                    if self.facingRight:
                        self.idleFrameCount = iterateFrames(self, window, bunny_idle_right_frames,
                                                            self.idleFrameCount, 8)
                    else:
                        self.idleFrameCount = iterateFrames(self, window, bunny_idle_left_frames,
                                                            self.idleFrameCount, 8)
                self.hitbox = pygame.Rect(self.x, self.y, 30, 40)
                pygame.draw.rect(window, (0, 0, 255), self.hitbox, 2)
        else:
            raise TypeError('Invalid window argument Bunny drawEnemy')

    def move(self, direction):
        super().move(direction)

    def hit(self):
        super().hit()
        print("Enemy hit")


# Az egyhelyben álló folyamatosan lövő ellenfél
class PlantEnemy(Enemy):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.canShoot = True
        self.canMove = False
        self.shootCooldown = 0

    def drawEnemy(self, window):
        super().drawEnemy(window)
        
    def hit(self):
        super().hit()

    # Hogy garantálom, hogy az animáció lejátszódjon mielőtt lő és utánna viszamegy idle-be?
    # self.shootingFrameCount = iterateFrames(self, window, plane_attack_left_frames, self.shootingFrameCount, 8)
    def shoot(self, direction):
        if self.shootCooldown == 0:
            self.isShooting = True
            super().shoot(direction)
        self.shootCooldown = 90
