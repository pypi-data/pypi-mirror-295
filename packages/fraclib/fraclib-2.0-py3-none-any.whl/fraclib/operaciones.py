# fraclib/operaciones.py

from .fraccionario import Fraccionario

def sumar(frac1, frac2):
    nuevo_numerador = frac1.numerador * frac2.denominador + frac2.numerador * frac1.denominador
    nuevo_denominador = frac1.denominador * frac2.denominador
    return Fraccionario(nuevo_numerador, nuevo_denominador)

def restar(frac1, frac2):
    nuevo_numerador = frac1.numerador * frac2.denominador - frac2.numerador * frac1.denominador
    nuevo_denominador = frac1.denominador * frac2.denominador
    return Fraccionario(nuevo_numerador, nuevo_denominador)

def multiplicar(frac1, frac2):
    nuevo_numerador = frac1.numerador * frac2.numerador
    nuevo_denominador = frac1.denominador * frac2.denominador
    return Fraccionario(nuevo_numerador, nuevo_denominador)

def dividir(frac1, frac2):
    nuevo_numerador = frac1.numerador * frac2.denominador
    nuevo_denominador = frac1.denominador * frac2.numerador
    if nuevo_denominador == 0:
        raise ValueError("La fracción resultante tiene denominador cero.")
    return Fraccionario(nuevo_numerador, nuevo_denominador)
# fraclib/operaciones.py

from .fraccionario import Fraccionario
from math import gcd
from functools import reduce

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def crear_fraccion(numerador, denominador):
    if denominador == 0:
        raise ValueError("El denominador no puede ser cero.")
    return Fraccionario(numerador, denominador)

def sumar(*fracciones):
    if not fracciones:
        raise ValueError("No se proporcionaron fracciones para sumar")

    # Obtener el denominador común
    denominador_comun = reduce(lambda x, y: lcm(x, y.denominador), fracciones, 1)

    # Sumar los numeradores ajustados al denominador común
    numerador_total = sum(
        frac.numerador * (denominador_comun // frac.denominador)
        for frac in fracciones
    )

    return Fraccionario(numerador_total, denominador_comun)

def restar(*fracciones):
    if not fracciones:
        raise ValueError("No se proporcionaron fracciones para restar")

    # Inicializar con la primera fracción
    frac_resultado = fracciones[0]

    for frac in fracciones[1:]:
        denominador_comun = lcm(frac_resultado.denominador, frac.denominador)
        numerador_resultado = (
            frac_resultado.numerador * (denominador_comun // frac_resultado.denominador)
            - frac.numerador * (denominador_comun // frac.denominador)
        )
        frac_resultado = Fraccionario(numerador_resultado, denominador_comun)

    return frac_resultado

def multiplicar(*fracciones):
    if not fracciones:
        raise ValueError("No se proporcionaron fracciones para multiplicar")

    numerador_total = 1
    denominador_total = 1

    for frac in fracciones:
        numerador_total *= frac.numerador
        denominador_total *= frac.denominador

    return Fraccionario(numerador_total, denominador_total)

def dividir(*fracciones):
    if not fracciones:
        raise ValueError("No se proporcionaron fracciones para dividir")

    numerador_total = fracciones[0].numerador
    denominador_total = fracciones[0].denominador

    for frac in fracciones[1:]:
        if frac.numerador == 0:
            raise ValueError("No se puede dividir por una fracción con numerador cero")
        numerador_total *= frac.denominador
        denominador_total *= frac.numerador

    if denominador_total == 0:
        raise ValueError("La fracción resultante tiene denominador cero.")

    return Fraccionario(numerador_total, denominador_total)
