import random
import numpy as np

class Car:
    """ 
    Modelamos cada carro con una orientación (NS o WE) y un afán (eagerness) que afecta su tiempo de espera. 
    Además, para tener variedad de simulaciones podemos definir diferentes distribuciones para el afán.
    Cada auto mantiene su propio tiempo de espera.
    """
    def __init__(self, orientation: str, eagerness: int = None, eagerness_distribution: str = "poisson"):
        # Diferentes distribuciones para el eagerness
        if eagerness is not None:
            self.eagerness = eagerness
        elif eagerness_distribution == "poisson":
            # Poisson con lambda=2 (mayoría 1-3, raramente >5)
            self.eagerness = min(np.random.poisson(2) + 1, 10)
        elif eagerness_distribution == "exponential":
            # Exponencial truncada (mayoría bajos, algunos muy altos)
            self.eagerness = min(int(np.random.exponential(2)) + 1, 10)
        elif eagerness_distribution == "beta":
            # Beta(2,5) sesgada hacia valores bajos
            self.eagerness = max(1, int(np.random.beta(2, 5) * 10))
        elif eagerness_distribution == "normal_low":
            # Normal con media baja (μ=3, σ=1.5)
            self.eagerness = max(1, min(10, int(np.random.normal(3, 1.5))))
        else:  # "uniform" (original)
            self.eagerness = random.randint(1, 10)
            
        self.orientation = orientation
        self.wait_time = 0

class TrafficLight:
    """ 
    Cada semáforo tiene una orientación (NS o WE), un booleano, que indica si está en verde, y un contador del tiempo que lleva en verde.
    """
    def __init__(self, orientation: str):
        self.orientation = orientation
        self.is_green = False
        self.time_green = 0
    
    def switch(self):
        self.is_green = not self.is_green
        if not self.is_green:
            self.time_green = 0
            
    def update_time(self):
        if self.is_green:
            self.time_green += 1

class Intersection:
    """ 
    Para esta intersección en particular, tenemos dos semáforos (NS y WE) y listas de carros esperando en cada dirección.
        Parámetros:
        - eagerness_distribution: distribución para el afán de los carros
    """
    def __init__(self, eagerness_distribution: str = "poisson"):
        self.ns_traffic_light = TrafficLight("NS")
        self.we_traffic_light = TrafficLight("WE")
        self.ns_cars = []
        self.we_cars = []
        self.eagerness_distribution = eagerness_distribution
        
    def add_car(self):
        """ 
        Agrega nuevos carros a la intersección con cierta probabilidad (podría ajustarse para que se pase por parámetro los valores de p y q).
        """
        p = random.uniform(0,1)
        q = random.uniform(0,1)
        if p < 0.5:
            self.ns_cars.append(Car("NS", eagerness_distribution=self.eagerness_distribution))
        
        if q < 0.2:
            self.we_cars.append(Car("WE", eagerness_distribution=self.eagerness_distribution))

    def getState(self):
        """ 
        Modelamos cada estado de la intersección como una tupla con:
        - ns_green: booleano, si el semáforo NS está en verde
        - ns_cars: número de coches en el carril NS
        - we_cars: número de coches en el carril WE
        - ns_weight: suma del afán de los coches en el carril NS
        - we_weight: suma del afán de los coches en el carril WE
        - max_time_green: tiempo máximo que ha estado verde alguno de los semáforos
        """
        return (
            self.ns_traffic_light.is_green, 
            len(self.ns_cars), 
            len(self.we_cars), 
            sum(car.eagerness for car in self.ns_cars),
            sum(car.eagerness for car in self.we_cars),
            max(self.ns_traffic_light.time_green, self.we_traffic_light.time_green)
        )

    def step(self, action: str):
        """ 
        Simula un paso en la intersección dado una acción ("switch" o "stay").
        Cambia los semáforos, actualiza tiempos, agrega carros, deja pasar carros y calcula la recompensa.
        Devuelve la recompensa en negativo del afán total de los carros esperando en el carril rojo, esto
        pues debemos maximizar la recompensa y queremos minimizar el afán de los carros esperando.
        """
        if action == "switch":
            self.ns_traffic_light.switch()
            self.we_traffic_light.switch()
        
        self.ns_traffic_light.update_time()
        self.we_traffic_light.update_time()
        
        self.add_car()
        
        # Incrementar tiempo de espera de todos los carros
        for car in self.ns_cars:
            car.wait_time += 1
        for car in self.we_cars:
            car.wait_time += 1
        
        # Dejar pasar carros y registrar su tiempo de espera
        cars_passed_wait_time = 0
        if self.ns_traffic_light.is_green and self.ns_cars:
            car = self.ns_cars.pop(0)
            cars_passed_wait_time = car.wait_time
        if self.we_traffic_light.is_green and self.we_cars:
            car = self.we_cars.pop(0)
            cars_passed_wait_time = car.wait_time
            
        # Penalización por espera (usando afán)
        wait_penalty = 0
        if self.ns_traffic_light.is_green:
            wait_penalty = sum(car.eagerness for car in self.we_cars)
        else:
            wait_penalty = sum(car.eagerness for car in self.ns_cars)
            
        return self.getState(), -wait_penalty, cars_passed_wait_time