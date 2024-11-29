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
    RECURSIVO_ALGORITMOS = [
        "Triangulo de Sierpinsky",
        "Alfombra de Sierpinsky",
        "Curva de Koch",
        "Curva de Hilbert",
        "Arbol",
    ]
    RECURSIVO_ALGORITMOS_DEFAULT = RECURSIVO_ALGORITMOS[0]

    RECURSIVO_COLOR = "Elegir color:"
    RECURSIVO_COLOR_BOTON = "Color"
    RECURSIVO_COLOR_DEFAULT = "#BFBF80"

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
    JULIA_COLORES = [
        "inferno",
        "viridis",
        "plasma",
        "magma",
        "cividis",
        "copper",
        "hot",
        "twilight",
        "twilight_shifted",
        "hsv",
    ]
    JULIA_COLORES_DEFAULT = JULIA_COLORES[0]
    JULIA_GENERAR = "Generar Fractal Julia"

    # Sección: Mandelbrot
    MANDELBROT = "Fractal Mandelbrot"
    MANDELBROT_COLOR = "Elegir color:"
    MANDELBROT_COLORES = [
        "inferno",
        "viridis",
        "plasma",
        "magma",
        "cividis",
        "copper",
        "hot",
        "twilight",
        "twilight_shifted",
        "hsv",
    ]
    MANDELBROT_COLORES_DEFAULT = MANDELBROT_COLORES[0]
    MANDELBROT_GENERAR = "Generar Fractal Mandelbrot"

    # Sección: IFS
    IFS = "Fractal IFS"

    IFS_COLOR = "Elegir color:"
    IFS_COLOR_BOTON = "Color"
    IFS_COLOR_DEFAULT = "#BFBF80"

    # Definir las funciones IFS predefinidas
    IFS_ALGORITMOS = [
        "Sierspinski",
        "Sierspinski alfombra",
        "Dragon",
        "Fern",
        "Koch Snowflake",
        "Monster",
    ]

    IFS_SIERPINSKI = [
        # Primera transformación
        (
            {"a": "0.5", "c": "0.0", "e": "0.0", "b": "0.0", "d": "0.5", "f": "0.0"},
            "0.333",
            "#FFFFB3",  # Amarillo pastel
        ),
        # Segunda transformación
        (
            {"a": "0.5", "c": "0.0", "e": "0.5", "b": "0.0", "d": "0.5", "f": "0.0"},
            "0.333",
            "#B3FFB3",  # Verde pastel
        ),
        # Tercera transformación
        (
            {"a": "0.5", "c": "0.0", "e": "0.25", "b": "0.0", "d": "0.5", "f": "0.5"},
            "0.334",
            "#B3D9FF",  # Azul pastel
        ),
    ]
    IFS_ALFOMBRA_SIERPINSKI = [
        # Primera transformación: Rojo pastel
        (
            {
                "a": "0.3333",
                "c": "0.0",
                "e": "0.0",
                "b": "0.0",
                "d": "0.3333",
                "f": "0.0",
            },
            "0.125",
            "#FFB3B3",  # Rojo pastel
        ),
        # Segunda transformación: Naranja pastel
        (
            {
                "a": "0.3333",
                "c": "0.0",
                "e": "0.3333",
                "b": "0.0",
                "d": "0.3333",
                "f": "0.0",
            },
            "0.125",
            "#FFD9B3",  # Naranja pastel
        ),
        # Tercera transformación: Amarillo pastel
        (
            {
                "a": "0.3333",
                "c": "0.0",
                "e": "0.6666",
                "b": "0.0",
                "d": "0.3333",
                "f": "0.0",
            },
            "0.125",
            "#FFFFB3",  # Amarillo pastel
        ),
        # Cuarta transformación: Verde pastel
        (
            {
                "a": "0.3333",
                "c": "0.0",
                "e": "0.0",
                "b": "0.0",
                "d": "0.3333",
                "f": "0.3333",
            },
            "0.125",
            "#B3FFB3",  # Verde pastel
        ),
        # Quinta transformación: Azul pastel
        (
            {
                "a": "0.3333",
                "c": "0.0",
                "e": "0.6666",
                "b": "0.0",
                "d": "0.3333",
                "f": "0.3333",
            },
            "0.125",
            "#B3D9FF",  # Azul pastel
        ),
        # Sexta transformación: Añil pastel
        (
            {
                "a": "0.3333",
                "c": "0.0",
                "e": "0.0",
                "b": "0.0",
                "d": "0.3333",
                "f": "0.6666",
            },
            "0.125",
            "#D9B3FF",  # Añil pastel
        ),
        # Séptima transformación: Violeta pastel
        (
            {
                "a": "0.3333",
                "c": "0.0",
                "e": "0.3333",
                "b": "0.0",
                "d": "0.3333",
                "f": "0.6666",
            },
            "0.125",
            "#FFB3FF",  # Violeta pastel
        ),
        # Octava transformación: Rosa pastel
        (
            {
                "a": "0.3333",
                "c": "0.0",
                "e": "0.6666",
                "b": "0.0",
                "d": "0.3333",
                "f": "0.6666",
            },
            "0.125",
            "#FFB3D9",  # Rosa pastel
        ),
    ]

    IFS_CURVA_DRAGON = [
        # Primera transformación: Blanco pastel
        (
            {"a": "0.5", "c": "-0.5", "e": "0.0", "b": "0.5", "d": "0.5", "f": "0.0"},
            "0.5",
            "#F5F5F5",  # Blanco pastel
        ),
        # Segunda transformación: Dorado suave
        (
            {"a": "-0.5", "c": "0.5", "e": "1.0", "b": "-0.5", "d": "-0.5", "f": "0.0"},
            "0.5",
            "#FFD700",  # Dorado suave
        ),
    ]

    IFS_FERN = [
        (
            {"a": "0.0", "c": "0.0", "e": "0.0", "b": "0.0", "d": "0.16", "f": "0.0"},
            "0.01",
            "#006400",
        ),  # Verde oscuro
        (
            {
                "a": "0.85",
                "c": "0.04",
                "e": "0.0",
                "b": "-0.04",
                "d": "0.85",
                "f": "1.6",
            },
            "0.85",
            "#228B22",
        ),  # Verde bosque
        (
            {
                "a": "0.2",
                "c": "-0.26",
                "e": "0.0",
                "b": "0.23",
                "d": "0.22",
                "f": "1.6",
            },
            "0.07",
            "#32CD32",
        ),  # Verde lima
        (
            {
                "a": "-0.15",
                "c": "0.28",
                "e": "0.0",
                "b": "0.26",
                "d": "0.24",
                "f": "0.44",
            },
            "0.07",
            "#7FFF00",
        ),  # Verde chartreuse
    ]

    IFS_KOCH_SNOWFLAKE = [
        # Primera transformación: Azul hielo
        (
            {
                "a": "-0.1667",
                "c": "0.2887",
                "e": "0.1667",
                "b": "-0.2887",
                "d": "-0.1667",
                "f": "0.2887",
            },
            "0.132857",
            "#B3E5FF",  # Azul hielo
        ),
        # Segunda transformación: Azul claro
        (
            {
                "a": "0.1667",
                "c": "-0.2887",
                "e": "0.1667",
                "b": "0.2887",
                "d": "0.1667",
                "f": "0.2887",
            },
            "0.132857",
            "#99CCFF",  # Azul claro
        ),
        # Tercera transformación: Azul celeste
        (
            {
                "a": "0.333",
                "c": "0",
                "e": "0.333",
                "b": "0",
                "d": "0.333",
                "f": "0.5774",
            },
            "0.132857",
            "#66B2FF",  # Azul celeste
        ),
        # Cuarta transformación: Azul profundo
        (
            {
                "a": "0.1667",
                "c": "0.2887",
                "e": "0.6667",
                "b": "-0.2887",
                "d": "0.1667",
                "f": "0.5774",
            },
            "0.132857",
            "#3399FF",  # Azul profundo
        ),
        # Quinta transformación: Azul hielo
        (
            {
                "a": "0.5",
                "c": "-0.2887",
                "e": "0.333",
                "b": "0.2887",
                "d": "0.5",
                "f": "0",
            },
            "0.202857",
            "#B3E5FF",  # Azul hielo
        ),
        # Sexta transformación: Azul claro
        (
            {"a": "-0.333", "c": "0", "e": "0.6667", "b": "0", "d": "-0.333", "f": "0"},
            "0.132857",
            "#99CCFF",  # Azul claro
        ),
        # Séptima transformación: Azul celeste
        (
            {"a": "0.333", "c": "0", "e": "0.6667", "b": "0", "d": "0.333", "f": "0"},
            "0.132857",
            "#66B2FF",  # Azul celeste
        ),
    ]

    IFS_MONSTER = [
        # Primera transformación: Blanco cálido
        (
            {"a": "0.5", "c": "0.5", "e": "0.0", "b": "-0.5", "d": "0.5", "f": "0.0"},
            "0.25",
            "#F5F5DC",  # Blanco cálido
        ),
        # Segunda transformación: Dorado pálido
        (
            {"a": "0.5", "c": "-0.5", "e": "0.0", "b": "0.5", "d": "0.5", "f": "0.0"},
            "0.25",
            "#FFD700",  # Dorado pálido
        ),
        # Tercera transformación: Amarillo suave
        (
            {"a": "0.5", "c": "0.5", "e": "0.0", "b": "0.0", "d": "0.5", "f": "0.1"},
            "0.25",
            "#FFFACD",  # Amarillo suave
        ),
        # Cuarta transformación: Crema oscuro
        (
            {"a": "0.5", "c": "-0.5", "e": "0.0", "b": "0.0", "d": "0.5", "f": "0.1"},
            "0.25",
            "#F0E68C",  # Crema oscuro
        ),
    ]

    IFS_PREDEFINIDOS = {
        "Sierspinski": IFS_SIERPINSKI,
        "Sierspinski alfombra": IFS_ALFOMBRA_SIERPINSKI,
        "Dragon": IFS_CURVA_DRAGON,
        "Fern": IFS_FERN,
        "Koch Snowflake": IFS_KOCH_SNOWFLAKE,
        "Monster": IFS_MONSTER,
    }

    IFS_LISTA_DEFAULT = IFS_SIERPINSKI


class UserEvents:
    LEFT_CLICK = "<Button-1>"  # Clic izquierdo
    RIGHT_CLICK = "<Button-3>"  # Clic derecho
    LEFT_PRESS = "<ButtonPress-1>"  # Mantener clic izquierdo
    RIGHT_PRESS = "<ButtonPress-3>"  # Mantener clic derecho
    LEFT_RELEASE = "<ButtonRelease-1>"  # Liberar clic izquierdo
    RIGHT_RELEASE = "<ButtonRelease-3>"  # Liberar clic derecho

    MOUSE_WHEEL = "<MouseWheel>"  # Movimiento de la rueda del ratón
    MOUSE_WHEEL_DRAG = "<B2-Motion>"  # Arrastre con rueda del ratón

    MOUSE_MOVE = "<Motion>"


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
    WINDOW_WIDTH = 1050
    WINDOW_HEIGHT = 1118

    # titulos
    TITLE_RECURSIVO = "Fractal recursivo"
    TITLE_JULIA = "Fractal julia"
    TITLE_MANDELBROT = "Fractal mandelbrot"
    TITLE_IFS = "Fractal ifs"
