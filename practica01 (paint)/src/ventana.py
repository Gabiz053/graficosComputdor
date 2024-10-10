"""
Archivo: ventana.py

Se define la clase abstracta Ventana y sus métodos. Esta clase base permite
la creación de distintas ventanas con dimensiones y título personalizados.

Autor: Gabriel Gomez Garcia
Fecha: 20 de septiembre de 2024
"""

# Imports estándar
import tkinter as tk
from abc import ABC, abstractmethod

# Imports de terceros
import customtkinter as ctk

# Imports locales
from constantes import Default, ErrorMessages


class Ventana(ABC):
    """
    Clase base abstracta que representa una ventana genérica usando customtkinter.
    Esta clase no puede ser instanciada directamente. Debe ser heredada
    por otras clases que implementen el método _crear_contenido_ventana.

    Atributos de instancia:
        _width (int): El ancho de la ventana en píxeles.
        _height (int): La altura de la ventana en píxeles.
        _title (str): El título de la ventana.
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
        Inicializa una nueva ventana con dimensiones y título.

        Args:
            width (int): El ancho de la ventana en píxeles.
            height (int): La altura de la ventana en píxeles.
            title (str): El título de la ventana.

        Raises:
            ValueError: Si el ancho o el alto no son valores enteros positivos.
            TypeError: Si el título no es una cadena de texto.
        """
        self._validar_dimensiones(width, height)
        self._validar_titulo(title)

        self._width = width
        self._height = height
        self._title = title
        self._ventana = self._crear_ventana()
        self._fuente = self._crear_estilo()

    ########### Métodos de inicialización ###########

    def _crear_ventana(self) -> ctk.CTk:
        """
        Crea la ventana principal de tkinter con las dimensiones y el título indicados.

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

    ########### Métodos de validación ###########

    def _validar_dimensiones(self, width: int, height: int) -> None:
        """Valida las dimensiones de la ventana."""
        if not isinstance(width, int) or width <= 0:
            raise ValueError(ErrorMessages.WIDTH)
        if not isinstance(height, int) or height <= 0:
            raise ValueError(ErrorMessages.HEIGHT)

    def _validar_titulo(self, title: str) -> None:
        """Valida el título de la ventana."""
        if not isinstance(title, str):
            raise TypeError(ErrorMessages.TITLE)

    def _validar_fuente(self, fuente: ctk.CTkFont) -> None:
        """Valida la fuente de la ventana."""
        if not isinstance(fuente, ctk.CTkFont):
            raise TypeError(ErrorMessages.FONT)

    ########### Métodos de ciclo de vida ###########

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
        Método abstracto que debe ser implementado por las subclases para agregar
        contenido a la ventana.
        """
        raise NotImplementedError(ErrorMessages.NOT_IMPLEMENTED)

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
            raise RuntimeError(ErrorMessages.WINDOW_INITIALIZATION)
        except Exception as e:
            print(e)
            raise RuntimeError(ErrorMessages.GENERAL)

    ########### Métodos mágicos ###########

    def __repr__(self) -> str:
        """
        Devuelve una representación técnica de la ventana para depuración.

        Returns:
            str: Descripción técnica con su título, ancho y altura.
        """
        return (
            f"Ventana(título='{self._title}', ancho={self._width}, alto={self._height})"
        )

    ########### Getters y setters ###########

    @property
    def width(self) -> int:
        """Obtiene el ancho de la ventana."""
        return self._width

    @width.setter
    def width(self, valor: int) -> None:
        """Establece el ancho de la ventana."""
        self._validar_dimensiones(valor, self._height)
        self._width = valor
        self._ventana.geometry(f"{self._width}x{self._height}")

    @property
    def height(self) -> int:
        """Obtiene la altura de la ventana."""
        return self._height

    @height.setter
    def height(self, valor: int) -> None:
        """Establece la altura de la ventana."""
        self._validar_dimensiones(self._width, valor)
        self._height = valor
        self._ventana.geometry(f"{self._width}x{self._height}")

    @property
    def title(self) -> str:
        """Obtiene el título de la ventana."""
        return self._title

    @title.setter
    def title(self, valor: str) -> None:
        """Establece el título de la ventana."""
        self._validar_titulo(valor)
        self._title = valor
        self._ventana.title(self._title)

    @property
    def ventana(self) -> ctk.CTk:
        """Obtiene la instancia de la ventana customtkinter."""
        return self._

    @property
    def fuente(self) -> ctk.CTkFont:
        """Obtiene la fuente de la ventana."""
        return self._fuente

    @fuente.setter
    def fuente(self, valor: ctk.CTkFont) -> None:
        """Establece la fuente de la ventana."""
        self._validar_fuente(valor)
        self._fuente = valor
