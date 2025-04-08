import os
import unittest
import pygame

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Game')))
from Game.Entity.Projectile import EnemyProjectile
from Game.Entity.Enemy import Enemy


class TestEnemy(unittest.TestCase):
    def setUp(self):
        self.dummy_enemy = Enemy(51, 52, 'l')

    def test_correct_init(self):
        self.assertEqual(self.dummy_enemy.x, 51)
        self.assertEqual(self.dummy_enemy.y, 52)
        self.assertEqual(self.dummy_enemy.width, 32)
        self.assertEqual(self.dummy_enemy.height, 32)
        self.assertEqual(self.dummy_enemy.vel, 5)
        self.assertEqual(self.dummy_enemy.health, 1)
        self.assertFalse(self.dummy_enemy.canShoot)
        self.assertTrue(self.dummy_enemy.canMove)
        self.assertEqual(self.dummy_enemy.idleFrameCount, 0)
        self.assertEqual(self.dummy_enemy.movingFrameCount, 0)
        self.assertEqual(self.dummy_enemy.shootingFrameCount, 0)
        self.assertFalse(self.dummy_enemy.isShooting)
        self.assertTrue(self.dummy_enemy.isAlive)
        self.assertTrue(self.dummy_enemy.canBeJumped)
        self.assertTrue(self.dummy_enemy.isIdle)
        self.assertTrue(self.dummy_enemy.facingLeft)
        self.assertFalse(self.dummy_enemy.facingRight)
        self.assertFalse(self.dummy_enemy.isMoving)
        self.assertEqual(self.dummy_enemy.hitbox, pygame.Rect(51, 52, 30, 40))

    def test_incorrect_init(self):
        with self.assertRaises(ValueError):
            Enemy(1, 1, 'jobbra')
            Enemy(1, 1, 1)

        with self.assertRaises(TypeError):
            Enemy('string', 1)
            Enemy(1, 'string')

    def test_hit(self):
        self.dummy_enemy.hit()

        self.assertEqual(self.dummy_enemy.health, 0)
        self.assertFalse(self.dummy_enemy.isAlive)
        self.assertFalse(self.dummy_enemy.isVisible)

    def test_correct_shoot(self):
        # Nem tud lőni
        self.assertEqual(self.dummy_enemy.shoot(1), None)

        # Tud lőni
        self.dummy_enemy.canShoot = True
        self.assertTrue(isinstance(self.dummy_enemy.shoot(1), EnemyProjectile))

        self.pos_bullet = self.dummy_enemy.shoot(1)
        self.assertEqual(self.pos_bullet.x, round(51 + 32 // 2))
        self.assertEqual(self.pos_bullet.y, round(52 + 32 // 2))
        self.assertEqual(self.pos_bullet.dir, 1)

        self.neg_bullet = self.dummy_enemy.shoot(-1)
        self.assertEqual(self.neg_bullet.x, round(51 + 32 // 2))
        self.assertEqual(self.neg_bullet.y, round(52 + 32 // 2))
        self.assertEqual(self.neg_bullet.dir, -1)

    def test_incorrect_shoot(self):
        self.dummy_enemy.canShoot = True
        with self.assertRaises(ValueError):
            self.dummy_enemy.shoot(2)
            self.dummy_enemy.shoot(-50)
            self.dummy_enemy.shoot(10.1)
            self.dummy_enemy.shoot('asd')

    def test_correct_canMove_move(self):
        self.dummy_enemy.move('left')
        self.assertEqual(self.dummy_enemy.x, 46)
        self.assertFalse(self.dummy_enemy.isIdle)
        self.assertTrue(self.dummy_enemy.isMoving)
        self.assertTrue(self.dummy_enemy.facingLeft)
        self.assertFalse(self.dummy_enemy.facingRight)

        self.dummy_enemy.move('right')
        self.assertEqual(self.dummy_enemy.x, 51)
        self.assertFalse(self.dummy_enemy.isIdle)
        self.assertTrue(self.dummy_enemy.isMoving)
        self.assertFalse(self.dummy_enemy.facingLeft)
        self.assertTrue(self.dummy_enemy.facingRight)

    def test_correct_cantMove_move(self):
        self.dummy_enemy.canMove = False
        self.dummy_enemy.move('left')
        self.assertEqual(self.dummy_enemy.x, 51)
        self.assertTrue(self.dummy_enemy.isIdle)
        self.assertFalse(self.dummy_enemy.isMoving)
        self.assertTrue(self.dummy_enemy.facingLeft)
        self.assertFalse(self.dummy_enemy.facingRight)

    def test_incorrect_move(self):
        with self.assertRaises(ValueError):
            self.dummy_enemy.move('asd')
            self.dummy_enemy.move(1)
            self.dummy_enemy.move(1.5)
            self.dummy_enemy.move(-50)
