"""
Archivo: punto.py

Este archivo define un punto como un array para aplicar transformaciones geometricas

Autor: Gabriel Gomez Garcia
Fecha: 23 de septiembre de 2024
"""

import numpy as np


class Punto:
    """
    Clase que representa un punto en un espacio bidimensional utilizando un array de NumPy.
    Almacena las coordenadas en formato columna para facilitar operaciones vectoriales.
    """

    def __init__(self, x: int, y: int):
        """
        Inicializa el punto con las coordenadas x e y almacenadas en un array columna de NumPy.

        Args:
            x (int): Coordenada horizontal del punto.
            y (int): Coordenada vertical del punto.
        """
        self._coordenadas = np.array(
            [[x], [y]], dtype=int
        )  # Almacena las coordenadas en formato columna

    def __str__(self) -> str:
        """
        Devuelve una representación en cadena del punto.

        Returns:
            str: Representación textual del punto en formato 'Punto(x, y)'.
        """
        return f"Punto(x={self._coordenadas[0, 0]}, y={self._coordenadas[1, 0]})"

    def obtener_coordenadas(self) -> np.ndarray:
        """
        Devuelve las coordenadas del punto como un array de NumPy en formato columna.

        Returns:
            np.ndarray: Matriz columna de tamaño (2, 1) que contiene las coordenadas [x, y].
        """
        return (
            self._coordenadas.copy()
        )  # Devuelve una copia para evitar mutaciones accidentales externas

    def _set_coordenadas(self, coordenadas: np.ndarray) -> None:
        """
        Establece las coordenadas del punto directamente a partir de un array NumPy en formato columna.
        Esta operación está pensada para uso interno.

        Args:
            coordenadas (np.ndarray): Matriz columna de tamaño (2, 1) que contiene las nuevas coordenadas [x, y].
        """
        if coordenadas.shape == (2, 1):
            self._coordenadas = coordenadas
        else:
            raise ValueError("Las coordenadas deben ser una matriz de tamaño (2, 1).")

    @property
    def x(self) -> int:
        """
        Devuelve la coordenada x del punto.

        Returns:
            int: Valor de la coordenada x.
        """
        return self._coordenadas[0, 0]

    @x.setter
    def x(self, valor: int):
        """
        Establece un nuevo valor para la coordenada x del punto.

        Args:
            valor (int): Nuevo valor para la coordenada x.
        """
        self._coordenadas[0, 0] = valor

    @property
    def y(self) -> int:
        """
        Devuelve la coordenada y del punto.

        Returns:
            int: Valor de la coordenada y.
        """
        return self._coordenadas[1, 0]

    @y.setter
    def y(self, valor: int):
        """
        Establece un nuevo valor para la coordenada y del punto.

        Args:
            valor (int): Nuevo valor para la coordenada y.
        """
        self._coordenadas[1, 0] = valor
