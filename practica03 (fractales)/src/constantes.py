"""
Archivo: constantes.py

Este archivo almacena todas las constantes que van a usar las diferentes
clases de la aplicación.

Autor: Gabriel Gomez Garcia
Fecha: 17 de septiembre de 2024
"""


# Colores
class Color:
    """Clase que contiene los colores utilizados en la aplicación."""

    WHITE = "white"  # Color blanco
    BLACK = "black"  # Color negro
    LIGHT_GRAY = "#333333"
    DARK_GRAY = "#242424"
    GRAY = "#2B2B2B"
    GREEN = "#2FA572"
    LIGHT_LIGHT_GREY = "#3B3B3B"


# Mensajes de error
class ErrorMessages:
    """Clase que contiene mensajes de error utilizados en la aplicación."""

    WIDTH = "El ancho debe ser un entero positivo."
    HEIGHT = "El alto debe ser un entero positivo."
    TITLE = "El título debe ser una cadena de texto."
    FONT = "La fuente debe ser una instancia de ctkFont"

    WINDOW_INITIALIZATION = "Error al iniciar la ventana: "
    GENERAL = "Error inesperado en la ventana"
    NOT_IMPLEMENTED = "Este método debe ser implementado en las subclases."


# Textos de la aplicación
class Texts:
    """Clase que contiene los textos utilizados en la aplicación."""

    # Sección: Menus
    SECCION_FRACTALES = "Visualización de fractales."

    # Sección: Recursivos
    RECURSIVO = "Fractal recursivo"
    RECURSIVO_EJEMPLO = "Ejemplo: "
    RECURSIVO_ALGORITMOS = ["Algoritmo1", "Algoritmo2", "Algoritmo3"]
    RECURSIVO_ALGORITMOS_DEFAULT = RECURSIVO_ALGORITMOS[0]

    RECURSIVO_COLOR = "Elegir color:"
    RECURSIVO_COLOR_BOTON = "Color"
    RECURSIVO_COLOR_DEFAULT = "#000000"

    RECURSIVO_NIVEL = "Nivel de recursividad:"
    RECURSIVO_NIVEL_MIN = 1
    RECURSIVO_NIVEL_MAX = 10
    RECURSIVO_NIVEL_DEFAULT = 5

    RECURSIVO_GENERAR = "Generar fractal recursivo"

    # Sección: Julia Set
    JULIA = "Fractal Julia Set"
    JULIA_REAL = "Número Real:"
    JULIA_IMAGINARIO = "Número Imaginario:"
    JULIA_XMIN = "Xmin:"
    JULIA_XMAX = "Xmax:"
    JULIA_YMIN = "Ymin:"
    JULIA_YMAX = "Ymax:"
    JULIA_EJEMPLO = "Ejemplo: "
    JULIA_ALGORITMOS = ["Ninguno", "Algoritmo1", "Algoritmo2", "Algoritmo3"]
    JULIA_ALGORITMOS_DEFAULT = JULIA_ALGORITMOS[0]

    JULIA_COLOR = "Elegir color:"
    JULIA_COLORES = ["Rojo", "Verde", "Azul", "Amarillo", "Magenta", "Cian"]
    JULIA_COLORES_DEFAULT = JULIA_COLORES[0]
    JULIA_GENERAR = "Generar Fractal Julia"

    # Sección: Mandelbrot
    MANDELBROT = "Fractal Mandelbrot"
    MANDELBROT_COLOR = "Elegir color:"
    MANDELBROT_COLORES = ["Rojo", "Verde", "Azul", "Amarillo", "Magenta", "Cian"]
    MANDELBROT_COLORES_DEFAULT = MANDELBROT_COLORES[0]
    MANDELBROT_GENERAR = "Generar Fractal Mandelbrot"

    # Sección: IFS
    IFS = "Fractal IFS"

    IFS_COLOR = "Elegir color:"
    IFS_COLOR_BOTON = "Color"
    IFS_COLOR_DEFAULT = "#000000"


# Configuraciones por defecto
class Default:
    """Clase que define las constantes por defecto para la aplicación."""

    # Dimensiones de ventana y canvas
    WINDOW_WIDTH = 1000  # Ancho de la ventana
    WINDOW_HEIGHT = 1150  # Alto de la ventana
    WINDOW_TITLE = "Ventana con Menú y Fractales"  # Título por defecto

    CANVAS_BACKGROUND_COLOR = Color.WHITE  # Color de fondo del canvas

    # Apariencia de la ventana
    WINDOW_THEME = "green"  # Tema
    FONT_FAMILY = "Segoe UI"  # Fuente
    FONT_SIZE = 12  # Tamaño de fuente


class Fractales:
    # ventana
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 1000

    # titulos
    TITLE_RECURSIVO = "Fractal recursivo"
    TITLE_JULIA = "Fractal julia"
    TITLE_MANDELBROT = "Fractal mandelbrot"
    TITLE_IFS = "Fractal ifs"
