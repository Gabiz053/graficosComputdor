"""
Archivo: forma.py

Este archivo define las distintas formas que se pueden pintar en el lienzo.
Utiliza el patron Composite para organizar y crear estas formas.

Autor: Gabriel Gomez Garcia
Fecha: 23 de septiembre de 2024
"""

import numpy as np

class Punto():
    """Clase que representa un punto en un espacio bidimensional usando un array de NumPy."""

    def __init__(self, x: int, y: int):
        """Inicializa el punto con las coordenadas x e y en un array de NumPy.

        Args:
            x (int): Coordenada horizontal del punto.
            y (int): Coordenada vertical del punto.
        """
        self._coordenadas = np.array([x, y], dtype=int)

    def __str__(self) -> str:
        """Devuelve una representacion en cadena del punto."""
        return f"Punto({self._coordenadas[0]}, {self._coordenadas[1]})"

    @property
    def x(self) -> int:
        """Getter para la coordenada x."""
        return self._coordenadas[0]

    @x.setter
    def x(self, valor: int):
        """Setter para la coordenada x."""
        self._coordenadas[0] = valor

    @property
    def y(self) -> int:
        """Getter para la coordenada y."""
        return self._coordenadas[1]

    @y.setter
    def y(self, valor: int):
        """Setter para la coordenada y."""
        self._coordenadas[1] = valor

    def obtener_coordenadas(self) -> np.ndarray:
        """Devuelve las coordenadas del punto como un array de NumPy.

        Returns:
            np.ndarray: Array con las coordenadas [x, y].
        """
        return self._coordenadas