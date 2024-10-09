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
        
        L = []  # Lista de píxeles de la línea
        
        # para las pendientes
        dx = x_final - x_inicial
        dy = y_final - y_inicial

        # si es una linea vertical (no  cambia x)
        if dx == 0:  # Modificación 2: división por cero
            for y in range(y_inicial, y_final + 1):
                L.append((x_inicial, y))
            return L

        m = dy / dx
        b = y_inicial - m * x_inicial

        if m > 1:  # Modificación 3: pendiente mayor que 1
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

        if m > 1:  # Volver a intercambiar las variables x e y
            L = [(y, x) for x, y in L]

        return L



class DDALineStrategy(AlgoritmoDibujo):

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
        pixeles = max(abs(dx), abs(dy))

        # Calcular los incrementos de x e y
        x_incremento = dx / pixeles
        y_incremento = dy / pixeles
        
        x = x_inicial + 0.5
        y = y_inicial + 0.5
        
        for _ in range(pixeles + 1):

            # Redondear las coordenadas a la cuadrícula del pack
            x_pack = math.floor(x * tamanho_pincel)
            y_pack = math.floor(y * tamanho_pincel)

            # Dibujar un pack de 5x5 en lugar de un solo píxel
            self._dibujar_pack(lienzo, color, tamanho_pincel, x_pack, y_pack)
            
            x += x_incremento
            y += y_incremento

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
                
class BresenhamLineStrategyInt(AlgoritmoDibujo):

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