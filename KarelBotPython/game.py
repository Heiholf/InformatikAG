import pygame as pyg
import time
import sys
import math


def colorize(image, newColor):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param newColor: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()

    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pyg.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(newColor[0:3] + (0,), None, pyg.BLEND_RGBA_ADD)

    return image


class Level:

    position = (0, 0)
    orientation = 0

    def read(self, data):
        lines = data.split("\n")
        self.position = (int(lines[0].split(",")[0]),
                         int(lines[0].split(",")[1]))
        self.orientation = int(lines[1])


running = False
orientation = 0
screen = None
level = Level()
gems = [(1, 1)]
carrying = False

width = 600
height = 600
tileSize = 50
positionX = 0
positionY = 0
image = pyg.image.load("arrow.png")
image = pyg.transform.scale(image, (tileSize, tileSize))

gemImage = pyg.image.load("gem.png")
gemImage = colorize(gemImage, (50, 255, 50))
gemImage = pyg.transform.scale(gemImage, (tileSize, tileSize))
gemImage.set_alpha(200)

gemIndicator = pyg.image.load("gemIndicator.png")
gemIndicator = colorize(gemIndicator, ((50, 255, 50)))
gemIndicator = pyg.transform.scale(
    gemIndicator, (math.floor(tileSize * 1.5), math.floor(tileSize * 1.5)))
gemIndicator.set_alpha(200)


backgroundimage = pyg.image.load("background.png")
backgroundimage = pyg.transform.scale(backgroundimage, (tileSize, tileSize))
backgroundimage.set_alpha(100)


def start():

    global running
    running = True
    global screen
    pyg.init()
    pyg.display.set_caption("Spiel")
    screen = pyg.display.set_mode((width, height))

    redraw()

    """
    while running:
        # event handling, gets all event from the event queue
        for event in pyg.event.get():
            # only do something if the event is of type QUIT
            if event.type == pyg.QUIT:
                # change the value to False, to exit the main loop
                running = False"""


def turnLeft():
    global orientation
    orientation = orientation + 1
    redraw()


def turnRight():
    global orientation
    orientation = orientation - 1
    redraw()


def move():

    global positionX
    global positionY
    rotation = orientation % 4
    print(rotation)
    if(rotation == 0):
        positionY = positionY - 1
    elif(rotation == 1):
        positionX = positionX - 1
    elif(rotation == 2):
        positionY = positionY + 1
    else:
        positionX = positionX + 1
    redraw()


def redraw():
    animate()
    global screen
    screen.fill((0, 0, 0))

    # Hintergrund
    for x in range(0, width, 50):
        for y in range(0, width, 50):
            screen.blit(backgroundimage, (x, y))

    # Gems
    for gem in gems:
        screen.blit(gemImage, (gem[0] * 50, gem[1] * 50))

    # Charakter
    new = pyg.transform.rotate(image, 90 * orientation)
    screen.blit(new, (positionX * tileSize, positionY * tileSize)),

    # GemAnzeige
    if(carrying):
        screen.blit(gemIndicator, (0, 0))

    pyg.display.flip()


def animate():
    time.sleep(0.3)


def pause():
    pause = True
    while pause:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                sys.exit()
            if event.type == pyg.KEYDOWN:
                pause = False


def load(index):
    global level
    global positionX
    global positionY
    global orientation
    filename = "Level" + str(index) + ".lvl"
    with open(filename) as file:
        content = file.read()
        l = Level()
        l.read(content)
        level = l
        positionX = l.position[0]
        positionY = l.position[1]
        orientation = l.orientation
    redraw()


def pickUp():
    global gems
    global carrying
    if(carrying):
        raise Exception("Der Charakter trägt schon etwas.")
    i = False
    for gem in gems:
        if (positionX, positionY) == gem:
            i = True
            carrying = True
            gems.remove(gem)
            break
    if(not i):
        raise Exception(
            "An der Position des Charakters gab es nichts zum Aufheben.")
    redraw()


def drop():
    global gems
    global carrying
    i = False
    for gem in gems:
        if (positionX, positionY) == gem:
            i = True
            break
    if(i):
        raise Exception("An dem Ort lag schon etwas.")
    if(carrying):
        gems.append((positionX, positionY))
        carrying = False
    else:
        raise Exception("Der Charakter hatte nichts aufgehoben.")
    redraw()
