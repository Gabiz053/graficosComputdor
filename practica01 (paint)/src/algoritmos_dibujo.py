"""
Archivo: algoritmos_dibujo.py

Este archivo define los distintos algoritmos de dibujo que se pueden
usar en el lienzo.

Autor: Gabriel Gomez Garcia
Fecha: 23 de septiembre de 2024
"""

from abc import ABC, abstractmethod
from tkinter import Canvas

import math


class AlgoritmoDibujo(ABC):
    """Clase base para cada figura que tendrá su algoritmo de dibujo."""

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
        Dibuja una linea en el lienzo.

        Debe ser implementado por cada algoritmo de dibujado.

        Args:
            lienzo: El lienzo donde se dibuja la línea.
            color: Color de la línea.
            x_inicial: Coordenada x inicial.
            y_inicial: Coordenada y inicial.
            x_final: Coordenada x final.
            y_final: Coordenada y final.
        """
        raise NotImplementedError("Error.NO_IMPLEMENTADO")

    def _dibujar_pack(
        self, lienzo: Canvas, color: str, tamanho_pincel: int, x: int, y: int
    ) -> None:
        """
        Dibuja un rectángulo de 5x5 en lugar de un píxel individual.

        Args:
            lienzo: El lienzo donde se dibuja el pack.
            color: Color del pack.
            x: Coordenada x del pack.
            y: Coordenada y del pack.
        """
        lienzo.create_rectangle(
            x, y, x + tamanho_pincel, y + tamanho_pincel, outline=color, fill=color
        )


class SlopeLineStrategy(AlgoritmoDibujo):

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
        dx = x_final - x_inicial
        dy = y_final - y_inicial

        if dx == 0:
            # Caso vertical: solo incrementamos en y
            for y in range(y_inicial, y_final + 1):
                # Dibujar un pack de 5x5 en lugar de un solo píxel
                self._dibujar_pack(lienzo, color, x_inicial, y)
                
        # el caso horizontal no hace falta se pinta bien
        
        # TODO: cambiar punto inicial por final para que pinte de arriba a abajo
        else:
            pendiente = dy / dx
            y = y_inicial

            # Dibujar punto por punto desde x_inicial a x_final
            for x in range(x_inicial, x_final):
                y += pendiente
                # Redondear las coordenadas a la cuadrícula del pack
                x_pack = round(x / tamanho_pincel) * tamanho_pincel
                y_pack = round(y / tamanho_pincel) * tamanho_pincel
                # Dibujar un pack de 5x5 en lugar de un solo píxel
                self._dibujar_pack(lienzo, color, tamanho_pincel, x_pack, y_pack)


class DDALineStrategy(AlgoritmoDibujo):

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
        dx = x2 - x1
        dy = y2 - y1
        pasos = max(abs(dx), abs(dy))

        # Calcular los incrementos de x e y
        x_incremento = dx / pasos
        y_incremento = dy / pasos
        x = x1 + 0.5
        y = y1 + 0.5

        for _ in range(pasos):
            x += x_incremento
            y += y_incremento

            # Redondear las coordenadas a la cuadrícula del pack
            x_pack = math.floor(x / tamanho_pincel) * tamanho_pincel
            y_pack = math.floor(y / tamanho_pincel) * tamanho_pincel

            # Dibujar un pack de 5x5 en lugar de un solo píxel
            self._dibujar_pack(lienzo, color, tamanho_pincel, x_pack, y_pack)


class BresenhamLineStrategy(AlgoritmoDibujo):

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
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            # Redondear las coordenadas a la cuadrícula del tamanho
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

#TODO : bresenham con entero y con reales