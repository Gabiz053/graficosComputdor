"""
Archivo: VentanaMenuCanvas.py

Este archivo define la clase VentanaMenuCanvas, que extiende la funcionalidad
de la clase VentanaMenu anhadiendo un canvas con funcionalidad para dibujar

Autor: Gabriel Gomez Garcia
Fecha: 21 de septiembre de 2024
"""

import tkinter as tk

from ventana_menu import VentanaMenu
from forma import Linea
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
        self.lineas = []  # Lista para almacenar las líneas dibujadas
        self.punto_inicial = None  # Almacenar el primer punto

    def crear_lienzo(self) -> None:
        """
        Crea el lienzo de dibujo (Canvas) y configura los eventos del raton para
        permitir la interaccion del usuario.

        Returns:
            tk.Label: El Label que actúa como lienzo.
        """
        
        self.imagen = tk.PhotoImage()

        # Crear un Label para mostrar la imagen
        self.label = tk.Label(self._ventana, image=self.imagen)
        self.label.pack(fill=tk.BOTH, expand=True)

        # Asignar eventos para dibujar con el botón izquierdo del ratón
        self.label.bind("<Button-1>", self.iniciar_dibujo)

        return self.label

    def crear_contenido_ventana(self) -> None:
        """
        Sobrescribe el metodo de VentanaMenu para anadir el lienzo a la ventana.
        """
        super().crear_contenido_ventana()
        self.canvas = self.crear_lienzo()

    def iniciar_dibujo(self, event: tk.Event) -> None:
        # Obtener el tamaño del Label
        width = self.label.winfo_width()
        height = self.label.winfo_height()

        # Convertir las coordenadas para que (0, 0) esté en el centro
        x = event.x - width // 2
        y = height // 2 - event.y

        if self.punto_inicial is None:
            self.punto_inicial = (x, y)  # Guardar el primer punto
        else:
            # Guardar el segundo punto y dibujar la línea
            self.dibujar_linea(self.punto_inicial[0], self.punto_inicial[1], x, y)
            self.punto_inicial = None  # Resetear el primer punto

    def dibujar_linea(self, x1, y1, x2, y2) -> None:
        nueva_linea = Linea(x1, y1, x2, y2, self._color_seleccionado, 2)
        self.lineas.append(nueva_linea)
        self.redibujar()  # Redibujar todas las líneas
        self.bresenham(
            x1, y1, x2, y2
        )  # Dibujar la línea usando el algoritmo de Bresenham

    def bresenham(self, x1, y1, x2, y2) -> None:
        """Dibuja una línea entre (x1, y1) y (x2, y2) usando el algoritmo de Bresenham."""
        dx = x2 - x1
        dy = y2 - y1
        sx = 1 if dx > 0 else -1
        sy = 1 if dy > 0 else -1
        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            err = dx / 2.0
            while x1 != x2:
                # Ajustar la posición
                self.imagen.put(
                    "black",
                    (
                        x1 + self.label.winfo_width() // 2,
                        self.label.winfo_height() // 2 - y1,
                    ),
                )
                err -= dy
                if err < 0:
                    y1 += sy
                    err += dx
                x1 += sx
        else:
            err = dy / 2.0
            while y1 != y2:
                # Ajustar la posición
                self.imagen.put(
                    "black",
                    (
                        x1 + self.label.winfo_width() // 2,
                        self.label.winfo_height() // 2 - y1,
                    ),
                )
                err -= dx
                if err < 0:
                    x1 += sx
                    err += dy
                y1 += sy

    def redibujar(self) -> None:
        # Limpiar el lienzo simulado
        self.imagen.put(
            self._color_seleccionado, to=(0, 0, self.label.winfo_width(), self.label.winfo_height())
        )

        # Dibujar cada línea almacenada
        for linea in self.lineas:
            self.bresenham(linea.x1, linea.y1, linea.x2, linea.y2)

        # Actualizar la imagen en el Label
        self.label.config(image=self.imagen)
