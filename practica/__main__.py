
from practica import agent_profunditat,agent_informat,agent_Min_Max, joc


def main():
    mida = (10, 10)

    agents = [
        agent_profunditat.Viatger("Agent 1", mida_taulell=mida),
        #agent_informat.Viatger("Agent 2", mida_taulell=mida)
    ]

    lab = joc.Laberint(agents, mida_taulell=mida)

    lab.comencar()



if __name__ == "__main__":
    main()
