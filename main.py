import itertools
import sys

class Solver:
    """
    Solver for a given sudoku.
    """
    def __init__(self, start_layout, grid_x, grid_y, value_set):
        """
        Parameters
        ----------
        start_layout : nested list of the board given as one row per inside list.

        grid_x : number of cells in the width of a grid

        grid_y : number of cells in the height of a grid

        value_set : set of values that make up one row/col/grid
        """
        
        assert all([len(r) == len(start_layout) for r in start_layout]), "Number of rows != number of columns for one or more rows."
        self.rows = start_layout
        self.cols = [list(row) for row in zip(*self.rows)]

        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grids = [[] for i in range(len(self.rows))]
        self.coords = []

        for i, row in enumerate(self.rows):
            for j, val in enumerate(row):
                if val is None:
                    self.coords.append((i, j, j//self.grid_x + grid_y*(i//self.grid_y)))
                self.grids[j//self.grid_x + grid_y*(i//self.grid_y)].append(val)
            
        self.value_set = set(list(value_set)+[None])

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def get_grids(self):
        return self.grids

    def get_coords(self):
        return self.coords

    def update_options(self):
        existing = {c: set(self.rows[c[0]] + self.cols[c[1]] + self.grids[c[2]])
        for c in self.coords}
        self.options = {c: self.value_set - existing[c] for c in self.coords}

    def get_options(self):
        return self.options

    def update_board(self):
    
        empty = list(self.options.keys())

        for c in empty:
            if len(self.options[c]) == 1:
                only_choice = self.options.pop(c).pop()
                self.rows[c[0]][c[1]] = only_choice
                self.cols[c[1]][c[0]] = only_choice
                self.grids[c[2]][self.grid_x*(c[0]%self.grid_x) + (c[1]%self.grid_y)] = only_choice

        self.coords = list(self.options.keys())

    def solve(self, limit=1000, verbose=False):
        i=0
        while (len(self.coords) > 0):
            if i > limit:
                print("Limit reached of {:d} iterations".format(limit))
                sys.exit(1)
            self.update_options()
            self.update_board()
            if verbose:
                print("{:d} cells left to solve".format(len(self.coords)))
                print(self.options)
            i+=1
        
        print("Solved in {:d} iterations".format(i))

        return self.rows




if __name__=="__main__":
    easy_sudoku = [
        [8, None, None, None ,6,4,1,5,7],
        [None, 4, None, None, None, 9, None, None, 3],
        [None, None, None, 5, 7, 2, 8, 9, None],
        [3, None, None, 2, None, None, None, None, 9],
        [None, 7, None, None, None, 8, None, None, 6],
        [4, 5, None, 9, None, 7, None, None, None],
        [2, 6, 8, None, None, None, 9, 1, None],
        [1, None, 4, None, None, 5, 3, 7, 8],
        [7, None, None, 8, None, None, None, None, 2]
    ]

    hard_sudoku = [
        [None, None,9,8,None, 6, None, 3, 4],
        [4, None, None,1, None, None,None, 8, 7],
        [2, None, None, 4, None , None, None ,9 , None],
        [3, None, None, None, None, None, None, None, None],
        [None, None, 7, None, 5, None, 8, None, None],
        [None, None, None, None, None, None, None, None, 6],
        [None, 7, None, None, None, 2, None, None, 8],
        [8, 4, None, None, None, 1, None, None, 3],
        [6,3,None, 5, None, 8, 7, None, None]

    ]

    s = Solver(easy_sudoku, 3, 3, range(1,10))
    print("Attempting easy sudoku.\n", s.solve())

    s = Solver(hard_sudoku, 3, 3, range(1,10))
    print("Attempting hard sudoku.\n", s.solve(limit=1, verbose=True))