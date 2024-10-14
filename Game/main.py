import pygame
from Game.Entity.PowerUp import (Apple, Pineapple, Strawberry, Cherry)
from Game.Entity.Player import Player
from Game.Entity.Enemy import (BunnyEnemy)
from Game.Game_Graphics.Graphics_Loader import level1_bg

pygame.init()

# Az animációk 20 FPS-re vannak megcsinálva
clock = pygame.time.Clock()


# Unit tesztelés extrém tesztesetek
# A háttér
def drawBackground():
    for row in range(tiles_down):
        for col in range(tiles_across):
            x_pos = col * level1_bg.get_width()
            y_pos = row * level1_bg.get_height()
            win.blit(level1_bg, (x_pos, y_pos))


def drawProjectiles():
    for fproj in friendlyProjectiles:
        fproj.draw(win)


def redrawGameWindow():
    win.fill((0, 0, 0))
    drawBackground()
    mc.drawPlayer(win)
    apple.drawApple(win)
    pineapple.drawPineapple(win)
    cherry.drawCherry(win)
    strawberry.drawStrawberry(win)
    drawProjectiles()
    bunny.drawEnemy(win)
    pygame.display.update()

# Terv: Az alapokat kifejelszteni: player, block, projectile,powerup, enemy, block alapú map editor elkészítése és
# miután ez megvan: pályák ,egy főmenü, score system, leaderboard


window_width = 500
window_height = 500
tiles_across = window_width // level1_bg.get_width()+1
tiles_down = window_height // level1_bg.get_height()+1

win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('MyGame')


mc = Player(0, 255, 32, 32)
apple = Apple(200, 255, 32, 32)
cherry = Cherry(250, 255, 32, 32)
pineapple = Pineapple(150, 255, 32, 32)
strawberry = Strawberry(300, 255, 32, 32)
bunny = BunnyEnemy(100, 255, 32, 32)
friendlyProjectiles = []
enemyProjectiles = []
invincibleTimer = 0

# shootLimit azért hogy legyen egy kis delay a lövések között
shootLimit = 0
run = True

# Mainloop
while run:
    clock.tick(20)

    keys = pygame.key.get_pressed()

    for proj in friendlyProjectiles:
        if window_width > proj.x > 0:
            proj.x += proj.vel
            # hit check ide jön majd kell majd projectile hit method
        else:
            friendlyProjectiles.pop(friendlyProjectiles.index(proj))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not any(keys):
        mc.isRunning = False
        mc.isIdle = True

    if keys[pygame.K_LEFT]:
        mc.move('left')

    if keys[pygame.K_RIGHT]:
        mc.move('right')

    if shootLimit > 0:
        shootLimit += 1
    if shootLimit > 3:
        shootLimit = 0

    if keys[pygame.K_SPACE]:
        mc.isIdle = True
        if mc.canShoot and shootLimit == 0:
            if len(friendlyProjectiles) < 5:
                if mc.facingRight:
                    friendlyProjectiles.append(mc.shoot(1))
                else:
                    friendlyProjectiles.append(mc.shoot(-1))
                shootLimit = 1

    if mc.isInvincible:
        if invincibleTimer > 0:
            invincibleTimer -= 1
            print(f'{invincibleTimer} miliseconds remaining')
        else:
            print('no longer invincible')
            mc.isInvincible = False

    if mc.hitbox.colliderect(pineapple.hitbox) and pineapple.isVisible:
        pineapple.pickUp(mc)
    if mc.hitbox.colliderect(apple.hitbox) and apple.isVisible:
        apple.pickUp(mc)
    if mc.hitbox.colliderect(cherry.hitbox) and cherry.isVisible:
        cherry.pickUp(mc)
    if mc.hitbox.colliderect(strawberry.hitbox) and strawberry.isVisible:
        invincibleTimer = 200
        strawberry.pickUp(mc)

    if bunny.x >= 0:
        bunny.move('left')

    if mc.hitbox.colliderect(bunny.hitbox) and mc.isInvincible and bunny.isAlive:
        bunny.hit()

    if mc.hitbox.colliderect(bunny.hitbox) and bunny.isAlive and mc.hp > 0:
        if mc.hitbox.bottom < bunny.hitbox.top + 15:
            bunny.hit()
        else:
            mc.hit()

    # Ugrás viselkedés: Parabola megoldás
    if not mc.isJump:
        if keys[pygame.K_UP]:
            mc.isJump = True
    else:
        mc.jump()
    redrawGameWindow()

pygame.quit()
