"""
Archivo: ventana.py

Se define la clase abstracta Ventana y sus metodos. Esta clase base permite
la creacion de distintas ventanas con dimensiones y titulo personalizado.
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
    por otras clases que implementen el metodo _crear_contenido_ventana.

    Atributos de instancia:
        _width (int): El ancho de la ventana en pixeles.
        _height (int): La altura de la ventana en pixeles.
        _title (str): El titulo de la ventana.
        _ventana (tk.Tk): La instancia de la ventana principal de tkinter.
    """

    def __init__(
        self,
        width: int = Default.VENTANA_WIDTH,
        height: int = Default.VENTANA_HEIGHT,
        title: str = Default.VENTANA_TITLE,
    ):
        """
        Inicializa una nueva ventana con dimensiones y titulo.

        Args:
            width (int): El ancho de la ventana en pixeles.
            height (int): La altura de la ventana en pixeles.
            title (str): El titulo de la ventana.

        Raises:
            ValueError: Si el ancho o el alto no son valores enteros positivos.
            TypeError: Si el titulo no es una cadena de texto.
        """
        if not isinstance(width, int) or width <= 0:
            raise ValueError(Error.WIDTH)
        if not isinstance(height, int) or height <= 0:
            raise ValueError(Error.HEIGHT)
        if not isinstance(title, str):
            raise TypeError(Error.TITLE)

        self._width = width
        self._height = height
        self._title = title
        self._ventana = self._crear_ventana()

    def __str__(self) -> str:
        """
        Devuelve una representacion en forma de cadena de la ventana.

        Returns:
            str: Una descripcion de la ventana con su titulo, ancho y altura.
        """
        return (
            f"Ventana(titulo='{self._title}', ancho={self._width}, alto={self._height})"
        )

    def mostrar_ventana(self) -> None:
        """
        Prepara el contenido de la ventana y la muestra iniciando el bucle principal.
        """
        self._crear_contenido_ventana()
        self._iniciar_bucle()

    def cerrar_ventana(self) -> None:
        """Cierra la ventana de forma segura."""
        self._ventana.destroy()

    def _crear_ventana(self) -> tk.Tk:
        """
        Crea la ventana principal de tkinter con las dimensiones y el titulo indicados.

        Returns:
            tkinter.Tk: Una instancia de la ventana de tkinter.
        """
        ventana = tk.Tk()
        ventana.title(self._title)
        ventana.geometry(f"{self._width}x{self._height}")
        return ventana

    @abstractmethod
    def _crear_contenido_ventana(self) -> None:
        """
        Metodo abstracto que debe ser implementado por las subclases para agregar
        contenido a la ventana.
        """
        raise NotImplementedError(Error.NO_IMPLEMENTADO)

    def _iniciar_bucle(self) -> None:
        """
        Inicia el bucle principal de la ventana.

        Raises:
            RuntimeError: Si ocurre un error al iniciar el bucle de la ventana.
            RuntimeError: Si ocurre un error general inesperado.
        """
        try:
            self._ventana.mainloop()
        except tk.TclError as e:
            print(e)
            raise RuntimeError(Error.VENTANA)
        except Exception as e:
            print(e)
            raise RuntimeError(Error.GENERAL)

    ########### getters y setters ##############
    @property
    def width(self):
        """Obtiene el ancho de la ventana."""
        return self._width

    @width.setter
    def width(self, valor):
        """Establece el ancho de la ventana."""
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError(Error.WIDTH)
        self._width = valor
        self._ventana.geometry(f"{self._width}x{self._height}")

    @property
    def height(self):
        """Obtiene la altura de la ventana."""
        return self._height

    @height.setter
    def height(self, valor):
        """Establece la altura de la ventana."""
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError(Error.HEIGHT)
        self._height = valor
        self._ventana.geometry(f"{self._width}x{self._height}")

    @property
    def title(self):
        """Obtiene el título de la ventana."""
        return self._title

    @title.setter
    def title(self, valor):
        """Establece el título de la ventana."""
        if not isinstance(valor, str):
            raise TypeError(Error.TITLE)
        self._title = valor
        self._ventana.title(self._title)

    @property
    def ventana(self):
        """Obtiene la instancia de la ventana tkinter."""
        return self._ventana
