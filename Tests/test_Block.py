import os
import pytest
from unittest.mock import patch, MagicMock
import pygame

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Game')))
from Game.Entity.Block import Block, BrickBlock, SteelBlock, GoldBlock, Inside
from Game.Entity.PowerUp import Apple

@pytest.fixture
def setup_pygame():
    pygame.init()
    yield
    pygame.quit()


@patch('Game.Game_Graphics.Graphics_Loader.brick_frame', new_callable=MagicMock)
def test_block_initialization(mock_brick_frames, setup_pygame):
    # Helytelen innit
    with pytest.raises(TypeError):
        Block('not int', 50)
    with pytest.raises(TypeError):
        Block(50, 'not int')
    with pytest.raises(TypeError):
        Block(50, 50, 'starwberry')

    # Helyes innit
    block = Block(50, 50)

    assert block.x == 50
    assert block.y == 50
    assert block.width == 40
    assert block.height == 40
    assert block.hitbox == pygame.Rect(50, 50, 40, 40)
    assert block.isBreakable
    assert not block.isContainer
    assert block.inside == Inside.NOTHING
    assert block.isVisible

    # Brick block innit

    brick_block = BrickBlock(50, 50)
    assert brick_block.x == 50
    assert brick_block.y == 50
    assert brick_block.width == 40
    assert brick_block.height == 40
    assert brick_block.hitbox == pygame.Rect(50, 50, 40, 40)
    assert brick_block.isBreakable
    assert not brick_block.isContainer
    assert brick_block.inside == Inside.NOTHING
    assert brick_block.isVisible

    # Steelblock innit
    steel_block = SteelBlock(50, 50)
    assert steel_block.x == 50
    assert steel_block.y == 50
    assert steel_block.width == 40
    assert steel_block.height == 40
    assert steel_block.hitbox == pygame.Rect(50, 50, 40, 40)
    assert not steel_block.isBreakable
    assert not steel_block.isContainer
    assert steel_block.inside == Inside.NOTHING
    assert steel_block.isVisible

    # Goldblock innit
    gold_block = GoldBlock(50, 50, Inside.APPLE)
    assert gold_block.x == 50
    assert gold_block.y == 50
    assert gold_block.width == 40
    assert gold_block.height == 40
    assert gold_block.hitbox == pygame.Rect(50, 50, 40, 40)
    assert gold_block.isBreakable
    assert gold_block.isContainer
    assert gold_block.inside == Inside.APPLE
    assert gold_block.isVisible

@patch('Game.Game_Graphics.Graphics_Loader.brick_frame', new_callable=MagicMock)
def test_block_destroy(mock_brick_frames, setup_pygame):
    block = Block(50, 50)
    assert block.destroy() is None

    assert block.x == 50
    assert block.y == 50
    assert block.width == 40
    assert block.height == 40
    assert block.hitbox == pygame.Rect(50, 50, 40, 40)
    assert block.isBreakable
    assert not block.isContainer
    assert block.inside == Inside.NOTHING
    assert not block.isVisible

    # Brick block innit

    brick_block = BrickBlock(50, 50)
    assert brick_block.destroy() is None

    assert brick_block.x == 50
    assert brick_block.y == 50
    assert brick_block.width == 40
    assert brick_block.height == 40
    assert brick_block.hitbox == pygame.Rect(50, 50, 40, 40)
    assert brick_block.isBreakable
    assert not brick_block.isContainer
    assert brick_block.inside == Inside.NOTHING
    assert not brick_block.isVisible

    # Steelblock innit
    steel_block = SteelBlock(50, 50)
    assert steel_block.destroy() is None

    assert steel_block.x == 50
    assert steel_block.y == 50
    assert steel_block.width == 40
    assert steel_block.height == 40
    assert steel_block.hitbox == pygame.Rect(50, 50, 40, 40)
    assert not steel_block.isBreakable
    assert not steel_block.isContainer
    assert steel_block.inside == Inside.NOTHING
    assert steel_block.isVisible

    # Goldblock innit
    gold_block = GoldBlock(50, 50, Inside.APPLE)
    assert isinstance(gold_block.destroy(), Apple)

    assert gold_block.x == 50
    assert gold_block.y == 50
    assert gold_block.width == 40
    assert gold_block.height == 40
    assert gold_block.hitbox == pygame.Rect(50, 50, 40, 40)
    assert gold_block.isBreakable
    assert gold_block.isContainer
    assert gold_block.inside == Inside.APPLE
    assert not gold_block.isVisible