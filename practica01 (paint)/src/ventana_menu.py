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
from algoritmos_dibujo import *
from constantes import MenuVen, Texto, Herramienta, Default


class VentanaMenu(Ventana):
    """
    Clase que representa una ventana con un menu desplegable interactivo.

    Hereda de la clase abstracta Ventana, anadiendo un menu superior y
    una seccion de herramientas para interactuar con el lienzo.

    Atributos heredados:
        _width (int): El ancho de la ventana en pixeles.
        _height (int): La altura de la ventana en pixeles.
        _title (str): El titulo de la ventana.
        _ventana (tk.Tk): La instancia de la ventana principal de tkinter.

    Atributos de instancia:
        _color_seleccionado (str): color seleccionado para dibujar.
        _herramienta_seleccionada (str): herramienta seleccionada para dibujar.
        _tamanho_pincel (int): grosor de las figuras dibujadas.
    """

    def __init__(
        self,
        width: int = Default.VENTANA_WIDTH,
        height: int = Default.VENTANA_HEIGHT,
        title: str = Default.VENTANA_TITLE,
        color_seleccionado: str = Default.COLOR,
        herramienta_seleccionada: AlgoritmoDibujo = Default.HERRAMIENTA,
        tamanho_pincel: int = Default.TAMANHO_DIBUJAR,
    ) -> None:
        """
        Inicializa la ventana con las dimensiones y el titulo proporcionados.

        Args:
            width (int): Ancho de la ventana en pixeles.
            height (int): Alto de la ventana en pixeles.
            title (str): Titulo de la ventana.
            color_seleccionado (str): Color seleccionado para dibujar.
            herramienta_seleccionada (AlgoritmoDibujo): Herramienta seleccionada para dibujar.
            tamanho_pincel (int): grosor de las figuras dibujadas.
        """
        super().__init__(width, height, title)
        self._color_seleccionado = color_seleccionado
        self._herramienta_seleccionada = herramienta_seleccionada
        self._tamanho_pincel = tamanho_pincel

    def _crear_contenido_ventana(self) -> None:
        """
        Configura el contenido de la ventana anadiendo un menu de opciones.

        Este metodo sobrescribe la funcion abstracta heredada para implementar
        un menu superior y una barra de herramientas
        """
        self._crear_menu_superior()
        self._crear_menu_herramientas()

    def _crear_menu_superior(self) -> None:
        """Crea el menu superior con secciones Archivo y Ayuda."""
        menu_barra = Menu(self._ventana)

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
        menu_archivo.add_command(
            label=MenuVen.ARCHIVO_SALIR, command=self._ventana.quit
        )

        # Menu Ayuda
        menu_ayuda = Menu(menu_barra, tearoff=0)
        menu_barra.add_cascade(label=MenuVen.AYUDA, menu=menu_ayuda)
        menu_ayuda.add_command(
            label=MenuVen.AYUDA_ACERCA, command=self.mostrar_acerca_de
        )

        self._ventana.config(menu=menu_barra)

    def _crear_menu_herramientas(self) -> None:
        """Crea el menu de herramientas con opciones para el lienzo."""
        self._cambiar_tema(Default.MENU_TEMA)

        menu_herramientas = tk.Frame(self._ventana, bg=Default.BG_MENU)
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

        # Boton Elegir Color
        btn_elegir_color = ttk.Button(
            menu_herramientas,
            text=MenuVen.BOTON_COLORCHOSER,
            command=self.seleccionar_elegir_color,
        )
        btn_elegir_color.grid(row=0, column=4, padx=5, pady=5)

        # Separador antes de elegir tamanho
        separador_2 = ttk.Separator(menu_herramientas, orient="vertical")
        separador_2.grid(row=0, column=5, rowspan=2, sticky="ns", padx=10)

        # Control de tamaño de pincel
        self._label_tamanho_actual = tk.Label(
            menu_herramientas,
            text=f"Tamaño actual: {self._tamanho_pincel}",
            bg=Default.BG_MENU,
        )
        self._label_tamanho_actual.grid(row=0, column=7, padx=5, pady=5)

        scale_tamanho_pincel = ttk.Scale(
            menu_herramientas,
            from_=1,
            to=50,
            orient="horizontal",
            command=self._actualizar_tamanho_pincel,
        )
        scale_tamanho_pincel.set(self._tamanho_pincel)
        scale_tamanho_pincel.grid(row=0, column=8, padx=5, pady=5)

        # Separador antes del boton Borrar
        separador_3 = ttk.Separator(menu_herramientas, orient="vertical")
        separador_3.grid(row=0, column=10, rowspan=2, sticky="ns", padx=10)

        # Botones de otras herramientas
        btn_borrador = ttk.Button(
            menu_herramientas,
            text=MenuVen.BOTON_BORRADOR,
            command=self.seleccionar_borrador,
        )
        btn_borrador.grid(row=0, column=11, padx=5, pady=5)

        btn_borrar_todo = ttk.Button(
            menu_herramientas,
            text=MenuVen.BOTON_BORRAR_TODO,
            command=self.seleccionar_borrar_todo,
        )
        btn_borrar_todo.grid(row=0, column=12, padx=5, pady=5)

    def _actualizar_tamanho_pincel(self, valor: float) -> None:
        """Actualiza el tamaño del pincel y refleja el valor en la interfaz."""
        self._tamanho_pincel = int(float(valor))
        self._label_tamanho_actual.config(text=f"Tamaño actual: {self._tamanho_pincel}")

    def _cambiar_tema(self, nuevo_tema: str) -> None:
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
        self._herramienta_seleccionada = Herramienta.LAPIZ_1
        print(Texto.LAPIZ1)

    def seleccionar_lapiz_2(self) -> None:
        """Selecciona la herramienta 'Lapiz 2'."""
        self._herramienta_seleccionada = Herramienta.LAPIZ_2
        print(Texto.LAPIZ2)

    def seleccionar_lapiz_3(self) -> None:
        """Selecciona la herramienta 'Lapiz 3'."""
        self._herramienta_seleccionada = Herramienta.LAPIZ_3
        print(Texto.LAPIZ3)

    def seleccionar_borrador(self) -> None:
        """Selecciona la herramienta 'Borrador' para borrar en el lienzo."""
        print(Texto.BORRADOR)

    def seleccionar_borrar_todo(self) -> None:
        """Borra todo el contenido del lienzo."""
        print(Texto.BORRAR_TODO)

    def seleccionar_elegir_color(self) -> None:
        """Permite seleccionar un color para dibujar."""
        color = colorchooser.askcolor(title="Elegir color")
        if color[1]:
            self._color_seleccionado = color[1]
            print(f"Color seleccionado: {self._color_seleccionado}")

    ########### getters y setters ##############
    @property
    def herramienta_seleccionada(self) -> Herramienta:
        """Obtiene la herramienta seleccionada."""
        return self._herramienta_seleccionada

    @herramienta_seleccionada.setter
    def herramienta_seleccionada(self, valor: Herramienta) -> None:
        """Establece la herramienta seleccionada."""
        self._herramienta_seleccionada = valor

    @property
    def color_seleccionado(self) -> str:
        """Obtiene el color seleccionado."""
        return self._color_seleccionado

    @color_seleccionado.setter
    def color_seleccionado(self, valor: str) -> None:
        """Establece el color seleccionado."""
        self._color_seleccionado = valor

    @property
    def tamanho_pincel(self) -> int:
        """Obtiene el tamanho del pincel."""
        return self._tamanho_pincel

    @tamanho_pincel.setter
    def tamanho_pincel(self, valor: int) -> None:
        """Establece el tamanho del pincel."""
        self._tamanho_pincel = valor
