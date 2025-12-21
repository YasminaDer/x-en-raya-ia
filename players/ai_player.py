class AIPlayer:
    def __init__(self, symbol, agent):
        self.symbol = symbol
        self.agent = agent

    def choose_move(self, board):
        return self.agent.get_best_move(board, self.symbol)
