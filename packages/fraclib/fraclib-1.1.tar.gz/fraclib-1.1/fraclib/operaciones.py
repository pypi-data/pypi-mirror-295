from .fraccionario import Fraccionario
from math import gcd
from functools import reduce

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def sumar(fracciones):
    if not fracciones:
        raise ValueError("La lista de fracciones está vacía")

    # Obtener el denominador común
    denominador_comun = reduce(lambda x, y: lcm(x, y.denominador), fracciones, 1)

    # Sumar los numeradores ajustados al denominador común
    numerador_total = sum(
        frac.numerador * (denominador_comun // frac.denominador)
        for frac in fracciones
    )

    return Fraccionario(numerador_total, denominador_comun)

def restar(fracciones):
    if not fracciones:
        raise ValueError("La lista de fracciones está vacía")

    # Obtener el denominador común
    denominador_comun = reduce(lambda x, y: lcm(x, y.denominador), fracciones, 1)

    # Restar los numeradores ajustados al denominador común
    numerador_total = fracciones[0].numerador * (denominador_comun // fracciones[0].denominador)
    numerador_total -= sum(
        frac.numerador * (denominador_comun // frac.denominador)
        for frac in fracciones[1:]
    )

    return Fraccionario(numerador_total, denominador_comun)

def multiplicar(fracciones):
    if not fracciones:
        raise ValueError("La lista de fracciones está vacía")

    numerador_total = reduce(lambda x, y: x * y.numerador, fracciones, 1)
    denominador_total = reduce(lambda x, y: x * y.denominador, fracciones, 1)

    return Fraccionario(numerador_total, denominador_total)

def dividir(fracciones):
    if not fracciones:
        raise ValueError("La lista de fracciones está vacía")

    numerador_total = reduce(lambda x, y: x * y.denominador, fracciones, fracciones[0].numerador)
    denominador_total = reduce(lambda x, y: x * y.numerador, fracciones, fracciones[0].denominador)

    if denominador_total == 0:
        raise ValueError("La fracción resultante tiene denominador cero.")
    
    return Fraccionario(numerador_total, denominador_total)
