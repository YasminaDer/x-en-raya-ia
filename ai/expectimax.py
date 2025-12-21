import math
from ai.search_agent import SearchAgent
from ai.default_heuristic import DefaultHeuristic

class ExpectimaxAgent(SearchAgent):
    def __init__(self, depth=3):
        self.depth = depth
        self.heuristic = DefaultHeuristic()

    def get_best_move(self, board, ai_symbol):
        human_symbol = 'O' if ai_symbol == 'X' else 'X'
        best_score = -math.inf
        best_move = None

        for (r, c) in board.get_legal_moves():
            board.place(r, c, ai_symbol)
            score = self.expectimax(board, self.depth - 1, False, ai_symbol, human_symbol)
            board.undo(r, c)

            if score > best_score:
                best_score = score
                best_move = (r, c)

        return best_move

    def expectimax(self, board, depth, maximizing, ai_symbol, human_symbol):
        if depth == 0 or board.has_winner(ai_symbol) or board.has_winner(human_symbol) or board.is_full():
            return self.heuristic.evaluate(board, ai_symbol, human_symbol)

        legal_moves = board.get_legal_moves()

        if maximizing:
            return max(
                self.simulate_move(board, r, c, ai_symbol, depth, False, ai_symbol, human_symbol)
                for (r, c) in legal_moves
            )
        else:
            # Nodo CHANCE: valor esperado
            total = 0
            for (r, c) in legal_moves:
                total += self.simulate_move(board, r, c, human_symbol, depth, True, ai_symbol, human_symbol)
            return total / len(legal_moves)

    def simulate_move(self, board, r, c, symbol, depth, next_max, ai_symbol, human_symbol):
        board.place(r, c, symbol)
        value = self.expectimax(board, depth - 1, next_max, ai_symbol, human_symbol)
        board.undo(r, c)
        return value
