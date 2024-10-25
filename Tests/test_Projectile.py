import os
import pytest
from unittest.mock import patch, MagicMock
import pygame

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Game')))
from Game.Entity.Projectile import Projectile, FriendlyProjectile, EnemyProjectile


@pytest.fixture
def setup_pygame():
    pygame.init()
    yield
    pygame.quit()

def test_Projectile_init(setup_pygame):
    #<editor-fold desc= "Helyes innit">

    defaultProjectilepos = Projectile(100, 100, 1)
    assert defaultProjectilepos.x == 100
    assert defaultProjectilepos.y == 100
    assert defaultProjectilepos.dir == 1
    assert defaultProjectilepos.hitbox == pygame.Rect(100 - 5, 100 - 5, 10, 10)
    assert defaultProjectilepos.color == pygame.Color('blue')
    assert defaultProjectilepos._vel == 10 * 1
    assert defaultProjectilepos._isFriendly == None

    defaultProjectileneg = Projectile(100, 100, -1)
    assert defaultProjectileneg.x == 100
    assert defaultProjectileneg.y == 100
    assert defaultProjectileneg.dir == -1
    assert defaultProjectileneg.hitbox == pygame.Rect(100 - 5, 100 - 5, 10, 10)
    assert defaultProjectileneg.color == pygame.Color('blue')
    assert defaultProjectileneg._vel == 10 * -1
    assert defaultProjectileneg._isFriendly == None

    #</editor-fold>

    # <editor-fold desc= "Helytelen innit">
    with pytest.raises(TypeError):
        Projectile(100, 100, 'not 1 or -1')
    with pytest.raises(TypeError):
        Projectile(100, 100, -999)
    with pytest.raises(TypeError):
        Projectile('not int or float', 100, 1)
    with pytest.raises(TypeError):
        Projectile(100, 'not int or float', 1)
    with pytest.raises(TypeError):
        Projectile(100, 100, 1.5)

    # </editor-fold>