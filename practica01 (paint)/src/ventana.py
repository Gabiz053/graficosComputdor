"""
Archivo: ventana.py

Se define la clase abstracta Ventana y sus metodos. Esta clase base permite
la creacion de distintas ventanas con dimensiones y titulo personalizados.

Autor: Gabriel Gomez Garcia
Fecha: 20 de septiembre de 2024
"""

# Imports estandar
import tkinter as tk
from abc import ABC, abstractmethod

# Imports de terceros
import customtkinter as ctk

# Imports locales
from constantes import Default, ErrorMessages


class Ventana(ABC):
    """
    Clase base abstracta que representa una ventana generica usando customtkinter.
    Esta clase no puede ser instanciada directamente. Debe ser heredada
    por otras clases que implementen el metodo _crear_contenido_ventana.

    Atributos de instancia:
        _width (int): El ancho de la ventana en pixeles.
        _height (int): La altura de la ventana en pixeles.
        _title (str): El titulo de la ventana.
        _ventana (ctk.CTk): La instancia de la ventana principal de customtkinter.
        _fuente (ctk.CTkFont): La fuente de la ventana.
    """

    def __init__(
        self,
        width: int = ErrorMessages.WIDTH,
        height: int = ErrorMessages.HEIGHT,
        title: str = ErrorMessages.TITLE,
    ) -> None:
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
        self._validar_dimensiones(width, height)
        self._validar_titulo(title)

        self._width = width
        self._height = height
        self._title = title
        self._ventana = self._crear_ventana()
        self._fuente = self._crear_estilo()

    ########### Metodos de inicializacion ###########

    def _crear_ventana(self) -> ctk.CTk:
        """
        Crea la ventana principal de tkinter con las dimensiones y el titulo indicados.

        Returns:
            ctk.CTk: Una instancia de la ventana de customtkinter.
        """
        ventana = ctk.CTk()
        ventana.title(self._title)
        ventana.geometry(f"{self._width}x{self._height}")
        return ventana

    def _crear_estilo(self) -> ctk.CTkFont:
        """
        Aplica el tema y crea la fuente de la ventana.

        Returns:
            ctk.CTkFont: La fuente creada para la ventana.
        """
        ctk.set_default_color_theme(Default.WINDOW_THEME)
        fuente = ctk.CTkFont(family=Default.FONT_FAMILY, size=Default.FONT_SIZE)
        return fuente

    ########### Metodos de validacion ###########

    def _validar_dimensiones(self, width: int, height: int) -> None:
        """Valida que las dimensiones de la ventana sean enteros positivos."""
        if not isinstance(width, int) or width <= 0:
            raise ValueError(ErrorMessages.WIDTH)
        if not isinstance(height, int) or height <= 0:
            raise ValueError(ErrorMessages.HEIGHT)

    def _validar_titulo(self, title: str) -> None:
        """Valida que el titulo de la ventana sea una cadena de texto."""
        if not isinstance(title, str):
            raise TypeError(ErrorMessages.TITLE)

    def _validar_fuente(self, fuente: ctk.CTkFont) -> None:
        """Valida que la fuente proporcionada sea una instancia de ctk.CTkFont."""
        if not isinstance(fuente, ctk.CTkFont):
            raise TypeError(ErrorMessages.FONT)

    ########### Metodos de ciclo de vida ###########

    def mostrar_ventana(self) -> None:
        """Prepara el contenido de la ventana y la muestra iniciando el bucle principal."""
        self._crear_contenido_ventana()
        self._iniciar_bucle()

    def cerrar_ventana(self) -> None:
        """Cierra la ventana de forma segura."""
        self._ventana.destroy()

    @abstractmethod
    def _crear_contenido_ventana(self) -> None:
        """
        Metodo abstracto que debe ser implementado por las subclases para agregar
        contenido a la ventana.
        """
        raise NotImplementedError(ErrorMessages.NOT_IMPLEMENTED)

    def _iniciar_bucle(self) -> None:
        """
        Inicia el bucle principal de la ventana.

        Raises:
            RuntimeError: Si ocurre un error al iniciar el bucle de la ventana.
        """
        try:
            self._ventana.mainloop()
        except tk.TclError as e:
            print(e)
            raise RuntimeError(ErrorMessages.WINDOW_INITIALIZATION)
        except Exception as e:
            print(e)
            raise RuntimeError(ErrorMessages.GENERAL)

    ########### Metodos magicos ###########

    def __repr__(self) -> str:
        """
        Devuelve una representacion tecnica de la ventana para depuracion.

        Returns:
            str: Descripcion tecnica con su titulo, ancho y altura.
        """
        return (
            f"Ventana(titulo='{self._title}', ancho={self._width}, alto={self._height})"
        )

    ########### Getters y setters ###########

    @property
    def width(self) -> int:
        """Obtiene el ancho de la ventana."""
        return self._width

    @width.setter
    def width(self, valor: int) -> None:
        """Establece el ancho de la ventana y actualiza la geometria."""
        self._validar_dimensiones(valor, self._height)
        self._width = valor
        self._ventana.geometry(f"{self._width}x{self._height}")

    @property
    def height(self) -> int:
        """Obtiene la altura de la ventana."""
        return self._height

    @height.setter
    def height(self, valor: int) -> None:
        """Establece la altura de la ventana y actualiza la geometria."""
        self._validar_dimensiones(self._width, valor)
        self._height = valor
        self._ventana.geometry(f"{self._width}x{self._height}")

    @property
    def title(self) -> str:
        """Obtiene el titulo de la ventana."""
        return self._title

    @title.setter
    def title(self, valor: str) -> None:
        """Establece el titulo de la ventana y actualiza la ventana correspondiente."""
        self._validar_titulo(valor)
        self._title = valor
        self._ventana.title(self._title)

    @property
    def ventana(self) -> ctk.CTk:
        """Obtiene la instancia de la ventana customtkinter."""
        return self._ventana

    @property
    def fuente(self) -> ctk.CTkFont:
        """Obtiene la fuente de la ventana."""
        return self._fuente

    @fuente.setter
    def fuente(self, valor: ctk.CTkFont) -> None:
        """Establece la fuente de la ventana."""
        self._validar_fuente(valor)
        self._fuente = valor
