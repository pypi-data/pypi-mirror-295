# fraclib/fraccionario.py

from math import gcd

class Fraccionario:
    def __init__(self, numerador, denominador):
        if denominador == 0:
            raise ValueError("El denominador no puede ser cero.")
        self.numerador = numerador
        self.denominador = denominador
        self.simplificar()
    
    def simplificar(self):
        comun_divisor = gcd(self.numerador, self.denominador)
        self.numerador //= comun_divisor
        self.denominador //= comun_divisor
    
    def __str__(self):
        return f"({self.numerador})/({self.denominador})"

    def __repr__(self):
        return f"Fraccionario({self.numerador}, {self.denominador})"

    # Métodos para realizar operaciones se agregarán en operaciones.py
