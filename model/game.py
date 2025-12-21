class Game:
    def __init__(self, board, human_player, ai_player):
        self.board = board
        self.human = human_player
        self.ai = ai_player
        self.current_player = 'X'
        self.finished = False

    def switch_turn(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_end(self):
        if self.board.has_winner('X'):
            self.finished = True
            return 'X'
        if self.board.has_winner('O'):
            self.finished = True
            return 'O'
        if self.board.is_full():
            self.finished = True
            return 'Draw'
        return None
