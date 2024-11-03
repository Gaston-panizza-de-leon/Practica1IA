from practica import joc
from practica.joc import Accions
from practica.estatMin_Max import Estat


class Viatger(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)
        self._nombre = args[0]
        self.__tancats = None

    def cerca(self, estat, alpha, beta, desti: tuple[int, int], torn_max=True, n_profundidad=1):
        if estat.es_meta(desti) or n_profundidad == 30:
            if n_profundidad == 30:
                return estat, 0
            else:
                return estat, (1 if not torn_max else -1)

        puntuacio_fills = []
        for fill in estat.genera_fills(torn_max):
            if fill not in self.__tancats:
                punt_fill = self.cerca(fill, alpha, beta, desti, not torn_max, n_profundidad + 1)
                self.__tancats[fill] = punt_fill
                # Guarda la puntuación y el estado como una tupla


                if torn_max:
                    alpha = max(alpha, punt_fill[1])
                else:
                    beta = min(beta, punt_fill[1])
                if alpha >= beta:
                    break

            puntuacio_fills.append(self.__tancats[fill])  # Guarda la tupla completa

        # Asegúrate de que puntuacio_fills no esté vacío antes de procesarlo
        if not puntuacio_fills:
            return estat, 0  # Retorna un estado y puntuación si no hay fills

        puntuacio_fills = sorted(puntuacio_fills, key=lambda x: x[1])  # Aquí x[1] será la puntuación
        if torn_max:
            return puntuacio_fills[0]   # Puntuación más baja
        else:
            return puntuacio_fills[-1]  # Puntuación más alta

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

        estat_inicial = Estat(percepcio["TAULELL"], parets, posicio_inicial[self._nombre],posicion_inicial2)

        print(f"Estado inicial: {estat_inicial}")
        res = self.cerca(estat_inicial, alpha, beta, desti)

        if isinstance(res, tuple):
            print(f"Resultado de la búsqueda: {res}")
            if res[0].accions_previes:
                solucio, _ = res
                print(f"Moviendo a: {solucio.accions_previes[0][1]}")
                return Accions.MOURE, solucio.accions_previes[0][1]
            else:
                print("No hay acciones previas disponibles.")
                return Accions.ESPERAR
        else:
            print("Resultado no válido.")
            return Accions.ESPERAR
