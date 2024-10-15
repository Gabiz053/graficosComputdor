"""
Archivo: forma.py

Este archivo define las distintas formas que se pueden pintar en el lienzo.
Utiliza el patrón Composite para organizar y crear estas formas.

Autor: Gabriel Gomez Garcia
Fecha: 23 de septiembre de 2024
"""

# Imports externos
from abc import ABC, abstractmethod

# Imports de terceros
import numpy as np
from tkinter import Canvas

# Imports locales
from algoritmos_dibujo import AlgoritmoDibujo
from constantes import Default, ErrorMessages
from punto import Punto


class ObjetoDibujo(ABC):
    """
    Clase base abstracta para todos los objetos de dibujo.

    Esta clase define la estructura general que deben seguir todos los
    objetos de dibujo, obligando a las subclases a implementar el método
    'dibujar' para aparecer en el dibujo.
    """

    def __init__(
        self,
        lienzo: Canvas,
        color: str = Default.DRAWING_COLOR,
        herramienta: AlgoritmoDibujo = Default.DRAWING_TOOL,
        tamanho: int = Default.DRAWING_SIZE,
    ):
        """
        Inicializa un objeto de dibujo con color y tamaño de trazo.

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

    # Getters y setters
    @property
    def lienzo(self) -> Canvas:
        return self._lienzo

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, valor: str):
        self._color = valor

    @property
    def herramienta(self) -> AlgoritmoDibujo:
        return self._herramienta

    @herramienta.setter
    def herramienta(self, valor: AlgoritmoDibujo):
        self._herramienta = valor

    @property
    def tamanho(self) -> int:
        return self._tamanho

    @tamanho.setter
    def tamanho(self, valor: int):
        self._tamanho = valor

    # Métodos abstractos
    @abstractmethod
    def dibujar(self) -> list:
        """Método abstracto para dibujar el objeto en el lienzo."""
        raise NotImplementedError(ErrorMessages.NOT_IMPLEMENTED)

    @abstractmethod
    def mover(self, dx: int, dy: int):
        """Método abstracto para mover el objeto de dibujo."""
        raise NotImplementedError(ErrorMessages.NOT_IMPLEMENTED)
    
    def borrar(self) -> bool:
        """Método abstracto para borrar el objeto de dibujo."""
        raise NotImplementedError(ErrorMessages.NOT_IMPLEMENTED)
    
    def cambiar_color(self):
        """Método abstracto para cambiar color del el objeto de dibujo."""
        raise NotImplementedError(ErrorMessages.NOT_IMPLEMENTED)
    
    def cambiar_outline(self):
        """Método abstracto para cambiar el outline del objeto de dibujo al seleccioanrlo."""
        raise NotImplementedError(ErrorMessages.NOT_IMPLEMENTED)


class Linea(ObjetoDibujo):
    """Clase que representa una línea definida por dos puntos."""

    def __init__(
        self,
        punto_inicial: Punto,
        punto_final: Punto,
        lienzo: Canvas,
        color: str = Default.DRAWING_COLOR,
        herramienta: AlgoritmoDibujo = Default.DRAWING_TOOL,
        tamanho: int = Default.DRAWING_SIZE,
    ):
        """
        Inicializa la línea con dos puntos, color, tamaño y herramienta.

        Args:
            punto_inicial (Punto): El primer punto que define el inicio de la línea.
            punto_final (Punto): El segundo punto que define el final de la línea.
            lienzo (Canvas): La instancia de lienzo principal de tkinter.
            color (str): Color de la línea.
            herramienta (AlgoritmoDibujo): Herramienta utilizada para dibujar la línea.
            tamanho (int): Tamaño de la línea.
        """
        super().__init__(lienzo, color, herramienta, tamanho)
        self._puntos: np.ndarray = np.array(
            [[punto_inicial.x, punto_inicial.y], [punto_final.x, punto_final.y]]
        )
        self._puntos_dibujados = [] # lista de id de puntos que se han dibujado

    def __str__(self) -> str:
        """Devuelve una representación en cadena de la línea."""
        return f"Línea de color {self.color} desde {self.punto_inicial} hasta {self.punto_final}"

    # Getters
    @property
    def punto_inicial(self) -> Punto:
        return Punto(self._puntos[0][0], self._puntos[0][1])

    @property
    def punto_final(self) -> Punto:
        return Punto(self._puntos[1][0], self._puntos[1][1])
    
    @property
    def puntos_dibujados(self) -> list[int]:
        """Obtiene la lista de IDs de puntos dibujados."""
        return self._puntos_dibujados

    @puntos_dibujados.setter
    def puntos_dibujados(self, ids: list[int]) -> None:
        """Establece la lista de IDs de puntos dibujados."""
        self._puntos_dibujados = ids

    # Métodos principales
    def dibujar(self) -> list:
        """Dibuja una línea en el lienzo."""
        lista_puntos, self._puntos_dibujados = self.herramienta.dibujar_linea(
            self.lienzo, self.color, self.tamanho, *self._puntos.flatten()
        )
        return lista_puntos

    def mover(self, dx: int, dy: int) -> None:
        """Mueve la línea desplazando ambos puntos."""
        self.borrar()
        self._puntos += np.array([[dx, dy]])
        self.dibujar()
        
    def borrar(self) -> bool:
        """Borra los puntos dibujados del lienzo."""
        if len(self.puntos_dibujados) == 0:
            return False
        for punto_id in self.puntos_dibujados:
            self.lienzo.delete(punto_id)
        return True
    
    def cambiar_color(self, color):
        self._color = color
        for punto in self._puntos_dibujados:
            self._lienzo.itemconfig(punto, fill=color, outline=color)

    def cambiar_outline(self, color):
        """
        Cambia el outline de la línea para resaltar cuando está seleccionada.
        """
        for punto in self._puntos_dibujados:
            self._lienzo.itemconfig(punto, outline=color)  # Cambia el outline a un color específico

class Puntos(ObjetoDibujo):
    """Clase que representa una figura geométrica formada por varios puntos."""

    def __init__(self, puntos: list[Punto]):
        """
        Inicializa una figura con una lista de puntos.

        Args:
            puntos (list[Punto]): Lista de puntos que forman la figura.
        """
        if len(puntos) < 3:
            raise ValueError("Una figura debe tener al menos 3 puntos.")
        self._puntos = puntos

    def __str__(self) -> str:
        """Devuelve una representación en cadena de la figura mostrando sus puntos."""
        return f"Figura con {len(self._puntos)} puntos: " + ", ".join(
            [str(punto) for punto in self._puntos]
        )

    # Getters
    def obtener_puntos(self) -> list[Punto]:
        """Devuelve una lista con los puntos que forman la figura."""
        return self._puntos.copy()

    # Métodos principales
    def agregar_punto(self, punto: Punto) -> None:
        """Agrega un nuevo punto a la figura."""
        self._puntos.append(punto)

    def obtener_punto(self, indice: int) -> Punto:
        """Devuelve el punto en la posición indicada."""
        if 0 <= indice < len(self._puntos):
            return self._puntos[indice]
        else:
            raise IndexError("Índice fuera de rango.")

    def transformar(self, matriz_transformacion: np.ndarray) -> None:
        """Aplica una transformación a todos los puntos de la figura."""
        for punto in self._puntos:
            nuevas_coordenadas = np.dot(
                matriz_transformacion, punto.obtener_coordenadas()
            )
            punto._set_coordenadas(nuevas_coordenadas)


class Figura(ObjetoDibujo):
    """Clase que representa una colección de objetos de dibujo."""

    def __init__(self):
        """Inicializa una colección vacía para almacenar objetos de dibujo."""
        self._elementos: list[ObjetoDibujo] = []

    # Métodos principales
    def dibujar(self) -> None:
        """Dibuja todos los objetos en la colección."""
        for elemento in self._elementos:
            elemento.dibujar()

    def mover(self, dx: int, dy: int) -> None:
        """Mueve todos los elementos de la colección."""
        for elemento in self._elementos:
            elemento.mover(dx, dy)

    def anhadir(self, elemento: ObjetoDibujo) -> None:
        """Agrega un objeto de dibujo a la colección."""
        self._elementos.append(elemento)

    def eliminar(self, elemento: ObjetoDibujo) -> bool:
        """Elimina un objeto de dibujo específico de la colección."""
        elemento.borrar()  # Intenta borrar del lienzo
        return True
        
    def eliminar_todo(self) -> None:
        """Elimina todos los objetos de la colección."""
        self._elementos.clear()
        
    def cambiar_color(self, color):
        """Cambia el color de todos los elementos de la colección."""
        for elemento in self._elementos:
            elemento.cambiar_color(color)
            
    def desagrupar(self):
        """Desagrupa los elementos devolviéndolos a la lista general de figuras."""
        return self._elementos[:]
    
    def cambiar_outline(self, color):
        """
        Cambia el outline de todos los elementos en la figura.
        """
        for elemento in self._elementos:
            elemento.cambiar_outline(color)  # Llama al método de cada elemento
            
    def borrar(self) -> bool:
        """Borra cada linea."""
        for elemento in self._elementos:
            elemento.borrar()
        self.eliminar_todo()
        
        return True
    
    # Métodos para iteración
    def __iter__(self):
        """Devuelve un iterador para las figuras."""
        self._indice = 0  # Inicializa el índice
        return self

    def __next__(self) -> ObjetoDibujo:
        """Devuelve la siguiente figura o levanta StopIteration."""
        if self._indice < len(self._elementos):
            figura = self._elementos[self._indice]
            self._indice += 1
            return figura
        else:
            raise StopIteration  # Fin de la iteración
