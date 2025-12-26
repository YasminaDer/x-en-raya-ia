from abc import ABC, abstractmethod

class SearchAgent(ABC):
    @abstractmethod
    def get_best_move(self, board, symbol):
        """
        Debe devolver DecisionInfo (no solo (row,col)).
        use_stochastic y epsilon se configuran desde GUI (investigación).
        """
        pass
