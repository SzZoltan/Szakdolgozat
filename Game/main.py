import pygame

from Game.Entity import PowerUp
from Game.Entity.Block import Block, GoldBlock, SteelBlock, BrickBlock, Inside
from Game.Entity.PowerUp import (Apple, Pineapple, Strawberry, Cherry, Powerup)
from Game.Entity.Player import Player
from Game.Entity.Enemy import (BunnyEnemy, PlantEnemy)
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
    for eproj in enemyProjectiles:
        eproj.draw(win)


def drawPowerUp():
    for pup in poweruplist:
        pup.drawPowerup(win)


def drawBlocks():
    for blocks in blocklist:
        blocks.draw(win)


def drawEnemies():
    for e in enemylist:
        if e.isVisible:
            e.drawEnemy(win)


def redrawGameWindow():
    win.fill((0, 0, 0))
    drawBackground()
    mc.drawPlayer(win)
    drawPowerUp()
    drawProjectiles()
    drawEnemies()
    drawBlocks()
    pygame.display.update()

# Terv: Az alapokat kifejelszteni: player, block, projectile,powerup, enemy, block alapú map editor elkészítése és
# miután ez megvan: pályák ,egy főmenü, score system, leaderboard


offset_x = 205
window_width = 500
window_height = 500
map_width = 600
tiles_across = map_width // level1_bg.get_width()+1
tiles_down = window_height // level1_bg.get_height()+1

win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('MyGame')


mc = Player(0, 255)
apple = Apple(200, 255)
cherry = Cherry(250, 255)
pineapple = Pineapple(150, 255)
strawberry = Strawberry(300, 255)
bunny = BunnyEnemy(100, 255)
plant = PlantEnemy(400, 255)
plant2 = PlantEnemy(550, 255)
invincibleTimer = 0
testgoldblock = GoldBlock(30, 200, Inside.APPLE)
testbrick = BrickBlock(70, 200)
teststeel = SteelBlock(110, 200)
testbrick2 = BrickBlock(190, 290)
endbrick = BrickBlock(600, 255)
# shootLimit azért hogy legyen egy kis delay a lövések között
shootLimit = 0
friendlyProjectiles = []
enemyProjectiles = []
blocklist = [testbrick, teststeel, testgoldblock, testbrick2, endbrick]
poweruplist = [apple, cherry, pineapple, strawberry]
entitylist = [mc, bunny, plant, plant2]
enemylist = [bunny, plant, plant2]
spritelist = blocklist + poweruplist + entitylist + friendlyProjectiles + enemyProjectiles
run = True

# Mainloop
while run:
    clock.tick(20)
    spritelist = blocklist + poweruplist + entitylist + friendlyProjectiles + enemyProjectiles
    keys = pygame.key.get_pressed()

    # Friendly Projectile
    for proj in friendlyProjectiles:
        popped = False
        if window_width > proj.x > 0:
            proj.x += proj.vel
        else:
            friendlyProjectiles.pop(friendlyProjectiles.index(proj))
            popped = True
            break
        for enemy in enemylist:
            if popped:
                break
            if proj.hitbox.colliderect(enemy.hitbox) and enemy.isAlive:
                enemy.hit()
                friendlyProjectiles.pop(friendlyProjectiles.index(proj))
                popped = True
                break
        for block in blocklist:
            if popped:
                break
            if proj.hitbox.colliderect(block.hitbox):
                friendlyProjectiles.pop(friendlyProjectiles.index(proj))
                popped = True
                break

    # Enemy projectiles
    for proj in enemyProjectiles:
        popped = False
        if window_width > proj.x > 0:
            proj.x += proj.vel
        else:
            enemyProjectiles.pop(enemyProjectiles.index(proj))
            popped = True
            break
        for block in blocklist:
            if popped:
                break
            if proj.hitbox.colliderect(block.hitbox):
                enemyProjectiles.pop(enemyProjectiles.index(proj))
                popped = True
                break
        if not popped and proj.hitbox.colliderect(mc.hitbox):
            mc.hit()
            enemyProjectiles.pop(enemyProjectiles.index(proj))
            break

    # Gravitáció
    for entity in entitylist:
        for block in blocklist:
            if entity.isAlive and entity.hitbox.colliderect(block.hitbox):
                if (entity.hitbox.bottom+block.height-10 < block.hitbox.bottom
                        and block.isVisible and entity.isAlive):
                    entity.isFalling = False
                    break
            elif entity.y+entity.height >= 320:
                entity.isFalling = False
            else:
                entity.isFalling = True
        if entity.isFalling:
            entity.y += 7

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not any(keys):
        mc.isRunning = False
        mc.isIdle = True

    if keys[pygame.K_LEFT]:
        collision = False
        for block in blocklist:
            if mc.hitbox.colliderect(block.hitbox):
                if (block.hitbox.right > mc.hitbox.left > block.hitbox.left and mc.hitbox.bottom +
                        block.height/2 > block.hitbox.bottom and block.isVisible):
                    collision = True
        if not collision and mc.x != 0:
            mc.move('left')

    if keys[pygame.K_RIGHT]:
        collision = False
        for block in blocklist:
            if mc.hitbox.colliderect(block.hitbox):
                if (block.hitbox.left < mc.hitbox.right < block.hitbox.right and mc.hitbox.bottom +
                        block.height/2 > block.hitbox.bottom and block.isVisible):
                    collision = True
        if not collision and mc.x != window_width - 30:
            if mc.x + offset_x > endbrick.x:
                mc.move('right')
            elif mc.x == offset_x:
                for sprites in spritelist:
                    sprites.x -= mc.vel
                mc.move('right')
            else:
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

    for enemies in enemylist:
        if enemies.canShoot and enemies.isVisible:
            if enemies.facingLeft:
                proj = enemies.shoot(-1)
                if proj is not None:
                    enemyProjectiles.append(proj)
            else:
                proj = enemies.shoot(1)
                if proj is not None:
                    enemyProjectiles.append(proj)

    if mc.isInvincible:
        if invincibleTimer > 0:
            invincibleTimer -= 1
            print(f'{invincibleTimer} miliseconds remaining')
        else:
            print('no longer invincible')
            mc.isInvincible = False

    for powerup in poweruplist:
        if mc.hitbox.colliderect(powerup.hitbox) and isinstance(powerup, Strawberry):
            invincibleTimer = 200
            powerup.pickUp(mc)
            poweruplist.remove(powerup)
        if mc.hitbox.colliderect(powerup.hitbox) and not isinstance(powerup, Strawberry):
            powerup.pickUp(mc)
            poweruplist.remove(powerup)

    if bunny.x >= 0:
        bunny.move('left')

    for enemies in enemylist:
        if enemies.x < window_width and enemies.x+enemies.width > 0:
            enemies.isVisible = True
        if mc.hitbox.colliderect(enemies.hitbox) and mc.isInvincible and enemies.isAlive:
            enemies.hit()
        if mc.hitbox.colliderect(enemies.hitbox) and enemies.isAlive and mc.hp > 0:
            if enemies.canBeJumped and mc.hitbox.bottom < enemies.hitbox.top + 15:
                enemies.hit()
                mc.bounce()
            else:
                mc.hit()

    for block in blocklist:
        if mc.hitbox.colliderect(block.hitbox) and block.isVisible:
            if (mc.hitbox.bottom > block.hitbox.bottom and mc.hitbox.left + 25 > block.hitbox.left and
                    mc.hitbox.right - 25 < block.hitbox.right and mc.isJump):
                result = block.destroy()
                mc.interruptJump()
                if result is not None:
                    poweruplist.append(result)

    # Ugrás viselkedés: fél-Parabola megoldás
    if not mc.isJump and not mc.isFalling:
        if keys[pygame.K_UP]:
            mc.isJump = True
    else:
        mc.jump()
    redrawGameWindow()

pygame.quit()
