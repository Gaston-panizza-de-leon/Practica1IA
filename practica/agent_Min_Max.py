import random

from practica import joc
from practica.joc import Accions
from practica.estat import Estat


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

#    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
#        if self.__proves:
#            acc = random.choice(self.__proves)
#            return acc
#        return Accions.ESPERAR


#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    PODA = True

    def cerca(self, estat, alpha, beta, torn_max=True):
        if estat.es_meta():
            return estat, (1 if not torn_max else -1)

        puntuacio_fills = []
        for fill in estat.genera_fills():
            if fill not in self.__tancats:
                punt_fill = self.cerca(fill, alpha, beta, not torn_max)

                if Viatger.PODA:
                    if torn_max:
                        alpha = max(alpha, punt_fill[1])
                    else:
                        beta = min(beta, punt_fill[1])
                    if alpha > beta:
                        break

                self.__tancats[fill] = punt_fill
            puntuacio_fills.append(self.__tancats[fill])

        puntuacio_fills = sorted(puntuacio_fills, key=lambda x: x[1])
        if torn_max:
            return puntuacio_fills[0]   # Puntuación mas baja
        else:
            return puntuacio_fills[-1]  # Puntuación mas alta

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        self.__tancats = {}
        posicio_inicial = percepcio["AGENTS"][self.nom]
        desti = percepcio["DESTI"]
        parets = percepcio["PARETS"]

        estat_inicial = Estat(percepcio["taulell"], desti, parets)
        res = self.cerca(estat_inicial, alpha=-float('inf'), beta=float('inf'))

        if isinstance(res, tuple) and res[0].accions_previes:
            solucio, _ = res
            return Accio.MOURE, solucio.accions_previes[0][1]
        else:
            return Accio.ESPERAR