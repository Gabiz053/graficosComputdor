"""
Archivo: algoritmos_dibujo.py

Este archivo define los distintos algoritmos de dibujo que se pueden
usar en el lienzo.

Autor: Gabriel Gomez Garcia
Fecha: 23 de septiembre de 2024
"""

# Imports externos
from abc import ABC, abstractmethod
import math

# Imports de terceros
from tkinter import Canvas

# No hay imports locales en este archivo


class AlgoritmoDibujo(ABC):
    """
    Clase base para cada figura que tendrá su algoritmo de dibujo.
    """

    @abstractmethod
    def dibujar_linea(
        self,
        lienzo: Canvas,
        color: str,
        tamanho_pincel: int,
        x_inicial: int,
        y_inicial: int,
        x_final: int,
        y_final: int,
    ) -> None:
        """
        Dibuja una línea en el lienzo.

        Este método debe ser implementado por cada clase que extienda AlgoritmoDibujo.
        """
        raise NotImplementedError("Error.NO_IMPLEMENTADO")

    def _dibujar_pack(
        self, lienzo: Canvas, color: str, tamanho_pincel: int, x: int, y: int
    ) -> None:
        """
        Dibuja un rectángulo de tamanho_pincel x tamanho_pincel en lugar de un píxel individual.

        Esto permite que las líneas se vean más gruesas según el tamaño de la brocha.
        """
        lienzo.create_rectangle(
            x, y, x + tamanho_pincel, y + tamanho_pincel, outline=color, fill=color
        )


class SlopeLineStrategy(AlgoritmoDibujo):
    """
    Estrategia de dibujo de líneas utilizando el cálculo de la pendiente.
    """

    def dibujar_linea(
        self,
        lienzo: Canvas,
        color: str,
        tamanho_pincel: int,
        x_inicial: int,
        y_inicial: int,
        x_final: int,
        y_final: int,
    ) -> None:
        """
        Dibuja una línea en el lienzo usando el algoritmo de pendiente.
        """

        L = []
        dx = x_final - x_inicial
        dy = y_final - y_inicial

        if dx == 0:
            for y in range(y_inicial, y_final + 1):
                L.append((x_inicial, y))
            return L

        m = dy / dx
        b = y_inicial - m * x_inicial

        if m > 1:
            x_inicial, y_inicial = y_inicial, x_inicial
            x_final, y_final = y_final, x_final
            dx, dy = dy, dx
            m = 1 / m
            b = y_inicial - m * x_inicial

        x = x_inicial
        y = y_inicial
        while x <= x_final:
            L.append((x, round(m * x + b)))
            x += 1

        if m > 1:
            L = [(y, x) for x, y in L]

        for x, y in L:
            self._dibujar_pack(lienzo, color, tamanho_pincel, x, y)


class DDALineStrategy(AlgoritmoDibujo):
    """
    Estrategia de dibujo de líneas usando el algoritmo DDA.
    """

    def dibujar_linea(
        self,
        lienzo: Canvas,
        color: str,
        tamanho_pincel: int,
        x_inicial: int,
        y_inicial: int,
        x_final: int,
        y_final: int,
    ) -> None:
        """
        Dibuja una línea en el lienzo usando el algoritmo DDA (Digital Differential Analyzer).
        """

        dx = x_final - x_inicial
        dy = y_final - y_inicial
        pixeles = max(abs(dx), abs(dy))

        x_incremento = dx / pixeles
        y_incremento = dy / pixeles

        x = x_inicial + 0.5
        y = y_inicial + 0.5

        for _ in range(pixeles + 1):
            x_pack = math.floor(x * tamanho_pincel)
            y_pack = math.floor(y * tamanho_pincel)
            self._dibujar_pack(lienzo, color, tamanho_pincel, x_pack, y_pack)
            x += x_incremento
            y += y_incremento


class BresenhamLineStrategy(AlgoritmoDibujo):
    """
    Estrategia de dibujo de líneas usando el algoritmo Bresenham.
    """

    def dibujar_linea(
        self,
        lienzo: Canvas,
        color: str,
        tamanho_pincel: int,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
    ) -> None:
        """
        Dibuja una línea en el lienzo usando el algoritmo de Bresenham.
        """

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            x_pack = math.floor(x1 / tamanho_pincel) * tamanho_pincel
            y_pack = math.floor(y1 / tamanho_pincel) * tamanho_pincel
            self._dibujar_pack(lienzo, color, tamanho_pincel, x_pack, y_pack)

            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy


class BresenhamLineStrategyInt(AlgoritmoDibujo):
    """
    Estrategia de dibujo de líneas usando el algoritmo Bresenham con enteros.
    """

    def dibujar_linea(
        self,
        lienzo: Canvas,
        color: str,
        tamanho_pincel: int,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
    ) -> None:
        """
        Dibuja una línea en el lienzo usando el algoritmo de Bresenham utilizando operaciones con enteros.
        """

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            x_pack = math.floor(x1 / tamanho_pincel) * tamanho_pincel
            y_pack = math.floor(y1 / tamanho_pincel) * tamanho_pincel
            self._dibujar_pack(lienzo, color, tamanho_pincel, x_pack, y_pack)

            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
