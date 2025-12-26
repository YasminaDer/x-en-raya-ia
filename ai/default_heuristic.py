from ai.heuristic import Heuristic

class DefaultHeuristic(Heuristic):
    def evaluate(self, board, ai_symbol, human_symbol):
        if board.has_winner(ai_symbol):
            return 100
        if board.has_winner(human_symbol):
            return -100
        return 0

    def explain_move(self, board, move, ai_symbol, human_symbol):
        r, c = move

        # 1) Si con esta jugada gano ya
        board.place(r, c, ai_symbol)
        if board.has_winner(ai_symbol):
            board.undo(r, c)
            return "Gana inmediatamente (victoria directa)."
        board.undo(r, c)

        # 2) Si bloqueo una victoria inmediata del rival
        board.place(r, c, human_symbol)
        if board.has_winner(human_symbol):
            board.undo(r, c)
            return "Bloquea una victoria inmediata del rival."
        board.undo(r, c)

        # 3) Si no hay patrón claro
        return "Mejora posición según evaluación heurística."
