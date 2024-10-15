"""
Archivo: forma.py

Este archivo define las distintas formas que se pueden pintar en el lienzo.
Utiliza el patron Composite para organizar y crear estas formas.

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
    objetos de dibujo, obligando a las subclases a implementar los metodos
    'dibujar', 'mover', 'borrar', 'cambiar_color' y 'cambiar_outline'
    para aparecer y comportarse correctamente en el dibujo.
    """

    def __init__(
        self,
        lienzo: Canvas,
        color: str = Default.DRAWING_COLOR,
        herramienta: AlgoritmoDibujo = Default.DRAWING_TOOL,
        tamanho: int = Default.DRAWING_SIZE,
    ) -> None:
        """
        Inicializa un objeto de dibujo con color y tamano de trazo.

        Args:
            lienzo (Canvas): La instancia de lienzo principal de tkinter.
            color (str): Color del objeto de dibujo.
            herramienta (AlgoritmoDibujo): Herramienta utilizada para dibujar.
            tamanho (int): Tamano del objeto de dibujo.
        """
        self._lienzo = lienzo
        self._color = color
        self._herramienta = herramienta
        self._tamanho = tamanho

    # Getters y setters
    @property
    def lienzo(self) -> Canvas:
        """Obtiene el lienzo en el que se dibuja el objeto."""
        return self._lienzo

    @property
    def color(self) -> str:
        """Obtiene el color del objeto de dibujo."""
        return self._color

    @color.setter
    def color(self, valor: str) -> None:
        """Establece el color del objeto de dibujo.

        Args:
            valor (str): El nuevo color del objeto.
        """
        self._color = valor

    @property
    def herramienta(self) -> AlgoritmoDibujo:
        """Obtiene la herramienta utilizada para dibujar."""
        return self._herramienta

    @herramienta.setter
    def herramienta(self, valor: AlgoritmoDibujo) -> None:
        """Establece la herramienta utilizada para dibujar.

        Args:
            valor (AlgoritmoDibujo): La nueva herramienta para dibujar.
        """
        self._herramienta = valor

    @property
    def tamanho(self) -> int:
        """Obtiene el tamano del objeto de dibujo."""
        return self._tamanho

    @tamanho.setter
    def tamanho(self, valor: int) -> None:
        """Establece el tamano del objeto de dibujo.

        Args:
            valor (int): El nuevo tamano del objeto.
        """
        self._tamanho = valor

    # Metodos abstractos
    @abstractmethod
    def dibujar(self) -> list:
        """Metodo abstracto para dibujar el objeto en el lienzo.

        Debe ser implementado por las subclases para realizar la
        representacion grafica del objeto.
        """
        raise NotImplementedError(ErrorMessages.NOT_IMPLEMENTED)

    @abstractmethod
    def mover(self, dx: int, dy: int) -> None:
        """Metodo abstracto para mover el objeto de dibujo.

        Args:
            dx (int): Desplazamiento en el eje x.
            dy (int): Desplazamiento en el eje y.
        """
        raise NotImplementedError(ErrorMessages.NOT_IMPLEMENTED)

    @abstractmethod
    def borrar(self) -> bool:
        """Metodo abstracto para borrar el objeto de dibujo.

        Returns:
            bool: True si el objeto fue borrado correctamente, False si no habia nada que borrar.
        """
        raise NotImplementedError(ErrorMessages.NOT_IMPLEMENTED)

    @abstractmethod
    def cambiar_color(self, color: str) -> None:
        """Metodo abstracto para cambiar el color del objeto de dibujo.

        Args:
            color (str): El nuevo color para el objeto de dibujo.
        """
        raise NotImplementedError(ErrorMessages.NOT_IMPLEMENTED)

    @abstractmethod
    def cambiar_outline(self, color: str) -> None:
        """Metodo abstracto para cambiar el outline del objeto de dibujo al seleccionarlo.

        Args:
            color (str): El nuevo color del outline para resaltar el objeto.
        """
        raise NotImplementedError(ErrorMessages.NOT_IMPLEMENTED)


class Linea(ObjetoDibujo):
    """Clase que representa una linea definida por dos puntos."""

    def __init__(
        self,
        punto_inicial: Punto,
        punto_final: Punto,
        lienzo: Canvas,
        color: str = Default.DRAWING_COLOR,
        herramienta: AlgoritmoDibujo = Default.DRAWING_TOOL,
        tamanho: int = Default.DRAWING_SIZE,
    ) -> None:
        """
        Inicializa la linea con dos puntos, color, tamano y herramienta.

        Args:
            punto_inicial (Punto): El primer punto que define el inicio de la linea.
            punto_final (Punto): El segundo punto que define el final de la linea.
            lienzo (Canvas): La instancia de lienzo principal de tkinter.
            color (str): Color de la linea.
            herramienta (AlgoritmoDibujo): Herramienta utilizada para dibujar la linea.
            tamanho (int): Tamano de la linea.
        """
        super().__init__(lienzo, color, herramienta, tamanho)
        self._puntos: np.ndarray = np.array(
            [[punto_inicial.x, punto_inicial.y], [punto_final.x, punto_final.y]]
        )
        self._puntos_dibujados: list[int] = (
            []
        )  # Lista de IDs de puntos que se han dibujado

    def __str__(self) -> str:
        """Devuelve una representacion en cadena de la linea."""
        return f"Linea de color {self.color} desde {self.punto_inicial} hasta {self.punto_final}"

    # Getters
    @property
    def punto_inicial(self) -> Punto:
        """Obtiene el punto inicial de la linea."""
        return Punto(self._puntos[0][0], self._puntos[0][1])

    @property
    def punto_final(self) -> Punto:
        """Obtiene el punto final de la linea."""
        return Punto(self._puntos[1][0], self._puntos[1][1])

    @property
    def puntos_dibujados(self) -> list[int]:
        """Obtiene la lista de IDs de puntos dibujados."""
        return self._puntos_dibujados

    @puntos_dibujados.setter
    def puntos_dibujados(self, ids: list[int]) -> None:
        """Establece la lista de IDs de puntos dibujados.

        Args:
            ids (list[int]): Lista de IDs de puntos dibujados.
        """
        self._puntos_dibujados = ids

    # Metodos principales
    def dibujar(self) -> list:
        """Dibuja una linea en el lienzo.

        Returns:
            list: Lista de IDs de los elementos dibujados.
        """
        lista_puntos, self._puntos_dibujados = self.herramienta.dibujar_linea(
            self.lienzo, self.color, self.tamanho, *self._puntos.flatten()
        )
        return lista_puntos

    def mover(self, dx: int, dy: int) -> None:
        """Mueve la linea desplazando ambos puntos.

        Args:
            dx (int): Desplazamiento en el eje x.
            dy (int): Desplazamiento en el eje y.
        """
        self.borrar()
        self._puntos += np.array([[dx, dy]])
        self.dibujar()

    def borrar(self) -> bool:
        """Borra los puntos dibujados del lienzo.

        Returns:
            bool: True si se borro con exito, False si no habia puntos que borrar.
        """
        if len(self._puntos_dibujados) == 0:
            return False
        for punto_id in self._puntos_dibujados:
            self.lienzo.delete(punto_id)
        return True

    def cambiar_color(self, color: str) -> None:
        """Cambia el color de la linea.

        Args:
            color (str): El nuevo color de la linea.
        """
        self.color = color
        for punto in self._puntos_dibujados:
            self.lienzo.itemconfig(punto, fill=color, outline=color)

    def cambiar_outline(self, color: str) -> None:
        """Cambia el outline de la linea para resaltar cuando esta seleccionada.

        Args:
            color (str): El nuevo color del outline.
        """
        for punto in self._puntos_dibujados:
            self.lienzo.itemconfig(
                punto, outline=color
            )  # Cambia el outline a un color especifico


class Puntos(ObjetoDibujo):
    """Clase que representa una figura geometrica basada en puntos."""

    def __init__(
        self,
        lista_puntos: list[Punto],
        lienzo: Canvas,
        color: str = Default.DRAWING_COLOR,
        herramienta: AlgoritmoDibujo = Default.DRAWING_TOOL,
        tamanho: int = Default.DRAWING_SIZE,
    ) -> None:
        """
        Inicializa la figura geometrica con una lista de puntos.

        Args:
            lista_puntos (list[Punto]): Lista de puntos que definen la figura.
            lienzo (Canvas): La instancia de lienzo principal de tkinter.
            color (str): Color de los puntos.
            herramienta (AlgoritmoDibujo): Herramienta utilizada para dibujar.
            tamanho (int): Tamano de los puntos.
        """
        super().__init__(lienzo, color, herramienta, tamanho)
        self._lista_puntos: list[Punto] = lista_puntos
        self._puntos_dibujados: list[int] = []

    def __str__(self) -> str:
        """Devuelve una representacion en cadena de los puntos."""
        return f"Puntos: {', '.join(str(punto) for punto in self._lista_puntos)}"

    @property
    def lista_puntos(self) -> list[Punto]:
        """Obtiene la lista de puntos que componen la figura."""
        return self._lista_puntos

    @property
    def puntos_dibujados(self) -> list[int]:
        """Obtiene la lista de IDs de puntos dibujados."""
        return self._puntos_dibujados

    @puntos_dibujados.setter
    def puntos_dibujados(self, ids: list[int]) -> None:
        """Establece la lista de IDs de puntos dibujados.

        Args:
            ids (list[int]): Lista de IDs de puntos dibujados.
        """
        self._puntos_dibujados = ids

    def dibujar(self) -> list:
        """Dibuja la figura en el lienzo.

        Returns:
            list: Lista de IDs de los elementos dibujados.
        """
        self.puntos_dibujados = [
            self.lienzo.create_oval(
                punto.x - self.tamanho / 2,
                punto.y - self.tamanho / 2,
                punto.x + self.tamanho / 2,
                punto.y + self.tamanho / 2,
                fill=self.color,
                outline=self.color,
            )
            for punto in self.lista_puntos
        ]
        return self.puntos_dibujados

    def mover(self, dx: int, dy: int) -> None:
        """Mueve los puntos de la figura en el lienzo.

        Args:
            dx (int): Desplazamiento en el eje x.
            dy (int): Desplazamiento en el eje y.
        """
        self.borrar()
        for punto in self.lista_puntos:
            punto.x += dx
            punto.y += dy
        self.dibujar()

    def borrar(self) -> bool:
        """Borra los puntos dibujados del lienzo.

        Returns:
            bool: True si se borro con exito, False si no habia puntos que borrar.
        """
        if len(self.puntos_dibujados) == 0:
            return False
        for punto_id in self.puntos_dibujados:
            self.lienzo.delete(punto_id)
        return True

    def cambiar_color(self, color: str) -> None:
        """Cambia el color de los puntos.

        Args:
            color (str): El nuevo color de los puntos.
        """
        self.color = color
        for punto in self.puntos_dibujados:
            self.lienzo.itemconfig(punto, fill=color, outline=color)

    def cambiar_outline(self, color: str) -> None:
        """Cambia el outline de los puntos para resaltar cuando estan seleccionados.

        Args:
            color (str): El nuevo color del outline.
        """
        for punto in self.puntos_dibujados:
            self.lienzo.itemconfig(
                punto, outline=color
            )  # Cambia el outline a un color especifico


class Figura(ObjetoDibujo):
    """
    Representa una coleccion de objetos de dibujo, gestionando sus operaciones en conjunto.
    """

    def __init__(self) -> None:
        """Inicializa una coleccion vacia para objetos de dibujo."""
        self._elementos: list[ObjetoDibujo] = []

    # Getters y setters
    @property
    def elementos(self) -> list[ObjetoDibujo]:
        """Devuelve la lista de elementos en la coleccion."""
        return self._elementos

    @elementos.setter
    def elementos(self, nuevos_elementos: list[ObjetoDibujo]) -> None:
        """Permite establecer una nueva lista de elementos."""
        self._elementos = nuevos_elementos

    # Gestión de la colección
    def anhadir(self, elemento: ObjetoDibujo) -> None:
        """
        Agrega un objeto de dibujo a la coleccion.

        Args:
            elemento (ObjetoDibujo): El objeto a agregar.
        """
        self._elementos.append(elemento)

    def eliminar(self, elemento: ObjetoDibujo) -> bool:
        """
        Elimina un objeto especifico de la coleccion.

        Args:
            elemento (ObjetoDibujo): El objeto a eliminar.

        Returns:
            bool: True si se elimino con exito, False si no estaba presente.
        """
        elemento.borrar()  # Intenta borrar del lienzo
        return True

    def eliminar(self, elemento: ObjetoDibujo) -> bool:
        """Elimina un objeto de dibujo específico de la colección."""
        elemento.borrar()  # Intenta borrar del lienzo
        return True

    def eliminar_todo(self) -> None:
        """Elimina todos los objetos de la colección."""
        self._elementos.clear()

    def desagrupar(self) -> list[ObjetoDibujo]:
        """
        Devuelve todos los elementos de la coleccion y vacia la lista interna.

        Returns:
            list[ObjetoDibujo]: Lista de objetos de dibujo.
        """
        elementos = self._elementos.copy()
        self._elementos.clear()
        return elementos

    # Operaciones sobre los elementos
    def dibujar(self) -> None:
        """Dibuja todos los objetos de la coleccion."""
        for elemento in self._elementos:
            elemento.dibujar()

    def mover(self, dx: int, dy: int) -> None:
        """
        Mueve todos los elementos de la coleccion.

        Args:
            dx (int): Desplazamiento en el eje x.
            dy (int): Desplazamiento en el eje y.
        """
        for elemento in self._elementos:
            elemento.mover(dx, dy)

    def cambiar_color(self, color: str) -> None:
        """
        Cambia el color de todos los elementos de la coleccion.

        Args:
            color (str): El nuevo color para los elementos.
        """
        for elemento in self._elementos:
            elemento.cambiar_color(color)

    def cambiar_outline(self, color: str) -> None:
        """
        Cambia el outline de todos los elementos en la coleccion.

        Args:
            color (str): El nuevo color para resaltar el outline.
        """
        for elemento in self._elementos:
            elemento.cambiar_outline(color)

    def borrar(self) -> bool:
        """
        Borra cada objeto en la coleccion y elimina todos los elementos.

        Returns:
            bool: True si se borraron los elementos.
        """
        for elemento in self._elementos:
            elemento.borrar()
        self.eliminar_todo()
        return True

    # Iteración
    def __iter__(self) -> "Figura":
        """Devuelve un iterador para recorrer los elementos de la coleccion."""
        self._indice = 0
        return self

    def __next__(self) -> ObjetoDibujo:
        """Devuelve el siguiente objeto de dibujo o levanta StopIteration."""
        if self._indice < len(self._elementos):
            elemento = self._elementos[self._indice]
            self._indice += 1
            return elemento
        raise StopIteration
