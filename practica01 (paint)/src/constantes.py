"""
Archivo: constantes.py

Este archivo almacena todas las constantes que van a usar las diferentes
clases de la aplicación.

Autor: Gabriel Gomez Garcia
Fecha: 17 de septiembre de 2024
"""

from algoritmos_dibujo import (
    SlopeLineStrategy,
    DDALineStrategy,
    BresenhamLineStrategy,
    BresenhamLineStrategyInt,
)


class Color:
    """Clase que contiene los colores utilizados en la aplicación."""

    WHITE = "white"  # Color blanco
    BLACK = "black"  # Color negro
    LIGHT_GRAY = "#333333"
    DARK_GRAY = "#242424"
    GRAY = "#2B2B2B"


class ErrorMessages:
    """Clase que contiene mensajes de error utilizados en la aplicación."""

    WIDTH = "El ancho debe ser un entero positivo."
    HEIGHT = "El alto debe ser un entero positivo."
    TITLE = "El título debe ser una cadena de texto."
    FONT = "La fuente debe ser una instancia de ctkFont"

    WINDOW_INITIALIZATION = "Error al iniciar la ventana: "
    GENERAL = "Error inesperado en la ventana"
    NOT_IMPLEMENTED = "Este método debe ser implementado en las subclases."


class MenuLabels:
    """Clase que define las constantes utilizadas en el menú de la aplicación."""

    FILE = "Archivo"
    NEW_FILE = "Nuevo"
    OPEN_FILE = "Abrir"
    SAVE_FILE = "Guardar"
    EXIT = "Salir"
    HELP = "Ayuda"
    ABOUT = "Acerca de"
    PENCIL_1 = "lápiz M1"
    PENCIL_2 = "lápiz M2"
    PENCIL_3 = "lápiz M3"
    PENCIL_4 = "lápiz M4"
    ERASER = "borrador"
    CLEAR_ALL = "borrar todo"
    COLOR_CHOOSER = "elegir color"
    BRUSH_SIZE_LABEL = "Tamaño pincel"


class Texts:
    """Clase que contiene los textos utilizados en la aplicación."""

    SELECT_COLOR = "Color seleccionado:"
    SELECT_TOOL = "Herramienta seleccionada:"
    SELECT_SIZE = "Tamaño de línea:"

    SHAPE_CLEAR = "Borrar al hacer clic sobre figura"
    SHAPE_CLEAR_ALL = "Borrar todo"
    SHAPE_UNDO = "Deshacer última acción"
    SHAPE_GROUP = "Figuras agrupadas:"
    SHAPE_UNGROUP = "Desagrupando"

    SECTION_OPTIONS = "Opciones de Pincel"
    SECTION_OPTIONS_LINE = "Tamaño de línea:"

    SECTION_CLEAR = "Borradores"
    SECTION_CLEAR_LAST = "Borrar Última"
    SECTION_CLEAR_ALL = "Borrar Todo"
    SECTION_CLEAR_UNDO = "Deshacer"

    SECTION_COLOR = "Colores"
    SECTION_COLOR_SELECT = "Seleccionar Color"

    SECTION_GROUP = "Agrupar figuras"
    SECTION_GROUP_GROUP = "Agrupar"
    SECTION_GROUP_UNGROUP = "Desagrupar"

    SECTION_TEXT = "Salida de texto"
    SECTION_TEXT_CLEAR = "Limpiar"

    LEFT_FRAME_LABEL = "Área de trabajo"
    RIGHT_FRAME_LABEL = "Herramientas"


class DrawingStrategies:
    """Clase que define las estrategias de dibujo disponibles como constantes."""

    STRATEGIES = {
        "SlopeLine": SlopeLineStrategy(),
        "DDALine": DDALineStrategy(),
        "BresenhamLine Float": BresenhamLineStrategy(),
        "BresenhamLine Integer": BresenhamLineStrategyInt(),
    }


class UserEvents:
    """Clase que define los eventos de interacción del usuario."""

    LEFT_CLICK = "<Button-1>"  # Evento de clic izquierdo
    LEFT_DRAG = "<B1-Motion>"  # Evento de movimiento con clic izquierdo
    LEFT_RELEASE = "<ButtonRelease-1>"  # Evento de liberación del clic izquierdo
    RIGHT_CLICK = "<Button-3>"  # Evento de clic derecho
    RIGHT_DRAG = "<B3-Motion>"  # Evento de movimiento con clic derecho
    RIGHT_RELEASE = "<ButtonRelease-3>"  # Evento de liberación del clic derecho
    MOUSE_WHEEL = "<MouseWheel>"  # Evento al mover la rueda del ratón
    MOUSE_WHEEL_DRAG = "<B2-Motion>"  # Evento al mover la rueda del ratón


class Default:
    """Clase que define las constantes por defecto para la aplicación."""

    WINDOW_WIDTH = 1600  # Ancho de la ventana por defecto
    WINDOW_HEIGHT = 800  # Alto de la ventana por defecto
    WINDOW_TITLE = "Ventana con Menú y Canvas Interactivo"  # Título de la ventana
    CANVAS_BACKGROUND_COLOR = Color.WHITE  # Color de fondo del canvas

    ZOOM_FACTOR = 1
    ZOOM_OUT_FACTOR = 0.9  # Más pequeño
    ZOOM_IN_FACTOR = 1.1  # Más grande
    ZOOM_LIMIT_MIN = 0.5
    ZOOM_LIMIT_MAX = 3.0

    MIN_DISTANCE = 10  # Distancia mínima para ciertas interacciones

    DRAWING_COLOR = Color.BLACK  # Color de dibujo por defecto
    DRAWING_TOOL = DrawingStrategies.STRATEGIES[
        "BresenhamLine Float"
    ]  # Pincel por defecto
    DRAWING_TOOL_NAME = list(DrawingStrategies.STRATEGIES.keys())[2]
    DRAWING_SIZE = 1  # Tamaño del pincel para dibujar

    WINDOW_THEME = "green"  # Tema de la ventana
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE = 12
