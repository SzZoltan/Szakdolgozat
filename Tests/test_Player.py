import os
import pytest
from unittest.mock import patch, MagicMock
import pygame

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Game')))
from Game.Entity.Player import Player  # Importáld a Player osztályt

# mock Player a grafikák elkerülésért talán?
# pytest unittest helyett
# DM-be van egy csomó hasznos link tanuláshoz
@pytest.fixture
def setup_pygame():
    pygame.init()
    yield
    pygame.quit()

@patch('Game.Game_Graphics.Graphics_Loader.mc_idle_right_frames', new_callable=MagicMock)

def test_player_initialization(mock_idle_frames, setup_pygame):

    mock_idle_frames.return_value = [pygame.Surface((50, 50))]

    player = Player(100, 100, 25, 25)

    assert player.hitbox.topleft == (100, 100)
    assert player.width == 25
    assert player.height == 25


def test_invalid_attribute():
    with pytest.raises(TypeError):
        Player('not int', 0, 50, 50)
    with pytest.raises(TypeError):
        Player(1.5, 0, 50, 50)
    with pytest.raises(TypeError):
        Player(0, 'not int', 50, 50)
    with pytest.raises(TypeError):
        Player(0, 0.15, 50, 50)
    with pytest.raises(TypeError):
        Player(0, 0, 'not int', 50)
    with pytest.raises(TypeError):
        Player(0, 0, 50.2, 50)
    with pytest.raises(TypeError):
        Player(0, 0, 50, 'not int')
    with pytest.raises(TypeError):
        Player(0, 0, 50, 50.1)
