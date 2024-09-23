"""
Archivo: Ventana_menu_canvas.py

Este archivo define la clase VentanaMenuCanvas, que extiende la funcionalidad
de la clase VentanaMenu anhadiendo un canvas con funcionalidad para dibujar

Autor: Gabriel Gomez Garcia
Fecha: 21 de septiembre de 2024
"""

import tkinter as tk

from ventana_menu import VentanaMenu
from forma import *
from constantes import Default, Event, Herramienta, Color


class VentanaMenuCanvas(VentanaMenu):
    """
    Clase que extiende VentanaMenu para permitir la interaccion en un lienzo.

    Anhade la funcionalidad de dibujar en un canvas utilizando diferentes herramientas.
    Esta clase gestiona eventos del raton para detectar acciones del usuario y dibujar.

    Atributos heredados:
        width (int): El ancho de la ventana en pixeles.
        height (int): La altura de la ventana en pixeles.
        title (str): El titulo de la ventana.
        ventana (tk.Tk): La instancia de la ventana principal de tkinter.
        herramienta_seleccionada (str): herramienta seleccionada para dibujar.
        color_seleccionado (str): color seleccionado para dibujar.

    Atributos de instancia:

    """

    def __init__(
        self,
        width: int = Default.VENTANA_WIDTH,
        height: int = Default.VENTANA_HEIGHT,
        title: str = Default.VENTANA_TITLE,
        herramientaSeleccionada: str = Default.HERRAMIENTA,
        colorSeleccionado: str = Default.COLOR,
    ):
        """
        Constructor de la clase VentanaMenuCanvas.

        Inicializa la ventana con el tamanho y el titulo proporcionados, y ademas configura
        la interaccion del lienzo.

        Args:
            width (int): Ancho de la ventana en pixeles.
            height (int): Alto de la ventana en pixeles.
            title (str): Titulo de la ventana.
            herramientaSeleccionada (str): Herramienta seleccionada para dibujar.
            colorSeleccionado (str): Color seleccionado para dibujar.
        """

        super().__init__(
            width, height, title, herramientaSeleccionada, colorSeleccionado
        )
        self.punto_inicial = None

    def crear_lienzo(self) -> None:
        """
        Crea el lienzo de dibujo (Canvas) y configura los eventos del raton para
        permitir la interaccion del usuario.

        Returns:
            tk.Label: El Label que actúa como lienzo.
        """

        self.lienzo = tk.PhotoImage()

        # Crear un Label para mostrar el lienzo
        self.label = tk.Label(self._ventana, image=self.lienzo)
        self.label.pack(fill=tk.BOTH, expand=True)

        # Asignar eventos para dibujar con el botón izquierdo del ratón
        self.label.bind("<Button-1>", self.iniciar_dibujo)

        return self.label

    def _crear_contenido_ventana(self) -> None:
        """
        Sobrescribe el metodo de VentanaMenu para anadir el lienzo a la ventana.
        """
        super()._crear_contenido_ventana()
        self.canvas = self.crear_lienzo()

    def iniciar_dibujo(self, event: tk.Event) -> None:
        # Obtener el tamaño del Label
        width = self.label.winfo_width()
        height = self.label.winfo_height()

        # Convertir las coordenadas para que (0, 0) esté en el centro
        x = event.x - width // 2
        y = height // 2 - event.y

        if self.punto_inicial is None:
            self.punto_inicial = Punto(
                x,
                y,
                self.color_seleccionado,
                Default.TAMANHO_DIBUJAR,
                self.herramienta_seleccionada,
            )
        else:
            punto_final = Punto(
                x,
                y,
                self.color_seleccionado,
                Default.TAMANHO_DIBUJAR,
                self.herramienta_seleccionada,
            )
            # Guardar el segundo punto y dibujar la línea
            linea = Linea(self.punto_inicial, punto_final)
            print(linea)
            self.punto_inicial = None  # Resetear el primer punto
