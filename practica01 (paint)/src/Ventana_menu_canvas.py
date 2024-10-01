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
from forma import *


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
        self.nivel_zoom = Default.ZOOM
        
        # Almacenar líneas
        self.linea_seleccionada = None  # Línea seleccionada
        self.offset_x = 0  # Desplazamiento en x
        self.offset_y = 0  # Desplazamiento en y
        
    def crear_lienzo(self) -> tk.Canvas:
        """
        Crea el lienzo de dibujo (Canvas) y configura los eventos del raton para
        permitir la interaccion del usuario.

        Returns:
            tk.Canvas: El Canvas que actua como lienzo.
        """

        lienzo = tk.Canvas(self._ventana, bg="white")
        lienzo.pack(fill=tk.BOTH, expand=True)
        lienzo.config(scrollregion=lienzo.bbox("all"))  # Asegúrate de que el área de desplazamiento incluya todos los elementos

        lienzo.bind(Event.ON_LEFT_CLICK, self.iniciar_dibujo)
        lienzo.bind(Event.ON_LEFT_MOVEMENT, self.dibujar_en_movimiento)
        lienzo.bind(Event.ON_LEFT_RELEASE, self.terminar_dibujo)
        
        lienzo.bind(Event.ON_RIGHT_CLICK, self.seleccionar_linea)  # Click derecho para seleccionar
        # lienzo.bind(Event.ON_RIGHT_MOVEMENT, self.mover_linea)  # Mover línea mientras arrastra el clic derecho
        # lienzo.bind(Event.ON_RIGHT_RELEASE, self.finalizar_mover_linea)  # Finalizar movimiento   
        
        lienzo.bind(Event.ON_MOUSE_WHEEL, self.zoom)
        
        return lienzo
    
    
    def seleccionar_linea(self, event):
        """Selecciona una línea si el cursor está cerca de ella."""
        self.linea_seleccionada = None
        for linea in self.figuras:
            if isinstance(linea, Linea):
                # Verifica si el cursor está cerca de la línea (en un rango de 10 píxeles)
                if self.es_cercano_a_linea(event.x, event.y, linea):
                    self.linea_seleccionada = linea
                    print(self.lienzo.coords(linea))
                    # print(f"ME HAN SELECCIONADO {linea._punto_final}")
                    # # Calcular el desplazamiento inicial
                    # self.offset_x = event.x - linea.punto_inicial.x  # Desplazamiento desde el primer punto de la línea
                    # self.offset_y = event.y - linea.punto_inicial.y  # Desplazamiento desde el segundo punto de la línea
                    break
                
    def es_cercano_a_linea(self, x, y, linea: Linea):
        """Verifica si el punto (x, y) está cerca de la línea definida por coords."""
        x1 = linea.punto_inicial.x
        y1 = linea.punto_inicial.y
        x2 = linea.punto_final.x
        y2 = linea.punto_final.y
        # Distancia mínima al segmento
        distancia_minima = 10  
        return (min(abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) /
                       ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5, 
                       abs(y - y1) + abs(y - y2) + abs(x - x1) + abs(x - x2)) < distancia_minima)

    def mover_linea(self, event):
        """Mueve la línea seleccionada con el ratón."""
        if self.linea_seleccionada:

            # Calcular el nuevo punto de inicio y final usando el desplazamiento
            new_x1 = event.x - self.offset_x
            new_y1 = event.y - self.offset_y

            # Mover la línea a las nuevas coordenadas
            self.linea_seleccionada.mover(new_x1,new_y1)
            
    def finalizar_mover_linea(self, event):
        """Finaliza el movimiento de la línea."""
        self.linea_seleccionada = None
            
    def zoom(self, evento: tk.Event) -> None:
        # Ajustar el nivel de zoom
        scale_factor = Default.AMPLIAR if evento.delta > 0 else Default.REDUCIR  # Cambia la escala según el movimiento
        self.nivel_zoom *= scale_factor
        
        # Cambia el tamaño del canvas basado en el nivel de zoom
        self.lienzo.scale("all", evento.x, evento.y, scale_factor, scale_factor)
        
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
            self.tamanho_pincel,
        )
        self._figuras.anhadir(linea)  # Anhadir la linea al almacen de figuras
        linea.dibujar()  # Dibujar la linea en el lienzo
        self._punto_inicial = None  # Resetear puntos
        self._punto_final = None  # Resetear puntos

    def seleccionar_borrar_todo(self) -> None:
        """Borra todo el contenido del lienzo."""
        super().seleccionar_borrar_todo()
        self.lienzo.delete("all")
        self._figuras.eliminar_todo()
        
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




    # def dibujar_rejilla(self):
    #     """Dibuja una rejilla en el lienzo."""
    #     for i in range(0, 5000, 50):
    #         self.lienzo.create_line(i, 0, i, 720, fill='gray')  # Líneas verticales
    #     for i in range(0, 5000, 50):
    #         self.lienzo.create_line(0, i, 1280, i, fill='gray')  # Líneas horizontales