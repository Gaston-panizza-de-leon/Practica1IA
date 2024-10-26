import random

from practica import joc
from practica.estat import Estat
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
            agents = percepcio["AGENTS"]

            # Obtener la posición del "agente 1"
            posicion_agente_1 = agents["Agent 1"]
            print(posicion_agente_1)
            return acc
        return Accions.ESPERAR
