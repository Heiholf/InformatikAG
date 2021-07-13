import game as Game

Game.start()
Game.load(1)
print("Started")
Game.turnLeft()
print(Game.isInFrontOfWall())
Game.pause()
Game.move()
Game.turnLeft()
Game.move()
Game.pickUp()
Game.turnRight()
Game.turnRight()
Game.move()
Game.move()
Game.drop()

Game.pause()


print("Finished")

