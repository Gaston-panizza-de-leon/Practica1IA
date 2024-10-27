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

        self.__oberts.put((estat.heuristica(desti), estat))

        actual = None
        while not self.__oberts.empty():
            _, actual = self.__oberts.get()
            if actual in self.__tancats:
                continue
            if actual.es_meta(desti):
                print("YESSSSSSSSSSSSSSS")
                self.__accions = actual.accions_previes
                break

            estats_fills = actual.genera_fills()

            for estat_f in estats_fills:
                self.__oberts.put((estat_f.heuristica(desti), estat_f))

            self.__tancats.add(actual)



    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        
        pos_agent = percepcio["AGENTS"]
        estat_inicial = Estat(percepcio["TAULELL"],percepcio["PARETS"], pos_agent["Agent 1"])
        desti = percepcio["DESTI"]
        if self.__accions is None:
             self.cerca(estat_inicial, desti)

        if self.__accions:
            acc = self.__accions.pop(0)

            return acc[0], acc[1]
        else:
            return Accions.ESPERAR
