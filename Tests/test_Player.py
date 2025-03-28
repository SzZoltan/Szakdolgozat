import os
import pytest
from unittest.mock import patch, MagicMock
import pygame
from Game.Entity.Projectile import FriendlyProjectile

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Game')))
from Game.Entity.Player import Player


@pytest.fixture
def setup_pygame():
    pygame.init()
    yield
    pygame.quit()


@patch('Game.Game_Graphics.Graphics_Loader.mc_idle_right_frames', new_callable=MagicMock)
def test_player_initialization(mock_idle_frames, setup_pygame):
    mock_idle_frames.return_value = [pygame.Surface((50, 50))]
    # Helytelen argumentumok
    with pytest.raises(TypeError):
        Player('not int', 0)
    with pytest.raises(TypeError):
        Player(0, 'not int')

    # Helyes inicializálás
    player = Player(100, 100)

    assert player.hitbox.topleft == (100, 100)
    assert player.width == 32
    assert player.height == 32
    assert player.hp == 1
    assert player.x == 100
    assert player.y == 100
    assert player.lives == 3
    assert player.vel == 7
    assert player.jumpCount == 10
    assert player.idleFrameCount == 0
    assert player.runningFrameCount == 0
    assert player.iFrames == 0
    assert not player.isInvincible
    assert not player.canShoot
    assert not player.isFalling
    assert not player.isJump
    assert player.isIdle
    assert not player.facingLeft
    assert player.facingRight
    assert not player.isRunning


@patch('Game.Game_Graphics.Graphics_Loader.mc_idle_right_frames', new_callable=MagicMock)
@patch('Game.Game_Graphics.Graphics_Loader.mc_jump_right_frames', new_callable=MagicMock)
def test_player_jump(mock_mc_jump, mock_idle_frames, setup_pygame):
    mock_mc_jump.return_value = [pygame.Surface((50, 50))]
    mock_idle_frames.return_value = [pygame.Surface((50, 50))]

    # Ugrás amikor nem lehet
    player = Player(100, 100)
    player.jump()
    assert player.jumpCount == 10
    assert player.y == 100
    assert not player.isJump
    assert not player.isFalling

    # Ugrás mikor lehet
    player.isFalling = False
    player.isJump = True
    player.jumpCount = 10
    player.jump()
    assert player.jumpCount == 9
    assert player.y == 65
    assert player.isJump

    # Ugrás vége
    player.jumpCount = -10
    player.isFalling = False
    player.isJump = True
    player.jump()
    assert player.jumpCount == 10
    player.isFalling = True
    player.isJump = False


@patch('Game.Game_Graphics.Graphics_Loader.mc_idle_right_frames', new_callable=MagicMock)
def test_player_hit(mock_idle_frames, setup_pygame):
    mock_idle_frames.return_value = [pygame.Surface((50, 50))]
    player = Player(100, 100)

    # Általános hit 1 hp-ról 0-ra
    player.hit()
    assert player.hp == 0
    assert player.iFrames == 30

    # Invincible Player-re meghívjuk a hit függvény
    player.hp = 1
    player.iFrames = 0
    player.isInvincible = True
    player.hit()
    assert player.hp == 1
    assert player.iFrames == 0

    # Negatív lehet a hp teszt
    player.hp = 1
    player.isInvincible = False
    player.hit()
    player.hit()
    assert player.hp == 0


@patch('Game.Game_Graphics.Graphics_Loader.mc_idle_right_frames', new_callable=MagicMock)
@patch('Game.Game_Graphics.Graphics_Loader.mc_idle_left_frames', new_callable=MagicMock)
@patch('Game.Game_Graphics.Graphics_Loader.mc_run_right_frames', new_callable=MagicMock)
@patch('Game.Game_Graphics.Graphics_Loader.mc_run_left_frames', new_callable=MagicMock)
def test_player_move(mock_idle_right_frames, mock_idle_left_frames, mock_mc_run_right, mock_mc_run_left, setup_pygame):
    mock_idle_right_frames.return_value = [pygame.Surface((50, 50))]
    mock_idle_left_frames.return_value = [pygame.Surface((50, 50))]
    mock_mc_run_left.return_value = [pygame.Surface((50, 50))]
    mock_mc_run_right.return_value = [pygame.Surface((50, 50))]
    player = Player(100, 100)

    # Invalid move tesztek
    with pytest.raises(ValueError):
        player.move(12)

    with pytest.raises(ValueError):
        player.move('not a dir')

    # Helyes input balra
    player.move('left')
    assert player.x == 93
    assert player.y == 100
    assert player.isIdle is False
    assert player.facingRight is False
    assert player.facingLeft is True
    assert player.isRunning is True
    del player

    # Helyes input jobbra
    player = Player(150, 100)
    player.move('right')
    assert player.x == 157
    assert player.y == 100
    assert player.isIdle is False
    assert player.facingRight is True
    assert player.facingLeft is False
    assert player.isRunning is True


@patch('Game.Game_Graphics.Graphics_Loader.mc_idle_right_frames', new_callable=MagicMock)
@patch('Game.Entity.Projectile.FriendlyProjectile', new_callable=MagicMock)
def test_player_shoot(mock_idle_frames, mock_projectile, setup_pygame):
    mock_idle_frames.return_value = [pygame.Surface((50, 50))]

    # Rossz direction
    player = Player(100, 100)
    player.canShoot = True
    with pytest.raises(ValueError):
        player.shoot('wrong')
    with pytest.raises(ValueError):
        player.shoot(99)
    with pytest.raises(ValueError):
        player.shoot(-99)
    with pytest.raises(ValueError):
        player.shoot(-1.5)

    # canShoot False-al lőni
    player.canShoot = False
    assert player.shoot(1) is None
    assert player.shoot(-1) is None

    # Helyes viselkedés
    player.canShoot = True
    assert isinstance(player.shoot(1), FriendlyProjectile)
    assert player.shoot(1).dir == 1
    assert player.shoot(1).x == round(player.x + player.width // 2)
    assert player.shoot(1).y == round(player.y + player.height // 2)

    assert isinstance(player.shoot(-1), FriendlyProjectile)
    assert player.shoot(-1).dir == -1
    assert player.shoot(-1).x == round(player.x + player.width // 2)
    assert player.shoot(-1).y == round(player.y + player.height // 2)

@patch('Game.Game_Graphics.Graphics_Loader.mc_idle_right_frames', new_callable=MagicMock)
def test_player_clear_effects(mock_idle_frames, setup_pygame):
    mock_idle_frames.return_value = [pygame.Surface((50, 50))]
    player = Player(100, 100)
    player.clear_effects()
    assert player.hp == 1
    assert player.isInvincible is False
    assert player.isFalling is False
    assert player.isJump is False
    assert player.isRunning is False
    assert player.isIdle is True
    assert player.facingRight is True
    assert player.facingLeft is False
    assert player.canShoot is False
    assert player.iFrames == 0
    assert player.jumpCount == 10
