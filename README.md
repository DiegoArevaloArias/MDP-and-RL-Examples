# MDP-and-RL-Examples
This repository implements Markov Decision Processes (MDPs) and reinforcement learning to solve two problems: the first is a traffic intersection problem aimed at minimizing the wait time for cars, and the second is the optimization of a machine in a factory.


# 1. Definición del Problema 

En un entorno industrial, se busca maximizar la producción total de una unidad de manufactura a lo largo de un horizonte de tiempo $T = 1,000,000$ minutos (aprox. 2 años). La máquina sufre degradación progresiva basada en la velocidad de operación y posee un riesgo estocástico de fallo crítico. El objetivo es encontrar la política óptima $\pi^*$ que decida en cada instante qué velocidad utilizar o si es necesario realizar un mantenimiento preventivo.
---
# 2. Formulación Matemática (Enfoque MDP)

Definimos el problema como un Proceso de Decisión de Markov (MDP) dado por la tupla $(S, A, P, R, \gamma)$.

### A. Espacio de Estados ($S$)
El estado representa el nivel de desgaste de la máquina.

$$S = \{0, 1, 2, ..., 9, 10\}$$

* $s=0$: Máquina nueva.
* $s=1..9$: Grados de desgaste creciente.
* $s=10$: Fallo crítico (Estado absorbente temporal).

### B. Espacio de Acciones ($A$)
En cada paso de tiempo (ej. $t = 100$ minutos), el agente decide:

$$A = \{\text{Lento}, \text{Medio}, \text{Rápido}, \text{Reparar}\}$$

> **Nota:** Se añade "Reparar" como acción voluntaria (mantenimiento preventivo).

---

# Tablas solicitadas

## 1. Probabilidades de aumento de desgaste ($\alpha_a$)

| Acción | Interpretación | $\alpha_a$ |
|--------|----------------|------------|
| Lento  | Prob. de aumentar desgaste si tarda 1000 min | 1/1000 |
| Medio  | Prob. de aumentar desgaste si tarda 800 min  | 1/800  |
| Rápido | Prob. de aumentar desgaste si tarda 600 min  | 1/600  |

---

## 2. Probabilidad de fallo ($\beta_s$)

| Estado $s$ | $\beta_s$ |
|------------|-----------|
| 0 | 0.0 |
| 1 | 0.001 |
| 2 | 0.005 |
| 3 | 0.01 |
| 4 | 0.02 |
| 5 | 0.05 |
| 6 | 0.1 |
| 7 | 0.2 |
| 8 | 0.4 |
| 9 | 0.6 |

---

## 3. Recompensas ($R$)

| Estado | Acción | Recompensa |
|--------|--------|-------------|
| s | Lento | +10 |
| s | Medio | +25 |
| s | Rápido | +50 |
| s | Reparar | 0 |
| s=10 | Cualquier acción | -INF |

---

## 4. Tiempos de reparación (penalización)

| Estado antes de reparar | $T_{rep}(s)$ (min) |
|--------------------------|--------------------|
| 1 | 100 |
| 2 | 300 |
| 3 | 500 |
| 4 | 700 |
| 5 | 1000 |
| 6 | 1500 |
| 7 | 2000 |
| 8 | 2500 |
| 9 | 3000 |
---

# Continuación del texto original

### C. Dinámica de Transición ($P$) y Probabilidades

La transición de estado $s_t \to s_{t+1}$ se define así:

* Si $a =$ Operar (Lento/Medio/Rápido):
    * La máquina falla con probabilidad $\beta_s \rightarrow s_{t+1} = 10$.
    * Si no falla, aumenta desgaste con prob. $\alpha_a \rightarrow s_{t+1} = s_t + 1$.
    * Si no falla ni aumenta desgaste, se mantiene $\rightarrow s_{t+1} = s_t$.
* Si $a =$ Reparar:
    * La máquina pasa al estado de "Mantenimiento" (o salta directamente al estado recuperado $s=1$ tras $N$ pasos de tiempo de penalización).

---

# 3. Enfoque de Solución

### Iteración de valores
Asumimos que conocemos perfectamente todas las probabilidades y los tiempos de reparación descritos arriba:
* Utilizaremos el algoritmo de **Value Iteration** o **Policy Iteration**.
* Calcularemos la matriz de transición $P(s'|s,a)$ exacta.
* **Objetivo:** Obtener la política teórica óptima $\pi^*(s)$ que nos diga, por ejemplo: "En estado 4, opera Rápido. En estado 8, opera Lento. En estado 9, Repara inmediatamente".

### Parte 2: Solución con Aprendizaje por Refuerzo
Simulamos un escenario donde no conocemos las probabilidades de fallo. El agente debe aprender interactuando.

* **Ambiente:** Un simulador de la máquina usando las reglas del punto 2.
* **Algoritmos:** Q-Learning : Para aprender la utilidad de las acciones arriesgadas mientras se explora.
* **Exploración:** Epsilon-Greedy decadente (empezar probando todo, terminar explotando la mejor estrategia).

---
# 4. Justificación de los Dos Enfoques

### MDP
En ciertas ocasiones o para ciertas máquinas comerciales va a ser posible saber las probabilidades de fallo exactas con mayor seguridad entonces un enfoque exacto nos dará la mejor respuesta. 

### Aprendizaje por refuerzo:
Para nuevas máquinas o componentes no muy conocidos no se conocen las probabilidades con exactitud sin embargo es posible simularlos, con el fin de obtener las mejores políticas.


---
# 5. Resultados

### Mencionar las politica escogida, las iteraciones hasta la estabilizacion, son iguales en ambos casos? 


