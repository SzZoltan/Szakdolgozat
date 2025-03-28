import pickle
import sys

import pygame

from Game.Button.Button import Button
from Game.Entity.Block import GoldBlock, SteelBlock, BrickBlock, Inside
from Game.Entity.PowerUp import (Apple, Finish)
from Game.Entity.Player import Player
from Game.Entity.Enemy import (BunnyEnemy, PlantEnemy, TurtleEnemy, Enemy)
from Game.Game_Graphics.Graphics_Loader import (level1_bg, level2_bg, level3_bg, pause_pic, unpause_pic, quit_btn_pic,
                                                full_heart_pic, half_heart_pic, empty_heart_pic, health_head_pic,
                                                again_btn_pic, yes_btn_pic, no_btn_pic, save_btn_pic, cherries_pic)
from DAO.DAO_sqlite import SQLiteDAO
pygame.init()

background_id = 1
mcx_spawn = 0
mcy_spawn = 0
mc = Player(0, 200)
finish = Finish(600, 255)
DAO = SQLiteDAO('./Database/leaderboard.db')


def game_loop(level: int):
    """
    A játék képernyőjét valósítsa meg
    :param level: int, amelyik pályát szeretnénk betölteni
    """
    global mc, finish, mcx_spawn, mcy_spawn, background_id, DAO
    # Az animációk 20 FPS-re vannak megcsinálva

    clock = pygame.time.Clock()
    second_counter = 20
    FPS = 20
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    score = 10000
    font = pygame.font.SysFont(None, 50)

    offset_x = 205
    window_width = 1000
    window_height = 640
    map_data = {}
    tiles_across = window_width // level1_bg.get_width() + 1
    tiles_down = window_height // level1_bg.get_height() + 1
    game_paused = False

    pause_btn = Button(window_width - 50, 15, pause_pic, 1)
    unpause_btn = Button(window_width // 2 - 50, window_height // 2 - 50, unpause_pic, 1)
    quit_btn = Button(window_width // 2 - 70, window_height // 2, quit_btn_pic, 1)

    win = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(f"Pink Guy's Adventures - Level: {level}")

    invincibleTimer = 0

    # shootLimit azért hogy legyen egy kis delay a lövések között

    shootLimit = 0
    friendlyProjectiles = []
    enemyProjectiles = []
    blocklist = []
    poweruplist = []
    enemylist = []
    entitylist = []
    spritelist = blocklist + poweruplist + entitylist + friendlyProjectiles + enemyProjectiles

    # Unit tesztelés extrém tesztesetek

    def load_level():
        """
        Betölti a megadott pályát Pickle segítségével
        :return: a betöltött pálya adatai és a háttér amelyik be kell tölteni
        """
        try:
            with open(f'Maps/level_{level}_data', 'rb') as pickle_in:
                data = pickle.load(pickle_in)
                return data
        except FileNotFoundError as fnfe:
            print(f'Map not found error: {fnfe}')
        except pickle.UnpicklingError as upe:
            print(f'Map unpickling error: {upe}')
        except Exception as e:
            print(f'Something went wrong: {e}')

    map_data = load_level()
    background_id = map_data['background']
    map_data = map_data['world_data']

    def place_entities(declaremc: bool):
        """
        Elhelyezi az entitásokat a pályán a beolvasott adatok alapján
        :param declaremc: bool, a Játékost deklarálja-e vagy nem
        """
        global mc, mcx_spawn, mcy_spawn, finish

        for y in range(len(map_data)):
            for x in range(len(map_data[y])):
                if map_data[y][x] == -1:
                    continue
                elif map_data[y][x] == 0:
                    blocklist.append(BrickBlock(x*40, y*40))
                elif map_data[y][x] == 1:
                    blocklist.append(GoldBlock(x*40, y*40, Inside.APPLE))
                elif map_data[y][x] == 2:
                    blocklist.append(GoldBlock(x*40, y*40, Inside.PINEAPPLE))
                elif map_data[y][x] == 3:
                    blocklist.append(GoldBlock(x*40, y*40, Inside.CHERRY))
                elif map_data[y][x] == 4:
                    blocklist.append(GoldBlock(x*40, y*40, Inside.STRAWBERRY))
                elif map_data[y][x] == 5:
                    blocklist.append(SteelBlock(x*40, y*40))
                elif map_data[y][x] == 6 and declaremc:
                    mc = Player(x*40, y*40)
                    mcx_spawn = x*40
                    mcy_spawn = y*40
                    entitylist.append(mc)
                elif map_data[y][x] == 7:
                    enemylist.append(BunnyEnemy(x*40, y*40-10))
                elif map_data[y][x] == 8:
                    enemylist.append(PlantEnemy(x*40, y*40-10))
                elif map_data[y][x] == 9:
                    enemylist.append(TurtleEnemy(x*40, y*40-5))
                elif map_data[y][x] == 10:
                    finish = Finish(x*40, y*40-25)
                    poweruplist.append(finish)

    place_entities(True)
    entitylist = enemylist.copy()
    entitylist.append(mc)
    distance = mcx_spawn
    # A háttér

    def drawBackground():
        """
        A háttér felrajzolásáért felelős a bakcground_id alapján cselekszik
        """
        if background_id == 1:
            for row in range(tiles_down):
                for col in range(tiles_across):
                    x_pos = col * level1_bg.get_width()
                    y_pos = row * level1_bg.get_height()
                    win.blit(level1_bg, (x_pos, y_pos))
        elif background_id == 2:
            for row in range(tiles_down):
                for col in range(tiles_across):
                    x_pos = col * level1_bg.get_width()
                    y_pos = row * level1_bg.get_height()
                    win.blit(level2_bg, (x_pos, y_pos))
        else:
            for row in range(tiles_down):
                for col in range(tiles_across):
                    x_pos = col * level1_bg.get_width()
                    y_pos = row * level1_bg.get_height()
                    win.blit(level3_bg, (x_pos, y_pos))

    def drawProjectiles():
        """
        Felrajzolja a Projectile-okat a képernyőre
        """
        for fproj in friendlyProjectiles:
            fproj.draw(win)
        for eproj in enemyProjectiles:
            eproj.draw(win)

    def drawPowerUp():
        """
        Felrajzolja a PowerUp-okat a képernyőre
        """
        for pup in poweruplist:
            pup.drawPowerup(win)

    def drawBlocks():
        """
        Felrajzolja a Block-okat a képernyőre
        """
        for blocks in blocklist:
            blocks.draw(win)

    def drawEnemies():
        """
        Felrajzolja a Enemy-ket a képernyőre
        """
        for e in enemylist:
            e.drawEnemy(win)

    def redrawGameWindow():
        """
        Mindent újrarajzól, meghívja az összes eddigi rajzoló metódust
        """
        drawBackground()
        mc.drawPlayer(win)
        drawPowerUp()
        drawProjectiles()
        drawEnemies()
        drawBlocks()
        draw_UI()

    def draw_UI():
        """
        Felrajzolja a felhasználói felületet ami változik a Játékos státusza alapján
        """
        paused_txt = font.render(f"x {mc.lives}", True, WHITE)
        score_text = font.render(f"{score}", True, WHITE)
        if mc.hp == 1:
            win.blit(half_heart_pic, (10, 15))
        elif mc.hp == 2:
            win.blit(full_heart_pic, (10, 15))
        else:
            win.blit(empty_heart_pic, (10, 15))
        if mc.canShoot:
            win.blit(cherries_pic, (145, 5))
        win.blit(health_head_pic, (75, 25))
        win.blit(paused_txt, (100, 15))
        win.blit(score_text, (window_width-200, 15))

    def draw_pause_screen():
        """
        Felrajzolja azt a képernyőt amikor a játék meg van álltva és a két gombot amivel ki lehet lépni vagy folytatni
        """
        overlay = pygame.Surface((window_width, window_height))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        win.blit(overlay, (0, 0))

        text = font.render("Paused", True, WHITE)
        win.blit(text, (window_width // 2 - 85, window_height // 2 - 100))

    def draw_death_screen():
        """
        Felrajzolja azt a képernyőt amikor a játékos meghal de még van élete, tudja folytatni, vagy kilép innen
        """
        run = True
        fade = pygame.Surface((window_width, window_height))
        fade.fill(BLACK)

        for alpha in range(0, 255):
            fade.set_alpha(alpha)
            win.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(2)

        mc.lives -= 1
        death_txt = font.render("You Died", True, WHITE)
        lives_txt = font.render(f"x {mc.lives}", True, WHITE)
        continue_txt = font.render("Press Space to continue", True, WHITE)

        win.blit(death_txt, (window_width // 2 - 85, window_height // 2 - 100))
        win.blit(lives_txt, (window_width // 2 - 20, window_height // 2 - 50))
        win.blit(health_head_pic, (window_width // 2 - 45, window_height // 2 - 40))
        win.blit(continue_txt, (window_width // 2 - 200, window_height // 2))

        while run:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if keys[pygame.K_SPACE]:
                run = False

            pygame.display.update()
        pygame.time.delay(100)

    def draw_game_over_screen():
        """
        Felrajzolja azt a képernyőt amikor a játékos meghal és nincs több élete, ki tud lépni vagy újrapróbálja innen
        :return: bool, a játékos döntése, True megpróbálja mégegyszer, False kilép
        """
        overlay = pygame.Surface((window_width, window_height))
        overlay.fill(BLACK)

        game_continue = False

        game_over_txt = font.render("Game Over", True, WHITE)
        again_btn = Button(window_width // 2 + 30, window_height // 2 - 50, again_btn_pic, 1)
        game_over_quit_btn = Button(window_width // 2 - 135, window_height // 2 - 50, quit_btn_pic, 1)

        win.blit(overlay, (0, 0))
        win.blit(game_over_txt, (window_width // 2 - game_over_txt.get_width() // 2, window_height // 2 - 100))

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if again_btn.draw(win):
                game_continue = True
                run = False

            if game_over_quit_btn.draw(win):
                game_continue = False
                run = False

            pygame.display.update()

        pygame.time.delay(100)
        return game_continue

    def draw_victory_screen():
        """
        Megrajzolja azt a képernyőt amikor felvette a Trófeát és nyer a Játékos, hozzátudja tenni a pontszámát a
        toplistához, vagy csak kilép
        """

        def draw_leaderboard_entry():
            """
            Megrajzolja azt a felület ahol beírja a Játékos a nevét és elmentheti a pontszámát ha úgy dönt
            """
            run = True
            win.fill(BLACK)
            player_name_txt = font.render("Write down your name", True, WHITE)
            enter_guide_txt = font.render("Press the Enter key to check if your name is valid", True, WHITE)
            click_back_txt = font.render("Click on the box to start typing", True, WHITE)
            textbox_name = ""
            color_passive_bad = pygame.Color("red")
            color_passive_good = pygame.Color("green")
            color_active = pygame.Color("lightblue")
            delay = 0

            input_rect = pygame.Rect(window_width // 2 - 35, window_height // 2-5, 100, 40)
            active = True

            save_score_btn = Button(window_width // 2 - save_btn_pic.get_width(), window_height // 2 + 100,
                                    save_btn_pic, 1)
            quit_leadearboard_btn = Button(window_width // 2 - quit_btn_pic.get_width() + 100, window_height // 2 + 100,
                                           quit_btn_pic, 1)

            while run:
                win.fill(BLACK)
                keys = pygame.key.get_pressed()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if input_rect.collidepoint(event.pos):
                            active = True

                    if keys[pygame.K_RETURN]:
                        active = False

                    if active:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                textbox_name = textbox_name[:-1]
                            elif len(textbox_name) < 3 and event.unicode.isalpha():
                                textbox_name += event.unicode
                                textbox_name = textbox_name.upper()

                if save_score_btn.draw(win):
                    if len(textbox_name) == 3:
                        run = False
                        with DAO:
                            DAO.insert(textbox_name, score, level)
                        pygame.time.delay(100)

                if quit_leadearboard_btn.draw(win):
                    run = False
                    pygame.time.delay(100)

                if active:
                    color = color_active
                elif len(textbox_name) == 3:
                    color = color_passive_good
                else:
                    color = color_passive_bad

                if len(textbox_name) == 0:
                    if delay > 1200:
                        delay = 0
                    else:
                        pygame.draw.rect(win, color, input_rect)
                else:
                    pygame.draw.rect(win, color, input_rect)
                delay += clock.tick(FPS)

                usr_name = font.render(textbox_name, True, WHITE)
                win.blit(usr_name, (window_width // 2 - 25, window_height // 2))
                win.blit(player_name_txt,
                         (window_width // 2 - player_name_txt.get_width() // 2, window_height // 2 - 200))
                win.blit(click_back_txt,
                         (window_width // 2 - click_back_txt.get_width() // 2, window_height // 2 - 100))
                win.blit(enter_guide_txt,
                         (window_width // 2 - enter_guide_txt.get_width() // 2, window_height // 2 - 150))
                pygame.display.update()

        run = True
        fade = pygame.Surface((window_width, window_height))
        fade.fill(BLACK)

        for alpha in range(0, 255):
            fade.set_alpha(alpha)
            win.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(2)

        victory_txt = font.render("Congratulations, You won!", True, WHITE)
        score_txt = font.render(f"Your final score: {score}", True, WHITE)
        leaderboard_txt = font.render("Want to publish your score?", True, WHITE)

        yes_btn = Button(window_width // 2 - yes_btn_pic.get_width(), window_height // 2 + 100, yes_btn_pic, 1)
        no_btn = Button(window_width // 2 - no_btn_pic.get_width() + 100, window_height // 2 + 100, no_btn_pic, 1)

        win.blit(victory_txt, (window_width // 2 - victory_txt.get_width() // 2, window_height // 2 - 200))
        win.blit(score_txt, (window_width // 2 - score_txt.get_width() // 2, window_height // 2 - 100))
        win.blit(leaderboard_txt, (window_width // 2 - leaderboard_txt.get_width() // 2, window_height // 2))

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if no_btn.draw(win):
                run = False

            if yes_btn.draw(win):
                pygame.time.delay(100)
                draw_leaderboard_entry()
                run = False

            pygame.display.update()

        pygame.time.delay(100)

    run = True

    def collisionchecker(entity: Player or Enemy, direction: str):
        """
        Ellenőrzi, hogy a beadott entitás ütközik-e valamelyik Block-al

        :param entity: Player vagy Enemy az entitás amit ellenőrzünk
        :param direction: string, 'left', ha az entitás balra megy, 'right' ha jobbra

        :return: bool, True ütközik, False nem ütközik
        """
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
                pygame.time.delay(100)
        else:
            redrawGameWindow()
            if pause_btn.draw(win):
                game_paused = not game_paused
                draw_pause_screen()

            # ==================Gravitáció==================

            for entity in entitylist:
                for block in blocklist:
                    if entity.isAlive and entity.hitbox.colliderect(block.hitbox):
                        if (entity.hitbox.bottom + block.height - 10 < block.hitbox.bottom
                                and block.isVisible):
                            entity.isFalling = False
                            break
                    elif entity.y + entity.height >= 640:
                        entity.isFalling = False
                        if isinstance(entity, Enemy):
                            entity.hit()
                        elif isinstance(entity, Player):
                            entity.kill()
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
                    if proj.hitbox.colliderect(block.hitbox) and block.isVisible:
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
                    if proj.hitbox.colliderect(block.hitbox) and block.isVisible:
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
                        draw_victory_screen()
                        run = False
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
                if enemies.canMove and enemies.isVisible:
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

            # ============================== Halál, Respawn és Game Over ==============================

            if mc.hp == 0:
                draw_death_screen()
                if mc.lives != 0:
                    score = 10000
                    mc.hp = 1
                    mc.clear_effects()
                    friendlyProjectiles = []
                    enemyProjectiles = []
                    blocklist = []
                    poweruplist = []
                    enemylist = []
                    entitylist = []
                    place_entities(False)
                    entitylist = enemylist.copy()
                    entitylist.append(mc)
                    spritelist = blocklist + poweruplist + entitylist + friendlyProjectiles + enemyProjectiles
                else:
                    if not draw_game_over_screen():
                        run = False
                    else:
                        score = 10000
                        friendlyProjectiles = []
                        enemyProjectiles = []
                        blocklist = []
                        poweruplist = []
                        enemylist = []
                        entitylist = []
                        place_entities(True)
                        entitylist = enemylist.copy()
                        entitylist.append(mc)
                        spritelist = blocklist + poweruplist + entitylist + friendlyProjectiles + enemyProjectiles

                if distance > offset_x:
                    for sprites in spritelist:
                        sprites.x -= distance
                distance = mcx_spawn
                mc.x = mcx_spawn
                mc.y = mcy_spawn

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
                    elif mc.x >= offset_x:
                        for sprites in spritelist:
                            sprites.x -= mc.vel
                        distance -= mc.vel
                        mc.move('right')
                    else:
                        mc.move('right')

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
                mc.isInvincible = False

            # Pontszám levonó

            if second_counter == 0:
                if score > 0:
                    score -= 10
                second_counter = 20
            else:
                second_counter -= 1

        pygame.display.update()


pygame.time.delay(100)
