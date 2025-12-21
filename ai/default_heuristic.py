from ai.heuristic import Heuristic

class DefaultHeuristic(Heuristic):
    def evaluate(self, board, ai_symbol, human_symbol):
        if board.has_winner(ai_symbol):
            return 100
        if board.has_winner(human_symbol):
            return -100
        return 0
