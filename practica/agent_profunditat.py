import random

from practica import joc
from practica.estat import Estat
from practica.joc import Accions


class Viatger(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)
        self.__moviments = [
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


def DFS(self, percepcio: dict, inicio, desti):
    # Pila para mantener las casillas por explorar y las acciones realizadas hasta llegar allí
    stack = [(inicio, [])]  # Cada elemento será (casilla, lista de acciones realizadas)
    visitados = set()  # Conjunto para registrar las casillas visitadas
    visitados.add((inicio.x, inicio.y))  # Marcamos la casilla inicial como visitada

    while True:
        pos_agent = percepcio["AGENTS"]

        # Probar cada acción posible
        for i in self.__moviments:
            acc = self.__moviments[i]

            stack.__add__(acc)
            if pos_agent["Agent 1"] == (desti.x, desti.y):
                return stack

        # Si no encontramos el objetivo, devolvemos False
        return False


    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        if self.__proves:
            acc = random.choice(self.__proves)
            agents = percepcio["AGENTS"]

            # Obtener la posición del "agente 1"
            posicion_agente_1 = agents["Agent 1"]
            print(posicion_agente_1)
            return acc
        return Accions.ESPERAR
