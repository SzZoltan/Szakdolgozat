import pygame
from Game.Entity.Projectile import EnemyProjectile
from Game.Game_Graphics.Graphics_Loader import (iterateFrames, bunny_run_left_frames, bunny_run_right_frames,
                                                bunny_idle_left_frames, bunny_idle_right_frames, mc_run_left_frames,
                                                mc_run_right_frames, mc_idle_left_frames, mc_idle_right_frames,
                                                plant_idle_left_frames, plant_idle_right_frames,
                                                plant_attack_right_frames, plant_attack_left_frames,
                                                turtle_idle_unspiked_frames, turtle_idle_spiked_frames,
                                                turtle_spikes_in_frames, turtle_spikes_out_frames)


# Enemy viselkedés
# Az összes ellenfélnek az alapja mind öröklődik innen

class Enemy:
    """
    Ez az Ellenfél osztályok őse, innen őröklődnek le a különböző Ellenfelek
    """
    def __init__(self, x: int or float, y: int or float, direction: str = 'l'):
        """
        Inicializálja az Enemy objektumot és általában a leszármazottak ezt fogják meghívni
        :param x: int vagy float, x koordinátája
        :param y: int vagy float, y koordinátája
        :param direction: 'r' jobbra vagy 'l' balra, melyik irányba nézzen, alapértelmezetten (balra)
        """
        self._x = x
        self._y = y
        self._width = 32
        self._height = 32
        self._vel = 5
        self._health = 1
        self._canShoot = False
        self._canMove = True
        self._idleFrameCount = 0
        self._movingFrameCount = 0
        self._shootingFrameCount = 0
        self._isShooting = False
        self._isAlive = True
        self._canBeJumped = True
        self._isIdle = True
        self._isMoving = False
        self._isFalling = False
        self._isVisible = False
        self._hitbox = pygame.Rect(self.x, self.y, 30, 40)
        if direction == 'l':
            self._facingLeft = True
            self._facingRight = False
        elif direction == 'r':
            self._facingLeft = False
            self._facingRight = True
        else:
            raise ValueError('Direction must be either "l" or "r"')

    # <editor-fold desc="Property-k és setterek">
    @property
    def x(self):
        """
        Az ellenfelek x koordinátáját adja vissza
        :return: int vagy float, x koordinátát
        """
        return self._x

    @property
    def y(self):
        """
        Az ellenfelek y koordinátáját adja vissza
        :return: int vagy float, y koordinátát
        """
        return self._y

    @property
    def width(self):
        """
        Az ellenfelek szélességét adja vissza
        :return: int, szélesség
        """
        return self._width

    @property
    def height(self):
        """
        Az ellenfelek magasságát adja vissza
        :return: int,  magasság
        """
        return self._height

    @property
    def vel(self):
        """
        Az ellenfelek sebességét adja vissza
        :return: int, sebbeség
        """
        return self._vel

    @property
    def health(self):
        """
        Az ellenfelek életerejét adja vissza
        :return: int, életerő
        """
        return self._health

    @property
    def idleFrameCount(self):
        """
        Az ellenfelek tétlen állapotában lévő képcokájának a jelenlegi számát adja vissza
        :return: int, ami a jelenlegi képre mutat
        """
        return self._idleFrameCount

    @property
    def movingFrameCount(self):
        """
        Az ellenfelek mozgás állapotában lévő képcokájának a jelenlegi számát adja vissza
        :return: int, ami a jelenlegi képre mutat
        """
        return self._movingFrameCount

    @property
    def canShoot(self):
        """
        Az ellenfelek lövési képességének jelenlegi értékét adja vissza
        :return: bool, ami megmondja, hogy tud-e lőni az ellenfél
        """
        return self._canShoot

    @property
    def canMove(self):
        """
        Az ellenfelek mozgási képességének jelenlegi értékét adja vissza
        :return: bool, ami megmondja, hogy tud-e mozogni az ellenfél
        """
        return self._canMove

    @property
    def canBeJumped(self):
        """
        Az ellenfelek-re rá lehet-e ugrani változó jelenlegi értékét adja vissza
        :return: bool, ami megmondja, hogy rá lehet-e ugrani az ellenfélre
        """
        return self._canBeJumped

    @property
    def isIdle(self):
        """
        Az ellenfelek tétlen állapotának az értékét adja vissza
        :return: bool ami megmondja, hogy az ellenfél az tétlen-e
        """
        return self._isIdle

    @property
    def shootingFrameCount(self):
        """
        Az ellenfelek lövésének képcokájának a jelenlegi számát adja vissza
        :return: int, ami a jelenlegi képre mutat
        """
        return self._shootingFrameCount

    @property
    def isShooting(self):
        """
        Az ellenfelek jelenleg lőnek-e állapotát adja vissza
        :return: bool, ami azt mondja, hogy lő-e most az ellenfél
        """
        return self._isShooting

    @property
    def isAlive(self):
        """
        Az ellenfelek jelenleg élnek-e állapotát adja vissza
        :return: bool, ami azt mondja, hogy él-e ellenfél
        """
        return self._isAlive

    @property
    def facingLeft(self):
        """
        Az ellenfelek jelenleg balra néznek-e értékét adja vissza
        :return: bool, ami azt mondja, hogy balra néz-e az ellenfél
        """
        return self._facingLeft

    @property
    def facingRight(self):
        """
        Az ellenfelek jelenleg jobbra néznek-e értékét adja vissza
        :return: bool, ami azt mondja, hogy jobbra néz-e az ellenfél
        """
        return self._facingRight

    @property
    def isMoving(self):
        """
        Az ellenfelek jelenleg mozognak-e változót adja vissza
        :return: bool, ami azt mondja, hogy mozog-e az ellenfél
        """
        return self._isMoving

    @property
    def hitbox(self):
        """
        Az ellenfelek hitboxát adja vissza
        :return: pygame.Rect változó ami az ellenfél hitboxára utal
        """
        return self._hitbox

    @property
    def isVisible(self):
        """
        Az ellenfelek jelenleg láthatóak-e változót adja vissza
        :return: bool, ami azt mondja, hogy látható-e az ellenfél
        """
        return self._isVisible

    @property
    def isFalling(self):
        """
        Az ellenfelek jelenleg esnek-e változót adja vissza
        :return: bool, ami azt mondja, hogy esik-e az ellenfél
        """
        return self._isFalling

    @x.setter
    def x(self, x: int or float):
        """
        Beállítja az ellenfelek x koordinátáját
        :param x: int vagy float érték amire beállítja az x kordinátát
        """
        if not isinstance(x, (int, float)):
            raise TypeError("x must be an integer of float")
        self._x = x

    @y.setter
    def y(self, y: int or float):
        """
        Beállítja az ellenfelek y koordinátáját
        :param y: int vagy float érték amire beállítja az y kordinátát
        """
        if not isinstance(y, (int, float)):
            raise TypeError("y must be an integer or float")
        self._y = y

    @width.setter
    def width(self, width: int):
        """
        Beállítja az ellenfelek szélességét
        :param width: int, amire beállítja a szélességet
        """
        if not isinstance(width, int):
            raise TypeError("width must be an integer")
        self._width = width

    @height.setter
    def height(self, height: int):
        """
        Beállítja az ellenfelek magasságát
        :param height: int, amire beállítja a magasságot
        """
        if not isinstance(height, int):
            raise TypeError("height must be an integer")
        self._height = height

    @health.setter
    def health(self, health: int):
        """
        Beállítja az ellenfelek életerejét
        :param health: int, amire beállítja az életerőt
        """
        if not isinstance(health, int):
            raise TypeError("health must be an integer")
        self._health = health

    @idleFrameCount.setter
    def idleFrameCount(self, idleFrameCount: int):
        """
        Beállítja az ellenfelek tétlen állapotában lévő képkockának a mutatóját
        :param idleFrameCount: int, amire beállítja a képkocka számlálót
        """
        if not isinstance(idleFrameCount, int):
            raise TypeError("idleFrameCount must be an integer")
        self._idleFrameCount = idleFrameCount

    @movingFrameCount.setter
    def movingFrameCount(self, movingFrameCount: int):
        """
        Beállítja az ellenfelek mozgó állapotában lévő képkockának a mutatóját
        :param movingFrameCount: int, amire beállítja a képkocka számlálót
        """
        if not isinstance(movingFrameCount, int):
            raise TypeError("movingFrameCount must be an integer")
        self._movingFrameCount = movingFrameCount

    @shootingFrameCount.setter
    def shootingFrameCount(self, shootingFrameCount: int):
        """
        Beállítja az ellenfelek lövő állapotában lévő képkockának a mutatóját
        :param shootingFrameCount: int, érték amire beállítja a képkocka számlálót
        """
        if not isinstance(shootingFrameCount, int):
            raise TypeError("shootingFrameCount must be an integer")
        self._shootingFrameCount = shootingFrameCount

    @isShooting.setter
    def isShooting(self, isShooting: bool):
        """
        Beállítja az ellenfelek lőnek-e változó értékét
        :param isShooting: bool, érték ami beállítja, hogy jelenleg lő-e az ellenfél
        """
        if not isinstance(isShooting, bool):
            raise TypeError("isShooting must be a bool")
        self._isShooting = isShooting

    @isAlive.setter
    def isAlive(self, isAlive: bool):
        """
        Beállítja az ellenfelek élnek-e változó értékét
        :param isAlive: bool, érték ami beállítja, hogy jelenleg él-e az ellenfél
        """
        if not isinstance(isAlive, bool):
            raise TypeError("isAlive must be a bool")
        self._isAlive = isAlive

    @facingLeft.setter
    def facingLeft(self, facingLeft: bool):
        """
        Beállítja az ellenfelek balra néznek-e változó értékét
        :param facingLeft: bool, érték ami beállítja, hogy jelenleg balra néz-e az ellenfél
        """
        if not isinstance(facingLeft, bool):
            raise TypeError("facingLeft must be a bool")
        self._facingLeft = facingLeft

    @facingRight.setter
    def facingRight(self, facingRight: bool):
        """
        Beállítja az ellenfelek jobbra néznek-e változó értékét
        :param facingRight: bool, érték ami beállítja, hogy jelenleg jobbra néz-e az ellenfél
        """
        if not isinstance(facingRight, bool):
            raise TypeError("facingRight must be a bool")
        self._facingRight = facingRight

    @isIdle.setter
    def isIdle(self, isIdle: bool):
        """
        Beállítja az ellenfelek tétlenek-e változó értékét
        :param isIdle: bool, érték ami beállítja, hogy jelenleg tétlen-e az ellenfél
        """
        if not isinstance(isIdle, bool):
            raise TypeError("isIdle must be a bool")
        self._isIdle = isIdle

    @canBeJumped.setter
    def canBeJumped(self, canBeJumped: bool):
        """
        Beállítja az ellenfelek rá lehet-e ugrani változó értékét
        :param canBeJumped: bool, érték ami beállítja, hogy jelenleg rá lehet-e ugrani az ellenfélre
        """
        if not isinstance(canBeJumped, bool):
            raise TypeError("canBeJumped must be a bool")
        self._canBeJumped = canBeJumped

    @isMoving.setter
    def isMoving(self, isMoving: bool):
        """
        Beállítja az ellenfelek jelenleg mozognak-e változó értékét
        :param isMoving: bool, érték ami beállítja, hogy jelenleg mozog-e az ellenfél
        """
        if not isinstance(isMoving, bool):
            raise TypeError("isMoving must be a bool")
        self._isMoving = isMoving

    @hitbox.setter
    def hitbox(self, hitbox: pygame.Rect):
        """
        Beállítja az ellenfelek hitbox változó értékét
        :param hitbox: pygame.Rect ami az új hitboxnak az értékét állitja be
        """
        if not isinstance(hitbox, pygame.Rect):
            raise TypeError("hitbox must be a pygame.Rect object")
        self._hitbox = hitbox

    @canShoot.setter
    def canShoot(self, canShoot: bool):
        """
        Beállítja az ellenfelek tudnak-e lőni változó értékét
        :param canShoot: bool, érték ami beállítja, hogy jelenleg tud-e lőni az ellenfél
        """
        if not isinstance(canShoot, bool):
            raise TypeError("canShoot must be a bool")
        self._canShoot = canShoot

    @canMove.setter
    def canMove(self, canMove: bool):
        """
        Beállítja az ellenfelek tudnak-e mozogni változó értékét
        :param canMove: bool, érték ami beállítja, hogy jelenleg mozog-e az ellenfél
        """
        if not isinstance(canMove, bool):
            raise TypeError("canMove must be a bool")
        self._canMove = canMove

    @isFalling.setter
    def isFalling(self, isFalling: bool):
        """
        Beállítja az ellenfelek jelenleg esnek-e változó értékét
        :param isFalling: bool, érték ami beállítja, hogy jelenleg esik-e az ellenfél
        """
        if not isinstance(isFalling, bool):
            raise TypeError("isFalling must be a bool")
        self._isFalling = isFalling

    @isVisible.setter
    def isVisible(self, isVisible: bool):
        """
        Beállítja az ellenfelek jelenleg láthatóak-e változó értékét
        :param isVisible: bool, érték ami beállítja, hogy jelenleg látható-e az ellenfél
        """
        if not isinstance(isVisible, bool):
            raise TypeError("isVisible must be a bool")
        self._isVisible = isVisible
    # </editor-fold>

    # Ez lesz a default Enemy animáció, a Főszereplő, de csak akkor ha nincs implementálva sajátja,
    # soha nem lesz hívva ha minden jól alakul
    def drawEnemy(self, window: pygame.Surface):
        """
        Felrajzolja az ellenfelet a megadott képernyőre
        :param window: pygame.Surface, az ablak amire rajzolja az Enemy-t
        """
        if isinstance(window, pygame.Surface):
            if self.isAlive:
                if self.isMoving:
                    if self.facingRight:
                        self.movingFrameCount = iterateFrames(self, window, mc_run_right_frames, self.movingFrameCount,
                                                              12)
                    else:
                        self.movingFrameCount = iterateFrames(self, window, mc_run_left_frames, self.movingFrameCount,
                                                              12)
                elif self.isIdle:
                    if self.facingRight:
                        self.idleFrameCount = iterateFrames(self, window, mc_idle_right_frames, self.idleFrameCount, 11)
                    else:
                        self.idleFrameCount = iterateFrames(self, window, mc_idle_left_frames, self.idleFrameCount, 11)
                self.hitbox = pygame.Rect(self.x, self.y, 30, 40)
        else:
            raise TypeError('Invalid window argument for drawEnemy')

    def hit(self):
        """
        Levesz 1 életerőt az élő ellenfél életerejéből, ha meghal ebbe akkor átírja az isAlive-ot is
        """
        if self.isAlive:
            self.health = self.health - 1
            if self.health == 0:
                self.isAlive = False

    def shoot(self, direction: int):
        """
        Az ellenfelek lővési képességét valósítsa meg, ha tudnak
        :param direction: 1 jobbra vagy -1 balra az irány amelyikbe szeretnénk lőni
        :return: A létrehozott ellenséges lövedék
        """
        if self.canShoot:
            if direction == 1 or direction == -1:
                if self.canShoot:
                    return EnemyProjectile(round(self.x + self.width // 2), round(self.y + self.height // 2), direction)
            else:
                raise ValueError('Invalid direction argument for Enemy shoot')

    def move(self, direction: str):
        """
        Az ellenfél mozgását valósítsa meg, ha tudnak
        :param direction: 'left', ha balra, 'right', ha jobbra más értékre hibát dob
        """
        if self.canMove:
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


class BunnyEnemy(Enemy):
    """
    A goomba féle ellenfél aki nem csinál semmit csak oda vissza járkál
    """
    def __init__(self, x: int or float, y: int or float, direction: str = 'l'):
        """
        Inicializálja a Bunny ellenfelet, az őst hívja meg
        :param x: int vagy float, x koordinátája
        :param y: int vagy float, y koordinátája
        :param direction: 'r' jobbra vagy 'l' balra, melyik irányba nézzen, alapértelmezetten (balra)
        """
        super().__init__(x, y, direction)
        self.canShoot = False
        self.canMove = True
        self.width = 32
        self.height = 32

    def drawEnemy(self, window: pygame.Surface):
        """
        Megrajzolja a Bunny ellenfelet a képernyőre bármilyen állapotban is legyen
        :param window: pygame.Surface, a képernyő amire rajzolni szeretnénk a Bunny-t
        """
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
                self.hitbox = pygame.Rect(self.x, self.y + 3, 30, 40)
        else:
            raise TypeError('Invalid window argument Bunny drawEnemy')

    def move(self, direction: str):
        """
        A Bunny ellenfél mozgását valósítssa meg, az Ősét hívja meg csak
        :param direction: 'left' balra, 'right' jobbra az irány amelyikbe menni szeretne
        """
        super().move(direction)

    def hit(self):
        """
        A Bunny ellenfél sebződését valósítsa meg, az Ősét hívja meg
        """
        super().hit()


class PlantEnemy(Enemy):
    """
    Az egyhelyben álló folyamatosan lövő ellenfél
    """
    def __init__(self, x: int or float, y: int or float, direction: str = 'l'):
        """
        Inicializálja a Plant ellenfelet, az őst hívja meg
        :param x: int vagy float, x koordinátája
        :param y: int vagy float, y koordinátája
        :param direction: 'r' jobbra vagy 'l' balra, melyik irányba nézzen, alapértelmezetten (balra)
        """
        super().__init__(x, y, direction)
        self.canShoot = True
        self.canMove = False
        self.shootCooldown = 45
        self.shootDelay = 8
        self.width = 32
        self.height = 32

    def drawEnemy(self, window: pygame.Surface):
        """
        Megrajzolja a Plant ellenfelet a képernyőre bármilyen állapotban is legyen
        :param window: pygame.Surface, a képernyő amire rajzolni szeretnénk a Plant-et
        """
        if isinstance(window, pygame.Surface):
            if self.isAlive:
                if self.isIdle:
                    if self.facingLeft:
                        self.idleFrameCount = iterateFrames(self, window, plant_idle_left_frames, self.idleFrameCount,
                                                            11)
                    else:
                        self.idleFrameCount = iterateFrames(self, window, plant_idle_right_frames, self.idleFrameCount,
                                                            11)
                elif self.isShooting:
                    if self.facingLeft:
                        self.shootingFrameCount = iterateFrames(self, window, plant_attack_left_frames,
                                                                self.shootingFrameCount, 8)
                    else:
                        self.shootingFrameCount = iterateFrames(self, window, plant_attack_right_frames,
                                                                self.shootingFrameCount, 8)
                if self.facingLeft:
                    self.hitbox = pygame.Rect(self.x+5, self.y, 40, 45)
                elif self.facingRight:
                    self.hitbox = pygame.Rect(self.x, self.y, 40, 45)
        else:
            raise TypeError('Invalid window argument Plant drawEnemy')

    def hit(self):
        """
        A Plant ellenfél sebződését valósítsa meg, az Ősét hívja meg
        """
        super().hit()

    def shoot(self, direction: int):
        """
        Megvalósítsa a Plant ellenfél lövését, késlelteti, hogy az animáció megfelelően lejátszódjon, az Őst hívja meg
        amikor lő
        :param direction: 1 jobbra vagy -1 balra az irány amelyikbe szeretnénk lőni
        :return: A létrehozott ellenséges lövedék
        """
        if self.canShoot and self.isAlive:
            if self.shootCooldown == 0:
                self.isIdle = False
                self.isShooting = True
                if self.shootCooldown == 0 and self.shootDelay == 3:
                    self.shootDelay -= 1
                    return super().shoot(direction)
                elif self.shootDelay == 0:
                    self.shootCooldown = 45
                    self.shootDelay = 8
                    self.isIdle = True
                    self.isShooting = False
                    self.shootingFrameCount = 0
                    self.idleFrameCount = 0
                else:
                    self.shootDelay -= 1
            else:
                self.shootCooldown -= 1


class TurtleEnemy(Enemy):
    """
     Az egyhelyben álló néha tüskés ellenfél akire csak akkor lehet ráugrani ha a tüskéi nincsenek kint,
     csak balra nézhet
    """
    def __init__(self, x: int or float, y: int or float):
        """
        Inicializálja a Turtle ellenfelet, az őst hívja meg, mivel csak balra nézhet ezért nincs direction paramétere
        :param x: int vagy float, x koordinátája
        :param y: int vagy float, y koordinátája
        """
        super().__init__(x, y, 'l')
        self.canMove = False
        self.isSpiked = True
        self.canBeJumped = False
        self.width = 32
        self.height = 16
        self.transitionFrameCount = 0
        self.spikeTransition = 50
        self.transitionTimer = 8

    def changeSpike(self):
        """
        A tüskés státuszát változtatja meg
        """
        self.isSpiked = not self.isSpiked
        if self.isSpiked:
            self.canBeJumped = False
        else:
            self.canBeJumped = True

    def drawEnemy(self, window: pygame.Surface):
        """
        Megrajzolja a Turtle ellenfelet bármilyk állapotában is legyen és a tranzíciót is tüskésből nem tüskésbe és
        fordítva is ez kezeli le
        :param window: pygame.Surface a felület amire rajzoljuk
        """
        if isinstance(window, pygame.Surface):
            if self.isAlive:
                if self.spikeTransition != 0:
                    if self.isSpiked:
                        self.idleFrameCount = iterateFrames(self, window, turtle_idle_spiked_frames,
                                                            self.idleFrameCount, 14)
                    else:
                        self.idleFrameCount = iterateFrames(self, window, turtle_idle_unspiked_frames,
                                                            self.idleFrameCount, 14)
                    self.spikeTransition -= 1
                else:
                    if self.transitionTimer != 0:
                        if self.isSpiked:
                            self.transitionFrameCount = iterateFrames(self, window, turtle_spikes_in_frames,
                                                                      self.transitionFrameCount, 8)
                        else:
                            self.transitionFrameCount = iterateFrames(self, window, turtle_spikes_out_frames,
                                                                      self.transitionFrameCount, 8)
                        self.transitionTimer -= 1
                    else:
                        self.changeSpike()
                        self.spikeTransition = 50
                        self.transitionTimer = 8
                        self.idleFrameCount = 0
                        self.transitionFrameCount = 0
                        if self.isSpiked:
                            self.idleFrameCount = iterateFrames(self, window, turtle_idle_spiked_frames,
                                                                self.idleFrameCount, 14)
                        else:
                            self.idleFrameCount = iterateFrames(self, window, turtle_idle_unspiked_frames,
                                                                self.idleFrameCount, 14)
                self.hitbox = pygame.Rect(self.x+3, self.y, 40, 25)

        else:
            raise TypeError('Invalid window argument Turtle drawEnemy')

    def hit(self):
        """
        A Turtle ellenfél sebződését valósítsa meg, az Ősét hívja meg
        """
        super().hit()
