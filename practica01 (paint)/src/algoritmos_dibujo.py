"""
Archivo: algoritmos_dibujo.py

Este archivo define los distintos algoritmos de dibujo que se pueden
usar en el lienzo.

Autor: Gabriel Gomez Garcia
Fecha: 23 de septiembre de 2024
"""

from abc import ABC, abstractmethod

from constantes import Error


class AlgoritmoDibujo(ABC):
    "Clase base, cada figura tendra su algoritmo"

    @abstractmethod
    def dibujar_linea(self, x_inicial, y_inicial, x_final, y_final):
        """
        Dibuja una linea en el lienzo

        Debe ser implementado por cada algoritmo de dibujado
        """
        raise NotImplementedError(Error.NO_IMPLEMENTADO)


# Estrategia 1: Dibujo de línea con la fórmula de la pendiente
class SlopeLineStrategy(AlgoritmoDibujo):
    def draw(self, x_inicial, y_inicial, x_final, y_final):
        print(
            f"Dibujando línea con pendiente desde ({x_inicial}, {y_inicial}) a ({x_final}, {y_final})"
        )


# Estrategia 2: Dibujo de línea con el algoritmo DDA
class DDALineStrategy(AlgoritmoDibujo):
    def draw(self, x_inicial, y_inicial, x_final, y_final):
        print(
            f"Dibujando línea con DDA desde ({x_inicial}, {y_inicial}) a ({x_final}, {y_final})"
        )


# Estrategia 3: Dibujo de línea con el algoritmo de Bresenham
class BresenhamLineStrategy(AlgoritmoDibujo):
    def draw(self, x_inicial, y_inicial, x_final, y_final):
        print(
            f"Dibujando línea con Bresenham desde ({x_inicial}, {y_inicial}) a ({x_final}, {y_final})"
        )

###### preguntar si usar factory o strategy y como

## creo que poner herramienta como un algoritmodibujo en vez de str.