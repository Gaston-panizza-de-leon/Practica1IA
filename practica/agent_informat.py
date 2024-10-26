import random
from queue import PriorityQueue

from practica import joc
from practica.joc import Accions
from practica.estat import Estat


class Viatger(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        pass

    def cerca(self, estat: Estat, desti: tuple [int, int]):
        self.__oberts = PriorityQueue()
        self.__tancats = set()



        self.__oberts.put((estat.calc_heuristica(), estat))

        actual = None
        while not self.__oberts.empty():
            _, actual = self.__oberts.get()
            if actual in self.__tancats:
                continue
            if actual.es_meta():
                break

            estats_fills = actual.genera_fills()

            for estat_f in estats_fills:
                self.__oberts.put((estat_f.calc_heuristica(), estat_f))

            self.__tancats.add(actual)

        if estat.es_meta(desti):
            return estat.accions_previes


    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        
        pos_agent = percepcio["AGENTS"]
        estat_inicial = Estat(percepcio["TAULELL"], pos_agent["Agent 1"])
        if self.visitats:
            return self.cerca(self, estat_inicial, percepcio["DESTI"])
        else:
            return Accions.ESPERAR
