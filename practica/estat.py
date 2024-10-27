import copy

from practica.joc import Accions


class Estat:
    def __init__(self, taulell, paredes, pos_robot: tuple[int, int], cost: int = 0, accions_previes=None):
        """
        Inicializa el estado del robot en el taulell.
        
        :param taulell: Una matriz (lista de listas) que representa el entorno del robot.
        :param pos_robot: Una tupla que representa la posición actual del robot (x, y).
        :param accions_previes: Lista de acciones anteriores realizadas por el robot.
        """
        self.taulell = taulell  # El taulell del entorno
        self.paredes = paredes
        self.pos_robot = pos_robot  # Posición actual del robot (x, y)
        self.accions_previes = accions_previes if accions_previes is not None else []
        self.cost = cost

    def __hash__(self):
        return hash(str(self.taulell))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return str(self.taulell)

    def __lt__(self, other):
        return False

    def es_meta(self, desti: tuple[int, int]) -> bool:
        """
        Verifica si el robot ha alcanzado su destino.
        
        :param desti: La posición destino en el taulell (x, y).
        :return: True si el robot está en la posición destino.
        """
        return self.pos_robot == desti

    def genera_fills(self):
        fills = []
        x, y = self.pos_robot

        movimientos = [
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

        # Lista de desplazamientos para los movimientos y saltos
        direccions = {
            "N": (-1, 0),
            "S": (1, 0),
            "E": (0, 1),
            "O": (0, -1)
        }

        for accio, direccio in movimientos:
            dx, dy = direccions[direccio]
            nou_x, nou_y = x + dx, y + dy

            # Movimiento normal (MOURE)
            if accio == Accions.MOURE:
                if self.es_posible(nou_x,nou_y):  # Verifica límites y paredes
                    fills.append(
                        Estat(
                            self.taulell,
                            self.paredes,
                            (nou_x, nou_y),
                            self.cost + 1,
                            self.accions_previes + [(Accions.BOTAR, direccio)]
                        )
                    )

            # Salto (BOTAR) - salta una casilla más en la dirección dada
            elif accio == Accions.BOTAR:
                nou_x += dx
                nou_y += dy
                if self.es_posible(nou_x,nou_y):  # Verifica límites y paredes
                    fills.append(
                        Estat(
                            self.taulell,
                            self.paredes,
                            (nou_x, nou_y),
                            self.cost + 2,
                            self.accions_previes + [(Accions.BOTAR, direccio)]
                        )
                    )

            # Poner pared (POSAR_PARET) - Añade una pared en la dirección indicada si es un espacio vacío
            elif accio == Accions.POSAR_PARET:
                paret_x, paret_y = x + dx, y + dy
                if self.es_posible(paret_x,paret_y) and self.taulell[paret_x][paret_y] == "":
                    nueva_pared = tuple[paret_x,paret_y]
                    self.paredes.append(nueva_pared)
                    fills.append(
                        Estat(
                            self.taulell,
                            self.paredes,
                            (nou_x, nou_y),
                            self.cost + 4,
                            self.accions_previes + [(Accions.BOTAR, direccio)]
                        )
                    )
        return fills

    def heuristica(self, desti: tuple[int, int]) -> int:
        distancia_x = abs(self.pos_robot[0] - desti[0])
        distancia_y = abs(self.pos_robot[1] - desti[1])
        return distancia_x + distancia_y + self.cost

    def es_posible(self, x_nou: int, y_nou: int):
        limite = len(self.taulell)
        print(x_nou,y_nou)
        return 0 <= x_nou < limite and 0 <= y_nou < limite and self.taulell[x_nou][y_nou] not in self.paredes
