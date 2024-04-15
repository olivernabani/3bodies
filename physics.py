from math import sqrt, pow
import random

class Physics:
    def __init__(self) -> None:
        pass
    
    @staticmethod    
    def calculate_gravitational_force(body1, body2):
        G = 120 # Constante gravitacional
        distance_x = body2.x - body1.x
        distance_y = body2.y - body1.y
        distance = sqrt(distance_x**2 + distance_y**2)

        # Evitar división por cero
        if distance == 0:
            distance = 0.1

        force = G * body1.mass * body2.mass / distance**2
        numero_aleatorio = random.uniform(0.0001, 0.0005)
        force += numero_aleatorio
        #print(force)
        force_x = force * distance_x / distance
        force_y = force * distance_y / distance

        return force_x, force_y