from abc import ABC, abstractmethod

class SearchAgent(ABC):
    @abstractmethod
    def get_best_move(self, board, symbol):
        pass
