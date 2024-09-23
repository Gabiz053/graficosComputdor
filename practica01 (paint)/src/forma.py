"""
Archivo: forma.py

Este archivo define las distintas formas que se pueden pintar en el lienzo.
Utiliza el patron Composite para organizar y crear estas formas.

Autor: Gabriel Gomez Garcia
Fecha: 23 de septiembre de 2024
"""

from abc import ABC, abstractmethod
from typing import List

from constantes import Error, Default


class ObjetoDibujo(ABC):
    """
    Clase base abstracta para todos los objetos de dibujo.

    Esta clase define la estructura general que deben seguir todos los
    objetos de dibujo, obligando a las subclases a implementar el metodo
    'dibujar' para aparecer en el dibujo.
    """

    def __init__(
        self,
        color: str = Default.COLOR,
        tamanho: int = Default.TAMANHO_DIBUJAR,
        herramienta: str = Default.HERRAMIENTA,
    ):
        """Inicializa un objeto de dibujo con color y tamanho de trazo.

        Args:
            color: Color del objeto de dibujo.
            tamanho: Tamaño del objeto de dibujo.
            herramienta: Herramienta utilizada para dibujar.
        """
        self._color = color
        self._tamanho = tamanho
        self._herramienta = herramienta

    @property
    def color(self) -> str:
        """Getter para el color del objeto de dibujo."""
        return self._color

    @color.setter
    def color(self, valor: str):
        """Setter para el color del objeto de dibujo."""
        self._color = valor

    @property
    def tamanho(self) -> int:
        """Getter para el tamanho del objeto de dibujo."""
        return self._tamanho

    @tamanho.setter
    def tamanho(self, valor: int):
        """Setter para el tamanho del objeto de dibujo."""
        self._tamanho = valor

    @property
    def herramienta(self) -> str:
        """Getter para la herramienta utilizada en el dibujo."""
        return self._herramienta

    @herramienta.setter
    def herramienta(self, valor: str):
        """Setter para la herramienta utilizada en el dibujo."""
        self._herramienta = valor

    @abstractmethod
    def dibujar(self):
        """
        Metodo abstracto que debe ser implementado por las subclases.

        Este metodo contiene la logica necesaria para representar graficamente
        el objeto de dibujo en el lienzo.
        """
        raise NotImplementedError(Error.NO_IMPLEMENTADO)


class Punto(ObjetoDibujo):
    """Clase que representa un punto en un espacio bidimensional."""

    def __init__(
        self,
        x: int,
        y: int,
        color: str = Default.COLOR,
        tamanho: int = Default.TAMANHO_DIBUJAR,
        herramienta: str = Default.HERRAMIENTA,
    ):
        """Inicializa el punto con las coordenadas x e y, color y tamanho.

        Args:
            x: Coordenada horizontal del punto.
            y: Coordenada vertical del punto.
            color: Color del punto.
            tamanho: Tamaño del punto.
        """
        super().__init__(color, tamanho, herramienta)
        self._x = x
        self._y = y

    def __str__(self):
        """Devuelve una representacion en cadena del punto."""
        return f"Punto({self.x}, {self.y}) de color {self.color} con {self.herramienta}"

    def dibujar(self):
        """Pinta el punto en el lienzo."""
        # TODO: Implementar la logica para dibujar el punto en el lienzo

    @property
    def x(self) -> int:
        """Getter para la coordenada x."""
        return self._x

    @x.setter
    def x(self, valor: int):
        """Setter para la coordenada x."""
        self._x = valor

    @property
    def y(self) -> int:
        """Getter para la coordenada y."""
        return self._y

    @y.setter
    def y(self, valor: int):
        """Setter para la coordenada y."""
        self._y = valor


class Linea(ObjetoDibujo):
    """Clase que representa una linea definida por dos puntos."""

    def __init__(
        self,
        punto_inicial: Punto,
        punto_final: Punto,
        color: str = Default.COLOR,
        tamanho: int = Default.TAMANHO_DIBUJAR,
        herramienta: str = Default.HERRAMIENTA,
    ):
        """Inicializa la linea con un punto inicial, un punto final, color, tamanho y herramienta.

        Args:
            punto_inicial: El primer punto que define el inicio de la linea.
            punto_final: El segundo punto que define el final de la linea.
            color: Color de la linea.
            tamanho: Tamaño de la linea.
            herramienta: Herramienta utilizada para dibujar la linea.
        """
        super().__init__(color, tamanho, herramienta)
        self._punto_inicial = punto_inicial
        self._punto_final = punto_final

    def __str__(self):
        """Devuelve una representacion en cadena de la linea."""
        return f"Línea desde {self.punto_inicial} hasta {self.punto_final} de color {self.color}"
    @property
    def punto_inicial(self) -> Punto:
        """Getter para el punto inicial de la linea."""
        return self._punto_inicial

    @punto_inicial.setter
    def punto_inicial(self, valor: Punto):
        """Setter para el punto inicial de la linea."""
        self._punto_inicial = valor

    @property
    def punto_final(self) -> Punto:
        """Getter para el punto final de la linea."""
        return self._punto_final

    @punto_final.setter
    def punto_final(self, valor: Punto):
        """Setter para el punto final de la linea."""
        self._punto_final = valor

    def dibujar(self):
        """Dibuja una linea en el lienzo."""
        # TODO: Implementar la logica para dibujar la linea en el lienzo


class Figura(ObjetoDibujo):
    """Clase que representa una coleccion de objetos de dibujo."""

    def __init__(self):
        """Inicializa una coleccion vacia para almacenar objetos de dibujo."""
        self._elementos: List[ObjetoDibujo] = []

    def anhadir(self, elemento):
        """
        Agrega un objeto de dibujo a la coleccion.

        Args:
            elemento: Un objeto que es instancia de ObjetoDibujo.
            Este objeto sera añadido a la coleccion de elementos.
        """
        self._elementos.append(elemento)

    def dibujar(self):
        """
        Dibuja todos los objetos en la coleccion.

        Este metodo itera sobre todos los elementos de la coleccion y
        llama a su metodo 'dibujar'.
        """
        for elemento in self._elementos:
            elemento.dibujar()
