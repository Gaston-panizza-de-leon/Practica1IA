
from practica import joc
from practica.estat import Estat
from practica.joc import Accions


class Viatger(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None
        self.__nom = args[0]

    def pinta(self, display):
        pass

    def cerca(self, inicial: Estat, desti):
        self.__oberts = []
        self.__tancats = set()
        self.__oberts.append(inicial)
        
        while self.__oberts:
            
            estado = self.__oberts.pop(-1)

            if estado in self.__tancats:
                continue
            if estado.es_meta(desti):
                self.__accions = estado.accions_previes
                print(len(self.__accions))
                return self.__accions

            for f in estado.genera_fills():
                self.__oberts.append(f)

            self.__tancats.add(estado)

        return False

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:

        pos_agent = percepcio["AGENTS"]
        estat_inicial = Estat(percepcio["TAULELL"], percepcio["PARETS"], pos_agent["Agent 1"])
        desti = percepcio["DESTI"]
        if self.__accions is None:
            self.cerca(estat_inicial, desti)

        if self.__accions:
            acc = self.__accions.pop(0)
            return acc[0], acc[1]
        else:
            return Accions.ESPERAR
