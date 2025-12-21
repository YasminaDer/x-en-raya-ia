from abc import ABC, abstractmethod

class Heuristic(ABC):
    @abstractmethod
    def evaluate(self, board, ai_symbol, human_symbol):
        pass
