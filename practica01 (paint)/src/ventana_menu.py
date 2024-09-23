"""
Archivo: ventana_menu.py

Este archivo define la clase VentanaMenu que extiende la funcionalidad
de la clase abstracta Ventana. Crea una ventana con un menu para la
aplicacion grafica.

Autor: Gabriel Gomez Garcia
Fecha: 21 de septiembre de 2024
"""

import tkinter as tk
from tkinter import Menu, ttk, colorchooser

from ventana import Ventana
from constantes import MenuVen, Texto, Herramienta, Default


class VentanaMenu(Ventana):
    """
    Clase que representa una ventana con un menu desplegable interactivo.

    Hereda de la clase abstracta Ventana, añadiendo un menu superior y
    una seccion de herramientas para interactuar con el lienzo.

    Atributos heredados:
        width (int): El ancho de la ventana en pixeles.
        height (int): La altura de la ventana en pixeles.
        title (str): El titulo de la ventana.
        ventana (tk.Tk): La instancia de la ventana principal de tkinter.

    Atributos de instancia:
        herramienta_seleccionada (str): herramienta seleccionada para dibujar.
        color_seleccionado (str): color seleccionado para dibujar.
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
        Inicializa la ventana con las dimensiones y el titulo proporcionados.

        Args:
            width (int): Ancho de la ventana en pixeles.
            height (int): Alto de la ventana en pixeles.
            title (str): Titulo de la ventana.
            herramientaSeleccionada (str): Herramienta seleccionada para dibujar.
            colorSeleccionado (str): Color seleccionado para dibujar.
        """
        super().__init__(width, height, title)
        self.herramientaSeleccionada = herramientaSeleccionada
        self.colorSeleccionado = colorSeleccionado

    def _crear_contenido_ventana(self) -> None:
        """
        Configura el contenido de la ventana añadiendo un menu de opciones.

        Este metodo sobrescribe la funcion abstracta heredada para implementar
        un menu superior y una barra de herramientas
        """
        self._crear_menu_superior()
        self._crear_menu_herramientas()

    def _crear_menu_superior(self) -> None:
        """Crea el menu superior con secciones Archivo y Ayuda."""
        menu_barra = Menu(self.ventana)

        # Menu Archivo
        menu_archivo = Menu(menu_barra, tearoff=0)
        menu_barra.add_cascade(label=MenuVen.ARCHIVO, menu=menu_archivo)
        menu_archivo.add_command(
            label=MenuVen.ARCHIVO_NUEVO, command=self.nuevo_archivo
        )
        menu_archivo.add_command(
            label=MenuVen.ARCHIVO_ABRIR, command=self.abrir_archivo
        )
        menu_archivo.add_command(
            label=MenuVen.ARCHIVO_GUARDAR, command=self.guardar_archivo
        )
        menu_archivo.add_separator()
        menu_archivo.add_command(label=MenuVen.ARCHIVO_SALIR, command=self.ventana.quit)

        # Menu Ayuda
        menu_ayuda = Menu(menu_barra, tearoff=0)
        menu_barra.add_cascade(label=MenuVen.AYUDA, menu=menu_ayuda)
        menu_ayuda.add_command(
            label=MenuVen.AYUDA_ACERCA, command=self.mostrar_acerca_de
        )

        self.ventana.config(menu=menu_barra)

    def _crear_menu_herramientas(self) -> None:
        """Crea el menu de herramientas con opciones para el lienzo."""
        self._cambiar_tema(Default.MENU_TEMA)

        menu_herramientas = tk.Frame(self.ventana, bg=Default.BG_MENU)
        menu_herramientas.pack(side=tk.TOP, fill=tk.X)

        # Botones de lapices
        btn_lapiz_1 = ttk.Button(
            menu_herramientas,
            text=MenuVen.BOTON_LAPIZ_1,
            command=self.seleccionar_lapiz_1,
        )
        btn_lapiz_1.grid(row=0, column=0, padx=5, pady=5)

        btn_lapiz_2 = ttk.Button(
            menu_herramientas,
            text=MenuVen.BOTON_LAPIZ_2,
            command=self.seleccionar_lapiz_2,
        )
        btn_lapiz_2.grid(row=0, column=1, padx=5, pady=5)

        btn_lapiz_3 = ttk.Button(
            menu_herramientas,
            text=MenuVen.BOTON_LAPIZ_3,
            command=self.seleccionar_lapiz_3,
        )
        btn_lapiz_3.grid(row=0, column=2, padx=5, pady=5)

        # Separador entre herramientas
        separador_1 = ttk.Separator(menu_herramientas, orient="vertical")
        separador_1.grid(row=0, column=3, rowspan=2, sticky="ns", padx=10)

        # Botones de otras herramientas
        btn_borrador = ttk.Button(
            menu_herramientas,
            text=MenuVen.BOTON_BORRADOR,
            command=self.seleccionar_borrador,
        )
        btn_borrador.grid(row=0, column=4, padx=5, pady=5)

        btn_borrar_todo = ttk.Button(
            menu_herramientas,
            text=MenuVen.BOTON_BORRAR_TODO,
            command=self.seleccionar_borrar_todo,
        )
        btn_borrar_todo.grid(row=0, column=5, padx=5, pady=5)

        # Separador antes del boton Elegir Color
        separador_2 = ttk.Separator(menu_herramientas, orient="vertical")
        separador_2.grid(row=0, column=6, rowspan=2, sticky="ns", padx=10)

        # Boton Elegir Color
        btn_elegir_color = ttk.Button(
            menu_herramientas,
            text=MenuVen.BOTON_COLORCHOSER,
            command=self.seleccionar_elegir_color,
        )
        btn_elegir_color.grid(row=0, column=7, padx=5, pady=5)

    def _cambiar_tema(self, nuevo_tema) -> None:
        """Cambia el tema de la aplicacion."""
        estilo = ttk.Style()
        estilo.theme_use(nuevo_tema)

    def nuevo_archivo(self) -> None:
        """Abre un nuevo archivo o limpia el lienzo."""
        # TODO: Implementar funcionalidad para limpiar el lienzo o iniciar un nuevo archivo.

        print(Texto.NUEVO_ARCHIVO)

    def abrir_archivo(self) -> None:
        """Abre un archivo existente."""
        # TODO: Implementar funcionalidad para abrir y cargar un archivo en el lienzo.
        # Esta funcion debe abrir un cuadro de dialogo para seleccionar y cargar un archivo.

        print(Texto.ABRIR_ARCHIVO)

    def guardar_archivo(self) -> None:
        """Guarda el estado actual del proyecto."""
        # TODO: Implementar funcionalidad para guardar el contenido del lienzo en un archivo.

        print(Texto.GUARDAR_ARCHIVO)

    def mostrar_acerca_de(self) -> None:
        """Muestra informacion sobre la aplicacion."""
        # TODO: Implementar funcionalidad para mostrar un cuadro de dialogo con la informacion de la aplicacion.

        print(Texto.ACERCA_DE)

    def seleccionar_lapiz_1(self) -> None:
        """Selecciona la herramienta 'Lapiz 1'."""
        self.herramientaSeleccionada = Herramienta.LAPIZ_1
        print(Texto.LAPIZ1)

    def seleccionar_lapiz_2(self) -> None:
        """Selecciona la herramienta 'Lapiz 2'."""
        self.herramientaSeleccionada = Herramienta.LAPIZ_2
        print(Texto.LAPIZ2)

    def seleccionar_lapiz_3(self) -> None:
        """Selecciona la herramienta 'Lapiz 3'."""
        self.herramientaSeleccionada = Herramienta.LAPIZ_3
        print(Texto.LAPIZ3)

    def seleccionar_borrador(self) -> None:
        """Selecciona la herramienta 'Borrador' para borrar trazos en el lienzo."""
        # TODO: Implementar funcionalidad para el uso del borrador en el lienzo.

        print(Texto.BORRADOR)

    def seleccionar_borrar_todo(self) -> None:
        """
        Selecciona la herramienta 'Borrar todo' para limpiar el lienzo.
        """
        # TODO: Implementar funcionalidad para borrar todo el contenido del lienzo.
        # Se debe preguntar antes de limpiar todo el lienzo.

        print(Texto.BORRAR_TODO)

    def seleccionar_elegir_color(self) -> None:
        """Abre un menu para elegir el color del trazado."""
        print(Texto.COLORCHOSER)
        color = colorchooser.askcolor(title=Texto.COLORCHOSER_TITULO)[1]
        if color:
            self.colorSeleccionado = color
            print(Texto.COLORCHOSER_SELECCION, color)
