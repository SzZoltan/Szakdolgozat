from Game.Entity.Projectile import *
from Game.Entity.PowerUp import *
from Game.Entity.Player import Player
import pygame

pygame.init()

# Az animációk 20 FPS-re vannak megcsinálva
clock = pygame.time.Clock()


# A háttér
def drawBackground():
    for row in range(tiles_down):
        for col in range(tiles_across):
            x_pos = col * level1_bg.get_width()
            y_pos = row * level1_bg.get_height()
            win.blit(level1_bg, (x_pos, y_pos))


def drawProjectiles():
    for fproj in friendlyProjectiles:
        fproj.draw(win, (0, 255, 0))


def redrawGameWindow():
    win.fill((0, 0, 0))
    drawBackground()
    mc.drawPlayer(win)
    apple.drawApple(win)
    pineapple.drawPineapple(win)
    cherry.drawCherry(win)
    strawberry.drawStrawberry(win)
    drawProjectiles()
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
apple = Apple(200, 255, 32, 32, apple_frames)
cherry = Cherry(250, 255, 32, 32, cherry_frames)
pineapple = Pineapple(150, 255, 32, 32, pineapple_frames)
strawberry = Strawberry(300, 255, 32, 32, strawberry_frames)
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

    # Ugrás viselkedés: Parabola megoldás
    if not mc.isJump:
        if keys[pygame.K_UP]:
            mc.isJump = True
    else:
        mc.jump()
    redrawGameWindow()

pygame.quit()
