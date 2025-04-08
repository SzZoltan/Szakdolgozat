import os
import unittest
import pygame

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Game')))
from Game.Entity.PowerUp import Powerup, Apple, Pineapple, Cherry, Strawberry, Finish
from Game.Entity.Player import Player


class TestPowerUp(unittest.TestCase):
    def setUp(self):
        self.powerUp = Powerup(0, 1, 4, 5)
        self.dummyPlayer = Player(0, 0)

    def test_correct_init(self):
        self.assertEqual(self.powerUp.x, 0)
        self.assertEqual(self.powerUp.y, 1)
        self.assertEqual(self.powerUp.width, 4)
        self.assertEqual(self.powerUp.height, 5)
        self.assertEqual(self.powerUp.hitbox, pygame.Rect(5, 6, 20, 20))
        self.assertTrue(self.powerUp.isVisible)
        self.assertEqual(self.powerUp.frameCount, 0)
        self.assertEqual(self.powerUp.maxframes, 17)

    def test_incorrect_init(self):
        with self.assertRaises(TypeError):
            Powerup('string', 1, 4, 5)
            Powerup(1, 'string', 4, 5)
            Powerup(1, 1, 'string', 5)
            Powerup(1, 1, 4, 'string')

    def test_correct_setters(self):
        self.powerUp.x = 9
        self.assertEqual(self.powerUp.x, 9)

        self.powerUp.y = 10
        self.assertEqual(self.powerUp.y, 10)

        self.powerUp.hitbox = pygame.Rect(5, 6, 20, 20)
        self.assertEqual(self.powerUp.hitbox, pygame.Rect(5, 6, 20, 20))

        self.powerUp.isVisible = False
        self.assertFalse(self.powerUp.isVisible)

        self.powerUp.frameCount = 12
        self.assertEqual(self.powerUp.frameCount, 12)

    def test_incorrect_setters(self):
        with self.assertRaises(TypeError):
            self.powerUp.hitbox = 'not rect'
            self.powerUp.isVisible = 'not bool'
            self.powerUp.frameCount = '12'
            self.powerUp.frames = 'some string'

    def test_correct_apple_pickup(self):
        self.apple = Apple(0, 0, 0, 0)

        # Alma felvétel
        self.apple.pickUp(self.dummyPlayer)
        self.assertFalse(self.apple.isVisible)
        self.assertEqual(self.dummyPlayer.hp, 2)

    def test_correct_pineapple_pickup(self):
        self.pineapple = Pineapple(0, 0, 0, 0)

        # Ananász felvétel
        self.pineapple.pickUp(self.dummyPlayer)
        self.assertFalse(self.pineapple.isVisible)
        self.assertEqual(self.dummyPlayer.lives, 4)

    def test_correct_cherry_pickup(self):
        self.cherry = Cherry(0, 0, 0, 0)

        # Cseresznye felvétel
        self.cherry.pickUp(self.dummyPlayer)
        self.assertFalse(self.cherry.isVisible)
        self.assertTrue(self.dummyPlayer.canShoot)

    def test_correct_strawberry_pickup(self):
        self.strawberry = Strawberry(0, 0, 0, 0)

        # Eper felvétel
        self.strawberry.pickUp(self.dummyPlayer)
        self.assertFalse(self.strawberry.isVisible)
        self.assertTrue(self.dummyPlayer.isInvincible)
        self.assertEqual(self.dummyPlayer.iFrames, 100)

    def test_correct_finish_pickup(self):
        self.finish = Finish(0, 0, 0, 0)

        # Finish felvétel
        self.finish.pickUp(self.dummyPlayer)
        self.assertFalse(self.finish.isVisible)

    def test_correct_generic_pickup(self):
        # Generikus PowerUp felvétel
        self.powerUp.pickUp(self.dummyPlayer)
        self.assertFalse(self.powerUp.isVisible)

    def test_incorrect_pickup(self):
        self.apple = Apple(0, 0, 0, 0)
        self.pineapple = Pineapple(0, 0, 0, 0)
        self.cherry = Cherry(0, 0, 0, 0)
        self.strawberry = Strawberry(0, 0, 0, 0)
        self.finish = Finish(0, 0, 0, 0)

        with self.assertRaises(TypeError):
            self.powerUp.pickUp('not player')
            self.apple.pickUp('not player')
            self.pineapple.pickUp('not player')
            self.cherry.pickUp('not player')
            self.strawberry.pickUp('not player')
            self.finish.pickUp('not player')
