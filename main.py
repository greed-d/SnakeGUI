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

    def drawBody(self):
        for block in self.body:
            xPos = int(block.x * width)
            yPos = int(block.y * width)

            bodyRect = pygame.Rect(xPos, yPos, width, width)
            pygame.draw.rect(screen, (5, 19, 141), bodyRect)

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
            if block == self.snake.body:
                self.gameOver()

    def gameOver(self):
        pygame.quit()
        sys.exit()


mainGame = MAIN()

screenUPDATE = pygame.USEREVENT
pygame.time.set_timer(screenUPDATE, 150)
running = True


def main():
    global screen, running

    while running:

        screen.fill((21, 141, 5))

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

                elif event.key == pygame.K_s:
                    if mainGame.snake.direction.y != -1:
                        mainGame.snake.direction = Vector2(0, 1)

                elif event.key == pygame.K_d:
                    if mainGame.snake.direction.x != -1:
                        mainGame.snake.direction = Vector2(1, 0)

                elif event.key == pygame.K_a:
                    if mainGame.snake.direction.x != 1:
                        mainGame.snake.direction = Vector2(-1, 0)

        clock.tick(60)
        mainGame.drawElements()
        pygame.display.update()


main()
