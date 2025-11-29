#Se definen inicialmente los datos del problema conocidos

#Tiempo Total

T_TOTAL=1000000

#Intervalo de tiempo para cambio de accion
STEP=100

#Numero de pasos

NPASOS= T_TOTAL // STEP
#Acciones

ACCIONES=['Lento', 'Medio', 'Rapido', 'Reparar']

#Estados 
#0 nuevo 10 maquina rota
LISTAESTADOS=[0,1,2,3,4,5,6,7,8,9,10]



#Probabilidad de aumento de desgaste de acuerdo a accion actual, desgaste entre numero de minutos
# Se tiene que usar la funcion  def _prob_min_to_step(self, p_min) para pasarlo a step
#AccionACtual:ProbDesgaste
PROBDESGASTE={'Lento': (1/1000), 'Medio': (1/800), 'Rapido':(1/600)}

#Probabilidad de fallo de acuerdo a estado entre numero de steps
#Estado Maquina:ProbFallo
PROBFALLO={0:0.0, 1:0.001, 2: 0.005, 3: 0.01, 4:0.02, 5: 0.05, 6:0.1, 7:0.2, 8:0.4, 9:0.6}
PROBFALLO[10] = 1.0

#Recompensas
#Accion:Recompensa por minuto
RECOMPENSAS={'Lento': 10, 'Medio': 25, 'Rapido':50, 'Reparar':0}


#Tiempos de reparacion
TIEMPOREPARACION={1:100, 2:300, 3:500, 4:700, 5:1000, 6:1500, 7:2000, 8:2500, 9:3000}

#Se usa la ecuacion de Bellman en su forma exacta para solucionar este MDP

def _prob_min_to_step(self, p_min):
    """Convierte prob. por minuto a probabilidad por STEP."""
    return 1 - (1 - p_min)**self.STEP
    