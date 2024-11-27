"""
Archivo: fractal_recursivo.py

Descripción:
Este archivo contiene la implementación de la clase `FractalRecursivo`, que representa
una ventana interactiva destinada a la generación y visualización de fractales
utilizando algoritmos recursivos.

Características principales:
- Configuración personalizada de parámetros del fractal (algoritmo, color, nivel).
- Uso de CustomTkinter para una interfaz gráfica moderna.
- Integración con Matplotlib para la visualización del fractal generado.

Autor: Gabriel Gómez García
Fecha: 27 de Noviembre de 2024
"""

# Imports estándar
import numpy as np  # Para cálculos numéricos (en caso de ser necesario para el fractal).
import matplotlib.pyplot as plt  # Para la visualización de gráficos.
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
)  # Canvas para integrar Matplotlib con Tkinter.
from matplotlib.figure import Figure  # Representación de figuras en Matplotlib.

# Importación de Tkinter y CustomTkinter para la interfaz gráfica
import tkinter as tk  # Interfaz gráfica básica.
import customtkinter as ctk  # Extensión para interfaces modernas y personalizables.

# Imports locales
from ventana import Ventana  # Clase base para la ventana interactiva.
from constantes import (
    Default,
    Texts,
)  # Constantes y textos predeterminados para la configuración.


class FractalRecursivo(Ventana):
    """
    Clase que representa una ventana interactiva para la generación de fractales recursivos.

    Hereda de la clase `Ventana` y permite la personalización de diversos parámetros
    del fractal, como el algoritmo a usar, el color del dibujo y el nivel de recursión.

    Atributos:
        algoritmo_seleccionado (str): Algoritmo de fractal elegido.
        color_seleccionado (str): Color seleccionado para el fractal.
        nivel_seleccionado (int): Nivel de recursión o detalle del fractal.
    """

    def __init__(
        self,
        width: int = Default.WINDOW_WIDTH,
        height: int = Default.WINDOW_HEIGHT,
        title: str = Default.WINDOW_TITLE,
        algoritmo_seleccionado: str = Texts.RECURSIVO_ALGORITMOS_DEFAULT,
        color_seleccionado: str = Texts.RECURSIVO_COLOR_DEFAULT,
        nivel_seleccionado: int = Texts.RECURSIVO_NIVEL_DEFAULT,
    ) -> None:
        """
        Inicializa una nueva instancia de la clase FractalRecursivo.

        Args:
            width (int): Ancho de la ventana en píxeles. Valor por defecto definido en Default.WINDOW_WIDTH.
            height (int): Alto de la ventana en píxeles. Valor por defecto definido en Default.WINDOW_HEIGHT.
            title (str): Título de la ventana. Valor por defecto definido en Default.WINDOW_TITLE.
            algoritmo_seleccionado (str): Algoritmo seleccionado para generar el fractal.
                Valor por defecto definido en Texts.RECURSIVO_ALGORITMOS_DEFAULT.
            color_seleccionado (str): Color seleccionado para el fractal.
                Valor por defecto definido en Texts.RECURSIVO_COLOR_DEFAULT.
            nivel_seleccionado (int): Nivel de recursión del fractal.
                Valor por defecto definido en Texts.RECURSIVO_NIVEL_DEFAULT.
        """
        super().__init__(width, height, title)
        self.algoritmo_seleccionado = algoritmo_seleccionado
        self.color_seleccionado = color_seleccionado
        self.nivel_seleccionado = nivel_seleccionado

    def _crear_contenido_ventana(self) -> None:
        """
        Crea y configura los elementos de la ventana para la visualización del fractal.

        Este método genera un área de visualización para mostrar el fractal generado
        utilizando los parámetros seleccionados.

        Elementos creados:
        - Un frame (`CTkFrame`) como contenedor principal.
        - Una etiqueta (`CTkLabel`) para mostrar información inicial.
        """
        # Crear un frame para el área de visualización
        frame_visualizacion = ctk.CTkFrame(self.ventana, corner_radius=10)
        frame_visualizacion.pack(fill="both", expand=True, padx=10, pady=10)

        # Añadir un texto inicial o una etiqueta para indicar el propósito del área
        label_info = ctk.CTkLabel(
            frame_visualizacion, text="Fractal generado recursivamente."
        )
        label_info.pack(pady=20, padx=20)

        # Depuración: Mostrar los parámetros seleccionados en la consola
        print("Algoritmo:", self.algoritmo_seleccionado)
        print("Color:", self.color_seleccionado)
        print("Nivel:", self.nivel_seleccionado)
