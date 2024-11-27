"""
Archivo: main.py

Este archivo crea una instancia de la clase ventanaMenu y ejecuta la aplicacion grafica
con un menu para seleccionar herramientas.

Autor: Gabriel Gomez Garcia
Fecha: 17 de septiembre de 2024
"""

# Imports locales
from constantes import Default
from ventana_menu import VentanaMenu

# Definicion de las dimensiones y el titulo de la ventana
width: int = Default.WINDOW_WIDTH
height: int = Default.WINDOW_HEIGHT
title: str = Default.WINDOW_TITLE


def main() -> None:
    """
    Funcion principal que crea una instancia de VentanaMenuCanvasAnimacion y ejecuta la aplicación.

    Esta funcion inicializa la ventana principal de la aplicación, configurando su tamaño,
    titulo y color de fondo. También establece la herramienta y tamaño de dibujo por defecto.
    """
    # Crear una instancia de VentanaMenuCanvasAnimacion
    ventana = VentanaMenu(width, height, title)

    # Iniciar el bucle principal de la ventana
    ventana.mostrar_ventana()


if __name__ == "__main__":
    main()
