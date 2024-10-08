"""
Archivo: main.py

Este archivo crea una instancia de la clase VentanaMenuCanvas y ejecuta la aplicacion grafica
con un lienzo interactivo y un menu para seleccionar herramientas.

Autor: Gabriel Gomez Garcia
Fecha: 17 de septiembre de 2024
"""

from VentanaMenuCanvas import VentanaMenuCanvas
from constantes import Default

width = Default.VENTANA_WIDTH
height = Default.VENTANA_HEIGHT
title = Default.VENTANA_TITLE
canvasColor = Default.CANVAS_COLOR


def main():
    """
    Funcion principal que crea una instancia de VentanaMenuCanvas y ejecuta la aplicacion.
    """
    # Crear una instancia de VentanaMenuCanvas
    ventana = VentanaMenuCanvas(width, height, title, canvasColor)

    # Iniciar el bucle principal de la ventana
    ventana.mostrarVentana()


if __name__ == "__main__":
    main()
