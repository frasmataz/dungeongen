import random

class RoomProps:
    meanWidth = 5
    meanHeight = 10
    sizeStdDev = 2
    minNoOfRooms = 10
    maxNoOfRooms = 50
    colors = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    bgcolors = ['on_grey', 'on_red', 'on_green', 'on_yellow', 'on_blue', 'on_magenta', 'on_cyan', 'on_white']

class Room:
    def __init__(self):
        self.isColliding = False
        self.shoogleDir = [1,1]
        pass

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.isColliding = False
        self.shoogleDir = [1,1]

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def shoogle(self, mapx, mapy):
        #Randomly move X and Y by one
        dx = random.choice([0, self.shoogleDir[0]])
        dy = random.choice([0, self.shoogleDir[1]])

        if (self.x + self.w + dx < mapx and
            self.x + dx >= 0 and
            self.y + self.h + dy < mapy and
            self.y + dy >= 0):

            self.x = self.x + dx
            self.y = self.y + dy

    def getMidpoint(self):
        return [self.x + (self.w / 2), self.y + (self.h / 2)]

    def setColor(self, color):
        self.color = color

    def setBgColor(self, bgcolor):
        self.bgcolor = bgcolor