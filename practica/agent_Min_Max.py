import random

from practica import joc
from practica.joc import Accions


class Viatger(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)
        self.__proves = [
            (Accions.MOURE, "E"),
            (Accions.MOURE, "S"),
            (Accions.MOURE, "N"),
            (Accions.MOURE, "O"),
            (Accions.BOTAR, "S"),
            (Accions.BOTAR, "N"),
            (Accions.BOTAR, "E"),
            (Accions.BOTAR, "O"),
            (Accions.POSAR_PARET, "S"),
            (Accions.POSAR_PARET, "N"),
            (Accions.POSAR_PARET, "E"),
            (Accions.POSAR_PARET, "O"),

        ]

    def pinta(self, display):
        pass

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        if self.__proves:
            acc = random.choice(self.__proves)
            return acc
        return Accions.ESPERAR

------------------------------------------

import enum
from typing import Tuple, List


# Definición de las acciones
class Accions(enum.Enum):
    """ Accions que es poden realitzar

    MOURE -> Pes 1
    BOTAR -> Pes 2
    POSAR_PARET -> Pes 4
    """
    MOURE = 0
    POSAR_PARET = 1
    BOTAR = 2
    ESPERAR = 3


# Posibles movimientos y pesos de las acciones
accions_possibles = [
    (Accions.MOURE, "E"),
    (Accions.MOURE, "S"),
    (Accions.MOURE, "N"),
    (Accions.MOURE, "O"),
    (Accions.BOTAR, "S"),
    (Accions.BOTAR, "N"),
    (Accions.BOTAR, "E"),
    (Accions.BOTAR, "O"),
    (Accions.POSAR_PARET, "S"),
    (Accions.POSAR_PARET, "N"),
    (Accions.POSAR_PARET, "E"),
    (Accions.POSAR_PARET, "O"),
]


# Clase para el tablero
class Tauler:
    def __init__(self, mida_taulell: Tuple[int, int]):
        self.mida_taulell = mida_taulell
        self.tauler = [[None for _ in range(mida_taulell[1])] for _ in range(mida_taulell[0])]


# Función de evaluación
def evaluar_estado(pos_agent1: Tuple[int, int], pos_agent2: Tuple[int, int], desti: Tuple[int, int]) -> int:
    """Función de evaluación que retorna una puntuación en función de la distancia al destino."""
    distancia_agent1 = abs(pos_agent1[0] - desti[0]) + abs(pos_agent1[1] - desti[1])
    distancia_agent2 = abs(pos_agent2[0] - desti[0]) + abs(pos_agent2[1] - desti[1])
    return distancia_agent2 - distancia_agent1  # Puntaje positivo si el agente1 está más cerca


# Función para aplicar movimiento
def aplicar_moviment(pos: Tuple[int, int], moviment: Tuple[Accions, str]) -> Tuple[int, int]:
    x, y = pos
    accio, direccio = moviment

    if accio == Accions.MOURE:
        if direccio == "N":
            return (x, y - 1)
        elif direccio == "S":
            return (x, y + 1)
        elif direccio == "E":
            return (x + 1, y)
        elif direccio == "O":
            return (x - 1, y)
    elif accio == Accions.BOTAR:
        if direccio == "N":
            return (x, y - 2)
        elif direccio == "S":
            return (x, y + 2)
        elif direccio == "E":
            return (x + 2, y)
        elif direccio == "O":
            return (x - 2, y)
    # Accions.POSAR_PARET y Accions.ESPERAR no cambian la posición
    return pos


# Algoritmo Minimax con poda alfa-beta
def minimax_alfa_beta(pos_agent1: Tuple[int, int], pos_agent2: Tuple[int, int], desti: Tuple[int, int], depth: int,
                      alfa: int, beta: int, max_jugador: bool) -> int:
    """Función Minimax con poda alfa-beta para determinar la mejor acción"""

    # Condición terminal: llegar al destino o alcanzar la profundidad máxima
    if pos_agent1 == desti:
        return 1000  # Puntuación alta si el agente 1 alcanza el destino
    elif pos_agent2 == desti:
        return -1000  # Puntuación baja si el agente 2 alcanza el destino
    elif depth == 0:
        return evaluar_estado(pos_agent1, pos_agent2, desti)

    # Maximizar para el agente 1
    if max_jugador:
        max_eval = float('-inf')
        for moviment in accions_possibles:
            nueva_pos = aplicar_moviment(pos_agent1, moviment)
            eval = minimax_alfa_beta(nueva_pos, pos_agent2, desti, depth - 1, alfa, beta, False)
            max_eval = max(max_eval, eval)
            alfa = max(alfa, eval)
            if beta <= alfa:
                break  # Corte de poda beta
        return max_eval
    # Minimizar para el agente 2
    else:
        min_eval = float('inf')
        for moviment in accions_possibles:
            nueva_pos = aplicar_moviment(pos_agent2, moviment)
            eval = minimax_alfa_beta(pos_agent1, nueva_pos, desti, depth - 1, alfa, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alfa:
                break  # Corte de poda alfa
        return min_eval


# Función principal para obtener la mejor acción
def mejor_accion(pos_agent1: Tuple[int, int], pos_agent2: Tuple[int, int], desti: Tuple[int, int], depth: int) -> Tuple[
    Accions, str]:
    mejor_mov = None
    max_eval = float('-inf')
    alfa = float('-inf')
    beta = float('inf')

    # Explora cada movimiento posible para el agente 1
    for moviment in accions_possibles:
        nueva_pos = aplicar_moviment(pos_agent1, moviment)
        eval = minimax_alfa_beta(nueva_pos, pos_agent2, desti, depth - 1, alfa, beta, False)
        if eval > max_eval:
            max_eval = eval
            mejor_mov = moviment
        alfa = max(alfa, eval)
        if beta <= alfa:
            break  # Corte de poda beta
    return mejor_mov
