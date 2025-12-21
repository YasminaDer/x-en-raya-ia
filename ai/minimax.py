import math
from ai.search_agent import SearchAgent
from ai.default_heuristic import DefaultHeuristic

class MinimaxAgent(SearchAgent):
    def __init__(self, depth=3):
        self.depth = depth
        self.heuristic = DefaultHeuristic()

    def get_best_move(self, board, ai_symbol):
        human_symbol = 'O' if ai_symbol == 'X' else 'X'
        best_score = -math.inf
        best_move = None

        for (r, c) in board.get_legal_moves():
            board.place(r, c, ai_symbol)
            score = self.minimax(board, self.depth - 1, False, ai_symbol, human_symbol)
            board.undo(r, c)

            if score > best_score:
                best_score = score
                best_move = (r, c)

        return best_move

    def minimax(self, board, depth, maximizing, ai_symbol, human_symbol):
        if depth == 0 or board.has_winner(ai_symbol) or board.has_winner(human_symbol) or board.is_full():
            return self.heuristic.evaluate(board, ai_symbol, human_symbol)

        if maximizing:
            best = -math.inf
            for (r, c) in board.get_legal_moves():
                board.place(r, c, ai_symbol)
                best = max(best, self.minimax(board, depth - 1, False, ai_symbol, human_symbol))
                board.undo(r, c)
            return best
        else:
            best = math.inf
            for (r, c) in board.get_legal_moves():
                board.place(r, c, human_symbol)
                best = min(best, self.minimax(board, depth - 1, True, ai_symbol, human_symbol))
                board.undo(r, c)
            return best
