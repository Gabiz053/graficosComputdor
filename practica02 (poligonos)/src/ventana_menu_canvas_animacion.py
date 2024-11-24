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

    Esta clase proporciona métodos para iniciar, detener, pausar, y continuar
    animaciones en el canvas, incluyendo bucles infinitos si se activa.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Constructor de la clase VentanaMenuCanvasAnimacion.

        Args:
            *args: Argumentos adicionales para VentanaMenuCanvas.
            **kwargs: Argumentos adicionales para VentanaMenuCanvas.
        """
        super().__init__(*args, **kwargs)
        self.animacion_activa = False  # Indica si la animación está activa
        self.lista_frames: list = []  # Lista de frames para la animación
        self.frame_index = 0  # Índice del frame actual
        self.delay = 2  # Retraso entre frames (2 FPS por defecto)

    def iniciar_animacion(self) -> None:
        """
        Inicia o reinicia la animación en el lienzo.
        """
        if not self.animacion_activa and self.lista_frames:
            self.animacion_activa = True
            if self.frame_index >= len(self.lista_frames):  # Si se llegó al final
                self.frame_index = 0  # Reiniciar desde el principio
            self.lienzo.delete("all")  # Limpiar el lienzo
            self.actualizar_fps()
            self._ejecutar_animacion()

    def _pausar_animacion(self) -> None:
        """
        Pausa la animación en el lienzo.
        """
        super()._pausar_animacion()
        self.animacion_activa = False

    def _reanudar_animacion(self) -> None:
        """
        Reanuda la animación desde el frame actual.
        """
        super()._reanudar_animacion()
        if not self.animacion_activa:
            self.animacion_activa = True
            self.actualizar_fps()
            self._ejecutar_animacion()

    def detener_animacion(self) -> None:
        """
        Detiene completamente la animación y reinicia el índice de frame.
        """
        self.animacion_activa = False
        self.frame_index = 0
        print("Animación detenida")

    def _ejecutar_animacion(self) -> None:
        """
        Método privado que ejecuta la lógica de la animación.
        Este método se llamará repetidamente mientras la animación esté activa.
        """
        if self.animacion_activa:
            self._actualizar_canvas()  # Dibujar el frame actual
            self.frame_index += 1  # Pasar al siguiente frame

            if self.frame_index >= len(self.lista_frames):  # Fin de frames
                self.loop_activo = bool(
                    self.bucle_animacion.get()
                )  # Obtener valor del checkbox
                # print(self.loop_activo)
                if self.loop_activo:  # Si el bucle está activo
                    self.actualizar_fps()
                    self.frame_index = 0  # Reiniciar
                else:
                    self.detener_animacion()  # Detener la animación
                    return

            # Programar la siguiente ejecución de la animación
            self.ventana.after(self.delay, self._ejecutar_animacion)

    def _actualizar_canvas(self) -> None:
        """
        Actualiza el contenido del canvas para reflejar los cambios de la animación.
        """
        # Limpiar el lienzo para dibujar el siguiente frame
        self.lienzo.delete("all")

        # Obtener el frame actual
        frame_actual = self.lista_frames[self.frame_index]

        # Dibujar cada figura con sus puntos en el frame actual
        for figura, (puntos, color) in frame_actual.items():
            figura.puntos = puntos  # Actualizar los puntos de la figura
            figura.color = color
            figura.dibujar()  # Dibujar la figura en el canvas

    def _guardar_frame(self):
        """
        Guarda un frame con las figuras actuales y sus puntos.
        """
        super()._guardar_frame()

        # Crear un diccionario para almacenar las figuras y sus puntos en este frame
        info_frame = {}

        for figura in self._figuras:
            # Registrar cada figura y sus puntos actuales
            info_frame[figura] = (figura.puntos.copy(), figura.color)

        # Añadir este frame a la lista de frames
        self.lista_frames.append(info_frame)

        print(f"Frame {len(self.lista_frames)} guardado:")
        for figura, (puntos, color) in info_frame.items():
            print(f"  Figura: {figura}, Puntos: {puntos}")

    def _generar_peli(self):
        """
        Genera la animación iniciándola desde el principio.
        """
        super()._generar_peli()
        self.iniciar_animacion()

    def actualizar_fps(self) -> None:
        """
        Actualiza el delay de la animación basado en los FPS ingresados.
        """
        try:
            fps = float(self.input_fps.get())
            if fps > 0:
                self.delay = int(1000 / fps)  # Convertir FPS a milisegundos
                # print(f"FPS actualizado: {fps}")
        except ValueError:
            print("FPS inválido. Usando el valor anterior.")
