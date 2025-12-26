from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple, List


@dataclass(frozen=True)
class DecisionInfo:
    # Decisión
    move: Tuple[int, int]
    score: Optional[float] = None
    reason: str = "-"
    algorithm: str = "-"

    # Métricas
    nodes: int = 0
    time_ms: int = 0
    prunes: int = 0  # Solo AlphaBeta

    # Estocasticidad
    stochastic: bool = False
    epsilon: Optional[float] = None
    exploration_taken: bool = False

    # Extra opcional para botón “ver razonamiento”
    top_moves: Optional[List[Tuple[Tuple[int, int], float]]] = None
