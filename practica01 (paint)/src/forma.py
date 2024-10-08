"""
Archivo: forma.py

Este archivo define las distintas formas que se pueden pintar en el lienzo.
Utiliza el patron Composite para organizar y crear estas formas.

Autor: Gabriel Gomez Garcia
Fecha: 23 de septiembre de 2024
"""

from abc import ABC, abstractmethod
import numpy as np
from tkinter import Canvas
from algoritmos_dibujo import AlgoritmoDibujo
from constantes import Error, Default
from punto import Punto


class ObjetoDibujo(ABC):
    """
    Clase base abstracta para todos los objetos de dibujo.

    Esta clase define la estructura general que deben seguir todos los
    objetos de dibujo, obligando a las subclases a implementar el metodo
    'dibujar' para aparecer en el dibujo.
    """

    def __init__(
        self,
        lienzo: Canvas,
        color: str = Default.COLOR,
        herramienta: AlgoritmoDibujo = Default.HERRAMIENTA,
        tamanho: int = Default.TAMANHO_DIBUJAR,
    ):
        """Inicializa un objeto de dibujo con color y tamanho de trazo.

        Args:
            lienzo (Canvas): La instancia de lienzo principal de tkinter.
            color (str): Color del objeto de dibujo.
            herramienta (AlgoritmoDibujo): Herramienta utilizada para dibujar.
            tamanho (int): Tamaño del objeto de dibujo.
        """
        self._lienzo = lienzo
        self._color = color
        self._herramienta = herramienta
        self._tamanho = tamanho

    @property
    def lienzo(self) -> Canvas:
        """Getter para el lienzo del objeto de dibujo."""
        return self._lienzo

    @property
    def color(self) -> str:
        """Getter para el color del objeto de dibujo."""
        return self._color

    @color.setter
    def color(self, valor: str):
        """Setter para el color del objeto de dibujo."""
        self._color = valor

    @property
    def herramienta(self) -> AlgoritmoDibujo:
        """Getter para la herramienta utilizada en el dibujo."""
        return self._herramienta

    @herramienta.setter
    def herramienta(self, valor: AlgoritmoDibujo):
        """Setter para la herramienta utilizada en el dibujo."""
        self._herramienta = valor

    @property
    def tamanho(self) -> int:
        """Getter para el tamanho del objeto de dibujo."""
        return self._tamanho

    @tamanho.setter
    def tamanho(self, valor: int):
        """Setter para el tamanho del objeto de dibujo."""
        self._tamanho = valor

    @abstractmethod
    def dibujar(self):
        """
        Metodo abstracto que debe ser implementado por las subclases.

        Este metodo contiene la logica necesaria para representar graficamente
        el objeto de dibujo en el lienzo.
        """
        raise NotImplementedError(Error.NO_IMPLEMENTADO)

    @abstractmethod
    def mover(self, dx: int, dy: int):
        """
        Metodo abstracto para mover el objeto de dibujo.

        Args:
            dx (int): El desplazamiento en el eje x.
            dy (int): El desplazamiento en el eje y.
        """
        raise NotImplementedError(Error.NO_IMPLEMENTADO)


class Linea(ObjetoDibujo):
    """Clase que representa una linea definida por dos puntos."""

    def __init__(
        self,
        punto_inicial: Punto,
        punto_final: Punto,
        lienzo: Canvas,
        color: str = Default.COLOR,
        herramienta: AlgoritmoDibujo = Default.HERRAMIENTA,
        tamanho: int = Default.TAMANHO_DIBUJAR,
    ):
        """Inicializa la linea con dos puntos, color, tamaño y herramienta.

        Args:
            punto_inicial (Punto): El primer punto que define el inicio de la linea.
            punto_final (Punto): El segundo punto que define el final de la linea.
            lienzo (Canvas): La instancia de lienzo principal de tkinter.
            color (str): Color de la linea.
            herramienta (AlgoritmoDibujo): Herramienta utilizada para dibujar la linea.
            tamanho (int): Tamaño de la linea.
        """
        super().__init__(lienzo, color, herramienta, tamanho)
        self._puntos: np.ndarray = np.array(
            [[punto_inicial.x, punto_inicial.y], [punto_final.x, punto_final.y]]
        )

    def __str__(self) -> str:
        """Devuelve una representacion en cadena de la linea."""
        return f"Linea de color {self.color} desde {self.punto_inicial} hasta {self.punto_final}"

    @property
    def punto_inicial(self) -> Punto:
        """Getter para el punto inicial de la linea."""
        return Punto(self._puntos[0][0], self._puntos[0][1])

    @property
    def punto_final(self) -> Punto:
        """Getter para el punto final de la linea."""
        return Punto(self._puntos[1][0], self._puntos[1][1])

    def dibujar(self) -> None:
        """Dibuja una linea en el lienzo."""
        self.herramienta.dibujar_linea(
            self.lienzo,
            self.color,
            self.tamanho,
            *self._puntos.flatten(),  # Descompone el array en argumentos
        )

    def mover(self, dx: int, dy: int) -> None:
        """
        Mueve la linea desplazando ambos puntos por dx y dy.

        Args:
            dx (int): El desplazamiento en el eje x.
            dy (int): El desplazamiento en el eje y.
        """
        self._puntos += np.array(
            [[dx, dy]]
        )  # Aplica el desplazamiento a todos los puntos
        self.actualizar_lienzo()

    def actualizar_lienzo(self) -> None:
        """Actualiza las coordenadas en el lienzo de Tkinter y dibuja la linea."""
        self.lienzo.coords(self, *self._puntos.flatten())
        self.dibujar()


class Figura(ObjetoDibujo):
    """Clase que representa una coleccion de objetos de dibujo."""

    def __init__(self):
        """Inicializa una coleccion vacia para almacenar objetos de dibujo."""
        self._elementos: list[ObjetoDibujo] = []

    def __iter__(self):
        """Devuelve un iterador para las figuras."""
        self._indice = 0  # Inicializa el indice
        return self

    def __next__(self) -> ObjetoDibujo:
        """Devuelve la siguiente figura o levanta StopIteration."""
        if self._indice < len(self._elementos):
            figura = self._elementos[self._indice]
            self._indice += 1
            return figura
        else:
            raise StopIteration  # Fin de la iteracion

    def dibujar(self) -> None:
        """
        Dibuja todos los objetos en la coleccion.

        Este metodo itera sobre todos los elementos de la coleccion y
        llama a su metodo 'dibujar'.
        """
        for elemento in self._elementos:
            elemento.dibujar()

    def mover(self, dx: int, dy: int) -> None:
        """
        Mueve todos los elementos de la coleccion.

        Args:
            dx (int): El desplazamiento en el eje x.
            dy (int): El desplazamiento en el eje y.
        """
        for elemento in self._elementos:
            elemento.mover(dx, dy)

    def anhadir(self, elemento: ObjetoDibujo) -> None:
        """
        Agrega un objeto de dibujo a la coleccion.

        Args:
            elemento (ObjetoDibujo): Un objeto que es instancia de ObjetoDibujo.
            Este objeto sera añadido a la coleccion de elementos.
        """
        self._elementos.append(elemento)

    def eliminar(self, elemento: ObjetoDibujo) -> bool:
        """
        Elimina un objeto de dibujo específico de la coleccion.

        Args:
            elemento (ObjetoDibujo): El objeto que se desea eliminar.

        Returns:
            bool: True si el objeto fue eliminado, False si no se encontro.
        """
        if elemento in self._elementos:
            self._elementos.remove(elemento)
            return True
        return False

    def eliminar_todo(self) -> None:
        """
        Elimina todos los objetos de la coleccion.

        Este metodo vacia la coleccion de elementos.
        """
        self._elementos.clear()
