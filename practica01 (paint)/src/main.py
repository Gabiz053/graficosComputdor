"""
Archivo: main.py

Este archivo crea una instancia de la clase VentanaMenuCanvas y ejecuta la aplicacion grafica
con un lienzo interactivo y un menu para seleccionar herramientas.

Autor: Gabriel Gomez Garcia
Fecha: 17 de septiembre de 2024
"""

# Imports locales
from constantes import Default
from algoritmos_dibujo import AlgoritmoDibujo
from ventana_menu_canvas import VentanaMenuCanvas

# Definición de las dimensiones y el título de la ventana
width: int = Default.WINDOW_WIDTH
height: int = Default.WINDOW_HEIGHT
title: str = Default.WINDOW_TITLE
color: str = Default.DRAWING_COLOR
tool: AlgoritmoDibujo = Default.DRAWING_TOOL
drawing_size: int = Default.DRAWING_SIZE


def main() -> None:
    """
    Función principal que crea una instancia de VentanaMenuCanvas y ejecuta la aplicación.

    Esta función inicializa la ventana principal de la aplicación, configurando su tamaño,
    título y color de fondo. También establece la herramienta y tamaño de dibujo por defecto.
    """
    # Crear una instancia de VentanaMenuCanvas
    ventana = VentanaMenuCanvas(
        width, height, title, color, tool, drawing_size
    )

    # Iniciar el bucle principal de la ventana
    ventana.mostrar_ventana()


if __name__ == "__main__":
    main()
