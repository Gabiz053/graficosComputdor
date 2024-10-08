"""
Archivo: constantes.py

Este archivo almacena todas las constantes que van a usar las diferentes
clases de la aplicacion.

Autor: Gabriel Gomez Garcia
Fecha: 17 de septiembre de 2024
"""

from algoritmos_dibujo import *


class Error:
    """
    Clase que contiene mensajes de error utilizados en la aplicacion.
    """

    WIDTH = "El ancho debe ser un entero positivo."
    HEIGHT = "El alto debe ser un entero positivo."
    TITLE = "El titulo debe ser una cadena de texto."
    VENTANA = "Error al iniciar la ventana: "
    GENERAL = "Error inesperado en la ventana"

    NO_IMPLEMENTADO = "Este metodo debe ser implementado en las subclases."


class MenuVen:
    """
    Clase que define las constantes utilizadas en el menu de la aplicacion.
    """

    ARCHIVO = "Archivo"
    ARCHIVO_NUEVO = "Nuevo"
    ARCHIVO_ABRIR = "Abrir"
    ARCHIVO_GUARDAR = "Guardar"
    ARCHIVO_SALIR = "Salir"

    AYUDA = "Ayuda"
    AYUDA_ACERCA = "Acerca de"

    BOTON_LAPIZ_1 = "lapiz M1"
    BOTON_LAPIZ_2 = "lapiz M2"
    BOTON_LAPIZ_3 = "lapiz M3"
    BOTON_LAPIZ_4 = "lapiz M4"
    
    BOTON_BORRADOR = "borrador"
    BOTON_BORRAR_TODO = "borrar todo"
    BOTON_COLORCHOSER = "elegir color"
    
    BOTON_TAMANHO = "Tamanho pincel"


class Texto:
    """
    Clase que contiene los textos utilizados en la aplicacion.
    """

    NUEVO_ARCHIVO = "Nuevo archivo"
    ABRIR_ARCHIVO = "Abrir archivo"
    GUARDAR_ARCHIVO = "Guardar archivo"
    ACERCA_DE = "Acerca de la aplicacion"

    LAPIZ1 = "Herramienta seleccionada: Lapiz con SlopeLineStrategy"
    LAPIZ2 = "Herramienta seleccionada: Lapiz con DDALineStrategy"
    LAPIZ3 = "Herramienta seleccionada: Lapiz con BresenhamLineStrategy"
    LAPIZ4 = "Herramienta seleccionada: Lapiz con BresenhamLineStrategy Integer"
    
    BORRADOR = "Herramienta seleccionada: Borrador"
    BORRAR_TODO = "Herramienta seleccionada: Borrar todo"
    COLORCHOSER = "Herramienta seleccionada: Colorchoser"

    COLORCHOSER_TITULO = "Selecciona un color"
    COLORCHOSER_SELECCION = "Color seleccionado: "


class Herramienta:
    """
    Clase que define las estrategias de dibujo disponibles como constantes.
    """

    LAPIZ_1 = SlopeLineStrategy()  # Estrategia de linea por pendiente
    LAPIZ_2 = DDALineStrategy()  # Estrategia DDA para lineas
    LAPIZ_3 = BresenhamLineStrategy()  # Estrategia de Bresenham para lineas
    LAPIZ_4 = BresenhamLineStrategyInt()  # Estrategia de Bresenham para lineas


class Event:
    """
    Clase que define los eventos de interaccion del usuario.
    """

    ON_LEFT_CLICK = "<Button-1>"  # Evento de clic izquierdo
    ON_LEFT_MOVEMENT = "<B1-Motion>"  # Evento de movimiento con clic izquierdo)
    ON_LEFT_RELEASE = "<ButtonRelease-1>"  # Evento de liberacion del clic izquierdo
    
    ON_RIGHT_CLICK = "<Button-3>"  # Evento de clic derecho
    ON_RIGHT_MOVEMENT = "<B3-Motion>"  # Evento de movimiento con clic derecho)
    ON_RIGHT_RELEASE = "<ButtonRelease-3>"  # Evento de liberacion del clic derecho
    
    ON_MOUSE_WHEEL = "<MouseWheel>" # Evento al mover la rueda del raton
    ON_MOUSE_WHEEL_MOVEMENT = "<B2-Motion>" # Evento al mover la rueda del raton

class Color:
    """
    Clase que contiene los colores utilizados en la aplicacion.
    """

    WHITE = "white"  # Color blanco
    BLACK = "black"  # Color negro
    LIGHTGRAY = "lightgray"  # Color gris claro


# Default para la aplicacion (se pueden cambiar)#
class Default:
    """
    Clase que define las constantes por defecto para la aplicacion.
    """

    BG_MENU = Color.LIGHTGRAY  # Color de fondo del menu
    HERRAMIENTA = BresenhamLineStrategy()  # Herramienta por defecto
    TAMANHO_BORRADOR = 10  # Tamaño del borrador
    TAMANHO_DIBUJAR = 1  # Tamaño del pincel para dibujar

    VENTANA_WIDTH = 1280  # Ancho de la ventana por defecto
    VENTANA_HEIGHT = 720  # Alto de la ventana por defecto
    VENTANA_TITLE = "Ventana con Menu y Canvas Interactivo"  # Titulo de la ventana

    CANVAS_COLOR = Color.WHITE  # Color de fondo del canvas
    MENU_TEMA = "clam"  # Tema del menu
    COLOR = Color.BLACK  # Color de dibujo por defecto
    
    ZOOM = 1
    REDUCIR = 0.9 # mas pequenho mas rapido
    AMPLIAR = 1.1 # mas grande mas rapido
