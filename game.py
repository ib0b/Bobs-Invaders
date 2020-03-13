import math
import random
import numpy as np
import pygame
import time

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


class Player:
    def __init__(self, screen):
        self.img = pygame.image.load('player.png')
        self.x = 370
        self.y = 480
        self.screen = screen
        self.width = self.img.get_size()[0]

    def getShootPosX(self):
        return self.x + self.width/2.0

    def setPos(self, pos):
        self.x, self.y = pos

    def draw(self):
        self.screen.blit(self.img, (self.x, self.y))

    def getState(self):
        return np.array([self.x/WINDOW_WIDTH, self.y/WINDOW_HEIGHT])


class Bullet:
    def __init__(self, screen, orientation="up", x=0, y=0):
        self.bulletImg = pygame.image.load('bullet.png')
        self.x = x
        self.y = y
        self.show = False
        self.screen = screen
        if(orientation == "down"):
            self.bulletImg = pygame.transform.flip(self.bulletImg, False, True)

    def draw(self):
        if(self.show):
            self.screen.blit(self.bulletImg, (self.x, self.y))

    def setPos(self, pos):
        self.x, self.y = pos

    def getState(self):
        show = 1 if self.show else 0
        return np.array([show, self.x/WINDOW_WIDTH, self.y/WINDOW_HEIGHT])


class Enemy:
    def __init__(self, screen, x, y):
        self.enemyImg = pygame.image.load('enemy.png')
        self.bulletImg = pygame.image.load('bullet.png')
        self.bulletImgXSize = self.bulletImg.get_size()[0]/2
        self.x = x
        self.y = y
        self.alive = True
        self.screen = screen
        self.draw()

    def getState(self):
        alive = 1 if self.alive else 0
        return np.array([alive, self.x/WINDOW_WIDTH, self.y/WINDOW_HEIGHT])

    def collided(self, bulletX, bulletY):
        enemyCenterX = self.x+self.enemyImg.get_size()[0]/2
        enemyCenterY = self.y+self.enemyImg.get_size()[1]/2
        bulletCenterX = bulletX+self.bulletImgXSize/2
        bulletCenterY = bulletY

        distance = math.sqrt(math.pow(enemyCenterX - bulletCenterX, 2) +
                             (math.pow(enemyCenterY - bulletCenterY, 2)))

        # bullet bypass
        if(not self.alive):
            return False
        if distance < self.enemyImg.get_size()[0]/2:
            self.alive = False
            return True
        else:
            return False

    def draw(self):
        if(self.alive):
            self.screen.blit(self.enemyImg, (self.x, self.y))

    def getPos(self):
        return self.x, self.y


class EnemyBlock:
    def __init__(self, screen, num, x=0, y=0, maxX=600, maxY=400):
        self.enemyImg = pygame.image.load('enemy.png')
        self.enemyPointX = x
        self.enemyPointY = y
        self.alive = True
        self.screen = screen
        self.enemies = []
        self.num = num
        enemyImg = pygame.image.load('enemy.png')
        bulletImg = pygame.image.load('bullet.png')
        self.enemyXsize = enemyImg.get_size()[0]
        self.enemyYsize = enemyImg.get_size()[1]
        self.enemyXpad = 10 + self.enemyXsize
        self.enemyYpad = 5 + self.enemyXsize

        self.blockStartX = 50
        self.blockStartY = 50

        self.anchorX = self.blockStartX
        self.anchorY = self.blockStartY
        self.maxX = maxX
        self.maxY = maxY

        self.moveXSpeed = 2
        self.moveYSpeed = 20
        self.moveXVector = self.moveXSpeed
        self.moveYVector = self.moveYSpeed
        # enemy bullet
        self.enemyBullet = Bullet(self.screen, "down")
        self.enemyBulletSizeX = bulletImg.get_size()[1]
        self.enemyBulletSpeed = 5

        self.creatEnemies()

    def getState(self):
        state = np.array([])
        for i in range(self.num):
            state = np.append(state, self.enemies[i].getState())
        state = np.append(state, self.enemyBullet.getState())
        return state

    def shoot(self):
        # get bottom alive
        mostLeftX, mostRightX, mostBottomY = self.getEdges()
        bottomXs = []
        for i in range(self.num):
            if(self.enemies[i].y == mostBottomY and self.enemies[i].alive):
                bottomXs.append(self.enemies[i].x+self.enemyXsize/2)
        if(len(bottomXs) == 0):
            return
        try:
            enemyBulletX = random.sample(bottomXs, 1)[0]
        except ValueError:
            print("Booom", len(bottomXs))
            raise Exception('spam', 'eggs')
        enemyBulletY = mostBottomY + self.enemyYsize

        self.enemyBullet.x = enemyBulletX
        self.enemyBullet.y = enemyBulletY
        self.enemyBullet.show = True

    def getEdges(self):
        mostLeftX, mostRightX, mostBottomY = (800, 0, 0)
        for i in range(self.num):

            if(self.enemies[i].alive):
                if(self.enemies[i].x < mostLeftX):
                    mostLeftX = self.enemies[i].x
                if(self.enemies[i].x > mostRightX):
                    mostRightX = self.enemies[i].x + self.enemyXsize
                if(self.enemies[i].x > mostBottomY):
                    mostBottomY = self.enemies[i].y

        return mostLeftX, mostRightX, mostBottomY

    def playerShot(self, x, y):
        if(self.enemyBullet.y >= y-self.enemyBulletSizeX and self.enemyBullet.x < x + self.enemyBulletSizeX and self.enemyBullet.x > x):
            print("mayday")
            return True
        return False

    def checkCollisions(self, x, y):
        collided = False
        for i in range(self.num):
            collided = self.enemies[i].collided(x, y)
            if(collided):
                break
        return collided

    def moveAnchor(self):
        # get limits
        mostLeftX, mostRightX, mostBottomY = self.getEdges()

        if(mostLeftX < 0):
            self.moveXVector = self.moveXSpeed
            self.anchorY += self.moveYVector
        if(mostRightX > 800):
            self.moveXVector = -self.moveXSpeed
            self.anchorY += self.moveYVector
        self.anchorX += self.moveXVector

    def move(self):
        enemyPointX = 0
        enemyPointY = 0
        self.moveAnchor()
        for i in range(self.num):

            self.enemies[i].x = enemyPointX + self.anchorX
            self.enemies[i].y = enemyPointY + self.anchorY
            self.enemies[i].draw()

            enemyPointX += self.enemyXpad
            if(enemyPointX > self.maxX):
                enemyPointX = 0
                enemyPointY += self.enemyYpad

        # move bullet
        if(self.enemyBullet.show):
            # moving bullet

            self.enemyBullet.y += self.enemyBulletSpeed
            self.enemyBullet.draw()
            # check collisions with player

            # check collision with game boundary
            if(self.enemyBullet.y > 600):
                self.enemyBullet.show = False

        else:
            # print("shoting")
            if(not self.allDead()):
                self.enemyBullet.show = True
                self.shoot()
            else:
                print("all dead")

    def creatEnemies(self):

        for i in range(self.num):
            enemy = Enemy(self.screen, self.enemyPointX +
                          self.anchorX, self.enemyPointY+self.anchorY)
            self.enemies.append(enemy)
            self.enemyPointX += self.enemyXpad
            if(self.enemyPointX > self.maxX):
                self.enemyPointX = 0
                self.enemyPointY += self.enemyYpad

    def allDead(self):
        allDead = True
        for i in range(self.num):
            if(self.enemies[i].alive):
                allDead = False
                break
        return allDead

    def enemyInvasion(self):
        mostLeftX, mostRightX, mostBottomY = self.getEdges()

        if(mostBottomY > self.maxY):
            self.moveXSpeed = 0
            self.moveYSpeed = 0
            return True
        return False


class GameEnv:

    def __init__(self, framerate=0):
        self.gWidth = 800.0
        self.gHeight = 600.0
        self.framerate = framerate
        self.enemyXSpeed = 0
        enemyImg = pygame.image.load('enemy.png')
        self.enemyXsize = enemyImg.get_size()[0]/2
        self.enemyYsize = enemyImg.get_size()[1]/2

        self.reset()

    def getGameState(self):
        state = np.array([])
        # enemy states
        enemyBlockState = self.enemyBlock.getState()

        state = np.append(state, enemyBlockState)

        # playerBullet
        bulletState = self.playerBullet.getState()
        state = np.append(state, bulletState)

        # playerstates
        playerState = self.player.getState()
        state = np.append(state, playerState)

        return state

    def reset(self):
        pygame.init()
        print("game start")
        self.screen = pygame.display.set_mode(
            (int(self.gWidth), int(self.gHeight)))

        # self.ground
        self.background = pygame.image.load('background.png')
        # Caption and Icon
        pygame.display.set_caption("Space Invader")
        icon = pygame.image.load('ufo.png')
        pygame.display.set_icon(icon)

        self.font = pygame.font.Font('freesansbold.ttf', 32)

        # Game Over
        self.over_font = pygame.font.Font('freesansbold.ttf', 64)
        # Player
        self.player = Player(self.screen)
        self.playerXVector = 0
        self.playerXSpeed = 5

        self.done = False
        self.enemyBlock = EnemyBlock(self.screen, num=27, x=0, y=20)

        # Bullet
        self.playerBullet = Bullet(self.screen, y=480, x=0)
        self.bulletXSpeed = 0
        self.bulletYSpeed = 50

        # Score
        self.score_value = 0
        self.totalReward = 0
        return self.getGameState()

    def player(self, x, y):
        self.screen.blit(self.playerImg, (x, y))

    def show_score(self, x, y):
        score = self.font.render(f"Score : {self.score_value} reward {self.totalReward}",
                                 True, (255, 255, 255))
        self.screen.blit(score, (x, y))

    def playerShoot(self):
        self.playerBullet.show = True
        self.playerBullet.setPos(self.player)

    def loop(self):
        running = True
        action = 0
        totalReward = 0
        while running:

            if(self.done):
                running = False
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # if keystroke is pressed check whether its right or left
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        action = 1

                    if event.key == pygame.K_RIGHT:
                        action = 2
                    if event.key == pygame.K_SPACE:
                        action = 3

                if event.type == pygame.KEYUP:
                    # if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    action = 0

                if event.type == pygame.QUIT:
                    running = False
            state, reward, done, win = self.step(action)
            totalReward += reward
        print("tpt", totalReward)
        # if(done):
        #     running = False

    def step(self, action, finishGame=False):
        reward = -0.001
        win = 0
        if(finishGame):
            state = self.getGameState()
            pygame.quit()
            print("finish")
            return state, 0, True
        if(self.done):
            print("game done")
            state = self.getGameState()
            pygame.quit()
            print("game donedone")
            return state, 0, True

        pygame.event.pump()
        self.screen.fill((0, 0, 0))

        if action == 1:
            self.playerXVector = -self.playerXSpeed
        if action == 2:
            self.playerXVector = self.playerXSpeed
        if action == 3:
            if not self.playerBullet.show:
                # Get the current x cordinate of the spaceship

                self.playerBullet.x = self.player.getShootPosX()
                self.playerBullet.show = True

        if action == 0:
            self.playerXVector = 0

        self.screen.fill((0, 0, 0))
        # Background Image
        #self.screen.blit(self.background, (0, 0))

        # if keystroke is pressed check whether its right or left

        self.player.x += self.playerXVector
        if self.player.x <= 0:
            self.player.x = 0
        elif self.player.x >= 736:
            self.player.x = 736

        # show player
        self.player.draw()
        self.playerBullet.draw()
        # enemyMovement
        self.enemyBlock.move()
        # check player collisions
        playerShot = self.enemyBlock.playerShot(
            self.player.x, self.player.y)
        if(playerShot):
            reward = -3
            running = False
            self.done = True

        collision = self.enemyBlock.checkCollisions(
            self.playerBullet.x, self.playerBullet.y)
        if collision:
            # explosion# = mixer.Sound("explosion.wav")
            # explosionSound.play()
            self.playerBullet.y = self.player.y
            self.playerBullet.show = False
            reward = 3.0/self.enemyBlock.num
            self.score_value += 1

        # # Bullet Movement
        if self.playerBullet.y <= 0:
            self.playerBullet.y = 480
            self.playerBullet.show = False

        if self.playerBullet.show:
            self.playerBullet.y -= self.bulletYSpeed

        # gameover logic
        allDead = self.enemyBlock.allDead()
        invasion = False
        if(allDead):
            reward = 3
            running = False
            self.done = True
            win = 1
            print("gracefull win")
        else:
            invasion = self.enemyBlock.enemyInvasion()

        if(invasion):
            # invaded
            running = False
            self.done = True
            print("gracefull lose")
            reward = -3

        self.show_score(50, 50)
        if(self.framerate != 0):
            time.sleep(self.framerate)
        pygame.display.update()
        if(self.done):
            pygame.quit()
        self.totalReward += reward
        return self.getGameState(), reward, self.done, win
