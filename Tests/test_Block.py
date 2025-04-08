import os
import unittest
import pygame

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Game')))
from Game.Entity.Block import Block, GoldBlock, Inside
from Game.Entity.PowerUp import Apple


class TestBlock(unittest.TestCase):
    def setUp(self):
        self.dummy_block = Block(10, 5)

    def test_correct_init(self):
        self.assertEqual(self.dummy_block.x, 10)
        self.assertEqual(self.dummy_block.y, 5)
        self.assertEqual(self.dummy_block.width, 40)
        self.assertEqual(self.dummy_block.height, 40)
        self.assertEqual(self.dummy_block.hitbox, pygame.Rect(10, 5, 40, 40))
        self.assertTrue(self.dummy_block.isVisible)
        self.assertTrue(self.dummy_block.isBreakable)
        self.assertFalse(self.dummy_block.isContainer)
        self.assertEqual(self.dummy_block.inside, Inside.NOTHING)

    def test_incorrect_init(self):
        with self.assertRaises(TypeError):
            Block('10', 5)
            Block(10, '5')

    def test_correct_setters(self):
        self.dummy_block.x = 11
        self.assertEqual(self.dummy_block.x, 11)

        self.dummy_block.y = 6
        self.assertEqual(self.dummy_block.y, 6)

        self.dummy_block.width = 9
        self.assertEqual(self.dummy_block.width, 9)

        self.dummy_block.height = 7
        self.assertEqual(self.dummy_block.height, 7)

        self.dummy_block.hitbox = pygame.Rect(50, 50, 40, 40)
        self.assertEqual(self.dummy_block.hitbox, pygame.Rect(50, 50, 40, 40))

        self.dummy_block.inside = Inside.APPLE
        self.assertEqual(self.dummy_block.inside, Inside.APPLE)

        self.dummy_block.isVisible = False
        self.assertFalse(self.dummy_block.isVisible)

        self.dummy_block.isBreakable = False
        self.assertFalse(self.dummy_block.isBreakable)

        self.dummy_block.isContainer = False
        self.assertFalse(self.dummy_block.isContainer)

    def test_incorrect_setters(self):
        with self.assertRaises(TypeError):
            self.dummy_block.x = 'string'
            self.dummy_block.y = 'string'
            self.dummy_block.width = 'string'
            self.dummy_block.height = 'string'
            self.dummy_block.hitbox = 'string'
            self.dummy_block.inside = 'string'
            self.dummy_block.isVisible = 'string'
            self.dummy_block.isBreakable = 'string'
            self.dummy_block.isContainer = 'string'

    def test_destroy(self):
        self.gold_apple_block = GoldBlock(10, 5, inside=Inside.APPLE)

        self.assertEqual(self.dummy_block.destroy(), None)
        self.assertEqual(self.dummy_block.isVisible, False)

        self.dummy_block.isBreakable = False
        self.dummy_block.isVisible = True
        self.dummy_block.destroy()
        self.assertEqual(self.dummy_block.isVisible, True)

        self.assertTrue(isinstance(self.gold_apple_block.destroy(), Apple))
        self.assertFalse(self.gold_apple_block.isVisible)
