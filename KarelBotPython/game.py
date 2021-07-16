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
    gems = []
    walls = []
    gemGoals = []
    goalPosition = ()

    def read(self, data):
        lines = data.split("\n")
        self.position = eval(lines[0])
        self.orientation = eval(lines[1])
        if len(lines) >= 3:
            self.gems = eval(lines[2])
        if len(lines) >= 4:
            self.walls = eval(lines[3])
        if len(lines) >= 5:
            self.gemGoals = eval(lines[4])
        if len(lines) >= 6:
            self.goalPosition = eval(lines[5])


running = False
orientation = 0
screen = None
level = Level()
gems = []
walls = []
gemGoals = []
goalPosition = ()
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

gemIndicator = pyg.image.load("gemIndicator.png")
gemIndicator = colorize(gemIndicator, ((50, 255, 50)))
gemIndicator = pyg.transform.scale(
    gemIndicator, (math.floor(tileSize * 1.5), math.floor(tileSize * 1.5)))
gemIndicator.set_alpha(200)

gemGoalImage = gemImage.copy()
gemGoalImage.set_alpha(50)

goalImage = gemImage.copy()
goalImage = colorize(goalImage, (255,255,255))
goalImage.set_alpha(50)


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
    if(isInFrontOfWall()):
        raise Exception("Der Charakter stand vor einer Wand.")
    global positionX
    global positionY
    rotation = orientation % 4
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

    # GemGoals
    for gGoal in gemGoals:
        screen.blit(gemGoalImage, (gGoal[0] * 50, gGoal[1] * 50))

    # Goal
    if not goalPosition == ():
        screen.blit(goalImage, (goalPosition[0] * 50, goalPosition[1] * 50))

    # Walls
    for wall in walls:
        w = 50
        h = 50
        x = wall[0][0] * tileSize
        y = wall[0][1] * tileSize
        if wall[1] == "r":
            w = tileSize / 10
            h = tileSize
            x = x + tileSize
        elif wall[1] == "u":
            w = tileSize
            h = tileSize / 10
        elif wall[1] == "l":
            w = tileSize / 10
            h = tileSize
        elif wall[1] == "d":
            w = tileSize
            h = tileSize / 10
            y = y + tileSize
        pyg.draw.rect(screen, (255, 255, 255), (x, y, w, h))

    # Gems
    for gem in gems:
        screen.blit(gemImage, (gem[0] * 50, gem[1] * 50))

    # Charakter
    new = pyg.transform.rotate(image, 90 * orientation)
    screen.blit(new, (positionX * tileSize, positionY * tileSize)),

    # GemAnzeige
    if(carrying):
        screen.blit(gemIndicator, (0, 0))

    pyg.display.update()


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
    global gems
    global walls
    global gemGoals
    global goalPosition
    filename = "Level" + str(index) + ".lvl"
    with open(filename) as file:
        content = file.read()
        l = Level()
        l.read(content)
        level = l
        positionX = l.position[0]
        positionY = l.position[1]
        orientation = l.orientation
        gems = l.gems
        walls = l.walls
        gemGoals = l.gemGoals
        goalPosition = l.goalPosition
    redraw()


def pickUp():
    global gems
    global carrying
    if(carrying):
        raise Exception("Der Charakter trägt schon etwas.")
    if(isOnGem()):
        carrying = True
        gems.remove((positionX, positionY))
    else:
        raise Exception(
            "An der Position des Charakters gab es nichts zum Aufheben.")
    redraw()


def drop():
    global gems
    global carrying
    if(isOnGem()):
        raise Exception("An dem Ort lag schon etwas.")
    if(carrying):
        gems.append((positionX, positionY))
        carrying = False
    else:
        raise Exception("Der Charakter hatte nichts aufgehoben.")
    redraw()


def isOnGem():
    return (positionX, positionY) in gems


def isInFrontOfWall():
    return (((positionX, positionY), orientationToLetter(orientation)) in walls) or (((positionX + orientationToVector(orientation)[0], positionY + orientationToVector(orientation)[1]), orientationToLetter(orientation - 2))) in walls


def orientationToLetter(orientation):
    rotation = orientation % 4
    if(rotation == 0):
        return "u"
    elif(rotation == 1):
        return "l"
    elif(rotation == 2):
        return "d"
    else:
        return "r"


def orientationToVector(orientation):
    rotation = orientation % 4
    positionX = 0
    positionY = 0
    if(rotation == 0):
        positionY = positionY - 1
    elif(rotation == 1):
        positionX = positionX - 1
    elif(rotation == 2):
        positionY = positionY + 1
    else:
        positionX = positionX + 1
    return (positionX, positionY)


def isOnGemGoal():
    return (positionX, positionY) in gemGoals


def isOnGoal():
    return (positionX, positionY) == goalPosition

def hasFinished():
    try:
        finish()
    except:
        return False
    return True

def finish():
    if (not goalPosition == (positionX, positionY)) and (not goalPosition == ()):
        raise Exception("Spieler war nicht am Ziel")
    if not gems == gemGoals:
        raise Exception("Die Gems waren nicht alle  im Ziel")
    print("Level geschafft")
    pause()

    
