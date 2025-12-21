import math
from ai.search_agent import SearchAgent
from ai.default_heuristic import DefaultHeuristic

class AlphaBetaAgent(SearchAgent):
    def __init__(self, depth=4):
        self.depth = depth
        self.heuristic = DefaultHeuristic()

    def get_best_move(self, board, ai_symbol):
        human_symbol = 'O' if ai_symbol == 'X' else 'X'
        best_score = -math.inf
        best_move = None
        alpha = -math.inf
        beta = math.inf

        for (r, c) in board.get_legal_moves():
            board.place(r, c, ai_symbol)
            score = self.alphabeta(board, self.depth - 1, alpha, beta, False, ai_symbol, human_symbol)
            board.undo(r, c)

            if score > best_score:
                best_score = score
                best_move = (r, c)

            alpha = max(alpha, best_score)

        return best_move

    def alphabeta(self, board, depth, alpha, beta, maximizing, ai_symbol, human_symbol):
        if depth == 0 or board.has_winner(ai_symbol) or board.has_winner(human_symbol) or board.is_full():
            return self.heuristic.evaluate(board, ai_symbol, human_symbol)

        if maximizing:
            value = -math.inf
            for (r, c) in board.get_legal_moves():
                board.place(r, c, ai_symbol)
                value = max(value, self.alphabeta(board, depth - 1, alpha, beta, False, ai_symbol, human_symbol))
                board.undo(r, c)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        else:
            value = math.inf
            for (r, c) in board.get_legal_moves():
                board.place(r, c, human_symbol)
                value = min(value, self.alphabeta(board, depth - 1, alpha, beta, True, ai_symbol, human_symbol))
                board.undo(r, c)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value
