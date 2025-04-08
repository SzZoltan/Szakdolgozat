import os
import unittest
import pygame
from Game.Entity.Projectile import FriendlyProjectile

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Game')))
from Game.Entity.Player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.dummyPlayer = Player(100, 101)

    def test_correct_init(self):
        self.assertEqual(self.dummyPlayer.x, 100)
        self.assertEqual(self.dummyPlayer.y, 101)
        self.assertEqual(self.dummyPlayer.width, 32)
        self.assertEqual(self.dummyPlayer.height, 32)
        self.assertEqual(self.dummyPlayer.lives, 3)
        self.assertEqual(self.dummyPlayer.hp, 1)
        self.assertEqual(self.dummyPlayer.vel, 7)
        self.assertEqual(self.dummyPlayer.jumpCount, 10)
        self.assertEqual(self.dummyPlayer.idleFrameCount, 0)
        self.assertEqual(self.dummyPlayer.runningFrameCount, 0)
        self.assertEqual(self.dummyPlayer.iFrames, 0)
        self.assertEqual(self.dummyPlayer.hitbox, pygame.Rect(100, 101, 30, 35))
        self.assertFalse(self.dummyPlayer.isInvincible)
        self.assertFalse(self.dummyPlayer.canShoot)
        self.assertFalse(self.dummyPlayer.isFalling)
        self.assertFalse(self.dummyPlayer.isJump)
        self.assertFalse(self.dummyPlayer.facingLeft)
        self.assertFalse(self.dummyPlayer.isRunning)
        self.assertTrue(self. dummyPlayer.isIdle)
        self.assertTrue(self. dummyPlayer.facingRight)

    def test_incorrect_init(self):
        with self.assertRaises(TypeError):
            Player('asd', 0)
            Player(0, 'asd')

    def test_jump(self):
        # Ugrás amikor nem lehet
        self.dummyPlayer.jump()

        self.assertEqual(self.dummyPlayer.jumpCount, 10)
        self.assertEqual(self.dummyPlayer.y, 101)
        self.assertFalse(self.dummyPlayer.isJump)
        self.assertFalse(self.dummyPlayer.isFalling)

        # Ugrás mikor lehet
        self.dummyPlayer.isFalling = False
        self.dummyPlayer.isJump = True
        self.dummyPlayer.jump()

        self.assertEqual(self.dummyPlayer.jumpCount, 9)
        self.assertEqual(self.dummyPlayer.y, 66)
        self.assertTrue(self.dummyPlayer.isJump)

        # Ugrás vége
        self.dummyPlayer.jumpCount = -10
        self.dummyPlayer.jump()

        self.assertEqual(self.dummyPlayer.jumpCount, 10)
        self.assertFalse(self.dummyPlayer.isJump)
        self.assertTrue(self.dummyPlayer.isFalling)

    def test_hit(self):
        # Nem hal meg a sebbződésbe
        self.dummyPlayer.hp = 2
        self.dummyPlayer.hit()

        self.assertEqual(self.dummyPlayer.hp, 1)
        self.assertEqual(self.dummyPlayer.iFrames, 30)

        # Iframe-ekkel próbál sérülni

        self.dummyPlayer.hit()

        self.assertEqual(self.dummyPlayer.hp, 1)
        self.assertEqual(self.dummyPlayer.iFrames, 30)

        # Invincible játékosra meghívjuk
        self.dummyPlayer.iFrames = 0
        self.dummyPlayer.isInvincible = True
        self.dummyPlayer.hit()

        self.assertEqual(self.dummyPlayer.hp, 1)
        self.assertEqual(self.dummyPlayer.iFrames, 0)

        # Belehal a sebbződésbe
        self.dummyPlayer.isInvincible = False
        self.dummyPlayer.hit()

        self.assertEqual(self.dummyPlayer.hp, 0)
        self.assertEqual(self.dummyPlayer.iFrames, 30)

        # Negatívba esne az élete
        self.dummyPlayer.iFrames = 0
        self.dummyPlayer.hit()

        self.assertEqual(self.dummyPlayer.hp, 0)
        self.assertEqual(self.dummyPlayer.iFrames, 30)

    def test_clear_effects(self):
        self.dummyPlayer.clear_effects()

        self.assertEqual(self.dummyPlayer.hp, 1)
        self.assertEqual(self.dummyPlayer.iFrames, 0)
        self.assertEqual(self.dummyPlayer.jumpCount, 10)
        self.assertFalse(self.dummyPlayer.isInvincible)
        self.assertFalse(self.dummyPlayer.isJump)
        self.assertFalse(self.dummyPlayer.isFalling)
        self.assertFalse(self.dummyPlayer.isRunning)
        self.assertFalse(self.dummyPlayer.canShoot)
        self.assertTrue(self.dummyPlayer.isIdle)
        self.assertFalse(self.dummyPlayer.facingLeft)
        self.assertTrue(self.dummyPlayer.facingRight)

    def test_incorrect_move(self):
        with self.assertRaises(ValueError):
            self.dummyPlayer.move(10)
            self.dummyPlayer.move(-10)
            self.dummyPlayer.move('wrong')

    def test_correct_move(self):
        # Helyes input balra
        self.dummyPlayer.move('left')

        self.assertEqual(self.dummyPlayer.x, 93)
        self.assertEqual(self.dummyPlayer.y, 101)
        self.assertFalse(self.dummyPlayer.isIdle)
        self.assertFalse(self.dummyPlayer.facingRight)
        self.assertTrue(self.dummyPlayer.facingLeft)
        self.assertTrue(self.dummyPlayer.isRunning)

        # Helyes input jobbra
        self.dummyPlayer.move('right')
        self.assertEqual(self.dummyPlayer.x, 100)
        self.assertEqual(self.dummyPlayer.y, 101)
        self.assertFalse(self.dummyPlayer.isIdle)
        self.assertFalse(self.dummyPlayer.facingLeft)
        self.assertTrue(self.dummyPlayer.facingRight)
        self.assertTrue(self.dummyPlayer.isRunning)

    def test_incorrect_shoot(self):
        with self.assertRaises(ValueError):
            self.dummyPlayer.shoot(1.5)
            self.dummyPlayer.shoot(-2)
            self.dummyPlayer.shoot(2)
            self.dummyPlayer.shoot('asd')

    def test_correct_shoot(self):
        # Nem tud lőni
        self.dummyPlayer.canShoot = False

        self.assertEqual(self.dummyPlayer.shoot(1), None)
        self.assertEqual(self.dummyPlayer.shoot(-1), None)

        # Tud lőni
        self.dummyPlayer.canShoot = True

        self.assertTrue(self.dummyPlayer.shoot(1), FriendlyProjectile)
        self.assertEqual(self.dummyPlayer.shoot(1).dir, 1)
        self.assertEqual(self.dummyPlayer.shoot(1).x, round(100 + 32 // 2))
        self.assertEqual(self.dummyPlayer.shoot(1).y, round(101 + 32 // 2))

        self.assertTrue(self.dummyPlayer.shoot(-1), FriendlyProjectile)
        self.assertEqual(self.dummyPlayer.shoot(-1).dir, -1)
        self.assertEqual(self.dummyPlayer.shoot(-1).x, round(100 + 32 // 2))
        self.assertEqual(self.dummyPlayer.shoot(-1).y, round(101 + 32 // 2))
