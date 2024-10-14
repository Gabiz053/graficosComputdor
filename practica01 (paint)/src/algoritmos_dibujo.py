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
    ) -> list:
        """
        Dibuja una línea en el lienzo usando el algoritmo de pendiente.
        """
        lista_puntos = []

        # Transformar las coordenadas y para que sean positivas hacia arriba
        y_inicial = -y_inicial
        y_final = -y_final

        def plot_line_low(x0, y0, x1, y1):
            """Dibuja una línea de pendiente baja (0 <= m < 1)"""
            dx = x1 - x0
            dy = y1 - y0
            m = dy / dx
            b = y0 - m * x0  # altura de la línea en x=0

            for x in range(x0, x1 + 1, tamanho_pincel):
                y = m * x + b

                x_pack = math.floor(x / tamanho_pincel) * tamanho_pincel
                y_pack = math.floor(y / tamanho_pincel) * tamanho_pincel + tamanho_pincel

                # Invertir coordenada Y de nuevo antes de dibujar en el canvas
                y_pack_canvas = -y_pack  # Ajuste para invertir la coordenada y
                self._dibujar_pack(lienzo, color, tamanho_pincel, x_pack, y_pack_canvas)
                lista_puntos.append((x_pack // tamanho_pincel, y_pack // tamanho_pincel - 1))

        def plot_line_high(x0, y0, x1, y1):
            """Dibuja una línea de pendiente alta (m > 1 o m < -1)"""
            dx = x1 - x0
            dy = y1 - y0
            m = dx / dy  # Ahora la pendiente se calcula como dx/dy
            b = x0 - m * y0  # Nueva intersección en x=0

            for y in range(y0, y1 + 1, tamanho_pincel):
                x = m * y + b  # Resolviendo x en función de y

                x_pack = math.floor(x / tamanho_pincel) * tamanho_pincel
                y_pack = math.floor(y / tamanho_pincel) * tamanho_pincel + tamanho_pincel

                # Invertir coordenada Y de nuevo antes de dibujar en el canvas
                y_pack_canvas = -y_pack  # Ajuste para invertir la coordenada y
                self._dibujar_pack(lienzo, color, tamanho_pincel, x_pack, y_pack_canvas)
                lista_puntos.append((x_pack // tamanho_pincel, y_pack // tamanho_pincel- 1))

        # Lógica principal para elegir la dirección de trazado
        if abs(y_final - y_inicial) < abs(x_final - x_inicial):  # si la pendiente mayor que 1
            if x_inicial > x_final:
                plot_line_low(x_final, y_final, x_inicial, y_inicial)  # Invertir los puntos
            else:
                plot_line_low(x_inicial, y_inicial, x_final, y_final)
        else:
            if y_inicial > y_final:
                plot_line_high(x_final, y_final, x_inicial, y_inicial)  # Invertir los puntos
            else:
                plot_line_high(x_inicial, y_inicial, x_final, y_final)

        return lista_puntos


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
    ) -> list:
        """
        Dibuja una línea en el lienzo usando el algoritmo DDA (Digital Differential Analyzer).
        """
        # cambiamos las y positivas, al final se le suma a y tamanho pincel paraalinear el 0 0
        # es aasi porque el 0 0 se queda 1 por debajo del eje x porque las y iban hacia abajo
        y_inicial = -y_inicial
        y_final = -y_final

        lista_puntos = []
        dx = x_final - x_inicial
        dy = y_final - y_inicial

        # cambio: dividir entre el tamanho para que no se pinten de mas
        pixeles = max(abs(dx), abs(dy)) / tamanho_pincel

        x_incremento = dx / pixeles
        y_incremento = dy / pixeles

        x = x_inicial + 0.5
        y = y_inicial + 0.5

        i = 0
        while i <= pixeles:
            x_pack = math.floor(x / tamanho_pincel) * tamanho_pincel
            y_pack = math.floor(y / tamanho_pincel) * tamanho_pincel + tamanho_pincel

            # entre tamanho pincel para que se pinten bonitos de 1 en 1
            lista_puntos.append((x_pack / tamanho_pincel, y_pack / tamanho_pincel - 1))
            self._dibujar_pack(lienzo, color, tamanho_pincel, x_pack, -y_pack)

            x += x_incremento
            y += y_incremento
            i += 1

        return lista_puntos


class BresenhamLineStrategy(AlgoritmoDibujo):
    """
    Estrategia de dibujo de líneas usando el algoritmo Bresenham con números reales.
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
        ) -> list:
        """
        Dibuja una línea en el lienzo usando el algoritmo Bresenham con números reales.
        """
        lista_puntos = []

        # Transformar las coordenadas y para que sean positivas hacia arriba
        y_inicial = -y_inicial
        y_final = -y_final

        def plot_line_low(x0, y0, x1, y1):
            """Dibuja una línea de pendiente baja (0 <= pendiente < 1)"""
            dx = x1 - x0
            dy = y1 - y0
            yi = 1
            if dy < 0:  # Si la pendiente es negativa, invertimos el incremento de y
                yi = -1
                dy = -dy

            m = dy / dx  # Pendiente real
            y = y0
            e = m - 0.5  # Error inicial

            for x in range(x0, x1 + 1, tamanho_pincel):
                x_pack = math.floor(x / tamanho_pincel) * tamanho_pincel
                y_pack = math.floor(y / tamanho_pincel) * tamanho_pincel + tamanho_pincel

                # Invertir coordenada Y de nuevo antes de dibujar en el canvas
                y_pack_canvas = -y_pack
                self._dibujar_pack(lienzo, color, tamanho_pincel, x_pack, y_pack_canvas)
                lista_puntos.append((x_pack // tamanho_pincel, y_pack // tamanho_pincel -1))

                if e > 0:
                    y += yi * tamanho_pincel
                    e -= 1
                e += m

        def plot_line_high(x0, y0, x1, y1):
            """Dibuja una línea de pendiente alta (pendiente >= 1 o pendiente <= -1)"""
            dx = x1 - x0
            dy = y1 - y0
            xi = 1
            if dx < 0:  # Si la pendiente es negativa, invertimos el incremento de x
                xi = -1
                dx = -dx

            m = dx / dy  # Pendiente real
            x = x0
            e = m - 0.5  # Error inicial

            for y in range(y0, y1 + 1, tamanho_pincel):
                x_pack = math.floor(x / tamanho_pincel) * tamanho_pincel
                y_pack = math.floor(y / tamanho_pincel) * tamanho_pincel + tamanho_pincel

                # Invertir coordenada Y de nuevo antes de dibujar en el canvas
                y_pack_canvas = -y_pack
                self._dibujar_pack(lienzo, color, tamanho_pincel, x_pack, y_pack_canvas)
                lista_puntos.append((x_pack // tamanho_pincel, y_pack // tamanho_pincel -1))

                if e > 0:
                    x += xi * tamanho_pincel
                    e -= 1
                e += m

        # Lógica principal para elegir la dirección de trazado
        if abs(y_final - y_inicial) < abs(x_final - x_inicial):  # Si la pendiente es menor que 1
            if x_inicial > x_final:
                plot_line_low(x_final, y_final, x_inicial, y_inicial)  # Invertir los puntos
            else:
                plot_line_low(x_inicial, y_inicial, x_final, y_final)
        else:
            if y_inicial > y_final:
                plot_line_high(x_final, y_final, x_inicial, y_inicial)  # Invertir los puntos
            else:
                plot_line_high(x_inicial, y_inicial, x_final, y_final)

        return lista_puntos



class BresenhamLineStrategyInt(AlgoritmoDibujo):
    """
    Estrategia de dibujo de líneas usando el algoritmo Bresenham con enteros.
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
    ) -> list:
        """
        Dibuja una línea en el lienzo usando el algoritmo de Bresenham.
        """
        lista_puntos = []

        # Transformar las coordenadas y para que sean positivas hacia arriba
        y_inicial = - y_inicial
        y_final = - y_final

        def plot_line_low(x0, y0, x1, y1):
            """Dibuja una línea de pendiente baja (0 <= m < 1)"""
            dx = x1 - x0
            dy = y1 - y0
            yi = 1

            if dy < 0:
                yi = -1
                dy = -dy

            D = (2 * dy) - dx
            y = y0

            for x in range(x0, x1 + 1, tamanho_pincel):
                x_pack = math.floor(x / tamanho_pincel) * tamanho_pincel
                y_pack = math.floor(y / tamanho_pincel) * tamanho_pincel + tamanho_pincel

                # Invertir coordenada Y de nuevo antes de dibujar en el canvas
                y_pack_canvas = - y_pack
                self._dibujar_pack(lienzo, color, tamanho_pincel, x_pack, y_pack_canvas)
                lista_puntos.append((x_pack // tamanho_pincel, y_pack // tamanho_pincel - 1))

                if D > 0:
                    y += yi * tamanho_pincel
                    D += (2 * (dy - dx))
                else:
                    D += 2 * dy

        def plot_line_high(x0, y0, x1, y1):
            """Dibuja una línea de pendiente alta (m > 1 o m < -1)"""
            dx = x1 - x0
            dy = y1 - y0
            xi = 1

            if dx < 0:
                xi = -1
                dx = -dx

            D = (2 * dx) - dy
            x = x0

            for y in range(y0, y1 + 1, tamanho_pincel):
                x_pack = math.floor(x / tamanho_pincel) * tamanho_pincel 
                y_pack = math.floor(y / tamanho_pincel) * tamanho_pincel + tamanho_pincel

                # Invertir coordenada Y de nuevo antes de dibujar en el canvas
                y_pack_canvas = - y_pack
                self._dibujar_pack(lienzo, color, tamanho_pincel, x_pack, y_pack_canvas)
                lista_puntos.append((x_pack // tamanho_pincel, y_pack // tamanho_pincel - 1))

                if D > 0:
                    x += xi * tamanho_pincel
                    D += (2 * (dx - dy))
                else:
                    D += 2 * dx

        # Lógica principal para elegir la dirección de trazado
        if abs(y_final - y_inicial) < abs(x_final - x_inicial):  # si la pendiente mayor que 1
            if x_inicial > x_final:
                plot_line_low(x_final, y_final, x_inicial, y_inicial)  # Invertir los puntos
            else:
                plot_line_low(x_inicial, y_inicial, x_final, y_final)
        else:
            if y_inicial > y_final:
                plot_line_high(x_final, y_final, x_inicial, y_inicial)  # Invertir los puntos
            else:
                plot_line_high(x_inicial, y_inicial, x_final, y_final)

        return lista_puntos

