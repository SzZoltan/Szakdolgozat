import sys

import pygame

from Game.Button.Button import Button
from Game.Entity.Block import Block, GoldBlock, SteelBlock, BrickBlock, Inside
from Game.Entity.PowerUp import (Apple, Pineapple, Strawberry, Cherry, Finish, Powerup)
from Game.Entity.Player import Player
from Game.Entity.Enemy import (BunnyEnemy, PlantEnemy, TurtleEnemy, Enemy)
from Game.Game_Graphics.Graphics_Loader import (level1_bg, pause_pic, unpause_pic, quit_btn_pic, full_heart_pic,
                                                half_heart_pic, empty_heart_pic, health_head_pic)

pygame.init()


def game_loop():
    # Az animációk 20 FPS-re vannak megcsinálva

    clock = pygame.time.Clock()
    second_counter = 20
    FPS = 20
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    score = 10000
    font = pygame.font.SysFont(None, 50)

    offset_x = 205
    window_width = 500
    window_height = 500
    tiles_across = window_width // level1_bg.get_width() + 1
    tiles_down = window_height // level1_bg.get_height() + 1
    game_paused = False

    pause_btn = Button(window_width - 50, 15, pause_pic, 1)
    unpause_btn = Button(window_width // 2 - 50, window_height // 2 - 50, unpause_pic, 1)
    quit_btn = Button(window_width // 2 - 70, window_height // 2, quit_btn_pic, 1)

    win = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Pink Guy's Adventures - Game")

    mc_spawn = 0
    mc = Player(0, 200)
    blocker = BrickBlock(0, 255)
    apple = Apple(200, 255)
    cherry = Cherry(250, 255)
    pineapple = Pineapple(150, 255)
    strawberry = Strawberry(300, 255)
    bunny = BunnyEnemy(100, 255)
    turtle = TurtleEnemy(130, 255)
    plant = PlantEnemy(400, 255)
    plant2 = PlantEnemy(550, 255)
    invincibleTimer = 0
    testgoldblock = GoldBlock(30, 200, Inside.APPLE)
    testbrick = BrickBlock(70, 200)
    teststeel = SteelBlock(110, 200)
    testbrick2 = BrickBlock(190, 290)
    finish = Finish(600, 255)

    # shootLimit azért hogy legyen egy kis delay a lövések között

    shootLimit = 0
    friendlyProjectiles = []
    enemyProjectiles = []
    blocklist = [testbrick, teststeel, testgoldblock, testbrick2, blocker]
    poweruplist = [apple, cherry, pineapple, strawberry, finish]
    entitylist = [mc, bunny, plant, plant2, turtle]
    enemylist = [bunny, plant, plant2, turtle]
    spritelist = blocklist + poweruplist + entitylist + friendlyProjectiles + enemyProjectiles

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
        drawBackground()
        mc.drawPlayer(win)
        drawPowerUp()
        drawProjectiles()
        drawEnemies()
        drawBlocks()
        draw_UI()

    def draw_UI():
        text = font.render(f"x {mc.lives}", True, WHITE)
        score_text = font.render(f"{score}", True, WHITE)
        if mc.hp == 1:
            win.blit(half_heart_pic, (10, 15))
        elif mc.hp == 2:
            win.blit(full_heart_pic, (10, 15))
        else:
            win.blit(empty_heart_pic, (10, 15))

        win.blit(health_head_pic, (75, 25))
        win.blit(text, (100, 15))
        win.blit(score_text, (window_width-200, 15))


    def show_pause_screen():
        overlay = pygame.Surface((window_width, window_height))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        win.blit(overlay, (0, 0))

        text = font.render("Paused", True, WHITE)
        win.blit(text, (window_width // 2 - 85, window_height // 2 - 100))

    # Terv: Az alapokat kifejelszteni:  pályák ,egy főmenü, score system, leaderboard

    run = True

    # Megnézi hogy az entitás ütközik-e valamelyik bolckal

    def collisionchecker(entity, direction):
        if isinstance(entity, Player) or isinstance(entity, Enemy):
            if direction == 'left':
                col = False
                for block in blocklist:
                    if entity.hitbox.colliderect(block.hitbox):
                        if (block.hitbox.right > entity.hitbox.left > block.hitbox.left and entity.hitbox.bottom +
                                block.height / 2 > block.hitbox.bottom and block.isVisible):
                            col = True
                            break
                return col
            elif direction == 'right':
                col = False
                for block in blocklist:
                    if entity.hitbox.colliderect(block.hitbox):
                        if (block.hitbox.left < entity.hitbox.right < block.hitbox.right and entity.hitbox.bottom +
                                block.height / 2 > block.hitbox.bottom and block.isVisible):
                            col = True
                            break
                return col
            else:
                raise ValueError('Direction must be either "left" or "right"')
        else:
            raise ValueError('entity must be Player or Enemy type')

    # ==================Mainloop==================

    while run:
        clock.tick(FPS)
        spritelist = blocklist + poweruplist + entitylist + friendlyProjectiles + enemyProjectiles
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if game_paused:
            if unpause_btn.draw(win):
                game_paused = not game_paused
            if quit_btn.draw(win):
                run = False
        else:
            redrawGameWindow()
            if pause_btn.draw(win):
                game_paused = not game_paused
                show_pause_screen()

            # ==================Gravitáció==================

            for entity in entitylist:
                for block in blocklist:
                    if entity.isAlive and entity.hitbox.colliderect(block.hitbox):
                        if (entity.hitbox.bottom + block.height - 10 < block.hitbox.bottom
                                and block.isVisible and entity.isAlive):
                            entity.isFalling = False
                            break
                    elif entity.y + entity.height >= 320:
                        entity.isFalling = False
                    else:
                        entity.isFalling = True
                if entity.isFalling:
                    entity.y += 7

            # ==================Friendly Projectile==================

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
                        score += 200
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

            # ==================Enemy projectiles==================

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

            # ==================PowerUps==================

            for powerup in poweruplist:
                if mc.hitbox.colliderect(powerup.hitbox):
                    if isinstance(powerup, Apple) and mc.hp == 2:
                        powerup.pickUp(mc)
                        poweruplist.remove(powerup)
                        score += 300
                    elif isinstance(powerup, Finish):
                        powerup.pickUp(mc)
                        poweruplist.remove(powerup)
                        score += 1000
                    else:
                        powerup.pickUp(mc)
                        poweruplist.remove(powerup)
                        score += 100

            # ==================Enemies==================

            # Enemy-k lövése

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

            # Enemy-k hit detektálása

            for enemies in enemylist:
                if enemies.x < window_width and enemies.x + enemies.width > 0:
                    enemies.isVisible = True
                if mc.hitbox.colliderect(enemies.hitbox) and mc.isInvincible and enemies.isAlive:
                    enemies.hit()
                    score += 200
                if mc.hitbox.colliderect(enemies.hitbox) and enemies.isAlive and mc.hp > 0:
                    if enemies.canBeJumped and mc.hitbox.bottom < enemies.hitbox.top + 15:
                        enemies.hit()
                        mc.bounce()
                        score += 200
                    else:
                        mc.hit()
                        mc.bounce()

            # Enemy-k mozgása

            for enemies in enemylist:
                if enemies.canMove:
                    if enemies.facingLeft:
                        left_collision = collisionchecker(enemies, 'left')
                        if left_collision is False:
                            enemies.move('left')
                        else:
                            enemies.move('right')
                    else:
                        right_collision = collisionchecker(enemies, 'right')
                        if right_collision is False:
                            enemies.move('right')
                        else:
                            enemies.move('left')

            # ==================Blocks==================

            for block in blocklist:
                if mc.hitbox.colliderect(block.hitbox) and block.isVisible:
                    if (mc.hitbox.bottom > block.hitbox.bottom and mc.hitbox.left + 25 > block.hitbox.left and
                            mc.hitbox.right - 25 < block.hitbox.right and mc.isJump):
                        result = block.destroy()
                        mc.interruptJump()
                        if result is not None:
                            poweruplist.append(result)

            # ==================Gomb lenyomások kezelése==================

            if not any(keys):
                mc.isRunning = False
                mc.isIdle = True

            if keys[pygame.K_LEFT]:
                collision = collisionchecker(mc, 'left')
                if not collision and mc.x != 0:
                    mc.move('left')

            if keys[pygame.K_RIGHT]:
                collision = collisionchecker(mc, 'right')
                # Kamera
                if not collision and mc.x != window_width - 30:
                    if mc.x + offset_x > finish.x:
                        mc.move('right')
                    elif mc.x == offset_x:
                        for sprites in spritelist:
                            sprites.x -= mc.vel
                        mc_spawn -= mc.vel
                        mc.move('right')
                    else:
                        mc.move('right')
            if keys[pygame.K_F1]:
                print(mc.hp)
            if keys[pygame.K_F2]:
                for sprites in spritelist:
                    sprites.x -= mc_spawn
                mc_spawn = 0

            # Ugrás viselkedés: fél-Parabola megoldás

            if not mc.isJump and not mc.isFalling:
                if keys[pygame.K_UP]:
                    mc.isJump = True
            else:
                mc.jump()

            if keys[pygame.K_SPACE]:
                mc.isIdle = True
                if mc.canShoot and shootLimit == 0:
                    if len(friendlyProjectiles) < 5:
                        if mc.facingRight:
                            friendlyProjectiles.append(mc.shoot(1))
                        else:
                            friendlyProjectiles.append(mc.shoot(-1))
                        shootLimit = 1

            if shootLimit > 0:
                shootLimit += 1
            if shootLimit > 3:
                shootLimit = 0

            # Iframe és invincibility kezelő
            mc.iFrame()
            if mc.isInvincible and mc.iFrames == 0:
                print('no longer invincible')
                mc.isInvincible = False

            # Pontszám levonó
            if second_counter == 0:
                if score > 0:
                    score -= 10
                second_counter = 20
            else:
                second_counter -= 1

        pygame.display.update()
