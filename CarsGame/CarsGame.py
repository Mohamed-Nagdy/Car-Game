import pygame
import os
import random

# the screen properties
WIDTH = 800
HEIGHT = 500
FPS = 80
SPEED_UP_TIME = 2000
RADIUS = 30

# initialize pygame and the sound mixer
pygame.init()
pygame.mixer.init()
# set the caption of the screen
pygame.display.set_caption("My First Game")
# create a screen with width and height we declare before
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# get the clock of the game
clock = pygame.time.Clock()

# draw text on the screen
fontName = pygame.font.match_font('arial')

# ######################################## start of images region ########################################
# the images folder and the images
scriptDirectory = os.path.dirname(__file__)
imagesDir = os.path.join(scriptDirectory, 'images')

# get the player images
playerImage = pygame.transform.scale(pygame.image.load(os.path.join(imagesDir, 'sample.png')), (120, 90))
playerLiveImage = pygame.transform.scale(playerImage, (25, 19))

# the image of the road
roadImage = pygame.transform.scale(pygame.image.load(os.path.join(imagesDir, 'road_tile_1.png')), (1600, 300))
backGround = pygame.image.load(os.path.join(imagesDir, 'sky.png'))
backGroundRect = backGround.get_rect()

# list of the images of the rocks
extraShapes = []
extraShapesNames = ['house_1.png', 'house_3.png', 'lights_2.png', 'market_2.png']
for rock in extraShapesNames:
    extraShapes.append(pygame.transform.scale(pygame.image.load(os.path.join(imagesDir, rock)), (200, 150)))

# the list of the cars vs you
enemyList = []
for i in range(2, 4):
    enemyList.append(pygame.transform.scale(pygame.image.load(os.path.join(imagesDir, 'car{}.png'.format(i+1))), (120, 90)))

# the image of the bump
bumpImage = pygame.transform.scale(pygame.image.load(os.path.join(imagesDir, 'stone2.jpg')), (30, 200))

# ######################################## end of images region ########################################


# ######################################## Begin Of Utility Functions ########################################


# this function to draw any text on the screen with any size and at any place we need
def drawText(surface, text, size, x, y):

    font = pygame.font.Font(fontName, size)

    # this true or false to specify if the text is alias or not
    textSurface = font.render(text, True, (255, 255, 255))
    textRect = textSurface.get_rect()

    # put the text in the mid top of the text rectangle
    textRect.midtop = (x, y)

    # put the text on the text surface where the text ract is
    surface.blit(textSurface, textRect)


# this function is used to draw the bar of power of our player
def drawBar(surface, x, y, value):
    if value < 0:
        value = 0

    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    realValue = (value / 100) * BAR_LENGTH

    # this rectangle who contain the inside rectangle which is the power
    outRectangle = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)

    # this rectangle will change at every change of the shield value of the player
    insideRectangle = pygame.Rect(x, y, realValue, BAR_HEIGHT)

    # the 2 here is the border of the rectangle
    pygame.draw.rect(surface, (255, 255, 255), outRectangle, 2)

    # change the color of the inside rectangle with change of the shield value
    if 50 >= realValue > 30:
        pygame.draw.rect(surface, (255, 255, 0), insideRectangle)
    elif realValue <= 30:
        pygame.draw.rect(surface, (255, 0, 0), insideRectangle)
    else:
        pygame.draw.rect(surface, (0, 255, 0), insideRectangle)


# this function use for draw the lives of the player
def drawLives(surface, x, y, lives, image):
    # go through the number of lives the player has and draw the lives
    for i in range(lives):
        imageRect = image.get_rect()
        imageRect.x = x + 30 * i
        imageRect.y = y
        surface.blit(image, imageRect)


def showGameOverScreen():
    # set the background of the game to this screen
    # screen.blit(backGround, backgroundRect)
    # put some text to our screen
    drawText(screen, "Car Crash Game", 80, WIDTH / 2, HEIGHT / 16)
    drawText(screen, "If You Crash Any Car You Lose Points", 40, WIDTH / 2, HEIGHT - 300)
    drawText(screen, "Press Any Key To Start", 30, WIDTH / 2, HEIGHT - 150)
    # flip the display to show our new screen
    pygame.display.flip()
    # this waiting variable to wait any reaction from the user
    waiting = True
    # wait till the user take any reaction
    while waiting:
        clock.tick(FPS)
        # check the events and do the things the user need
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


# this function used for reset all the speeds
def resetSpeed():
    road.xSpeed = 1
    shape1.xSpeed = 1
    shape2.xSpeed = 1
    shape3.xSpeed = 1
    ene.xSpeed = 1


# this function use to speed down the game if the player hit a bump
def speed_down(speedDown):
    road.xSpeed -= speedDown
    shape1.xSpeed -= speedDown
    shape2.xSpeed -= speedDown
    shape3.xSpeed -= speedDown
    bump.xSpeed -= speedDown
# ######################################## End Of Utility Functions ########################################


# ######################################## start of Road class ########################################
class Road(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = roadImage
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        # the speed of the road
        self.xSpeed = 1
        # the time to rise the speed
        self.speedRise = pygame.time.get_ticks()
        # set the left side of the road to zero
        self.rect.left = 0
        # set the bottom side of the road to the end of the game
        self.rect.bottom = HEIGHT

    def update(self):
        # if 2 seconds past speed up
        if pygame.time.get_ticks() - self.speedRise >= SPEED_UP_TIME:
            self.speedRise = pygame.time.get_ticks()
            self.xSpeed += 1

        # move the road to left side
        self.rect.centerx -= self.xSpeed

        # check if the road is moved 200 pixels make it back again
        if (self.rect.centerx - 200) <= 0:
            self.rect.centerx = WIDTH - 200

# ######################################## End of Road class ########################################


# ######################################## start of Extra Items class ########################################
class ExtraItems(pygame.sprite.Sprite):
    def __init__(self, left):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(extraShapes)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.xSpeed = 1
        self.speedRise = pygame.time.get_ticks()
        self.rect.left = left
        self.rect.bottom = HEIGHT - 250

    def update(self):
        if pygame.time.get_ticks() - self.speedRise >= SPEED_UP_TIME:
            self.speedRise = pygame.time.get_ticks()
            self.xSpeed += 1

        self.rect.centerx -= self.xSpeed

        if self.rect.right <= 0:
            self.image = random.choice(extraShapes)
            self.rect.left = WIDTH

# ######################################## End of Extra Items class ########################################


# ######################################## start of Player class ########################################


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerImage
        self.image.set_colorkey((0, 0, 0))
        # self.image.fill((145, 78, 200))
        self.rect = self.image.get_rect()
        # set the player in the center of the screen and far from the bottom side of the screen by 40 pixels
        self.rect.left = 0
        self.rect.bottom = HEIGHT
        # set the speed of it by 0
        self.speedy = 5
        self.energy = 100
        self.radius = RADIUS
        self.lives = 3

    def update(self):
        if self.rect.left < 200:
            self.rect.left += 1
        # this line to get any key is pressed
        keystate = pygame.key.get_pressed()

        # check if the left key is pressed
        if keystate[pygame.K_DOWN]:
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
            else:
                self.rect.y += self.speedy

        # check if the right key is pressed
        if keystate[pygame.K_UP]:
            if self.rect.top <= HEIGHT - 200:
                self.rect.top = HEIGHT - 200
            else:
                self.rect.y -= self.speedy

    def hide(self):
        self.rect.right = 0
# ######################################## end of Player class ########################################


# ######################################## start of Enemy class ########################################


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(enemyList)
        self.image.set_colorkey((0, 0, 0))
        # self.image.fill((145, 78, 200))
        self.rect = self.image.get_rect()
        # set the player in the center of the screen and far from the bottom side of the screen by 40 pixels
        self.rect.left = random.randrange(WIDTH, WIDTH + 300)
        self.rect.bottom = random.randrange(HEIGHT - 100, HEIGHT)
        # set the speed of it by 0
        self.xSpeed = 5
        self.speedRise = pygame.time.get_ticks()
        self.radius = RADIUS

    def update(self):
        if pygame.time.get_ticks() - self.speedRise >= SPEED_UP_TIME:
            self.speedRise = pygame.time.get_ticks()
            self.xSpeed += 2

        self.rect.centerx -= self.xSpeed

        if self.rect.right <= 0:
            self.image = random.choice(enemyList)
            self.rect.left = random.randrange(WIDTH, WIDTH + 300)
            self.rect.bottom = random.randrange(HEIGHT - 100, HEIGHT)


# ######################################## end of Enemy class ########################################


# ######################################## start of Bump class ########################################

class Bump(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bumpImage
        self.image.set_colorkey((0, 0, 0))
        # self.image.fill((145, 78, 200))
        self.rect = self.image.get_rect()
        # set the player in the center of the screen and far from the bottom side of the screen by 40 pixels
        self.rect.left = random.randrange(WIDTH + 1000, WIDTH + 10000)
        self.rect.top = HEIGHT - 180
        # set the speed of it by 0
        self.xSpeed = 1
        self.speedRise = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.speedRise >= SPEED_UP_TIME:
            self.speedRise = pygame.time.get_ticks()
            self.xSpeed += 1

        self.rect.centerx -= self.xSpeed

        if self.rect.right <= 0:
            self.image = bumpImage
            self.rect.left = random.randrange(WIDTH + 1000, WIDTH + 10000)
            self.rect.top = HEIGHT - 180

# ######################################## end of Bump class ########################################


gameOver = True
running = True
while running:
    # ######################################## start of input section ########################################
    # set the frame per second of the game
    clock.tick(FPS)
    if gameOver:

        gameOver = False

        screen.blit(backGround, backGroundRect)
        showGameOverScreen()

        # create the Group of all entities in the game
        allEntities = pygame.sprite.Group()
        extraItemsGroup = pygame.sprite.Group()
        enemyGroup = pygame.sprite.Group()
        bumpGroup = pygame.sprite.Group()

        # create all the entities of the game
        # create player object
        player = Player()

        # create enemy
        ene = Enemy()

        # create the road object
        road = Road()

        # create the bump of the road
        bump = Bump()

        # create the extra shapes objects
        shape1 = ExtraItems(random.randrange(0, 100))
        shape2 = ExtraItems(random.randrange(200, 400))
        shape3 = ExtraItems(random.randrange(500, 800))

        # add the player to the general group of the game
        allEntities.add(road)
        allEntities.add(shape1)
        allEntities.add(shape2)
        allEntities.add(shape3)
        allEntities.add(bump)
        allEntities.add(ene)
        allEntities.add(player)

        # add the extra items to the extra items group
        extraItemsGroup.add(shape1)
        extraItemsGroup.add(shape2)
        extraItemsGroup.add(shape3)

        # add enemy to enemy group
        enemyGroup.add(ene)

        # add the bump to the bumps Group
        bumpGroup.add(bump)

    # go through all the events of py game and check the events we need
    for event in pygame.event.get():
        # check if the event is the quit event we just quit from the loop
        if event.type == pygame.QUIT:
            running = False

    # ######################################## start of update section ########################################

    allEntities.update()

    playerHitEnemyCar = pygame.sprite.spritecollide(player, enemyGroup, True, pygame.sprite.collide_circle)

    for hit in playerHitEnemyCar:
        ene = Enemy()
        enemyGroup.add(ene)
        allEntities.add(ene)
        player.energy -= 10

        if player.energy <= 0:
            player.hide()
            player.lives -= 1
            player.energy = 100
            resetSpeed()

    # playerHitBumps = pygame.sprite.spritecollide(player, bumpGroup, False, False)
    #
    # for hit in playerHitBumps:
    #     speed_down(1)

    if player.lives == 0:
        gameOver = True

    # ######################################## start of drawing section ########################################
    # set the back ground of the screen to red
    screen.fill((255, 0, 0))
    # set the back ground image of the screen to back ground we have in the background rectangle of this image
    screen.blit(backGround, backGroundRect)

    # now we make the allEntities group to draw every thing inside it
    allEntities.draw(screen)
    drawBar(screen, 20, 20, player.energy)
    drawLives(screen, WIDTH - 100, 30, player.lives, playerLiveImage)
    pygame.draw.circle(screen, (255, 255, 0), (player.rect.centerx, player.rect.centery), player.radius)
    pygame.draw.circle(screen, (255, 255, 0), (ene.rect.centerx, ene.rect.centery), ene.radius)
    # after all drawing we just flip the screen to show our new draw
    pygame.display.flip()
# ######################################## end of the game loop ########################################

# after end the game and game loop we just quit from the py game
pygame.quit()