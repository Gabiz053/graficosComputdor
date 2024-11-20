""" 
Archivo: ventana_menu_canvas_animacion.py

Descripción:
    Esta clase extiende las funcionalidades de VentanaMenuCanvas para incorporar
    la lógica de animación en el lienzo. Permite gestionar y ejecutar animaciones
    de manera independiente.

Autor: Gabriel Gomez Garcia
Fecha: 21 de septiembre de 2024
"""

# Importaciones estándar
import tkinter as tk
import numpy as np
from ventana_menu_canvas import VentanaMenuCanvas


class VentanaMenuCanvasAnimacion(VentanaMenuCanvas):
    """
    Clase que extiende VentanaMenuCanvas para manejar animaciones en el lienzo.

    Esta clase proporciona métodos para iniciar, detener y gestionar animaciones
    en el canvas, separando la lógica de animación de la lógica de dibujo.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Constructor de la clase VentanaMenuCanvasAnimacion.

        Inicializa la ventana con un lienzo interactivo y configura las propiedades
        necesarias para la animación.

        Args:
            *args: Argumentos adicionales para VentanaMenuCanvas.
            **kwargs: Argumentos adicionales para VentanaMenuCanvas.
        """
        super().__init__(*args, **kwargs)
        self.animaciones = []  # Lista para almacenar las animaciones en curso
        self.animacion_activa = False  # Estado de la animación

    def iniciar_animacion(self) -> None:
        """
        Inicia la animación en el lienzo.
        """
        if not self.animacion_activa:
            self.animacion_activa = True
            self._ejecutar_animacion()  # Llama al método que ejecuta la animación

    def detener_animacion(self) -> None:
        """
        Detiene la animación en el lienzo.
        """
        self.animacion_activa = False
        print("Animación acabada")

    def _ejecutar_animacion(self) -> None:
        """
        Método privado que ejecuta la lógica de la animación.
        Este método se llamará repetidamente mientras la animación esté activa.
        """
        # tiene que estar la animacion activa y que queden animaciones en curso
        if self.animacion_activa and len(self.lista_transformaciones) != 0:

            self._actualizar_canvas()  # Método para actualizar el canvas

            # Programar la siguiente ejecución de la animación
            self.ventana.after(1000, self._ejecutar_animacion)

    def _actualizar_canvas(self) -> None:
        """
        Actualiza el contenido del canvas para reflejar los cambios de la animación.
        """
        # Implementa la lógica para actualizar el canvas aquí
        # Por ejemplo, mover figuras, redibujar, etc.
        poligono, puntos = self.lista_transformaciones.pop(0)

        poligono.borrar()
        poligono.puntos = puntos
        poligono.dibujar()

    def _generar_peli(self):
        super()._generar_peli()
        self.iniciar_animacion()
