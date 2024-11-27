"""
Archivo: fractal_mandelbrot.py

Descripción:
Este archivo contiene la implementación de la clase `FractalMandelbrot`, que representa
una ventana interactiva diseñada para la visualización de fractales de Mandelbrot.

Características principales:
- Configuración personalizada del color del fractal.
- Uso de CustomTkinter para la interfaz gráfica.
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
from ventana import Ventana  # Clase base para ventanas.
from constantes import Default, Texts  # Constantes y textos predeterminados.


class FractalMandelbrot(Ventana):
    """
    Clase que representa una ventana interactiva para la visualización de fractales de Mandelbrot.

    Esta clase hereda de `Ventana` y permite la personalización del color del fractal,
    mostrando una representación gráfica basada en los parámetros seleccionados.

    Atributos:
        color_seleccionado (str): Color seleccionado para renderizar el fractal.
    """

    def __init__(
        self,
        width: int = Default.WINDOW_WIDTH,
        height: int = Default.WINDOW_HEIGHT,
        title: str = Default.WINDOW_TITLE,
        color_seleccionado: str = Texts.MANDELBROT_COLORES_DEFAULT,
    ) -> None:
        """
        Inicializa una nueva instancia de la clase FractalMandelbrot.

        Args:
            width (int): Ancho de la ventana en píxeles. Valor por defecto definido en Default.WINDOW_WIDTH.
            height (int): Alto de la ventana en píxeles. Valor por defecto definido en Default.WINDOW_HEIGHT.
            title (str): Título de la ventana. Valor por defecto definido en Default.WINDOW_TITLE.
            color_seleccionado (str): Color seleccionado para el fractal.
                Valor por defecto definido en Texts.MANDELBROT_COLORES_DEFAULT.
        """
        super().__init__(width, height, title)
        self.color_seleccionado = color_seleccionado

    def _crear_contenido_ventana(self) -> None:
        """
        Crea y configura los elementos de la ventana para la visualización del fractal.

        Este método genera un área de visualización para mostrar el fractal de Mandelbrot,
        utilizando el color seleccionado por el usuario.

        Elementos creados:
        - Un frame (`CTkFrame`) como contenedor principal.
        - Una etiqueta (`CTkLabel`) para mostrar información inicial.
        """
        # Crear un frame para el área de visualización
        frame_visualizacion = ctk.CTkFrame(self.ventana, corner_radius=10)
        frame_visualizacion.pack(fill="both", expand=True, padx=10, pady=10)

        # Añadir un texto inicial o una etiqueta para indicar el propósito del área
        label_info = ctk.CTkLabel(
            frame_visualizacion, text="Fractal generado: Mandelbrot"
        )
        label_info.pack(pady=20, padx=20)

        # Depuración: Mostrar el color seleccionado en la consola
        print("Color seleccionado:", self.color_seleccionado)
