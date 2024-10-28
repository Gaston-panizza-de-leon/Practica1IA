import random

from practica import joc
from practica.joc import Accions
from practica.estatMin_Max import Estat


class Viatger(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)
        self._nombre = args[0]

    def cerca(self, estat, alpha, beta, desti: tuple [int,int],  torn_max=True, ):
        if estat.es_meta(desti):
            return estat, (1 if not torn_max else -1)

        puntuacio_fills = []

        for fill in estat.genera_fills(torn_max):
            if fill not in self.__tancats:
                punt_fill = self.cerca(fill, alpha, beta, desti, not torn_max)

                if torn_max:
                    alpha = max(alpha, punt_fill[1])
                else:
                    beta = min(beta, punt_fill[1])
                if alpha > beta:
                    break

                self.__tancats[fill] = punt_fill

            puntuacio_fills.append(self.__tancats[fill])

        puntuacio_fills = sorted(puntuacio_fills, key=lambda x: x[1])
        assert puntuacio_fills, "La lista 'puntuacio_fills' está vacía, pero no debería estarlo"
        if torn_max:
            return puntuacio_fills[0]   # Puntuación mas baja
        else:
            return puntuacio_fills[-1]  # Puntuación mas alta

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        self.__tancats = {}
        posicio_inicial = percepcio["AGENTS"]
        desti = percepcio["DESTI"]
        parets = percepcio["PARETS"]
        alpha = -float('inf')
        beta = float('inf')
        if self._nombre == "Agent 1":
            posicion_inicial2 = posicio_inicial["Agent 2"]
        else:
            posicion_inicial2 = posicio_inicial["Agent 1"]

        estat_inicial = Estat(percepcio["TAULELL"], parets, posicio_inicial[self._nombre], posicion_inicial2)
        res = self.cerca(estat_inicial, alpha, beta, desti)

        if isinstance(res, tuple) and res[0].accions_previes:
            solucio, _ = res
            return Accions.MOURE, solucio.accions_previes[0][1]
        else:
            return Accions.ESPERAR