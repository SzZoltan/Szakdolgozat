import os
import pytest
from unittest.mock import patch, MagicMock
import pygame

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Game')))
from Game.Entity.PowerUp import Powerup, Apple, Pineapple, Cherry, Strawberry, Finish
from Game.Entity.Player import Player


@pytest.fixture
def setup_pygame():
    pygame.init()
    yield
    pygame.quit()


@patch('Game.Game_Graphics.Graphics_Loader.apple_frames', new_callable=MagicMock)
def test_PowerUp_initialization(mock_apple_frames, setup_pygame):
    mock_apple_frames.return_value = [pygame.Surface((50, 50))]
    # Helytelen argumentumok
    with pytest.raises(TypeError):
        Powerup('not int', 0, 50, 50)
    with pytest.raises(TypeError):
        Powerup(0, 'not int', 50, 50)
    with pytest.raises(TypeError):
        Powerup(0, 0, 'not int', 50)
    with pytest.raises(TypeError):
        Powerup(0, 0, 50.2, 50)
    with pytest.raises(TypeError):
        Powerup(0, 0, 50, 'not int')
    with pytest.raises(TypeError):
        Powerup(0, 0, 50, 50.1)

    # Helyes inicializálás
    defaultPowerup = Powerup(100, 100, 25, 25)

    assert defaultPowerup.hitbox.topleft == (100 + 5, 100 + 5)
    assert defaultPowerup.width == 25
    assert defaultPowerup.height == 25
    assert defaultPowerup.frameCount == 0
    assert defaultPowerup.isVisible
    assert defaultPowerup.x == 100
    assert defaultPowerup.y == 100
    assert defaultPowerup.frameCount == 0
    assert defaultPowerup.isVisible


@patch('Game.Game_Graphics.Graphics_Loader.apple_frames', new_callable=MagicMock)
@patch('Game.Game_Graphics.Graphics_Loader.pineapple_frames', new_callable=MagicMock)
@patch('Game.Game_Graphics.Graphics_Loader.cherry_frames', new_callable=MagicMock)
@patch('Game.Game_Graphics.Graphics_Loader.strawberry_frames', new_callable=MagicMock)
def test_PowerUpPickUp(mock_apple_frames, mock_pineapple_frames, mock_cherry_frames, mock_strawberry_frames,
                       setup_pygame):
    mock_apple_frames.return_value = [pygame.Surface((50, 50))]
    mock_pineapple_frames.return_value = [pygame.Surface((50, 50))]
    mock_cherry_frames.return_value = [pygame.Surface((50, 50))]
    mock_strawberry_frames.return_value = [pygame.Surface((50, 50))]
    player = Player(100, 100)

    # <editor-fold desc="Default PowerUp">

    defaultPowerup = Powerup(100, 100, 25, 25)
    defaultPowerup.pickUp(player)

    assert not defaultPowerup.isVisible
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

    del player
    # </editor-fold>

    # <editor-fold desc="Apple PowerUp">

    apple = Apple(100, 100, 25, 25)
    player = Player(100, 100)
    apple.pickUp(player)

    assert not apple.isVisible
    assert player.hitbox.topleft == (100, 100)
    assert player.width == 32
    assert player.height == 32
    assert player.hp == 2
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

    del player
    # </editor-fold>

    # <editor-fold desc="Pineapple PowerUp">

    player = Player(100, 100)
    pineapple = Pineapple(100, 100, 25, 25)
    pineapple.pickUp(player)

    assert not pineapple.isVisible
    assert player.hitbox.topleft == (100, 100)
    assert player.width == 32
    assert player.height == 32
    assert player.hp == 1
    assert player.x == 100
    assert player.y == 100
    assert player.lives == 4
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

    del player
    # </editor-fold>

    # <editor-fold desc="Cherry PowerUp">
    cherry = Cherry(100, 100, 25, 25)
    player = Player(100, 100)

    cherry.pickUp(player)
    assert not cherry.isVisible
    assert not defaultPowerup.isVisible
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
    assert player.canShoot
    assert not player.isFalling
    assert not player.isJump
    assert player.isIdle
    assert not player.facingLeft
    assert player.facingRight
    assert not player.isRunning

    del player

    # </editor-fold>

    # <editor-fold desc="Strawberry PowerUp">
    player = Player(100, 100)
    strawberry = Strawberry(100, 100, 25, 25)
    strawberry.pickUp(player)

    assert not strawberry.isVisible
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
    assert player.iFrames == 100
    assert player.isInvincible
    assert not player.canShoot
    assert not player.isFalling
    assert not player.isJump
    assert player.isIdle
    assert not player.facingLeft
    assert player.facingRight
    assert not player.isRunning

    del player
    # </editor-fold>

    # <editor-fold desc="Finish">
    player = Player(100, 100)
    finish = Finish(100, 100, 25, 25)
    finish.pickUp(player)

    assert not strawberry.isVisible
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

    del player
    # </editor-fold>

    # Helytelen Pickup argumentum
    with pytest.raises(TypeError):
        defaultPowerup.pickUp('not player')
    with pytest.raises(TypeError):
        apple.pickUp('not player')
    with pytest.raises(TypeError):
        pineapple.pickUp('not player')
    with pytest.raises(TypeError):
        cherry.pickUp('not player')
    with pytest.raises(TypeError):
        strawberry.pickUp('not player')
    with pytest.raises(TypeError):
        finish.pickUp('not player')