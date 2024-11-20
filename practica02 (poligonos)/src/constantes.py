"""
Archivo: constantes.py

Este archivo almacena todas las constantes que van a usar las diferentes
clases de la aplicación.

Autor: Gabriel Gomez Garcia
Fecha: 17 de septiembre de 2024
"""

# Importaciones
from algoritmos_dibujo import (
    SlopeLineStrategy,
    DDALineStrategy,
    BresenhamLineStrategy,
    BresenhamLineStrategyInt,
)


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


# Etiquetas del menú ( no las uso pero era parte de la barra de herramientas sin implementar)
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


# Textos de la aplicación
class Texts:
    """Clase que contiene los textos utilizados en la aplicación."""

    # Sección: Colores
    SELECT_COLOR = "Color seleccionado:"
    SELECT_TOGGLE_FILL = "Rellenar figuras"

    # Sección: Herramientas
    SELECT_TOOL = "Herramienta seleccionada:"
    SELECT_SIZE = ""

    # Sección: Figuras y acciones de dibujo
    SHAPE_CLEAR = "Borrar al hacer clic sobre figura"
    SHAPE_CLEAR_ALL = "Borrar todo"
    SHAPE_UNDO = "Deshacer última acción"
    SHAPE_GROUP = "Figuras agrupadas:"
    SHAPE_UNGROUP = "Desagrupando"

    # Sección: Opciones de pincel y acciones generales
    SECTION_OPTIONS = "Opciones de Pincel"
    SECTION_OPTIONS_LINE = ""
    SECTION_COLOR = "Colores"
    SECTION_COLOR_SELECT = "Seleccionar Color"
    SECTION_CLEAR = "Borradores"
    SECTION_CLEAR_ALL = "Borrar Todo"
    SECTION_CLEAR_UNDO = "Deshacer"

    # Sección: Acciones de grupo
    SECTION_ACTIONS = "Acciones"
    SECTION_ACTIONS_DELETE = "Borrar"
    SECTION_ACTIONS_CHANGE_COLOR = "Cambiar Color"

    SECTION_GRUPO = "Grupo"
    SECTION_GRUPO_GROUP = "Agrupar"
    SECTION_GRUPO_UNGROUP = "Desagrupar"

    # Otras secciones
    SECTION_TEXT = "Salida de texto"
    SECTION_TEXT_CLEAR = "Limpiar"

    SECTION_SETTINGS = "Ajustes aplicación"
    SECTION_SETTINGS_ZOOM = "Resetear zoom"
    SECTION_SETTINGS_EXIT = "Cerrar aplicación"

    LEFT_FRAME_LABEL = "Área de trabajo"
    RIGHT_FRAME_LABEL = "Herramientas"
    TRANS_FRAME_LABEL = "Transformaciones"

    TRANS = "Transformaciones"
    TRANS_TRASLACION = "Traslación"
    TRANS_ESCALADO = "Escalado"
    TRANS_ROTACION = "Rotación"
    TRANS_SHEARING = "Shearing"
    TRANS_REFLEXION = "Reflexión"
    TRANS_PELI = "Pelicula"

    TRANS_APLICAR = "Aplicar"
    TRANS_DESHACER = "Deshacer"
    TRANS_REHACER = "Rehacer"

    TRANS_TRAS_X = "X:"
    TRANS_TRAS_Y = "Y:"

    TRANS_ESCALADO_X = "X:"
    TRANS_ESCALADO_Y = "Y:"

    TRANS_ROTACION_ANGULO = "Ángulo (grados)"
    TRANS_ROTACION_CLOCK = "clockwise"

    TRANS_SHEARING_X = "X:"
    TRANS_SHEARING_Y = "Y:"

    TRANS_REFLEXION_M = "Pendiente:"
    TRANS_REFLEXION_B = "Ordenada origen:"

    REFLEXION_NINGUNA = "no-reflexion"
    REFLEXION_X_AXIS = "x-axis"
    REFLEXION_Y_AXIS = "y-axis"
    REFLEXION_ORIGEN = "origin"
    REFLEXION_LINE = "line"

    TRANS_PELI_CREAR = "Generar animación"


# Estrategias de dibujo
class DrawingStrategies:
    """Clase que define las estrategias de dibujo disponibles como constantes."""

    STRATEGIES = {
        "SlopeLine": SlopeLineStrategy(),
        "DDALine": DDALineStrategy(),
        "BresenhamLine Float": BresenhamLineStrategy(),
        "BresenhamLine Integer": BresenhamLineStrategyInt(),
    }


# Eventos del usuario
class UserEvents:
    """Clase que define los eventos de interacción del usuario."""

    DRAG = "<Motion>"  # Arrastre

    LEFT_CLICK = "<Button-1>"  # Clic izquierdo
    LEFT_DRAG = "<B1-Motion>"  # Arrastre con clic izquierdo
    LEFT_RELEASE = "<ButtonRelease-1>"  # Liberación del clic izquierdo

    RIGHT_CLICK = "<Button-3>"  # Clic derecho
    RIGHT_DRAG = "<B3-Motion>"  # Arrastre con clic derecho
    RIGHT_RELEASE = "<ButtonRelease-3>"  # Liberación del clic derecho

    MOUSE_WHEEL = "<MouseWheel>"  # Movimiento de la rueda del ratón
    MOUSE_WHEEL_DRAG = "<B2-Motion>"  # Arrastre con rueda del ratón

    SPACE = "<space>"  # Tecla Espacio

    TECLA_UP = "<KeyPress-w>"  # Tecla 'W'
    TECLA_LEFT = "<KeyPress-a>"  # Tecla 'A'
    TECLA_DOWN = "<KeyPress-s>"  # Tecla 'S'
    TECLA_RIGHT = "<KeyPress-d>"  # Tecla 'D'

    CONTROL_Z = "<Control-z>"  # Combinación Ctrl+Z
    CONTROL_Y = "<Control-y>"  # Combinación Ctrl+Y
    ENTER = "<Return>"

    ARROW_UP = "<Up>"  # Flecha arriba
    ARROW_DOWN = "<Down>"  # Flecha abajo
    ARROW_LEFT = "<Left>"  # Flecha izquierda
    ARROW_RIGHT = "<Right>"  # Flecha derecha

    TECLA_G = "g"  # Tecla 'G'
    TECLA_H = "h"  # Tecla 'H'

    TECLA_T = "t"  # Tecla 't'


# Configuraciones por defecto
class Default:
    """Clase que define las constantes por defecto para la aplicación."""

    # Dimensiones de ventana y canvas
    WINDOW_WIDTH = 1900  # Ancho de la ventana
    WINDOW_HEIGHT = 800  # Alto de la ventana
    WINDOW_TITLE = "Ventana con Menú y Canvas Interactivo"  # Título por defecto

    CANVAS_BACKGROUND_COLOR = Color.WHITE  # Color de fondo del canvas

    # Zoom
    ZOOM_FACTOR = 1
    ZOOM_OUT_FACTOR = -0.1  # Zoom alejar
    ZOOM_IN_FACTOR = 0.1  # Zoom acercar
    ZOOM_LIMIT_MIN = 0.4
    ZOOM_LIMIT_MAX = 3.0

    # Movimiento
    CANVAS_MOVE_X = 1  # Velocidad de desplazamiento en x
    CANVAS_MOVE_Y = 1  # Velocidad de desplazamiento en y

    # Parámetros adicionales
    MIN_DISTANCE = 10  # Distancia mínima para interacciones
    MIN_DISTANCE_SELECT = 20

    # Herramientas de dibujo
    DRAWING_COLOR = Color.BLACK  # Color de dibujo
    DRAWING_TOOL = DrawingStrategies.STRATEGIES["BresenhamLine Integer"]  # Pincel
    DRAWING_TOOL_NAME = list(DrawingStrategies.STRATEGIES.keys())[3]
    DRAWING_SIZE = 1  # Tamaño del pincel

    # Apariencia de la ventana
    WINDOW_THEME = "green"  # Tema
    FONT_FAMILY = "Segoe UI"  # Fuente
    FONT_SIZE = 12  # Tamaño de fuente

    ENTRY_COLOR = Color.GRAY
