"""
Archivo: fractal_ifs.py

Descripción:
Este archivo contiene la implementación de la clase `FractalIFS`, que representa
una ventana interactiva diseñada para la visualización de fractales generados mediante
sistemas de funciones iteradas (IFS, por sus siglas en inglés).

Características principales:
- Configuración personalizada mediante una lista de funciones y opciones adicionales.
- Uso de CustomTkinter para una interfaz gráfica moderna.
- Integración con Matplotlib para futuras visualizaciones del fractal.

Autor: Gabriel Gómez García
Fecha: 27 de Noviembre de 2024
"""

# Imports estándar
import numpy as np  # Para cálculos numéricos avanzados.
import matplotlib.pyplot as plt  # Para gráficos y visualizaciones.
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
)  # Integración de Matplotlib en Tkinter.
from matplotlib.figure import Figure  # Clase base para las figuras de Matplotlib.

# Importación de Tkinter y CustomTkinter para la interfaz gráfica
import tkinter as tk  # Biblioteca estándar para interfaces gráficas.
import customtkinter as ctk  # Biblioteca para interfaces gráficas modernas.

# Imports locales
from ventana_fractal import VentanaFractal  # Clase base para ventanas.
from constantes import Default, Texts  # Constantes y textos predeterminados.

import random

class FractalIFS(VentanaFractal):
    """
    Clase que representa una ventana interactiva para la visualización de fractales IFS.

    Esta clase hereda de `Ventana` y permite la configuración mediante una lista de
    funciones iteradas y opciones adicionales para personalizar la experiencia.

    Atributos:
        lista_funciones (list): Lista de funciones que definen el sistema iterado.
        checkbox_default_pro (bool): Opción adicional para configuración avanzada.
    """

    def __init__(
        self,
        width: int = Default.WINDOW_WIDTH,
        height: int = Default.WINDOW_HEIGHT,
        title: str = Default.WINDOW_TITLE,
        lista_funciones: list = Texts.IFS_LISTA_DEFAULT,
        checkbox_default_pro: bool = False,
        iterations: int = 100000,
        threshold: int = 30,
    ) -> None:
        """
        Inicializa una nueva instancia de la clase FractalIFS.

        Args:
            width (int): Ancho de la ventana en píxeles. Valor por defecto definido en Default.WINDOW_WIDTH.
            height (int): Alto de la ventana en píxeles. Valor por defecto definido en Default.WINDOW_HEIGHT.
            title (str): Título de la ventana. Valor por defecto definido en Default.WINDOW_TITLE.
            lista_funciones (list): Lista de funciones que define el sistema iterado. Por defecto, lista vacía.
            checkbox_default_pro (bool): Indicador para opciones avanzadas. Por defecto, False.
            iterations (int): Número de iteraciones para el fractal.
            threshold (int): Umbral que no se pinta nada para dejar que los puntos lleguen al fractal.
        """
        super().__init__(width, height, title)
        self.lista_funciones = lista_funciones
        self.checkbox_default_pro = checkbox_default_pro
        self.threshold = threshold
        self.iterations = iterations

    def _generar_fractal(self) -> None:
        """"""
        self.dibujar_ifs()

    def dibujar_ifs(self):
        """Genera y dibuja el fractal IFS agrupando puntos por función."""
        if not self.lista_funciones:
            print("Error: No se ha definido ninguna función en lista_funciones.")
            return

        # Inicializar el punto inicial
        x, y = 0, 0  # El punto inicial

        # Crear una estructura para almacenar los puntos y colores por función
        puntos_por_funcion = {i: [] for i in range(len(self.lista_funciones))}

        for i in range(self.iterations):
            funcion_seleccionada = self._seleccionar_funcion()
            valores, prob, color = funcion_seleccionada
            a, b, c, d, e, f = (
                float(valores["a"]),
                float(valores["b"]),
                float(valores["c"]),
                float(valores["d"]),
                float(valores["e"]),
                float(valores["f"]),
            )

            # Calcular el nuevo punto transformado
            x_nuevo = a * x + c * y + e
            y_nuevo = b * x + d * y + f

            # Solo almacenar puntos después de superar el umbral
            if i >= self.threshold:
                # Identificar el índice de la función seleccionada
                index_funcion = self.lista_funciones.index(funcion_seleccionada)
                puntos_por_funcion[index_funcion].append((x_nuevo, y_nuevo))

            # Actualizar el punto para la siguiente iteración
            x, y = x_nuevo, y_nuevo

        # Dibujar los puntos agrupados por función
        for i, puntos in puntos_por_funcion.items():
            if puntos:  # Asegurarse de que haya puntos para la función
                color = self.lista_funciones[i][2]  # Obtener el color asociado a la función
                puntos_x = [p[0] for p in puntos]
                puntos_y = [p[1] for p in puntos]
                self.ax.scatter(puntos_x, puntos_y, s=0.1, c=color)  # Dibujar los puntos

        self.canvas.draw()

    # Chaos game
    ###################################################################################

    def _seleccionar_funcion(self):
        """
        Selecciona una función de lista_funciones basada en un algoritmo tipo Chaos Game.

        Returns:
            tuple: Función seleccionada, Matriz de transformación, vector de traslación y color asociado.
        """

        # Probabilidades uniformes si se activa la opción avanzada
        if self.checkbox_default_pro:
            # Probabilidad uniforme si está activa la opción avanzada
            probabilidades = self._chaos_game()
            # print("Probabilidades uniformes:", probabilidades)
        else:
            # Usar probabilidades definidas en lista_funciones
            probabilidades = [float(prob) for _, prob, _ in self.lista_funciones]
            # print("Probabilidades definidas:", probabilidades)

        # Crear probabilidades acumulativas
        probabilidades_acumuladas = self._calcular_probabilidades_acumuladas(
            probabilidades
        )
        # print(probabilidades_acumuladas)

        # Elegir un número aleatorio entre 0 y 1
        num_aleatorio = random.random()
        # print(f"Valor aleatorio: {num_aleatorio}")

        # Seleccionar la función en función del número aleatorio
        for i, prob_acumulada in enumerate(probabilidades_acumuladas):
            if num_aleatorio < prob_acumulada:
                # Retornar la función y su información asociada
                return self.lista_funciones[i]

    def _calcular_probabilidades_acumuladas(self, probabilidades):
        """
        Calcula las probabilidades acumulativas a partir de las probabilidades individuales.

        Args:
            probabilidades (list): Lista de probabilidades.

        Returns:
            list: Lista de probabilidades acumuladas.
        """
        acumuladas = []
        acumulado = 0.0
        for prob in probabilidades:
            acumulado += prob
            acumuladas.append(acumulado)
        return acumuladas

    def _chaos_game(self):
        """"""
        
        determinantes = [abs(float(valores["a"]) * float(valores["d"]) - float(valores["b"]) * float(valores["c"])) for valores, _, _ in self.lista_funciones]
        total_prob = sum(determinantes)
        
        probabilidades = []
        for det in determinantes:
            probabilidades.append(det / total_prob)
        return probabilidades
    
###################################################################################

if __name__ == "__main__":
    FractalIFS().mostrar_ventana()
