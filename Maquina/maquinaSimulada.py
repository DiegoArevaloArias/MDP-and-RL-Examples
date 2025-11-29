#Se simula una caja negra que será el ambiente con el cual el agente interactue
import numpy as np
import math

class MachineEnv:
    def __init__(self, STEP=100,
                 PROBDESGASTE={'Lento':1/1000, 'Medio':1/800, 'Rapido':1/600},
                 PROBFALLO={0:0.0,1:0.001,2:0.005,3:0.01,4:0.02,5:0.05,6:0.1,7:0.2,8:0.4,9:0.6,10:1.0},
                 RECOMPENSAS={'Lento':10,'Medio':25,'Rapido':50,'Reparar':0},
                 TIEMPOREPARACION={1:100,2:300,3:500,4:700,5:1000,6:1500,7:2000,8:2500,9:3000},
                 penalidad_fallo = -1e6):
        
        self.STEP = STEP
        self.PROBDESGASTE = PROBDESGASTE
        self.PROBFALLO = PROBFALLO
        self.RECOMPENSAS = RECOMPENSAS
        self.TIEMPOREPARACION = TIEMPOREPARACION
        self.penalidad_fallo = penalidad_fallo
        self.ACCIONES = ['Lento','Medio','Rapido','Reparar']
        self.num_acc = len(self.ACCIONES)
        
        self.reset()

    def reset(self):
        """Resetea la simulacion."""
        self.state = 0               
        self.modoReparacion = False
        return self.state
    
    def _prob_min_to_step(self, p_min):
        """Convierte prob. por minuto a probabilidad por STEP."""
        return 1 - (1 - p_min)**self.STEP
    
    def step(self, action):
        """Ejecuta 1 paso de simulación. Devuelve: next_state, reward, done
        """
        a = action
        
        #Se reduce la el tiempo de espera si se encuentra en el modo de reparacion
        if self.modoReparacion:
            s_original, k_restantes = self.state  # estado = (s, k_restantes)
            k_restantes -= 1
            
            recompensa = 0  
            
            if k_restantes <= 0:
                self.state = 0
                self.modoReparacion = False
                return self.state, recompensa, False
            else:
                self.state = (s_original, k_restantes)
                return self.state, recompensa, False
        
        
        s = self.state
        #Si la maquina esta rota se queda en ese estado
        if s == 10:
            return 10, 0, True
        
        #Se inicia el proceso de reparacion
        if a == 'Reparar':
            if s == 0:
                return 0, 0, False

            dur = math.ceil(self.TIEMPOREPARACION[s] / self.STEP)
            self.state = (s, dur)
            self.modoReparacion = True
            recompensa = 0
            
            return self.state, recompensa, False
        
       #Se verifica la probabilida de fallo
        pFallo = self.PROBFALLO[s]   
        
        if np.random.rand() < pFallo:
            self.state = 10
            recompensa = self.penalidad_fallo
            return self.state, recompensa, True
        
       #Se verifica el desgaste de la maquina 
        lam = self.PROBDESGASTE[a]         
        pDesgaste = self._prob_min_to_step(lam)
        
        if np.random.rand() < pDesgaste:
            s_next=min(s+1,9) #Se pasa de estado
        else:
            s_next=s #Se mantiene igual
        

        self.state=s_next
    
        recompensa=self.RECOMPENSAS[a]*self.STEP

        #Retorno 
        
        return self.state, recompensa, False
