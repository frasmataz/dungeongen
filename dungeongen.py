import tiles
from room import RoomProps
from room import Room
import util
import random
import sys
import numpy as np
from termcolor import colored, cprint
from scipy.spatial import Delaunay
from pprint import pprint

mapx, mapy = 50, 50
firstFrame = True

def setupMap():
    return [[tiles.Wall() for y in range(mapy)] for x in range(mapx)]

def printmap(map):
    global firstFrame
    if not firstFrame:
        for i in range(mapx + 2):
            sys.stdout.write("\033[F")

    output = ''
    for i in range(mapx):
        for j in range(mapy):
            if type(map[i][j]) is tiles.Wall:
                output += colored('#', 'white', map[i][j].bgcolor)
            elif type(map[i][j]) is tiles.Air:
                output += colored(' ', 'white', map[i][j].bgcolor)
        output += '\n'
    print(output)
    print()
    firstFrame = False

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

            if w > 2 and h > 2:
                roomValid = True
                room = Room(w, h)

        x = int(np.random.normal((mapx-w)/2, 1.0))
        y = int(np.random.normal((mapy-h)/2, 1.0))

        room.setPos(x, y)
        rooms.append(room)

    #Shoogle rooms about until they're not touching
    roomsAreColliding = True
    cycles = 0

    while roomsAreColliding:
        cycles = cycles + 1
        for room in rooms:
            room.isColliding = False

        roomsAreColliding = False
        for room1 in rooms:
            for room2 in rooms:
                if not room1 == room2:
                    if util.rectCollide(room1.x, room1.y, room1.w, room1.h, room2.x, room2.y, room2.w, room2.h):
                        roomsAreColliding = True
                        room1.isColliding = True
                        room2.isColliding = True

                        if room1.getMidpoint()[0] >= room2.getMidpoint()[0]:
                            room1.shoogleDir[0] = 1
                            room2.shoogleDir[0] = -1
                        else:
                            room1.shoogleDir[0] = -1
                            room2.shoogleDir[0] = 1

                        if room1.getMidpoint()[1] >= room2.getMidpoint()[1]:
                            room1.shoogleDir[1] = 1
                            room2.shoogleDir[1] = -1
                        else:
                            room1.shoogleDir[1] = -1
                            room2.shoogleDir[1] = 1


        map = setupMap()

        for room in rooms:
            for x in range(room.x, room.x + room.w):
                for y in range(room.y, room.y + room.h):
                    map[x][y] = tiles.Air()

        if roomsAreColliding:
            for room in rooms:
                if room.isColliding:
                    room.shoogle(mapx, mapy)

    #Get triangulation
    midpoints = []
    for room in rooms:
        midpoints.append(room.getMidpoint())

    midpoints = np.array(midpoints)
    tris = Delaunay(midpoints)

    for tri in midpoints[tris.simplices]:
        a = tri[0]
        b = tri[1]
        c = tri[2]

        for pixel in util.interpolate_pixels_along_line(a[0], a[1], b[0], b[1]):
            if pixel[0] < mapx and pixel[1] < mapy:
                map[int(pixel[0])][int(pixel[1])].bgcolor = 'on_green'
        for pixel in util.interpolate_pixels_along_line(b[0], b[1], c[0], c[1]):
            if pixel[0] < mapx and pixel[1] < mapy:
                map[int(pixel[0])][int(pixel[1])].bgcolor = 'on_green'
        for pixel in util.interpolate_pixels_along_line(a[0], a[1], c[0], c[1]):
            if pixel[0] < mapx and pixel[1] < mapy:
                map[int(pixel[0])][int(pixel[1])].bgcolor = 'on_green'

    for mp in midpoints:
        map[mp[0]][mp[1]].bgcolor = 'on_red'


    printmap(map)

    print('Finished generating rooms in ' + str(cycles) + ' cycles')
    return map


def generate(map):
    map = addRooms(map)
    return map


map = setupMap()
map = generate(map)