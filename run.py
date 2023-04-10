from random import randint

class Board:
    """
    Main board class.
    """

    def __init__(self, size, player_name, board_type):
        """
        initializing the grid with '.' characters for each tile
        """
        self.size = size
        self.grid = [['.' for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.player_name = player_name
        self.board_type = board_type

    def __str__(self):
        """
        returns a string representation of the board, 
        which is printed when the board needs to be displayed
        """
        s = f'{self.player_name} {self.board_type}\n'
        s += '   ' + ' '.join(str(i) for i in range(self.size)) + '\n'
        for i in range(self.size):
            s += f'{i} |{"|".join(self.grid[i])}|\n'
        return s

    def mark_ship(self, x, y):
        """
        adds a ship at on the board by 
        setting the corresponding tile on the grid to 'O'
        """
        self.ships.append((x, y))
        self.grid[x][y] = 'O' 

    def has_ship(self, x, y):
        """
        returns true if has a ship on it
        """
        return (x, y) in self.ships

    def is_valid(self, x, y):
        """
        returns true if location is witihn bounds
        """
        return 0 <= x < self.size and 0 <= y < self.size and self.grid[x][y] == '.'
    
                   