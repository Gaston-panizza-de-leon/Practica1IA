import copy

from practica.joc import Accions


class Estat:
    def __init__(self, taulell, pos_robot: tuple[int, int], accions_previes=None):
        """
        Inicializa el estado del robot en el taulell.
        
        :param taulell: Una matriz (lista de listas) que representa el entorno del robot.
        :param pos_robot: Una tupla que representa la posición actual del robot (x, y).
        :param accions_previes: Lista de acciones anteriores realizadas por el robot.
        """
        self.taulell = taulell  # El taulell del entorno
        self.pos_robot = pos_robot  # Posición actual del robot (x, y)
        self.accions_previes = accions_previes if accions_previes is not None else []
        self.__es_meta = None  # Indicador si se ha alcanzado el destino

    def __hash__(self):
        return hash(str(self.taulell) + "," + str(self.pos_robot))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        # Representa el estado como el taulell con la posición del robot.
        return f"Mapa: {self.taulell}, Posición del robot: {self.pos_robot}"

    def es_meta(self, desti: tuple[int, int]) -> bool:
        """
        Verifica si el robot ha alcanzado su destino.
        
        :param desti: La posición destino en el taulell (x, y).
        :return: True si el robot está en la posición destino.
        """
        return self.pos_robot == desti

    def genera_fills(self, movimientos: tuple [Accions]):
        """
        Genera los posibles estados (movimientos) del robot.
        """
        fills = []
        for i in movimientos:
            nou_estat = copy.deepcopy(self)
            nou_estat.accions_previes.append(direccio)
            fills.append(nou_estat)
        return fills


    def genera_fills(self, movimientos: tuple [self.__proves]):
        """
        Genera los posibles estados (movimientos) del robot.
        """
        fills = []
        for i in movimientos.len:
            nou_estat = copy.deepcopy(self)
            movimientos[i]
            nou_estat.accions_previes.append(direccio)
            fills.append(nou_estat)
        return fills

        
"""
class Estat:

    def __init__(self, taulell, fitxa: str, accions_previes=None):
        self.taulell = taulell
        self.accions_previes = accions_previes
        self.fitxa = fitxa

        self.__es_meta = None

    def __hash__(self):
        return hash(str(self.taulell) + "," + self.fitxa)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return str(self.taulell)

    def genera_fills(self):
        fills = []

        for pos_x in range(len(self.taulell)):
            for pos_y in range(len(self.taulell[0])):
                casella = self.taulell[pos_x][pos_y]
                if casella == " ":
                    nou_estat = copy.copy(self)
                    nou_estat.taulell = copy.copy(self.taulell)

                    nou_estat.taulell[pos_x][pos_y] = self.fitxa
                    nou_estat.accions_previes = (pos_x, pos_y)
                    nou_estat.fitxa = Estat.gira(self.fitxa)
                    nou_estat.__es_meta = None

                    fills.append(nou_estat)

        return fills
"""