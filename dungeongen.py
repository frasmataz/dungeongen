import tiles
import random
from pprint import pprint

mapx, mapy = 30, 50

roomGenProps = {
    'minSize': [2, 3],
    'maxSize': [10, 15],
    'minNoOfRooms': 2,
    'maxNoOfRooms': 25
}

map = [[tiles.Wall() for y in range(mapy)] for x in range(mapx)]

def printmap():
    for i in range(mapx):
        for j in range(mapy):
            if type(map[i][j]) is tiles.Wall:
                print('#', end='')
            elif type(map[i][j]) is tiles.Air:
                print(' ', end='')
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


def addRooms():
    print('Generating rooms..')
    noOfRooms = random.randint(roomGenProps['minNoOfRooms'], roomGenProps['maxNoOfRooms'])
    rooms = []

    while len(rooms) < noOfRooms:
        width = random.randint(roomGenProps['minSize'][0], roomGenProps['maxSize'][0])
        height = random.randint(roomGenProps['minSize'][1], roomGenProps['maxSize'][1])
        x = random.randint(0, mapx-width)
        y = random.randint(0, mapy-height)

        spaceIsClear = True

        if len(rooms) > 0:
            for room in rooms:
                if rectCollide(room['x'], room['y'], room['w'], room['h'], x, y, width, height):
                    spaceIsClear = False

        if spaceIsClear:
            rooms.append({
                'x': x,
                'y': y,
                'w': width,
                'h': height
            })

    for room in rooms:
        for x in range(room['x'], room['x'] + room['w']):
            for y in range(room['y'], room['y'] + room['h']):
                map[x][y] = tiles.Air()

    print('Done generating rooms')



def generate():
    addRooms()

generate()
printmap()