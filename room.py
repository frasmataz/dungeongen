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
        pass

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.isColliding = False

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def shoogle(self, mapx, mapy):
        #Randomly move X and Y by one
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)

        if (self.x + self.w + dx < mapx and
            self.x + dx >= 0 and
            self.y + self.h + dy < mapy and
            self.y + dy >= 0):

            self.x = self.x + dx
            self.y = self.y + dy



    def setColor(self, color):
        self.color = color

    def setBgColor(self, bgcolor):
        self.bgcolor = bgcolor