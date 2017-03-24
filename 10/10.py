"""
Data structure for coroutiune puzzles.

Oliver Reid - 2569385
Thomas Youngson - 7444007
"""

class Coin:
    'Data structure to hold information and behaviour about coins in the'
    'coroutine puzzle'

    # Data fields
    x = 0
    y = 0

    # Helper method to 
    moves = {
        'N': [1, 0],
        'NE': [1, 1],
        'E': [0, 1],
        'SE': [-1, 1],
        'S': [-1, 0],
        'SW': [-1, -1],
        'W': [0, -1],
        'NW': [1, -1]
    }

    def __init__(self, y, x):
        self.y = y
        self.x = x

    def move(self, direction):
        self.y += self.moves.get(direction)[0]
        self.x += self.moves.get(direction)[1]

    def loc(self):
        print(self.y, self._fx)
    

class Grid:
    'Data structure to hold information about the coroutine puzzle grid'

    # Data fields


    grid = [[]]

c1 = Coin(0, 0)
c1.move('S')
c1.loc()