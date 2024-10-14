
import pytest
from Game.Entity import Player


# teszt generálás Pycharmban, AI plugin telepítése
# pytest unittest helyett
# DM-be van egy csomó hasznos link tanuláshoz

@pytest.fixture
def player1():
    return Player.Player(0, 0, 50, 50)


def test_invalid_attribute():
    with pytest.raises(TypeError):
        Player.Player('0', 0, 50, 50)
