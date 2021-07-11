import pygame as pyg
import time

running = False
orientation = 0
screen = None

width = 600
height = 600
tileSize = 50
positionX = 0
positionY = 0
image = pyg.image.load("arrow.png")
image = pyg.transform.scale(image, (tileSize,tileSize))



def start():
    
    global running
    running = True
    global screen
    pyg.init()
    pyg.display.set_caption("Spiel")
    screen = pyg.display.set_mode((width,height))

    
    screen.blit(image,(0,0))
    pyg.display.flip()

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
    screen.fill((0,0,0))
    new = pyg.transform.rotate(image, 90 * orientation)
    screen.blit(new,(positionX * tileSize, positionY * tileSize))
    pyg.display.flip()


def animate():
    time.sleep(0.3)

   
def pause():
    pause = True
    while pause:
        for event in pyg.event.get():
            if event.type == pyg.KEYDOWN:
                pause = False