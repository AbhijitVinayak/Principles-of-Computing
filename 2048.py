"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    prev = 0    #the last compared nonzero value
    merge_list = []   #the merge list
    for tile in line:
        if tile == prev and prev !=0: #merges
            prev = 0
            merge_list.pop()
            merge_list.append(tile*2)
        elif tile != 0:
            prev = tile
            merge_list.append(tile)
    return merge_list + [0 for dummy_x in range(len(line)-len(merge_list))]

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height #store the height and width of the grid
        self._grid_width = grid_width
        self._cells = []
        _up = [ (0, dummy_up) for dummy_up in range(grid_width)]
        _down = [ (grid_height-1, dummy_down) for dummy_down in range(grid_width)]
        _right = [ (dummy_right, grid_width-1) for dummy_right in range(grid_height)]
        _left = [ (dummy_left, 0) for dummy_left in range(grid_height)]
        self._direction = {UP: _up, DOWN: _down, LEFT: _left, RIGHT: _right}
        #creates the initial 2048 board
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._cells = [ [0 for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return ' '.join(''.join(str(dummy_tile) for dummy_tile in dummy_row) for dummy_row in self._cells)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        indice_list = self._direction[direction]
        line_range = {UP: range(self._grid_height), DOWN: range(self._grid_height),
                        LEFT: range(self._grid_width), RIGHT: range(self._grid_width)}
        new_add = 0
        for indice in indice_list:
            temporary = []
            for num in line_range[direction]:   # retrieve the line in on direction
                row = OFFSETS[direction][0]*num + indice[0]
                col = OFFSETS[direction][1]*num + indice[1]
                temporary += [ self._cells[row][col] ]
            temporary = merge(temporary)        # merge the line
            for num in line_range[direction]:   # store the merged tile values back into the grid
                row = OFFSETS[direction][0]*num + indice[0]
                col = OFFSETS[direction][1]*num + indice[1]
                if self._cells[row][col] != temporary[num]:
                    new_add =1                
                self._cells[row][col] = temporary[num]
        if new_add == 1:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty = [] # row and column of empty grid square
        random_tile = [2 for dummy_x in range(9)] + [4]
        for dummy_i, row in enumerate(self._cells):   # find empty grid square
            for dummy_j, tile in enumerate(row):
                if tile == 0: 
                    empty += [(dummy_i, dummy_j)]
        row, col = random.choice(empty)        # randomly select a grid
        self._cells[row][col] = random.choice(random_tile)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._cells[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._cells[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
