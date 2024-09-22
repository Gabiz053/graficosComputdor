"""
Archivo: VentanaMenuCanvas.py

Este archivo define la clase VentanaMenuCanvas, la cual extiende la funcionalidad de la clase VentanaMenu
anadiendo un canvas con funcionalidad para dibujar

Autor: Gabriel Gomez Garcia
Fecha: 17 de septiembre de 2024
"""

import tkinter as tk
from VentanaMenu import VentanaMenu
from constantes import Default, Event, Herramienta, Color
from Forma import Linea


class VentanaMenuCanvas(VentanaMenu):
    """
    Clase que extiende VentanaMenu para permitir la interaccion en un lienzo.

    Anade la funcionalidad de dibujar en un canvas utilizando diferentes herramientas
    como lapiz o borrador. Esta clase gestiona eventos del raton para detectar acciones
    del usuario y dibujar.

    Atributos heredados:
        width (int): El ancho de la ventana en pixeles.
        height (int): La altura de la ventana en pixeles.
        title (str): El titulo de la ventana.
        ventana (tk.Tk): La instancia de la ventana principal de tkinter.
        herramientaSeleccionada (str): Herramienta seleccionada para dibujar (lapiz o borrador).
    """

    def __init__(self, width: int, height: int, title: str, color: str):
        """
        Constructor de la clase VentanaMenuCanvas.

        Inicializa la ventana con el tamano y el titulo proporcionados, y ademas configura
        la interaccion del lienzo. El color de fondo del canvas tambien se establece aqui.

        Args:
            width (int): Ancho de la ventana en pixeles.
            height (int): Alto de la ventana en pixeles.
            title (str): Titulo de la ventana.
            color (str): Color de fondo del canvas donde se dibuja.
        """
        super().__init__(width, height, title)
        self.color = color  # Establece el color de fondo del lienzo
        self.lineas = []  # Lista para almacenar las líneas dibujadas
        self.punto_inicial = None  # Almacenar el primer punto

    def crearLienzo(self):
        """
        Crea el lienzo de dibujo (Canvas) y configura los eventos del raton para
        permitir la interaccion del usuario.

        Returns:
            tk.Label: El Label que actúa como lienzo.
        """
        # Crear el lienzo simulado
        self.imagen = tk.PhotoImage()

        # Crear un Label para mostrar la imagen
        self.label = tk.Label(self.ventana, image=self.imagen)
        self.label.pack(fill=tk.BOTH, expand=True)

        # Asignar eventos para dibujar con el botón izquierdo del ratón
        self.label.bind("<Button-1>", self.iniciarDibujo)

        return self.label

    def crearContenidoVentana(self):
        """
        Sobrescribe el metodo de VentanaMenu para anadir el lienzo a la ventana.
        """
        super().crearContenidoVentana()
        self.canvas = self.crearLienzo()

    def iniciarDibujo(self, event: tk.Event) -> None:
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
            self.dibujarLinea(self.punto_inicial[0], self.punto_inicial[1], x, y)
            self.punto_inicial = None  # Resetear el primer punto
            
    def dibujarLinea(self, x1, y1, x2, y2):
        nueva_linea = Linea(x1, y1, x2, y2, self.color, 2)
        self.lineas.append(nueva_linea)
        self.redibujar()  # Redibujar todas las líneas
        self.bresenham(x1, y1, x2, y2)  # Dibujar la línea usando el algoritmo de Bresenham

    def bresenham(self, x1, y1, x2, y2):
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
                self.imagen.put("black", (x1 + self.label.winfo_width() // 2, self.label.winfo_height() // 2 - y1))
                err -= dy
                if err < 0:
                    y1 += sy
                    err += dx
                x1 += sx
        else:
            err = dy / 2.0
            while y1 != y2:
                # Ajustar la posición
                self.imagen.put("black", (x1 + self.label.winfo_width() // 2, self.label.winfo_height() // 2 - y1))
                err -= dx
                if err < 0:
                    x1 += sx
                    err += dy
                y1 += sy

    def redibujar(self):
        # Limpiar el lienzo simulado
        self.imagen.put(self.color, to=(0, 0, self.label.winfo_width(), self.label.winfo_height()))

        # Dibujar cada línea almacenada
        for linea in self.lineas:
            self.bresenham(linea.x1, linea.y1, linea.x2, linea.y2)

        # Actualizar la imagen en el Label
        self.label.config(image=self.imagen)
