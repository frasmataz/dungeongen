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
    #Return a new map of wall tiles
    return [[tiles.Wall() for y in range(mapy)] for x in range(mapx)]

def printmap(map):
    global firstFrame

    #Scroll cursor up to print over the previous frame
    if not firstFrame:
        for i in range(mapx + 2):
            sys.stdout.write("\033[F")

    #Iterate through tiles; build string to output
    output = ''
    for i in range(mapx):
        for j in range(mapy):
            if type(map[i][j]) is tiles.Wall:
                output += colored('#', 'white', map[i][j].bgcolor)
            elif type(map[i][j]) is tiles.Air:
                output += colored(' ', 'white', map[i][j].bgcolor)
        output += '\n'

    #Print completed frame
    print(output)
    print()
    firstFrame = False

def addRooms(map):
    print('Generating rooms..')
    noOfRooms = random.randint(RoomProps.minNoOfRooms, RoomProps.maxNoOfRooms)
    rooms = []

    #Generate a heap of rooms in the centre of the map
    for i in range(noOfRooms):
        roomValid = False
        room = None

        while not roomValid:
            w = int(np.random.normal(RoomProps.meanWidth, RoomProps.sizeStdDev))
            h = int(np.random.normal(RoomProps.meanHeight, RoomProps.sizeStdDev))

            #Room is valid if it is over a certain size
            if w > 2 and h > 2:
                roomValid = True
                room = Room(w, h)

        #Place the room somewhere near the centre
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

                        #Shoogle rooms away from each other, speeds up generation
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


        if roomsAreColliding:
            for room in rooms:
                if room.isColliding:
                    room.shoogle(mapx, mapy)

    #Now that rooms are placed, mark them on the map
    for room in rooms:
        for x in range(room.x, room.x + room.w):
            for y in range(room.y, room.y + room.h):
                map[x][y] = tiles.Air()

    #Create triangulated graph between rooms, in advance of placing corridors
    midpoints = []
    for room in rooms:
        midpoints.append(room.getMidpoint())

    midpoints = np.array(midpoints)
    tris = Delaunay(midpoints)

    #Draw lines to visualise the generated graph
    #Not necessary, but nice for debugging
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

    #Calculate minimum spanning tree
    tree_edges = util.minimum_tree(midpoints.tolist())

    for edge in tree_edges:
        for pixel in util.interpolate_pixels_along_line(edge[0][0], edge[0][1], edge[1][0], edge[1][1]):
            if pixel[0] < mapx and pixel[1] < mapy:
                map[int(pixel[0])][int(pixel[1])].bgcolor = 'on_blue'

    #Color room midpoints red
    #Again, not necessary, just for debugging
    for mp in midpoints:
        map[mp[0]][mp[1]].bgcolor = 'on_red'

    #Print map to terminal
    printmap(map)

    print('Finished generating rooms in ' + str(cycles) + ' cycles')
    return map


def generate(map):
    map = addRooms(map)
    return map

#Main program flow
map = setupMap()
map = generate(map)