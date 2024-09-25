"""
Archivo: Ventana_menu_canvas.py

Este archivo define la clase VentanaMenuCanvas, que extiende la funcionalidad
de la clase VentanaMenu al anhadir un canvas con capacidades para dibujar.

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

    Anhadie la funcionalidad de dibujar en un canvas utilizando diferentes herramientas.
    Esta clase gestiona eventos del raton para detectar acciones del usuario y realizar el dibujo.

    Atributos heredados:
        width (int): El ancho de la ventana en pixeles.
        height (int): La altura de la ventana en pixeles.
        title (str): El titulo de la ventana.
        ventana (tk.Tk): La instancia de la ventana principal de tkinter.
        color_seleccionado (str): Color seleccionado para dibujar.
        herramienta_seleccionada (AlgoritmoDibujo): Herramienta seleccionada para dibujar.
        tamanho_pincel (int): Grosor de las figuras dibujadas.

    Atributos de instancia:
        _punto_inicial (Punto): Punto de inicio para el dibujo de lineas.
        _punto_final (Punto): Punto final para el dibujo de lineas.
        _figuras (Figura): Almacen de figuras dibujadas en el lienzo.
    """

    def __init__(
        self,
        width: int = Default.VENTANA_WIDTH,
        height: int = Default.VENTANA_HEIGHT,
        title: str = Default.VENTANA_TITLE,
        color_seleccionado: str = Default.COLOR,
        herramienta_seleccionada: AlgoritmoDibujo = Default.HERRAMIENTA,
        tamanho_pincel: int = Default.TAMANHO_DIBUJAR,
    ):
        """
        Constructor de la clase VentanaMenuCanvas.

        Inicializa la ventana con el tamanho y el titulo proporcionados, y ademas configura
        la interaccion del lienzo.

        Args:
            width (int): Ancho de la ventana en pixeles.
            height (int): Alto de la ventana en pixeles.
            title (str): Titulo de la ventana.
            color_seleccionado (str): Color seleccionado para dibujar.
            herramienta_seleccionada (AlgoritmoDibujo): Herramienta seleccionada para dibujar.
            tamanho_pincel (int): Grosor de las figuras dibujadas.
        """

        super().__init__(
            width,
            height,
            title,
            color_seleccionado,
            herramienta_seleccionada,
            tamanho_pincel,
        )

        # Inicializacion de variables para almacenar figuras y puntos para su creacion
        self._punto_inicial = None
        self._punto_final = None
        self._figuras = Figura()

    def crear_lienzo(self) -> tk.Canvas:
        """
        Crea el lienzo de dibujo (Canvas) y configura los eventos del raton para
        permitir la interaccion del usuario.

        Returns:
            tk.Canvas: El Canvas que actua como lienzo.
        """

        lienzo = tk.Canvas(self._ventana, bg="white")
        lienzo.pack(fill=tk.BOTH, expand=True)

        lienzo.bind(Event.ON_LEFT_CLICK, self.iniciar_dibujo)
        lienzo.bind(Event.ON_LEFT_MOVEMENT, self.dibujar_en_movimiento)
        lienzo.bind(Event.ON_LEFT_RELEASE, self.terminar_dibujo)
        return lienzo

    def _crear_contenido_ventana(self) -> None:
        """
        Sobrescribe el metodo de VentanaMenu para anhadir el lienzo a la ventana.
        """

        super()._crear_contenido_ventana()
        self.lienzo = self.crear_lienzo()

    def iniciar_dibujo(self, evento: tk.Event) -> None:
        """
        Inicializa el proceso de dibujo al hacer clic en el lienzo.

        Args:
            evento (tk.Event): Evento generado por el clic del raton.
        """

        self._punto_inicial = Punto(
            evento.x,
            evento.y,
        )

    def dibujar_en_movimiento(self, evento: tk.Event) -> None:
        """
        Dibuja una linea temporal en el lienzo mientras el raton se mueve.

        Args:
            evento (tk.Event): Evento generado por el movimiento del raton.
        """

        x_final = evento.x
        y_final = evento.y
        self.lienzo.delete("linea_temporal")  # Borra la linea temporal previa
        self.lienzo.create_line(
            self._punto_inicial.x,
            self._punto_inicial.y,
            x_final,
            y_final,
            fill=self.color_seleccionado,
            tags="linea_temporal",
        )

    def terminar_dibujo(self, evento: tk.Event) -> None:
        """
        Finaliza el proceso de dibujo y almacena la linea dibujada.

        Args:
            evento (tk.Event): Evento generado al soltar el clic del raton.
        """

        self._punto_final = Punto(
            evento.x,
            evento.y,
        )
        self.lienzo.delete("linea_temporal")  # Borra la linea temporal
        # Almacenar la linea como un vector
        linea = Linea(
            self._punto_inicial,
            self._punto_final,
            self.lienzo,
            self.color_seleccionado,
            self.herramienta_seleccionada,
        )
        self._figuras.anhadir(linea)  # Anhadir la linea al almacen de figuras
        linea.dibujar()  # Dibujar la linea en el lienzo
        self._punto_inicial = None  # Resetear puntos
        self._punto_final = None  # Resetear puntos

    # Getters y Setters
    @property
    def punto_inicial(self) -> Punto:
        """Obtiene el punto inicial del dibujo."""
        return self._punto_inicial

    @punto_inicial.setter
    def punto_inicial(self, valor: Punto) -> None:
        """Establece el punto inicial del dibujo."""
        self._punto_inicial = valor

    @property
    def punto_final(self) -> Punto:
        """Obtiene el punto final del dibujo."""
        return self._punto_final

    @punto_final.setter
    def punto_final(self, valor: Punto) -> None:
        """Establece el punto final del dibujo."""
        self._punto_final = valor

    @property
    def figuras(self) -> Figura:
        """Obtiene el almacen de figuras dibujadas."""
        return self._figuras

    @figuras.setter
    def figuras(self, valor: Figura) -> None:
        """Establece el almacen de figuras dibujadas."""
        self._figuras = valor
