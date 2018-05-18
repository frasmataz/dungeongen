import tiles
from room import RoomProps
from room import Room
import random
import numpy as np
from termcolor import cprint
from pprint import pprint

mapx, mapy = 30, 50

def setupMap():
    return [[tiles.Wall() for y in range(mapy)] for x in range(mapx)]

def printmap(map):
    for i in range(mapx):
        for j in range(mapy):
            if type(map[i][j]) is tiles.Wall:
                print('.', end='')
            elif type(map[i][j]) is tiles.Air:
                cprint(' ', 'white', map[i][j].bgcolor, end='')
        print()


def rectCollide(x1, y1, w1, h1, x2, y2, w2, h2):
    x1 = x1 - 1
    y1 = y1 - 1
    w1 = w1 + 1
    h1 = h1 + 1
    x2 = x2 - 1
    y2 = y2 - 1
    w2 = w2 + 1
    h2 = h2 + 1
    return (x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            h1 + y1 > y2)


def addRooms(map):
    print('Generating rooms..')
    noOfRooms = random.randint(RoomProps.minNoOfRooms, RoomProps.maxNoOfRooms)
    rooms = []

    for i in range(noOfRooms):
        #Create a room
        roomValid = False
        room = None

        while not roomValid:
            w = int(np.random.normal(RoomProps.meanWidth, RoomProps.sizeStdDev))
            h = int(np.random.normal(RoomProps.meanHeight, RoomProps.sizeStdDev))

            if w > 0 and h > 0:
                roomValid = True
                room = Room(w, h)

        x = int(np.random.normal((mapx-w)/2, 1.0))
        y = int(np.random.normal((mapy-h)/2, 1.0))

        room.setPos(x, y)
        room.setBgColor(random.choice(RoomProps.bgcolors))
        rooms.append(room)

    #Shoogle rooms about until they're not touching
    # roomsAreColliding = True
    # for room in rooms:

    for room in rooms:
        for x in range(room.x, room.x + room.w):
            for y in range(room.y, room.y + room.h):
                map[x][y] = tiles.Air()
                map[x][y].setBgColor(room.bgcolor)

    return map


def generate(map):
    map = addRooms(map)
    return map


map = setupMap()
map = generate(map)
printmap(map)