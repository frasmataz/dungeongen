class Tile:
    items = []
    colour = ''

class Wall(Tile):
    def __init__(self):
        self.colour = 'black'

class Air(Tile):
    def __init__(self):
        self.colour = 'white'