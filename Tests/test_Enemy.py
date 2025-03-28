import os
import pytest
from unittest.mock import patch, MagicMock
import pygame
from Game.Entity.Projectile import EnemyProjectile

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Game')))
from Game.Entity.Enemy import Enemy

@pytest.fixture
def setup_pygame():
    pygame.init()
    yield
    pygame.quit()

@patch('Game.Game_Graphics.Graphics_Loader.mc_idle_right_frames', new_callable=MagicMock)
def test_enemy_initialization(mock_defenemy_frames, setup_pygame):
    mock_defenemy_frames.return_value = [pygame.Surface((50, 50))]
    # Helytelen innit
    with pytest.raises(TypeError):
        Enemy('not int', 50, 'l')
    with pytest.raises(TypeError):
        Enemy(50, 'not int', 'l')
    with pytest.raises(ValueError):
        Enemy(50, 50, 50)
    with pytest.raises(ValueError):
        Enemy(50, 50, 'asd')

    # Helyes innit
    enemy = Enemy(51, 52, 'l')
    assert enemy.x == 51
    assert enemy.y == 52
    assert enemy.width == 32
    assert enemy.height == 32
    assert enemy._vel == 5
    assert enemy.health == 1
    assert not enemy.canShoot
    assert enemy.canMove
    assert enemy.idleFrameCount == 0
    assert enemy.movingFrameCount == 0
    assert enemy.shootingFrameCount == 0
    assert not enemy.isShooting
    assert enemy.isAlive
    assert enemy._canBeJumped
    assert enemy.isIdle
    assert enemy.facingLeft
    assert not enemy.facingRight
    assert not enemy.isMoving
    assert enemy.hitbox == pygame.Rect(51, 52, 30, 40)

@patch('Game.Game_Graphics.Graphics_Loader.mc_idle_right_frames', new_callable=MagicMock)
def test_enemy_methods(mock_defenemy_frames, setup_pygame):
    mock_defenemy_frames.return_value = [pygame.Surface((50, 50))]

    # <editor-fold desc="Enemy hit">
    enemy = Enemy(51, 52, 'l')
    enemy.hit()
    assert enemy.x == 51
    assert enemy.y == 52
    assert enemy.width == 32
    assert enemy.height == 32
    assert enemy._vel == 5
    assert enemy.health == 0
    assert not enemy.canShoot
    assert enemy.canMove
    assert enemy.idleFrameCount == 0
    assert enemy.movingFrameCount == 0
    assert enemy.shootingFrameCount == 0
    assert not enemy.isShooting
    assert not enemy.isAlive
    assert enemy._canBeJumped
    assert enemy.isIdle
    assert enemy.facingLeft
    assert not enemy.facingRight
    assert not enemy.isMoving
    assert enemy.hitbox == pygame.Rect(51, 52, 30, 40)

    del enemy

    # </editor-fold>

    # <editor-fold desc="Enemy shoot">

        # Rossz innit
    enemy = Enemy(51,52,'l')
    enemy.canShoot = True
    with pytest.raises(ValueError):
        enemy.shoot(2)
    with pytest.raises(ValueError):
        enemy.shoot(-50)
    with pytest.raises(ValueError):
        enemy.shoot(1.4)
    with pytest.raises(ValueError):
        enemy.shoot('str')
    with pytest.raises(ValueError):
        enemy.shoot('-1')

    del enemy
        # Helyes innit, de nem tud lőni
    enemy = Enemy(51,52,'l')

    assert enemy.shoot(1) is None
    assert enemy.shoot(-1) is None

        # Helyes innit és tud is lőni

    enemy.canShoot = True
    assert isinstance(enemy.shoot(1), EnemyProjectile)
    assert enemy.shoot(1).dir == 1
    assert enemy.shoot(1)
    assert enemy.shoot(1).x == round(enemy.x + enemy.width // 2)
    assert enemy.shoot(1).y == round(enemy.y + enemy.height // 2)

    assert isinstance(enemy.shoot(-1), EnemyProjectile)
    assert enemy.shoot(-1).dir == -1
    assert enemy.shoot(-1)
    assert enemy.shoot(-1).x == round(enemy.x + enemy.width // 2)
    assert enemy.shoot(-1).y == round(enemy.y + enemy.height // 2)

    del enemy
    # </editor-fold>

    # <editor-fold desc="Enemy move">
    enemy = Enemy(51,52,'l')

    # Helytelen argumentumok
    with pytest.raises(ValueError):
        enemy.move(1)
    with pytest.raises(ValueError):
        enemy.move(-1)
    with pytest.raises(ValueError):
        enemy.move('not left')
    with pytest.raises(ValueError):
        enemy.move('not right')

    # Helyes argumentumok, de nem tud mozogni
    enemy.canMove = False
    enemy.move('left')

    assert enemy.x == 51
    assert enemy.y == 52
    assert enemy.width == 32
    assert enemy.height == 32
    assert enemy._vel == 5
    assert enemy.health == 1
    assert not enemy.canShoot
    assert not enemy.canMove
    assert enemy.idleFrameCount == 0
    assert enemy.movingFrameCount == 0
    assert enemy.shootingFrameCount == 0
    assert not enemy.isShooting
    assert enemy.isAlive
    assert enemy._canBeJumped
    assert enemy.isIdle
    assert enemy.facingLeft
    assert not enemy.facingRight
    assert not enemy.isMoving
    assert enemy.hitbox == pygame.Rect(51, 52, 30, 40)

    del enemy

    # Helyes argumentumok és tud is mozogni

    enemy = Enemy(51, 52, 'l')
    enemy.canMove = True
    enemy.move('left')

    assert enemy.x == 46
    assert enemy.y == 52
    assert enemy.width == 32
    assert enemy.height == 32
    assert enemy._vel == 5
    assert enemy.health == 1
    assert not enemy.canShoot
    assert enemy.canMove
    assert enemy.idleFrameCount == 0
    assert enemy.movingFrameCount == 0
    assert enemy.shootingFrameCount == 0
    assert not enemy.isShooting
    assert enemy.isAlive
    assert enemy._canBeJumped
    assert not enemy.isIdle
    assert enemy.facingLeft
    assert not enemy.facingRight
    assert enemy.isMoving
    assert enemy.hitbox == pygame.Rect(51, 52, 30, 40)

    del enemy
    # </editor-fold>