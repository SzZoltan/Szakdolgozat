import os
import unittest
import pygame

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Game')))
from Game.Entity.Projectile import Projectile, FriendlyProjectile, EnemyProjectile


class TestProjectile(unittest.TestCase):
    def setUp(self):
        self.correct_positive = Projectile(100, 10, 1)
        self.correct_negative = Projectile(100, 5, -1)

    def test_correct_init(self):
        self.assertEqual(self.correct_positive.x, 100)
        self.assertEqual(self.correct_positive.y, 10)
        self.assertEqual(self.correct_positive.dir, 1)
        self.assertEqual(self.correct_positive.hitbox, pygame.Rect(100 - 5, 10 - 5, 10, 10))
        self.assertEqual(self.correct_positive.color, pygame.Color('blue'))
        self.assertEqual(self.correct_positive.vel, 10)
        self.assertEqual(self.correct_positive.isFriendly, None)

        self.assertEqual(self.correct_negative.x, 100)
        self.assertEqual(self.correct_negative.y, 5)
        self.assertEqual(self.correct_negative.dir, -1)
        self.assertEqual(self.correct_negative.hitbox, pygame.Rect(100 - 5, 5 - 5, 10, 10))
        self.assertEqual(self.correct_negative.color, pygame.Color('blue'))
        self.assertEqual(self.correct_negative.vel, -10)
        self.assertEqual(self.correct_negative.isFriendly, None)

    def test_incorrect_init(self):
        with self.assertRaises(TypeError):
            Projectile("100", 100, 1)

        with self.assertRaises(TypeError):
            Projectile(100, "100", -1)

        with self.assertRaises(TypeError):
            Projectile(100, 100, 0)

    def test_correct_setters(self):
        self.correct_positive.x = 101
        self.assertEqual(self.correct_positive.x, 101)

        self.correct_positive.y = 11
        self.assertEqual(self.correct_positive.y, 11)

        self.correct_positive.dir = -1
        self.assertEqual(self.correct_positive.dir, -1)

        self.correct_positive.hitbox = pygame.Rect(101 - 5, 11 - 5, 10, 10)
        self.assertEqual(self.correct_positive.hitbox, pygame.Rect(101 - 5, 11 - 5, 10, 10))

        self.correct_positive.color = pygame.Color('red')
        self.assertEqual(self.correct_positive.color, pygame.Color('red'))

        self.correct_positive.isFriendly = True
        self.assertEqual(self.correct_positive.isFriendly, True)

        self.correct_positive.x = 101.1
        self.assertEqual(self.correct_positive.x, 101.1)

        self.correct_positive.y = 11.1
        self.assertEqual(self.correct_positive.y, 11.1)

    def test_incorrect_setters(self):
        with self.assertRaises(TypeError):
            self.correct_positive.x = "not int"
            self.correct_positive.y = "not int"
            self.correct_positive.dir = 2
            self.correct_positive.dir = "not int"
            self.correct_positive.hitbox = "not rect"
            self.correct_positive.color = "not color"
            self.correct_positive.isFriendly = "not bool"
