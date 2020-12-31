import pygame, sys
from pygame.constants import K_LEFT
from pygame.math import Vector2
from random import randint

# Initialize game
pygame.init()

width = 40
rows = 20

# Setup screen
screen = pygame.display.set_mode((width * rows, width * rows))
clock = pygame.time.Clock()
apple = pygame.image.load("./images/apple.png").convert_alpha()
running = True


class FRUIT:
    def __init__(self):
        self.randomize()

    def drawFruit(self):
        fruitRect = pygame.Rect(self.x * width, self.y * width, width, width)
        screen.blit(apple, fruitRect)
        # pygame.draw.rect(screen, (255, 0, 0), fruitRect)

    def randomize(self):
        self.x = randint(0, rows - 1)
        self.y = randint(0, rows - 1)
        self.pos = Vector2(self.x, self.y)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.newBlock = False

        self.headUp = pygame.image.load("./images/headUp.png").convert_alpha()
        self.headDown = pygame.image.load("./images/headDown.png").convert_alpha()
        self.headLeft = pygame.image.load("./images/headLeft.png").convert_alpha()
        self.headRight = pygame.image.load("./images/headRight.png").convert_alpha()

        self.tailUp = pygame.image.load("./images/tailUp.png").convert_alpha()
        self.tailDown = pygame.image.load("./images/tailDown.png").convert_alpha()
        self.tailLeft = pygame.image.load("./images/tailLeft.png").convert_alpha()
        self.tailRight = pygame.image.load("./images/tailRight.png").convert_alpha()

        self.bodyVertical = pygame.image.load(
            "./images/bodyVertical.png"
        ).convert_alpha()
        self.bodyHorizontal = pygame.image.load(
            "./images/bodyHorizontal.png"
        ).convert_alpha()

        self.bodyTL = pygame.image.load("./images/bodyTL.png").convert_alpha()
        self.bodyTR = pygame.image.load("./images/bodyTR.png").convert_alpha()
        self.bodyBL = pygame.image.load("./images/bodyBL.png").convert_alpha()
        self.bodyBR = pygame.image.load("./images/bodyBR.png").convert_alpha()

    def drawBody(self):

        self.updateHeadGrapics()
        self.updateTailGraphics()

        for index, block in enumerate(self.body):
            xPos = int(block.x * width)
            yPos = int(block.y * width)

            bodyRect = pygame.Rect(xPos, yPos, width, width)

            # What direction is snake facing?
            if index == 0:
                screen.blit(self.head, bodyRect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, bodyRect)
            else:
                prevBlock = self.body[index + 1] - block
                nextBlock = self.body[index - 1] - block

                if prevBlock.x == nextBlock.x:
                    screen.blit(self.bodyVertical, bodyRect)

                if prevBlock.y == nextBlock.y:
                    screen.blit(self.bodyHorizontal, bodyRect)

                else:
                    if (
                        prevBlock.x == -1
                        and nextBlock.y == -1
                        or prevBlock.y == -1
                        and nextBlock.x == -1
                    ):
                        screen.blit(self.bodyTL, bodyRect)

                    elif (
                        prevBlock.x == -1
                        and nextBlock.y == 1
                        or prevBlock.y == 1
                        and nextBlock.x == -1
                    ):
                        screen.blit(self.bodyBL, bodyRect)

                    elif (
                        prevBlock.x == 1
                        and nextBlock.y == -1
                        or prevBlock.y == -1
                        and nextBlock.x == 1
                    ):
                        screen.blit(self.bodyTR, bodyRect)

                    elif (
                        prevBlock.x == 1
                        and nextBlock.y == 1
                        or prevBlock.y == 1
                        and nextBlock.x == 1
                    ):
                        screen.blit(self.bodyBR, bodyRect)

    def updateHeadGrapics(self):
        headRelation = self.body[1] - self.body[0]

        if headRelation == Vector2(1, 0):
            self.head = self.headLeft
        elif headRelation == Vector2(-1, 0):
            self.head = self.headRight
        elif headRelation == Vector2(0, 1):
            self.head = self.headUp
        elif headRelation == Vector2(0, -1):
            self.head = self.headDown

    def updateTailGraphics(self):
        tailRelation = self.body[-2] - self.body[-1]

        if tailRelation == Vector2(1, 0):
            self.tail = self.tailLeft
        elif tailRelation == Vector2(-1, 0):
            self.tail = self.tailRight
        elif tailRelation == Vector2(0, 1):
            self.tail = self.tailUp
        elif tailRelation == Vector2(0, -1):
            self.tail = self.tailDown

    def moveSnake(self):
        if self.newBlock == True:
            bodyCopy = self.body[:]
            bodyCopy.insert(0, bodyCopy[0] + self.direction)
            self.body = bodyCopy[:]
            self.newBlock = False

        else:
            bodyCopy = self.body[:-1]
            bodyCopy.insert(0, bodyCopy[0] + self.direction)
            self.body = bodyCopy[:]

    def addBlock(self):
        self.newBlock = True


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.moveSnake()
        self.checkCollision()
        self.checkFail()

    def drawElements(self):
        self.snake.drawBody()
        self.fruit.drawFruit()

    def checkCollision(self):
        if self.fruit.pos == self.snake.body[0]:
            # Reposition the fruit
            self.fruit.randomize()

            # Add extra block to the tail of snake
            self.snake.addBlock()

    def checkFail(self):
        # Check if snake hit the wall
        if not 0 <= self.snake.body[0].x < rows or not 0 <= self.snake.body[0].y < rows:
            self.gameOver()

        # Check if snake collided with itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver()

    def gameOver(self):
        pygame.quit()
        sys.exit()


mainGame = MAIN()

screenUPDATE = pygame.USEREVENT
pygame.time.set_timer(screenUPDATE, 100)
running = True


def main():
    global screen, running

    while running:

        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == screenUPDATE:
                mainGame.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if mainGame.snake.direction.y != 1:
                        mainGame.snake.direction = Vector2(0, -1)

                if event.key == pygame.K_s:
                    if mainGame.snake.direction.y != -1:
                        mainGame.snake.direction = Vector2(0, 1)

                if event.key == pygame.K_d:
                    if mainGame.snake.direction.x != -1:
                        mainGame.snake.direction = Vector2(1, 0)

                if event.key == pygame.K_a:
                    if mainGame.snake.direction.x != 1:
                        mainGame.snake.direction = Vector2(-1, 0)

        clock.tick(60)
        mainGame.drawElements()
        pygame.display.update()


main()
