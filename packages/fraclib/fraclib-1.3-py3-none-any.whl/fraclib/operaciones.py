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
