import numpy as np

# Parametros del problema

T_TOTAL = 1000000
STEP = 100
ACCIONES = ['Lento', 'Medio', 'Rapido', 'Reparar']
LISTAESTADOS = list(range(11))

PROBDESGASTE = {
    'Lento': 1/1000,
    'Medio': 1/800,
    'Rapido': 1/600
}

PROBFALLO = {
    0:0.0, 1:0.001, 2: 0.005, 3: 0.01, 4:0.02, 5: 0.05,
    6:0.1, 7:0.2, 8:0.4, 9:0.6, 10:1.0
}

RECOMPENSAS = {
    'Lento': 10,
    'Medio': 25,
    'Rapido': 50,
    'Reparar': 0
}


def prob_min_to_step(p_min, step):
    return 1 - (1 - p_min)**step


# Construcción de la MDP
def construir_MDP():
    estados = LISTAESTADOS
    acciones = ACCIONES

    P = {s: {a: {s2: 0.0 for s2 in estados} for a in acciones} for s in estados}
    R = {s: {a: 0.0 for a in acciones} for s in estados}

    for s in estados:
        for a in acciones:

            if s == 10:
                for accion in acciones:
                    P[s][accion][10] = 1.0
                    R[s][accion] = 0
                continue

            if a == 'Reparar':
                P[s][a][0] = 1.0
                R[s][a] = 0
                continue

            pF = PROBFALLO[s]
            pDesg = prob_min_to_step(PROBDESGASTE.get(a, 0), STEP)
            noF = 1 - pF

            P[s][a][10] += pF
            P[s][a][min(s+1, 9)] += noF * pDesg
            P[s][a][s] += noF * (1 - pDesg)

            R[s][a] = RECOMPENSAS[a] * STEP

    return P, R


# Iteración de valores
def value_iteration(P, R, gamma=0.9, tol=1e-6):
    estados = LISTAESTADOS
    acciones = ACCIONES
    V = {s: 0.0 for s in estados}

    while True:
        delta = 0
        Vnuevo = V.copy()

        for s in estados:
            Qs = [
                R[s][a] + gamma * sum(P[s][a][s2] * V[s2] for s2 in estados)
                for a in acciones
            ]
            Vnuevo[s] = max(Qs)
            delta = max(delta, abs(Vnuevo[s] - V[s]))

        V = Vnuevo
        if delta < tol:
            break

    politica = {}
    for s in estados:
        mejor = None
        mejorQ = -1e18
        for a in acciones:
            Q = R[s][a] + gamma * sum(P[s][a][s2] * V[s2] for s2 in estados)
            if Q > mejorQ:
                mejorQ = Q
                mejor = a
        politica[s] = mejor

    return V, politica



if __name__ == "__main__":
    P, R = construir_MDP()
    V, pi = value_iteration(P, R)

    print("\nPolítica óptima (Value Iteration):")
    for s in LISTAESTADOS:
        print(f"Estado {s}: {pi[s]}")
