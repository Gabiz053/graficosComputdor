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
from ventana import Ventana  # Clase base para ventanas.
from constantes import Default, Texts  # Constantes y textos predeterminados.


class FractalIFS(Ventana):
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
        lista_funciones: list = [],
        checkbox_default_pro: bool = False,
    ) -> None:
        """
        Inicializa una nueva instancia de la clase FractalIFS.

        Args:
            width (int): Ancho de la ventana en píxeles. Valor por defecto definido en Default.WINDOW_WIDTH.
            height (int): Alto de la ventana en píxeles. Valor por defecto definido en Default.WINDOW_HEIGHT.
            title (str): Título de la ventana. Valor por defecto definido en Default.WINDOW_TITLE.
            lista_funciones (list): Lista de funciones que define el sistema iterado. Por defecto, lista vacía.
            checkbox_default_pro (bool): Indicador para opciones avanzadas. Por defecto, False.
        """
        super().__init__(width, height, title)
        self.lista_funciones = lista_funciones
        self.checkbox_default_pro = checkbox_default_pro

    def _crear_contenido_ventana(self) -> None:
        """
        Crea y configura los elementos de la ventana para la visualización del fractal.

        Este método genera un área de visualización para mostrar el fractal IFS,
        utilizando las funciones y configuraciones definidas.

        Elementos creados:
        - Un frame (`CTkFrame`) como contenedor principal.
        - Una etiqueta (`CTkLabel`) para mostrar información inicial.
        """
        # Crear un frame para el área de visualización
        frame_visualizacion = ctk.CTkFrame(self.ventana, corner_radius=10)
        frame_visualizacion.pack(fill="both", expand=True, padx=10, pady=10)

        # Añadir un texto inicial o una etiqueta para indicar el propósito del área
        label_info = ctk.CTkLabel(frame_visualizacion, text="Fractal generado: IFS")
        label_info.pack(pady=20, padx=20)

        # Depuración: Mostrar en la consola los parámetros seleccionados
        print("Lista de funciones:", self.lista_funciones)
        print("Probabilidad por defecto?:", self.checkbox_default_pro)
