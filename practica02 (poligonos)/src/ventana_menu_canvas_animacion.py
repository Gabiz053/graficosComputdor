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
        self.animacion_activa = False  # Estado de la animación
        self.lista_frames: list = []  # Lista de frames para la animación
        self.frame_index = 0  # Índice del frame actual

    def iniciar_animacion(self) -> None:
        """
        Inicia la animación en el lienzo.
        """
        if not self.animacion_activa and self.lista_frames:
            self.animacion_activa = True
            self.frame_index = 0  # Reiniciar el índice del frame
            self.lienzo.delete("all")  # Limpiar el lienzo
            self._ejecutar_animacion()

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
        if self.animacion_activa and self.frame_index < len(self.lista_frames):
            self._actualizar_canvas()  # Dibujar el frame actual
            self.frame_index += 1  # Pasar al siguiente frame

            # Programar la siguiente ejecución de la animación
            self.ventana.after(1000, self._ejecutar_animacion)
        else:
            self.detener_animacion()  # Detener si no hay más frames

    def _actualizar_canvas(self) -> None:
        """
        Actualiza el contenido del canvas para reflejar los cambios de la animación.
        """
        # Limpiar el lienzo para dibujar el siguiente frame
        self.lienzo.delete("all")

        # Obtener el frame actual
        frame_actual = self.lista_frames[self.frame_index]

        # Dibujar cada figura con sus puntos en el frame actual
        for figura, puntos in frame_actual.items():
            figura.puntos = puntos  # Actualizar los puntos de la figura
            figura.dibujar()  # Dibujar la figura en el canvas

    def _generar_peli(self):
        """
        Genera la animación iniciándola desde el principio.
        """
        super()._generar_peli()
        self.iniciar_animacion()

    def _guardar_frame(self):
        """
        Guarda un frame con las figuras actuales y sus puntos.
        
        - Si es la primera vez que una figura aparece, registra su estado inicial.
        - Guarda las posiciones actuales de las figuras en un frame.
        """
        super()._guardar_frame()

        # Crear un diccionario para almacenar las figuras y sus puntos en este frame
        info_frame = {}

        for figura in self._figuras:
            # Registrar cada figura y sus puntos actuales
            info_frame[figura] = figura.puntos.copy()

        # Añadir este frame a la lista de frames
        self.lista_frames.append(info_frame)

        print(f"Frame {len(self.lista_frames)} guardado:")
        for figura, puntos in info_frame.items():
            print(f"  Figura: {figura}, Puntos: {puntos}")