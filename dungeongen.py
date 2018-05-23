import tiles
from room import RoomProps
from room import Room
import random
import sys
import numpy as np
from termcolor import colored, cprint
from scipy.spatial import Delaunay
from pprint import pprint
import math

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

def interpolate_pixels_along_line(x0, y0, x1, y1):
    """Uses Xiaolin Wu's line algorithm to interpolate all of the pixels along a
    straight line, given two points (x0, y0) and (x1, y1)

    Wikipedia article containing pseudo code that function was based off of:
        http://en.wikipedia.org/wiki/Xiaolin_Wu's_line_algorithm
    """
    pixels = []
    steep = abs(y1 - y0) > abs(x1 - x0)

    # Ensure that the path to be interpolated is shallow and from left to right
    if steep:
        t = x0
        x0 = y0
        y0 = t

        t = x1
        x1 = y1
        y1 = t

    if x0 > x1:
        t = x0
        x0 = x1
        x1 = t

        t = y0
        y0 = y1
        y1 = t

    dx = x1 - x0
    dy = y1 - y0
    if dx != 0 or dy != 0:
        gradient = dy / dx  # slope

        # Get the first given coordinate and add it to the return list
        x_end = round(x0)
        y_end = y0 + (gradient * (x_end - x0))
        xpxl0 = x_end
        ypxl0 = round(y_end)
        if steep:
            pixels.extend([(ypxl0, xpxl0), (ypxl0 + 1, xpxl0)])
        else:
            pixels.extend([(xpxl0, ypxl0), (xpxl0, ypxl0 + 1)])

        interpolated_y = y_end + gradient

        # Get the second given coordinate to give the main loop a range
        x_end = round(x1)
        y_end = y1 + (gradient * (x_end - x1))
        xpxl1 = x_end
        ypxl1 = round(y_end)

        # Loop between the first x coordinate and the second x coordinate, interpolating the y coordinates
        for x in range(xpxl0 + 1, xpxl1):
            if steep:
                pixels.extend([(math.floor(interpolated_y), x), (math.floor(interpolated_y) + 1, x)])

            else:
                pixels.extend([(x, math.floor(interpolated_y)), (x, math.floor(interpolated_y) + 1)])

            interpolated_y += gradient

        # Add the second given coordinate to the given list
        if steep:
            pixels.extend([(ypxl1, xpxl1), (ypxl1 + 1, xpxl1)])
        else:
            pixels.extend([(xpxl1, ypxl1), (xpxl1, ypxl1 + 1)])
    else:
        pixels.extend([(x0, x1), (y0, y1)])

    return pixels


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
                    if rectCollide(room1.x, room1.y, room1.w, room1.h, room2.x, room2.y, room2.w, room2.h):
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

        for pixel in interpolate_pixels_along_line(a[0], a[1], b[0], b[1]):
            if pixel[0] < mapx and pixel[1] < mapy:
                map[int(pixel[0])][int(pixel[1])].bgcolor = 'on_green'
        for pixel in interpolate_pixels_along_line(b[0], b[1], c[0], c[1]):
            if pixel[0] < mapx and pixel[1] < mapy:
                map[int(pixel[0])][int(pixel[1])].bgcolor = 'on_green'
        for pixel in interpolate_pixels_along_line(a[0], a[1], c[0], c[1]):
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