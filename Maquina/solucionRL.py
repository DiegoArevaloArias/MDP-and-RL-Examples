import numpy as np
from maquinaSimulada import MachineEnv 

def procesar_estado(s):
    if isinstance(s, tuple):
        return s[0]
    return s

def q_learning_exacta(
        episodes=100000,   
        alpha=0.7,
        gamma=0.9,
        epsilon=0.25,
        epsilon_decay=0.99995,
        epsilon_min=0.01
    ):

    env = MachineEnv()
    ACCIONES = env.ACCIONES
    ESTADOS = list(range(11))

    # Q inicial optimista
    Q = {s: {a: 10.0 for a in ACCIONES} for s in ESTADOS}

    for ep in range(episodes):
        estado = procesar_estado(env.reset())
        done = False

        while not done:
            # política epsilon-greedy
            if np.random.rand() < epsilon:
                a = np.random.choice(ACCIONES)
            else:
                a = max(Q[estado], key=Q[estado].get)

            next_state, reward, done = env.step(a)
            next_state_proc = procesar_estado(next_state)

            max_Q_next = max(Q[next_state_proc].values()) if not done else 0
            Q[estado][a] += alpha * (reward + gamma * max_Q_next - Q[estado][a])

            estado = next_state_proc

        # decaimiento de epsilon
        if epsilon > epsilon_min:
            epsilon *= epsilon_decay

    # política final greedy
    politica = {s: max(Q[s], key=Q[s].get) for s in ESTADOS}
    return Q, politica

if __name__ == "__main__":
    Q, politica = q_learning_exacta()
    print("\nPolítica aprendida por Q-Learning:")
    for s in range(11):
        print(f"Estado {s}: {politica[s]}")
