import random

from practica import joc
from practica.joc import Accions
from practica.estat import Estat


class Viatger(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)

        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def cerca(self, estat: Estat):
        self.__oberts = PriorityQueue()
        self.__tancats = set()

        if estat.es_meta(percepcio["desti"]):
            return estat.accions_previes
        



    def pinta(self, display):
        pass

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        
        pos_agent = percepcio["agents"]
        estat_inicial = Estat(percepcio["taulell"], pos_agent["agent 1"])
        if self.visitats:
            return cerca(self,estat_inicial)
        else:
            return Accions.ESPERAR
