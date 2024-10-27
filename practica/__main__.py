from practica import agent_profunditat,agent_informat,agent_Min_Max, joc


def main():
    mida = (6, 6)

    agents = [
        agent_profunditat.Viatger("Agent 1", mida_taulell=mida)
        #agent_profunditat.Viatger("Agent 2", mida_taulell=mida),
    ]

    lab = joc.Laberint(agents, mida_taulell=mida)

    lab.comencar()


if __name__ == "__main__":
    main()
