"""
Archivo: constantes.py

Este archivo almacena todas las constantes que van a usar las diferentes
clases de la aplicacion.

Autor: Gabriel Gomez Garcia
Fecha: 17 de septiembre de 2024
"""


class Error:
    WIDTH = "El ancho debe ser un entero positivo."
    HEIGHT = "El alto debe ser un entero positivo."
    TITLE = "El titulo debe ser una cadena de texto."
    VENTANA = "Error al iniciar la ventana: "


class MenuVen:
    ARCHIVO = "Archivo"
    ARCHIVO_NUEVO = "Nuevo"
    ARCHIVO_ABRIR = "Abrir"
    ARCHIVO_GUARDAR = "Guardar"
    ARCHIVO_SALIR = "Salir"

    AYUDA = "Ayuda"
    AYUDA_ACERCA = "Acerca de"

    BOTON_LAPIZ1 = "lapiz M1"
    BOTON_LAPIZ2 = "lapiz M2"
    BOTON_LAPIZ3 = "lapiz M3"
    BOTON_BORRADOR = "borrador"
    BOTON_BORRARTODO = "borrar todo"
    BOTON_COLORCHOSER = "elegir color"


class Texto:
    NUEVOARCHIVO = "Nuevo archivo"
    ABRIRARCHIVO = "Abrir archivo"
    GUARDARARCHIVO = "Guardar archivo"
    ACERCADE = "Acerca de la aplicacion"

    LAPIZ1 = "Herramienta seleccionada: Lapiz con metodo 1"
    LAPIZ2 = "Herramienta seleccionada: Lapiz con metodo 2"
    LAPIZ3 = "Herramienta seleccionada: Lapiz con metodo 3"
    BORRADOR = "Herramienta seleccionada: Borrador"
    BORRARTODO = "Herramienta seleccionada: Borrar todo"
    COLORCHOSER = "Herramienta seleccionada: Colorchoser"


class Herramienta:
    LAPIZ1 = "lapiz M1"
    LAPIZ2 = "lapiz M2"
    LAPIZ3 = "lapiz M3"


class Event:
    ON_LEFT_CLICK = "<Button-1>"
    ON_LEFT_MOVEMENT = "<B1-Motion>"


class Color:
    WHITE = "white"
    BLACK = "black"
    LIGHTGRAY = "lightgray"


# Default para la aplicacion (se pueden cambiar)#
class Default:
    BG_MENU = Color.LIGHTGRAY
    HERRAMIENTA = Herramienta.LAPIZ1
    TAMANHO_BORRADOR = 10

    VENTANA_WIDTH = 1280
    VENTANA_HEIGHT = 720
    VENTANA_TITLE = "Ventana con Menú y Canvas Interactivo"
    CANVAS_COLOR = Color.WHITE
    MENU_TEMA = "clam"
    COLOR = Color.BLACK
