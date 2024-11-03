
from practica.joc import Accions


class Estat:
    def __init__(self, taulell, paredes, pos_robot: tuple[int, int], cost: int = 0, accions_previes=None):

        self.taulell = taulell
        self.paredes = paredes
        self.pos_robot = pos_robot
        self.accions_previes = accions_previes if accions_previes is not None else []
        self.cost = cost

    def __hash__(self):
        return hash((self.pos_robot, tuple(self.paredes)))

    def __eq__(self, other):
        return isinstance(other, Estat) and self.pos_robot == other.pos_robot and self.paredes == other.paredes

    def __repr__(self):
        return str(self.taulell)

    def __lt__(self, other):
        return self.cost > other.cost

    def es_meta(self, desti: tuple[int, int]) -> bool:
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

        direccions = {
            "N": (0, -1),
            "O": (-1, 0),
            "S": (0, 1),
            "E": (1, 0),
        }

        for accio, direccio in movimientos:
            dx, dy = direccions[direccio]
            nou_x, nou_y = x + dx, y + dy


            if accio == Accions.MOURE:
                if self.es_posible(nou_x,nou_y):
                    fills.append(
                        Estat(
                            self.taulell,
                            self.paredes,
                            (nou_x, nou_y),
                            self.cost + 1,
                            self.accions_previes + [(Accions.MOURE, direccio)]
                        )
                    )

            elif accio == Accions.BOTAR:
                nou_x += dx
                nou_y += dy
                if self.es_posible(nou_x,nou_y):
                    fills.append(
                        Estat(
                            self.taulell,
                            self.paredes,
                            (nou_x, nou_y),
                            self.cost + 2,
                            self.accions_previes + [(Accions.BOTAR, direccio)]
                        )
                    )

            elif accio == Accions.POSAR_PARET:

                paret_x, paret_y = x + dx, y + dy
                if self.es_posible(paret_x,paret_y):
                    nueva_pared = (paret_x,paret_y)
                    self.paredes.add(nueva_pared)
                    fills.append(
                        Estat(
                            self.taulell,
                            self.paredes,
                            (x, y),
                            self.cost + 4,
                            self.accions_previes + [(Accions.POSAR_PARET, direccio)]
                        )
                    )

        return fills

    def heuristica(self, desti: tuple[int, int]) -> int:
        distancia_x = abs(self.pos_robot[0] - desti[0])
        distancia_y = abs(self.pos_robot[1] - desti[1])
        return distancia_x + distancia_y + self.cost

    def es_posible(self, x_nou: int, y_nou: int):
        limite = len(self.taulell)
        casilla_posible = (x_nou, y_nou)
        return 0 <= x_nou < limite and 0 <= y_nou < limite and casilla_posible not in self.paredes
