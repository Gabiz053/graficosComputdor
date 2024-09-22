"""
Archivo: ventana.py

Se define la clase abstracta Ventana y sus metodos.
Esta clase base permite la creacion de distintas ventanas con dimensiones 
y titulo personalizado.

Autor: Gabriel Gomez Garcia
Fecha: 20 de septiembre de 2024
"""

import tkinter as tk
from abc import ABC, abstractmethod

from constantes import Error, Default


class Ventana(ABC):
    """
    Clase base abstracta que representa una ventana generica usando tkinter.

    Esta clase no puede ser instanciada directamente. Debe ser heredada 
    por otras clases que implementen el metodo crear_contenido_ventana.

    Atributos de instancia:
        width (int): El ancho de la ventana en pixeles.
        height (int): La altura de la ventana en pixeles.
        title (str): El titulo de la ventana.
        ventana (tk.Tk): La instancia de la ventana principal de tkinter.
    """

    def __init__(self, width: int, height: int, title: str):
        """
        Inicializa una nueva ventana con dimensiones y titulo.

        Args:
            width (int): El ancho de la ventana en pixeles.
            height (int): La altura de la ventana en pixeles.
            title (str): El titulo de la ventana.

        Raises:
            ValueError: Si el ancho o el alto no es valor entero positivo.
            ValueError: Si el alto no es valor entero positivo.
            TypeError: Si el titulo no es una cadena de texto.
        """

        # Valida los argumentos de ancho, alto y titulo.
        if not isinstance(width, int) or width <= 0:
            raise ValueError(Error.WIDTH)
        if not isinstance(height, int) or height <= 0:
            raise ValueError(Error.HEIGHT)
        if not isinstance(title, str):
            raise TypeError(Error.TITLE)

        self.width = width
        self.height = height
        self.title = title
        self.ventana = self.crearVentana()

    def crearVentana(self) -> tk.Tk:
        """
        Crea la ventana principal de tkinter con las dimensiones y el titulo indicados.

        Esta funcion crea la instancia de la ventana principal (tk.Tk) y establece su
        titulo y tamano. Luego llama al metodo abstracto crearContenidoVentana para que
        las subclases puedan agregar contenido personalizado.

        Returns:
            tkinter.Tk: Una instancia de la ventana de tkinter.
        """
        ventana = tk.Tk()
        ventana.title(self.title)
        ventana.geometry(f"{self.width}x{self.height}")

        return ventana

    @abstractmethod
    def crearContenidoVentana(self):
        """
        Metodo abstracto que debe ser implementado por las subclases para agregar
        contenido a la ventana.
        """
        pass

    def mostrarVentana(self):
        """
        Inicia el bucle principal de la ventana para que permanezca abierta.

        Raises:
            RuntimeError: Si ocurre un error al iniciar el bucle de la ventana.
        """
        try:
            self.crearContenidoVentana()  # Metodo abstracto
            self.ventana.mainloop()
        except Exception as e:
            print(e)
            raise RuntimeError(Error.VENTANA)

    def cerrarVentana(self):
        """
        Cierra la ventana de forma segura.
        """
        self.ventana.destroy()
