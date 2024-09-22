"""
Archivo: VentanaMenu.py

Este archivo define la clase VentanaMenu, la cual extiende la funcionalidad de la clase abstracta Ventana.
La clase VentanaMenu crea una ventana con un menu en una aplicacion de interfaz grafica.

Autor: Gabriel Gomez Garcia
Fecha: 14 de septiembre de 2024
"""

import tkinter as tk
from tkinter import Menu, ttk, colorchooser
from Ventana import Ventana
from constantes import MenuVen, Texto, Herramienta, Default


class VentanaMenu(Ventana):
    """
    Clase que representa una ventana con un menu desplegable interactivo.

    Esta clase extiende de la clase abstracta Ventana y anade un menu superior y una seccion
    de herramientas con opciones para interactuar con el lienzo.

    Atributos heredados:
        width (int): El ancho de la ventana en pixeles.
        height (int): La altura de la ventana en pixeles.
        title (str): El titulo de la ventana.
        ventana (tk.Tk): La instancia de la ventana principal de tkinter.

    Atributos:
        herramientaSeleccionada (str): herramienta seleccionada para dibujar (lapiz por defecto).
    """

    def __init__(self, width: int, height: int, title: str):
        """
        Constructor de la clase VentanaMenu.

        Inicializa la ventana con las dimensiones y el titulo proporcionados, y
        prepara el contenido.

        Args:
            width (int): Ancho de la ventana en pixeles.
            height (int): Alto de la ventana en pixeles.
            title (str): Titulo de la ventana.
        """
        super().__init__(width, height, title)
        self.herramientaSeleccionada = Default.HERRAMIENTA  # Valor por defecto
        self.colorSeleccionado = Default.COLOR

    def crearContenidoVentana(self):
        """
        Configura el contenido de la ventana, anadiendo un menu de opciones y un lienzo.

        Este metodo sobrescribe la funcion abstracta heredada para implementar un menu superior y
        una barra de herramientas

        Args:
            ventana (tk.Tk): La instancia de tkinter donde se agrega el contenido.
        """
        self.crearMenuSuperior()
        self.crearMenuHerramientas()

    def crearMenuSuperior(self):
        # Crear la barra de menu superior con opciones de archivo
        menuBarra = Menu(self.ventana)

        # Crear el submenu 'Archivo' y anadirlo a la barra de menu
        menuBarraArchivo = Menu(menuBarra, tearoff=0)
        menuBarra.add_cascade(label=MenuVen.ARCHIVO, menu=menuBarraArchivo)

        # Opciones del menu 'Archivo'
        menuBarraArchivo.add_command(
            label=MenuVen.ARCHIVO_NUEVO, command=self.nuevoArchivo
        )
        menuBarraArchivo.add_command(
            label=MenuVen.ARCHIVO_ABRIR, command=self.abrirArchivo
        )
        menuBarraArchivo.add_command(
            label=MenuVen.ARCHIVO_GUARDAR, command=self.guardarArchivo
        )
        menuBarraArchivo.add_separator()
        menuBarraArchivo.add_command(
            label=MenuVen.ARCHIVO_SALIR, command=self.ventana.quit
        )

        # Crear el submenu 'Ayuda' y anadirlo a la barra de menu
        menuBarraAyuda = Menu(menuBarra, tearoff=0)
        menuBarra.add_cascade(label=MenuVen.AYUDA, menu=menuBarraAyuda)

        # Opcion del menu 'Ayuda'
        menuBarraAyuda.add_command(
            label=MenuVen.AYUDA_ACERCA, command=self.mostrarAcercaDe
        )

        # Asignar la barra de menu a la ventana
        self.ventana.config(menu=menuBarra)

    def crearMenuHerramientas(self):

        ## cambiamos a un tema para que se vea mas bonito
        self.cambiar_tema(Default.MENU_TEMA)

        menuHerramientas = tk.Frame(self.ventana, bg=Default.BG_MENU)
        menuHerramientas.pack(side=tk.TOP, fill=tk.X)

        # Botones de lápices
        btn_lapiz_1 = ttk.Button(
            menuHerramientas, text=MenuVen.BOTON_LAPIZ1, command=self.seleccionarLapiz1
        )
        btn_lapiz_1.grid(row=0, column=0, padx=5, pady=5)

        btn_lapiz_2 = ttk.Button(
            menuHerramientas, text=MenuVen.BOTON_LAPIZ2, command=self.seleccionarLapiz2
        )
        btn_lapiz_2.grid(row=0, column=1, padx=5, pady=5)

        btn_lapiz_3 = ttk.Button(
            menuHerramientas, text=MenuVen.BOTON_LAPIZ3, command=self.seleccionarLapiz3
        )
        btn_lapiz_3.grid(row=0, column=2, padx=5, pady=5)

        # Barra separadora entre las herramientas de lápiz y las demás herramientas
        separador1 = ttk.Separator(menuHerramientas, orient="vertical")
        separador1.grid(row=0, column=3, rowspan=2, sticky="ns", padx=10)

        # Botones de otras herramientas
        btn_borrador = ttk.Button(
            menuHerramientas,
            text=MenuVen.BOTON_BORRADOR,
            command=self.seleccionarBorrador,
        )
        btn_borrador.grid(row=0, column=4, padx=5, pady=5)

        btn_borrar_todo = ttk.Button(
            menuHerramientas,
            text=MenuVen.BOTON_BORRARTODO,
            command=self.seleccionarBorrarTodo,
        )
        btn_borrar_todo.grid(row=0, column=5, padx=5, pady=5)

        # Separador antes del botón "Elegir Color"
        separador2 = ttk.Separator(menuHerramientas, orient="vertical")
        separador2.grid(row=0, column=6, rowspan=2, sticky="ns", padx=10)

        # Botón "Elegir Color"
        btn_elegir_color = ttk.Button(
            menuHerramientas,
            text=MenuVen.BOTON_COLORCHOSER,
            command=self.seleccionarElegirColor,
        )
        btn_elegir_color.grid(row=0, column=7, padx=5, pady=5)

        # Separador después del botón "Elegir Color"
        separador3 = ttk.Separator(menuHerramientas, orient="vertical")
        separador3.grid(row=0, column=8, rowspan=2, sticky="ns", padx=10)

    def cambiar_tema(self, nuevoTema):
        # Crear un estilo
        estilo = ttk.Style()
        """Cambia el tema de la aplicación."""
        estilo.theme_use(nuevoTema)

    def nuevoArchivo(self):
        """
        Accion que se ejecuta al seleccionar la opcion 'Nuevo' en el menu.

        Esta funcion podria abrir un nuevo archivo o limpiar el lienzo para un nuevo proyecto.
        """
        print(Texto.NUEVOARCHIVO)

    def abrirArchivo(self):
        """
        Accion que se ejecuta al seleccionar la opcion 'Abrir' en el menu.

        Esta funcion podria abrir un cuadro de dialogo para seleccionar y cargar un archivo.
        """
        print(Texto.ABRIRARCHIVO)

    def guardarArchivo(self):
        """
        Accion que se ejecuta al seleccionar la opcion 'Guardar' en el menu.

        Esta funcion podria guardar el estado actual del lienzo o proyecto en un archivo.
        """
        print(Texto.GUARDARARCHIVO)

    def mostrarAcercaDe(self):
        """
        Muestra una ventana emergente con informacion sobre la aplicacion.

        Esta funcion puede mostrar una descripcion breve o los detalles del autor y la version de la aplicacion.
        """
        print(Texto.ACERCADE)

    ######################################################################################

    def seleccionarLapiz1(self):
        """
        Selecciona la herramienta 'Lapiz' para dibujar en el lienzo.

        Cambia el estado de la herramienta seleccionada a 'Lapiz'.
        """

        self.herramientaSeleccionada = Herramienta.LAPIZ1
        print(Texto.LAPIZ1)

    def seleccionarLapiz2(self):
        """
        Selecciona la herramienta 'Lapiz' para dibujar en el lienzo.

        Cambia el estado de la herramienta seleccionada a 'Lapiz'.
        """

        self.herramientaSeleccionada = Herramienta.LAPIZ2
        print(Texto.LAPIZ2)

    def seleccionarLapiz3(self):
        """
        Selecciona la herramienta 'Lapiz' para dibujar en el lienzo.

        Cambia el estado de la herramienta seleccionada a 'Lapiz'.
        """

        self.herramientaSeleccionada = Herramienta.LAPIZ3
        print(Texto.LAPIZ3)

    def seleccionarBorrador(self):
        """
        Selecciona la herramienta 'Borrador' para borrar trazos en el lienzo.

        Cambia el estado de la herramienta seleccionada a 'Borrador'.
        """
        print(Texto.BORRADOR)

    def seleccionarBorrarTodo(self):
        print(Texto.BORRARTODO)

    def seleccionarElegirColor(self):
        print(Texto.COLORCHOSER)
        color = colorchooser.askcolor(title="Selecciona un color")[1]
        if color:
            self.colorSeleccionado = color
            print(f"Color seleccionado: {color}")
