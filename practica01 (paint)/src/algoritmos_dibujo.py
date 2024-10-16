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
    Define la interfaz para dibujar líneas en un lienzo.
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
    ) -> tuple[list[tuple[int, int]], list[int]]:
        """
        Dibuja una línea en el lienzo.

        Este método debe ser implementado por cada clase que extienda AlgoritmoDibujo.

        Args:
            lienzo (Canvas): El lienzo donde se dibuja la línea.
            color (str): Color de la línea.
            tamanho_pincel (int): Tamaño del pincel para el grosor de la línea.
            x_inicial (int): Coordenada X inicial.
            y_inicial (int): Coordenada Y inicial.
            x_final (int): Coordenada X final.
            y_final (int): Coordenada Y final.

        Returns:
            tuple[list[tuple[int, int]], list[int]]:
                - lista de puntos dibujados (cada punto representado como una tupla de coordenadas).
                - lista de identificadores de los elementos dibujados en el lienzo.
        """
        raise NotImplementedError("Error: método no implementado")

    def _dibujar_pack(
        self, lienzo: Canvas, color: str, tamanho_pincel: int, x: int, y: int
    ) -> int:
        """
        Dibuja un rectángulo de tamanho_pincel x tamanho_pincel en lugar de un píxel individual.

        Esto permite que las líneas se vean más gruesas según el tamaño del pincel.

        Args:
            lienzo (Canvas): El lienzo donde se dibuja.
            color (str): Color del rectángulo.
            tamanho_pincel (int): Tamaño del pincel.
            x (int): Coordenada X donde se dibuja el rectángulo.
            y (int): Coordenada Y donde se dibuja el rectángulo.

        Returns:
            int: Identificador del rectángulo dibujado en el lienzo.
        """
        return lienzo.create_rectangle(
            x, y, x + tamanho_pincel, y + tamanho_pincel, outline=color, fill=color
        )


class SlopeLineStrategy(AlgoritmoDibujo):
    """
    Estrategia de dibujo de líneas utilizando el cálculo de la pendiente.
    Esta clase implementa el algoritmo de trazado de líneas basado en la
    pendiente, utilizando dos métodos privados para manejar líneas con
    pendientes bajas y altas.
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
    ) -> tuple[list[tuple[int, int]], list[int]]:
        """
        Dibuja una línea en el lienzo usando el algoritmo de pendiente.

        Este método determina si la línea tiene una pendiente baja o alta
        y llama al método correspondiente para realizar el trazado.

        Args:
            lienzo (Canvas): El lienzo donde se dibuja la línea.
            color (str): Color de la línea.
            tamanho_pincel (int): Tamaño del pincel para el grosor de la línea.
            x_inicial (int): Coordenada X inicial.
            y_inicial (int): Coordenada Y inicial.
            x_final (int): Coordenada X final.
            y_final (int): Coordenada Y final.

        Returns:
            tuple[list[tuple[int, int]], list[int]]:
                - lista de puntos dibujados.
                - lista de identificadores de los elementos dibujados en el lienzo.
        """
        lista_puntos = []
        lista_dibujados = []

        def _plot_line_low(x0: int, y0: int, x1: int, y1: int) -> None:
            """Dibuja una línea de pendiente baja (0 <= m < 1)."""
            dx = x1 - x0
            dy = y1 - y0
            m = dy / dx
            b = y0 - m * x0  # altura de la línea en x=0

            for x in range(x0, x1 + 2, tamanho_pincel):
                y = m * x + b

                x_pack = math.floor(x / tamanho_pincel) * tamanho_pincel
                y_pack = (
                    math.floor(y / tamanho_pincel) * tamanho_pincel + tamanho_pincel
                )

                # Invertir coordenada Y de nuevo antes de dibujar en el canvas
                y_pack_canvas = -y_pack  # Ajuste para invertir la coordenada y
                lista_dibujados.append(
                    self._dibujar_pack(
                        lienzo, color, tamanho_pincel, x_pack, y_pack_canvas
                    )
                )
                lista_puntos.append(
                    (x_pack // tamanho_pincel, y_pack // tamanho_pincel - 1)
                )

        def _plot_line_high(x0: int, y0: int, x1: int, y1: int) -> None:
            """Dibuja una línea de pendiente alta (m > 1 o m < -1)."""
            dx = x1 - x0
            dy = y1 - y0
            m = dx / dy  # Ahora la pendiente se calcula como dx/dy
            b = x0 - m * y0  # Nueva intersección en x=0

            for y in range(y0, y1 + 2, tamanho_pincel):
                x = m * y + b  # Resolviendo x en función de y

                x_pack = math.floor(x / tamanho_pincel) * tamanho_pincel
                y_pack = (
                    math.floor(y / tamanho_pincel) * tamanho_pincel + tamanho_pincel
                )

                # Invertir coordenada Y de nuevo antes de dibujar en el canvas
                y_pack_canvas = -y_pack  # Ajuste para invertir la coordenada y
                lista_dibujados.append(
                    self._dibujar_pack(
                        lienzo, color, tamanho_pincel, x_pack, y_pack_canvas
                    )
                )
                lista_puntos.append(
                    (x_pack // tamanho_pincel, y_pack // tamanho_pincel - 1)
                )

        # Lógica principal para elegir la dirección de trazado
        if abs(y_final - y_inicial) < abs(
            x_final - x_inicial
        ):  # si la pendiente es menor que 1
            if x_inicial > x_final:
                _plot_line_low(
                    x_final, y_final, x_inicial, y_inicial
                )  # Invertir los puntos
            else:
                _plot_line_low(x_inicial, y_inicial, x_final, y_final)
        else:
            if y_inicial > y_final:
                _plot_line_high(
                    x_final, y_final, x_inicial, y_inicial
                )  # Invertir los puntos
            else:
                _plot_line_high(x_inicial, y_inicial, x_final, y_final)

        return lista_puntos, lista_dibujados


class DDALineStrategy(AlgoritmoDibujo):
    """
    Estrategia de dibujo de líneas usando el algoritmo DDA (Digital Differential Analyzer).
    Esta clase implementa el algoritmo DDA para el trazado de líneas, calculando
    la posición de cada punto en la línea en función del cambio en las coordenadas.
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
    ) -> tuple[list[tuple[int, int]], list[int]]:
        """
        Dibuja una línea en el lienzo usando el algoritmo DDA.

        Este método calcula el número de pasos requeridos en función de la
        distancia máxima entre las coordenadas inicial y final, y utiliza
        incrementos para trazar la línea pixel por pixel.

        Args:
            lienzo (Canvas): El lienzo donde se dibuja la línea.
            color (str): Color de la línea.
            tamanho_pincel (int): Tamaño del pincel para el grosor de la línea.
            x_inicial (int): Coordenada X inicial.
            y_inicial (int): Coordenada Y inicial.
            x_final (int): Coordenada X final.
            y_final (int): Coordenada Y final.

        Returns:
            tuple[list[tuple[int, int]], list[int]]:
                - lista de puntos dibujados.
                - lista de identificadores de los elementos dibujados en el lienzo.
        """
        lista_puntos = []
        lista_dibujados = []

        dx = x_final - x_inicial
        dy = y_final - y_inicial

        # Calcular el incremento
        pixeles = max(abs(dx), abs(dy)) / tamanho_pincel

        x_incremento = dx / pixeles
        y_incremento = dy / pixeles

        x = x_inicial + 0.5
        y = y_inicial + 0.5

        i = 0
        while i <= pixeles:
            x_pack = math.floor(x / tamanho_pincel) * tamanho_pincel
            y_pack = math.floor(y / tamanho_pincel) * tamanho_pincel + tamanho_pincel
            # Invertir coordenada Y de nuevo antes de dibujar en el canvas
            y_pack_canvas = -y_pack
            lista_dibujados.append(
                self._dibujar_pack(lienzo, color, tamanho_pincel, x_pack, y_pack_canvas)
            )
            lista_puntos.append(
                (x_pack // tamanho_pincel, y_pack // tamanho_pincel - 1)
            )
            x += x_incremento
            y += y_incremento
            i += 1

        return lista_puntos, lista_dibujados


class BresenhamLineStrategy(AlgoritmoDibujo):
    """
    Estrategia de dibujo de lineas usando el algoritmo Bresenham con numeros reales.
    Esta clase implementa el algoritmo de Bresenham para dibujar lineas sobre un lienzo
    utilizando coordenadas en numeros reales.
    """

    def dibujar_linea(
        self,
        lienzo: object,
        color: str,
        tamanho_pincel: float,
        x_inicial: float,
        y_inicial: float,
        x_final: float,
        y_final: float,
    ) -> tuple[list[tuple[int, int]], list[object]]:
        """
        Dibuja una linea en el lienzo usando el algoritmo Bresenham con numeros reales.

        Args:
            lienzo: El lienzo donde se dibujara la linea.
            color: El color de la linea a dibujar.
            tamanho_pincel: El tamaño del pincel para el dibujo.
            x_inicial: Coordenada x inicial de la linea.
            y_inicial: Coordenada y inicial de la linea.
            x_final: Coordenada x final de la linea.
            y_final: Coordenada y final de la linea.

        Returns:
            Una lista de puntos que forman la linea y una lista de elementos dibujados en el lienzo.
        """
        lista_puntos = []
        lista_dibujados = []

        def plot_line_low(x0: float, y0: float, x1: float, y1: float) -> None:
            """Dibuja una linea de pendiente baja (0 <= pendiente < 1)"""
            dx = x1 - x0
            dy = y1 - y0
            yi = 1
            if dy < 0:  # Si la pendiente es negativa, invertimos el incremento de y
                yi = -1
                dy = -dy

            m = dy / dx  # Pendiente real
            y = y0
            e = m - 0.5  # Error inicial

            for x in range(int(x0), int(x1) + 1, int(tamanho_pincel)):
                x_pack = math.floor(x / tamanho_pincel) * tamanho_pincel
                y_pack = (
                    math.floor(y / tamanho_pincel) * tamanho_pincel + tamanho_pincel
                )

                # Invertir coordenada Y de nuevo antes de dibujar en el canvas
                y_pack_canvas = -y_pack
                lista_dibujados.append(
                    self._dibujar_pack(
                        lienzo, color, tamanho_pincel, x_pack, y_pack_canvas
                    )
                )
                lista_puntos.append(
                    (int(x_pack // tamanho_pincel), int(y_pack // tamanho_pincel - 1))
                )

                if e > 0:
                    y += yi * tamanho_pincel
                    e -= 1
                e += m

        def plot_line_high(x0: float, y0: float, x1: float, y1: float) -> None:
            """Dibuja una linea de pendiente alta (pendiente >= 1 o pendiente <= -1)"""
            dx = x1 - x0
            dy = y1 - y0
            xi = 1
            if dx < 0:  # Si la pendiente es negativa, invertimos el incremento de x
                xi = -1
                dx = -dx

            m = dx / dy  # Pendiente real
            x = x0
            e = m - 0.5  # Error inicial

            for y in range(int(y0), int(y1) + 1, int(tamanho_pincel)):
                x_pack = math.floor(x / tamanho_pincel) * tamanho_pincel
                y_pack = (
                    math.floor(y / tamanho_pincel) * tamanho_pincel + tamanho_pincel
                )

                # Invertir coordenada Y de nuevo antes de dibujar en el canvas
                y_pack_canvas = -y_pack
                lista_dibujados.append(
                    self._dibujar_pack(
                        lienzo, color, tamanho_pincel, x_pack, y_pack_canvas
                    )
                )
                lista_puntos.append(
                    (int(x_pack // tamanho_pincel), int(y_pack // tamanho_pincel - 1))
                )

                if e > 0:
                    x += xi * tamanho_pincel
                    e -= 1
                e += m

        # Lógica principal para elegir la dirección de trazado
        if abs(y_final - y_inicial) < abs(
            x_final - x_inicial
        ):  # Si la pendiente es menor que 1
            if x_inicial > x_final:
                plot_line_low(
                    x_final, y_final, x_inicial, y_inicial
                )  # Invertir los puntos
            else:
                plot_line_low(x_inicial, y_inicial, x_final, y_final)
        else:
            if y_inicial > y_final:
                plot_line_high(
                    x_final, y_final, x_inicial, y_inicial
                )  # Invertir los puntos
            else:
                plot_line_high(x_inicial, y_inicial, x_final, y_final)

        return lista_puntos, lista_dibujados


class BresenhamLineStrategyInt(AlgoritmoDibujo):
    """
    Estrategia de dibujo de lineas usando el algoritmo Bresenham con enteros.
    Esta clase implementa el algoritmo de Bresenham para dibujar lineas sobre un lienzo
    utilizando coordenadas enteras.
    """

    def dibujar_linea(
        self,
        lienzo: object,
        color: str,
        tamanho_pincel: int,
        x_inicial: int,
        y_inicial: int,
        x_final: int,
        y_final: int,
    ) -> tuple[list[tuple[int, int]], list[object]]:
        """
        Dibuja una linea en el lienzo usando el algoritmo de Bresenham.

        Args:
            lienzo: El lienzo donde se dibujara la linea.
            color: El color de la linea a dibujar.
            tamanho_pincel: El tamaño del pincel para el dibujo.
            x_inicial: Coordenada x inicial de la linea.
            y_inicial: Coordenada y inicial de la linea.
            x_final: Coordenada x final de la linea.
            y_final: Coordenada y final de la linea.

        Returns:
            Una lista de puntos que forman la linea y una lista de elementos dibujados en el lienzo.
        """
        lista_puntos = []
        lista_dibujados = []

        def plot_line_low(x0: int, y0: int, x1: int, y1: int) -> None:
            """Dibuja una linea de pendiente baja (0 <= m < 1)"""
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
                y_pack = (
                    math.floor(y / tamanho_pincel) * tamanho_pincel + tamanho_pincel
                )

                # Invertir coordenada Y de nuevo antes de dibujar en el canvas
                y_pack_canvas = -y_pack
                lista_dibujados.append(
                    self._dibujar_pack(
                        lienzo, color, tamanho_pincel, x_pack, y_pack_canvas
                    )
                )
                lista_puntos.append(
                    (x_pack // tamanho_pincel, y_pack // tamanho_pincel - 1)
                )

                if D > 0:
                    y += yi * tamanho_pincel
                    D += 2 * (dy - dx)
                else:
                    D += 2 * dy

        def plot_line_high(x0: int, y0: int, x1: int, y1: int) -> None:
            """Dibuja una linea de pendiente alta (m > 1 o m < -1)"""
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
                y_pack = (
                    math.floor(y / tamanho_pincel) * tamanho_pincel + tamanho_pincel
                )

                # Invertir coordenada Y de nuevo antes de dibujar en el canvas
                y_pack_canvas = -y_pack
                lista_dibujados.append(
                    self._dibujar_pack(
                        lienzo, color, tamanho_pincel, x_pack, y_pack_canvas
                    )
                )
                lista_puntos.append((x_pack, y_pack))

                if D > 0:
                    x += xi * tamanho_pincel
                    D += 2 * (dx - dy)
                else:
                    D += 2 * dx

        # Lógica principal para elegir la dirección de trazado
        if abs(y_final - y_inicial) < abs(
            x_final - x_inicial
        ):  # Si la pendiente es menor que 1
            if x_inicial > x_final:
                plot_line_low(
                    x_final, y_final, x_inicial, y_inicial
                )  # Invertir los puntos
            else:
                plot_line_low(x_inicial, y_inicial, x_final, y_final)
        else:
            if y_inicial > y_final:
                plot_line_high(
                    x_final, y_final, x_inicial, y_inicial
                )  # Invertir los puntos
            else:
                plot_line_high(x_inicial, y_inicial, x_final, y_final)

        return lista_puntos, lista_dibujados
