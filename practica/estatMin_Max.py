import copy

from practica.joc import Accions


class Estat:
    def __init__(self, taulell, paredes, pos_robot: tuple[int, int],pos_robot2: tuple[int, int], cost: int = 0, accions_previes=None):
        """
        Inicializa el estado del robot en el taulell.

        :param taulell: Una matriz (lista de listas) que representa el entorno del robot.
        :param pos_robot: Una tupla que representa la posición actual del robot (x, y).
        :param accions_previes: Lista de acciones anteriores realizadas por el robot.
        """
        self.taulell = taulell  # El taulell del entorno
        self.paredes = paredes
        self.pos_robot = pos_robot  # Posición actual del robot (x, y)
        self.pos_robot2 = pos_robot2
        self.accions_previes = accions_previes if accions_previes is not None else []
        self.cost = cost

    def __hash__(self):
        # Usa una combinación de la posición del robot y una tupla de las paredes para el hash
        return hash((self.pos_robot, tuple(self.paredes)))

    def __eq__(self, other):
        # Considera estados iguales si la posición y las paredes son iguales
        return isinstance(other, Estat) and self.pos_robot == other.pos_robot and self.paredes == other.paredes

    def __repr__(self):
        return str(self.taulell)

    def __lt__(self, other):
        return self.cost > other.cost

    def es_meta(self, desti: tuple[int, int]) -> bool:
        """
        Verifica si el robot ha alcanzado su destino.

        :param desti: La posición destino en el taulell (x, y).
        :return: True si el robot está en la posición destino.
        """
        return self.pos_robot == desti or self.pos_robot2 == desti

    def genera_fills(self, torn_max: bool):
        fills = []
        x, y = self.pos_robot
        x1, y1 = self.pos_robot2

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
            "N": (0, -1),
            "O": (-1, 0),
            "S": (0, 1),
            "E": (1, 0),
        }

        for accio, direccio in movimientos:
            dx, dy = direccions[direccio]
            if torn_max:
                nou_x, nou_y = x + dx, y + dy
            else:
                nou_x, nou_y = x1 + dx, y1 + dy

            # Movimiento normal (MOURE)
            if accio == Accions.MOURE:
                if self.es_posible(nou_x, nou_y):  # Verifica límites y paredes
                    if torn_max:
                        fills.append(
                            Estat(
                                self.taulell,
                                self.paredes,
                                (nou_x, nou_y),
                                (x1, y1),
                                self.cost + 1,
                                self.accions_previes + [(Accions.MOURE, direccio)]
                            )
                        )
                    else:
                        fills.append(
                            Estat(
                                self.taulell,
                                self.paredes,
                                (x, y),
                                (nou_x, nou_y),
                                self.cost + 1,
                                self.accions_previes
                            )
                        )

            # Salto (BOTAR) - salta una casilla más en la dirección dada
            elif accio == Accions.BOTAR:
                nou_x += dx
                nou_y += dy
                if self.es_posible(nou_x, nou_y):  # Verifica límites y paredes
                    if torn_max:
                        fills.append(
                            Estat(
                                self.taulell,
                                self.paredes,
                                (nou_x, nou_y),
                                (x1, y1),
                                self.cost + 2,
                                self.accions_previes + [(Accions.BOTAR, direccio)]
                            )
                        )
                    else:
                        fills.append(
                            Estat(
                                self.taulell,
                                self.paredes,
                                (x, y),
                                (nou_x, nou_y),
                                self.cost + 2,
                                self.accions_previes
                            )
                        )
            # Poner pared (POSAR_PARET) - Añade una pared en la dirección indicada si es un espacio vacío
            elif accio == Accions.POSAR_PARET:

                paret_x, paret_y = x + dx, y + dy
                """if self.es_posible(paret_x, paret_y):
                    if torn_max:
                        fills.append(
                            Estat(
                                self.taulell,
                                self.paredes,
                                (nou_x, nou_y),
                                (x1, y1),
                                self.cost + 4,
                                self.accions_previes + [(Accions.POSAR_PARET, direccio)]
                            )
                        )
                    else:
                        fills.append(
                            Estat(
                                self.taulell,
                                self.paredes,
                                (x, y),
                                (nou_x, nou_y),
                                self.cost + 4,
                                self.accions_previes
                            )
                        )"""

        return fills

    def heuristica(self, desti: tuple[int, int]) -> int:
        distancia_x = abs(self.pos_robot[0] - desti[0])
        distancia_y = abs(self.pos_robot[1] - desti[1])
        return distancia_x + distancia_y + self.cost

    def es_posible(self, x_nou: int, y_nou: int):
        limite = len(self.taulell)
        casilla_posible = (x_nou, y_nou)
        print(x_nou, y_nou)
        return 0 <= x_nou < limite and 0 <= y_nou < limite and casilla_posible not in self.paredes
