"""
Archivo: algoritmos_dibujo.py

Este archivo define los distintos algoritmos de dibujo que se pueden
usar en el lienzo.

Autor: Gabriel Gomez Garcia
Fecha: 23 de septiembre de 2024
"""

from abc import ABC, abstractmethod
from tkinter import Canvas


class AlgoritmoDibujo(ABC):
    """Clase base para cada figura que tendrá su algoritmo de dibujo."""

    @abstractmethod
    def dibujar_linea(
        self,
        lienzo: Canvas,
        color: str,
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

    def _dibujar_pack(self, lienzo: Canvas, color: str, x: int, y: int) -> None:
        """
        Dibuja un rectángulo de 5x5 en lugar de un píxel individual.

        Args:
            lienzo: El lienzo donde se dibuja el pack.
            color: Color del pack.
            x: Coordenada x del pack.
            y: Coordenada y del pack.
        """
        lienzo.create_rectangle(x, y, x + 5, y + 5, outline=color, fill=color)


class SlopeLineStrategy(AlgoritmoDibujo):
    """Estrategia 1: Dibujo de línea con la fórmula de la pendiente (solo primer cuadrante)."""

    def dibujar_linea(
        self,
        lienzo: Canvas,
        color: str,
        x_inicial: int,
        y_inicial: int,
        x_final: int,
        y_final: int,
    ) -> None:
        """
        Dibuja una línea usando la fórmula de la pendiente.

        Args:
            lienzo: El lienzo donde se dibuja la línea.
            color: Color de la línea.
            x_inicial: Coordenada x inicial.
            y_inicial: Coordenada y inicial.
            x_final: Coordenada x final.
            y_final: Coordenada y final.
        """
        print(
            f"Dibujando línea con pendiente desde ({x_inicial}, {y_inicial}) a ({x_final}, {y_final})"
        )


class DDALineStrategy(AlgoritmoDibujo):
    """Estrategia 2: Dibujo de línea con el algoritmo DDA."""

    def dibujar_linea(
        self, lienzo: Canvas, color: str, x1: int, y1: int, x2: int, y2: int
    ) -> None:
        """
        Dibuja una línea usando el algoritmo DDA.

        Args:
            lienzo: El lienzo donde se dibuja la línea.
            color: Color de la línea.
            x1: Coordenada x inicial.
            y1: Coordenada y inicial.
            x2: Coordenada x final.
            y2: Coordenada y final.
        """
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        x_increment = dx / steps
        y_increment = dy / steps
        x, y = x1, y1

        # Dibuja el primer "pack" de 5x5 píxeles
        self._dibujar_pack(lienzo, color, x, y)

        for _ in range(steps):
            x += x_increment
            y += y_increment
            # Dibuja un pack de 5x5 en lugar de un solo píxel
            self._dibujar_pack(lienzo, color, round(x), round(y))


class BresenhamLineStrategy(AlgoritmoDibujo):
    """Estrategia 3: Dibujo de línea con el algoritmo de Bresenham."""

    def dibujar_linea(
        self, lienzo: Canvas, color: str, x1: int, y1: int, x2: int, y2: int
    ) -> None:
        """
        Dibuja una línea usando el algoritmo de Bresenham.

        Args:
            lienzo: El lienzo donde se dibuja la línea.
            color: Color de la línea.
            x1: Coordenada x inicial.
            y1: Coordenada y inicial.
            x2: Coordenada x final.
            y2: Coordenada y final.
        """
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            # Dibuja un bloque de 5x5 en lugar de un solo píxel
            self._dibujar_pack(lienzo, color, x1, y1)

            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

            # Saltamos cada 5 píxeles para dibujar bloques de 5x5
            if abs(x1 - x2) % 5 == 0 and abs(y1 - y2) % 5 == 0:
                self._dibujar_pack(lienzo, color, x1, y1)
