from .fraccionario import Fraccionario
from math import gcd
from functools import reduce

# Función para calcular el mínimo común múltiplo
def lcm(a, b):
    return abs(a * b) // gcd(a, b)

# Función para simplificar la fracción
def simplificar(fraccion):
    divisor_comun = gcd(fraccion.numerador, fraccion.denominador)
    numerador_simplificado = fraccion.numerador // divisor_comun
    denominador_simplificado = fraccion.denominador // divisor_comun
    
    if denominador_simplificado == 1:
        return numerador_simplificado
    else:
        return Fraccionario(numerador_simplificado, denominador_simplificado)

# Función para convertir enteros en fracciones
def convertir_a_fraccion(valor):
    if isinstance(valor, Fraccionario):
        return valor
    elif isinstance(valor, int):
        return Fraccionario(valor, 1)
    else:
        raise ValueError("Solo se pueden operar fracciones o enteros.")

# Función para sumar fracciones y/o enteros
def sumar(*valores):
    if not valores:
        raise ValueError("No se proporcionaron valores para sumar")

    fracciones = [convertir_a_fraccion(valor) for valor in valores]

    denominador_comun = reduce(lambda x, y: lcm(x, y.denominador), fracciones, 1)
    numerador_total = sum(
        frac.numerador * (denominador_comun // frac.denominador)
        for frac in fracciones
    )

    fraccion_resultado = Fraccionario(numerador_total, denominador_comun)
    return simplificar(fraccion_resultado)

# Función para restar fracciones y/o enteros
def restar(*valores):
    if not valores:
        raise ValueError("No se proporcionaron valores para restar")

    fracciones = [convertir_a_fraccion(valor) for valor in valores]
    frac_resultado = fracciones[0]

    for frac in fracciones[1:]:
        denominador_comun = lcm(frac_resultado.denominador, frac.denominador)
        numerador_resultado = (
            frac_resultado.numerador * (denominador_comun // frac_resultado.denominador)
            - frac.numerador * (denominador_comun // frac.denominador)
        )
        frac_resultado = Fraccionario(numerador_resultado, denominador_comun)

    return simplificar(frac_resultado)

# Función para multiplicar fracciones y/o enteros
def multiplicar(*valores):
    if not valores:
        raise ValueError("No se proporcionaron valores para multiplicar")

    fracciones = [convertir_a_fraccion(valor) for valor in valores]

    numerador_total = 1
    denominador_total = 1

    for frac in fracciones:
        numerador_total *= frac.numerador
        denominador_total *= frac.denominador

    fraccion_resultado = Fraccionario(numerador_total, denominador_total)
    return simplificar(fraccion_resultado)

# Función para dividir fracciones y/o enteros
def dividir(*valores):
    if not valores:
        raise ValueError("No se proporcionaron valores para dividir")

    fracciones = [convertir_a_fraccion(valor) for valor in valores]
    numerador_total = fracciones[0].numerador
    denominador_total = fracciones[0].denominador

    for frac in fracciones[1:]:
        if frac.numerador == 0:
            raise ValueError("No se puede dividir por una fracción con numerador cero")
        numerador_total *= frac.denominador
        denominador_total *= frac.numerador

    if denominador_total == 0:
        raise ValueError("La fracción resultante tiene denominador cero.")

    fraccion_resultante = Fraccionario(numerador_total, denominador_total)
    return simplificar(fraccion_resultante)
