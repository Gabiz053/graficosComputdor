"""
Archivo: fractal_julia.py

Descripción:
Este archivo implementa la clase `FractalJulia`, que permite generar y visualizar fractales
de Julia en una ventana interactiva. Utiliza CustomTkinter para una interfaz gráfica moderna
y facilita la configuración de parámetros como los límites del plano complejo, el color y 
el conjunto de Julia seleccionado.

Autor: Gabriel Gómez García
Fecha: 27 de Noviembre de 2024
"""

# Imports estándar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Importación de Tkinter y CustomTkinter para la interfaz gráfica
import tkinter as tk
import customtkinter as ctk

# Imports locales
from ventana import Ventana
from constantes import Default, Texts


class FractalJulia(Ventana):
    """
    Clase que representa una ventana interactiva para la visualización de fractales de Julia.

    Esta clase hereda de `Ventana` y permite la configuración de parámetros esenciales
    para la generación del fractal, incluyendo el plano complejo, los colores y el conjunto
    específico de Julia.
    """

    def __init__(
        self,
        width: int = Default.WINDOW_WIDTH,
        height: int = Default.WINDOW_HEIGHT,
        title: str = Default.WINDOW_TITLE,
        julia_real: float = -0.7,
        julia_imaginario: float = 0.27015,
        julia_xmin: float = -1.5,
        julia_xmax: float = 1.5,
        julia_ymin: float = -1.5,
        julia_ymax: float = 1.5,
        julia_color_seleccionado: str = Texts.JULIA_COLORES_DEFAULT,
    ) -> None:
        """
        Inicializa una nueva instancia de la clase `FractalJulia`.

        Args:
            width (int): Ancho de la ventana en píxeles. Por defecto, Default.WINDOW_WIDTH.
            height (int): Alto de la ventana en píxeles. Por defecto, Default.WINDOW_HEIGHT.
            title (str): Título de la ventana. Por defecto, Default.WINDOW_TITLE.
            julia_real (float): Parte real del número complejo c para el conjunto de Julia.
            julia_imaginario (float): Parte imaginaria del número complejo c para el conjunto de Julia.
            julia_xmin (float): Límite mínimo del eje X en el plano complejo.
            julia_xmax (float): Límite máximo del eje X en el plano complejo.
            julia_ymin (float): Límite mínimo del eje Y en el plano complejo.
            julia_ymax (float): Límite máximo del eje Y en el plano complejo.
            julia_color_seleccionado (str): Color seleccionado para el fractal.
        """
        super().__init__(width, height, title)
        self.julia_real = julia_real
        self.julia_imaginario = julia_imaginario
        self.julia_xmin = julia_xmin
        self.julia_xmax = julia_xmax
        self.julia_ymin = julia_ymin
        self.julia_ymax = julia_ymax
        self.julia_color_seleccionado = julia_color_seleccionado

    def _crear_contenido_ventana(self) -> None:
        """
        Crea y configura los elementos de la ventana para la visualización del fractal.

        Este método genera un área de visualización para mostrar el fractal de Julia,
        utilizando los parámetros definidos.
        """
        # Crear un frame para el área de visualización
        frame_visualizacion = ctk.CTkFrame(self.ventana, corner_radius=10)
        frame_visualizacion.pack(fill="both", expand=True, padx=10, pady=10)

        # Añadir un texto inicial o una etiqueta para indicar el propósito del área
        label_info = ctk.CTkLabel(frame_visualizacion, text="Fractal generado: Julia")
        label_info.pack(pady=20, padx=20)

        # Depuración: Mostrar en la consola los parámetros seleccionados
        print("Parámetros seleccionados para el fractal de Julia:")
        print(f"  - Parte real: {self.julia_real}")
        print(f"  - Parte imaginaria: {self.julia_imaginario}")
        print(f"  - Xmin: {self.julia_xmin}, Xmax: {self.julia_xmax}")
        print(f"  - Ymin: {self.julia_ymin}, Ymax: {self.julia_ymax}")
        print(f"  - Color seleccionado: {self.julia_color_seleccionado}")
