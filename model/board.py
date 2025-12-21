import copy

class Board:
    """
    Representa el tablero del juego.
    """
    def __init__(self, size):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]

    def clone(self):
        return copy.deepcopy(self)

    def is_empty(self, row, col):
        return self.grid[row][col] == ' '

    def place(self, row, col, symbol):
        if self.is_empty(row, col):
            self.grid[row][col] = symbol
            return True
        return False

    def undo(self, row, col):
        self.grid[row][col] = ' '

    def get_legal_moves(self):
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self.is_empty(r, c):
                    moves.append((r, c))
        return moves

    def is_full(self):
        return all(self.grid[r][c] != ' ' for r in range(self.size) for c in range(self.size))

    def has_winner(self, symbol):
        n = self.size

        # Filas y columnas
        for i in range(n):
            if all(self.grid[i][j] == symbol for j in range(n)):
                return True
            if all(self.grid[j][i] == symbol for j in range(n)):
                return True

        # Diagonales
        if all(self.grid[i][i] == symbol for i in range(n)):
            return True
        if all(self.grid[i][n - i - 1] == symbol for i in range(n)):
            return True

        return False
