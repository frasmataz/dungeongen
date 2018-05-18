import random

class RoomProps:
    meanWidth = 5
    meanHeight = 10
    sizeStdDev = 2
    minNoOfRooms = 10
    maxNoOfRooms = 10
    colors = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    bgcolors = ['on_grey', 'on_red', 'on_green', 'on_yellow', 'on_blue', 'on_magenta', 'on_cyan', 'on_white']

class Room:
    def __init__(self):
        pass

    def __init__(self, w, h):
        self.w = w
        self.h = h

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def shoogle(self):
        #Randomly move X and Y by one
        self.x = self.x + random.randint(-1, 1)
        self.y = self.y + random.randint(-1, 1)

    def setColor(self, color):
        self.color = color

    def setBgColor(self, bgcolor):
        self.bgcolor = bgcolor