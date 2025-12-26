class AIPlayer:
    def __init__(self, symbol, agent, use_stochastic=False, epsilon=0.0):
        self.symbol = symbol
        self.agent = agent

        # Config desde GUI
        self.use_stochastic = use_stochastic
        self.epsilon = epsilon

        # Última decisión (para la pestaña de información)
        self.last_decision = None

    def choose_move(self, board):
        decision = self.agent.get_best_move(
            board,
            self.symbol,
            use_stochastic=self.use_stochastic,
            epsilon=self.epsilon
        )
        self.last_decision = decision
        return decision.move
