import math
import time
import random

from ai.search_agent import SearchAgent
from ai.default_heuristic import DefaultHeuristic
from ai.decision_info import DecisionInfo


class MinimaxAgent(SearchAgent):
    def __init__(self, depth=3):
        self.depth = depth
        self.heuristic = DefaultHeuristic()

        # stats (por decisión)
        self.nodes = 0

    def get_best_move(self, board, ai_symbol, use_stochastic=False, epsilon=0.0):
        start = time.time()
        self.nodes = 0

        human_symbol = 'O' if ai_symbol == 'X' else 'X'
        best_score = -math.inf
        best_moves = []  # para soportar empates de score

        root_scores = []  # top_moves opcional

        for (r, c) in board.get_legal_moves():
            board.place(r, c, ai_symbol)
            score = self.minimax(board, self.depth - 1, False, ai_symbol, human_symbol)
            board.undo(r, c)

            root_scores.append(((r, c), score))

            if score > best_score:
                best_score = score
                best_moves = [(r, c)]
            elif score == best_score:
                best_moves.append((r, c))

        # Mejor movimiento determinista (si hay empates, cualquiera de best_moves)
        best_move = best_moves[0] if best_moves else None

        exploration_taken = False

        # Estocasticidad SOLO en la raíz (ε-greedy) para análisis
        if use_stochastic and best_move is not None and epsilon > 0.0:
            if random.random() < epsilon:
                legal = board.get_legal_moves()
                if legal:
                    best_move = random.choice(legal)
                    exploration_taken = True

        reason = "-"
        if best_move is not None:
            reason = self.heuristic.explain_move(board, best_move, ai_symbol, human_symbol)

        time_ms = int((time.time() - start) * 1000)

        # Top moves (opcional): ordenamos por score desc
        root_scores.sort(key=lambda x: x[1], reverse=True)
        top_moves = root_scores[:5]

        return DecisionInfo(
            move=best_move,
            score=best_score if best_move is not None else None,
            reason=reason,
            algorithm="Minimax",
            nodes=self.nodes,
            time_ms=time_ms,
            prunes=0,
            stochastic=use_stochastic,
            epsilon=epsilon if use_stochastic else None,
            exploration_taken=exploration_taken,
            top_moves=top_moves
        )

    def minimax(self, board, depth, maximizing, ai_symbol, human_symbol):
        self.nodes += 1

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
