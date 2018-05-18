class Tile:
    items = []
    color = ''
    bgcolor = ''

    def setColor(self, color):
        self.color = color

    def setBgColor(self, bgcolor):
        self.bgcolor = bgcolor

class Wall(Tile):
    def __init__(self):
        self.colour = 'black'

class Air(Tile):
    def __init__(self):
        self.colour = 'white'