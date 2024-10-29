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
from transformaciones import Transformacion


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

    @abstractmethod
    def transformar(self, transformaciones: dict) -> None:
        """Aplica las transformaciones especificadas al objeto de dibujo.

        Args:
            transformaciones (dict): Diccionario con transformaciones a aplicar.
        """
        raise NotImplementedError(ErrorMessages.NOT_IMPLEMENTED)

class Linea(ObjetoDibujo):
    pass

class Poligono(ObjetoDibujo):
    """Clase que representa un polígono definido por varios puntos."""

    def __init__(
        self,
        lista_puntos: list[Punto],
        lienzo: Canvas,
        color: str = Default.DRAWING_COLOR,
        herramienta: AlgoritmoDibujo = Default.DRAWING_TOOL,
        tamanho: int = Default.DRAWING_SIZE,
    ) -> None:
        """
        Inicializa el polígono con una lista de puntos.

        Args:
            lista_puntos (list[Punto]): Lista de puntos que definen el polígono.
            lienzo (Canvas): La instancia de lienzo principal de tkinter.
            color (str): Color del polígono.
            herramienta (AlgoritmoDibujo): Herramienta utilizada para dibujar.
            tamanho (int): Tamaño del polígono.
        """
        super().__init__(lienzo, color, herramienta, tamanho)
        # Representar puntos como columnas
        self._puntos: np.ndarray = np.array(
            [[punto.x for punto in lista_puntos], [punto.y for punto in lista_puntos]]
        )
        self._puntos_dibujados: list[int] = []

    def __str__(self) -> str:
        """Devuelve una representación en cadena del polígono."""
        puntos_str = ", ".join(
            f"({x}, {y})" for x, y in zip(self._puntos[0], self._puntos[1])
        )
        return f"Polígono con puntos: {puntos_str}"

    @property
    def puntos(self) -> np.ndarray:
        """Obtiene la matriz de puntos como columnas."""
        return self._puntos

    @puntos.setter
    def puntos(self, nueva_matriz: np.ndarray) -> None:
        """Establece una nueva matriz de puntos.

        Args:
            nueva_matriz (np.ndarray): Nueva matriz de puntos en formato columna.
        """
        if nueva_matriz.shape[0] != 2:
            raise ValueError("La matriz debe tener exactamente 2 filas (x y y).")
        self._puntos = nueva_matriz

    def cambiar_punto(self, indice: int, nuevo_punto: Punto) -> None:
        """Cambia un punto específico en el polígono.

        Args:
            indice (int): Índice del punto a cambiar.
            nuevo_punto (Punto): Nuevo punto que reemplazará al existente.
        """
        if 0 <= indice < self._puntos.shape[1]:
            self._puntos[0, indice] = nuevo_punto.x
            self._puntos[1, indice] = nuevo_punto.y
        else:
            raise IndexError("Índice fuera de rango para los puntos del polígono.")

    def dibujar(self) -> list:
        """Dibuja el polígono en el lienzo.

        Returns:
            list: Lista de IDs de los elementos dibujados.
        """
        lista_puntos = []
        num_puntos = self._puntos.shape[1]  # Número de puntos en columnas

        for i in range(num_puntos):
            p1 = self._puntos[:, i]  # Obtener el i-ésimo punto como columna
            p2 = self._puntos[:, (i + 1) % num_puntos]  # Conectar al siguiente punto
            id_dibujo = self.herramienta.dibujar_linea(
                self.lienzo, self.color, self.tamanho, *p1, *p2
            )
            lista_puntos.extend(id_dibujo)

        self.puntos_dibujados = lista_puntos
        return lista_puntos

    def borrar(self) -> bool:
        """Borra los puntos dibujados del lienzo.

        Returns:
            bool: True si se borró con éxito, False si no había puntos que borrar.
        """
        if len(self._puntos_dibujados) == 0:
            return False
        for punto_id in self._puntos_dibujados:
            self.lienzo.delete(punto_id)
        self._puntos_dibujados.clear()  # Limpia la lista después de borrar
        return True

    def cambiar_color(self, color: str) -> None:
        """Cambia el color del polígono.

        Args:
            color (str): El nuevo color del polígono.
        """
        self.color = color
        for punto_id in self.puntos_dibujados:
            self.lienzo.itemconfig(punto_id, fill=color, outline=color)

    def cambiar_outline(self, color: str) -> None:
        """Cambia el outline del polígono para resaltar cuando está seleccionado.

        Args:
            color (str): El nuevo color del outline.
        """
        for punto_id in self.puntos_dibujados:
            self.lienzo.itemconfig(punto_id, outline=color)

    def transformar(self, transformaciones: dict) -> Transformacion:
        """
        Aplica todas las transformaciones a los puntos del polígono.

        Args:
            transformaciones (dict): Diccionario que contiene las transformaciones a aplicar al polígono.
            Las claves del diccionario pueden incluir:
                - 'traslacion': Parámetros para mover el polígono en el espacio.
                - 'escalado': Parámetros para cambiar el tamaño del polígono.
                - 'rotacion': Parámetros para rotar el polígono en torno a un punto.
                - 'shearing': Parámetros para deformar el polígono en un eje específico.

        Returns:
            Transformacion: Un objeto de la clase Transformacion que encapsula las transformaciones aplicadas.
            Este objeto puede ser utilizado posteriormente para revertir las transformaciones o realizar
            cálculos adicionales si es necesario.
        """
        # Crear un objeto de Transformacion utilizando el diccionario de transformaciones
        aplicacion_transformaciones = Transformacion(transformaciones)
        
        # como se va a mover hay que borrar y bolver a dibujar
        self.borrar()
        aplicacion_transformaciones.transformar(self._puntos)
        self.dibujar()
        
        # Retornar el objeto de transformaciones, que puede ser utilizado para otros fines
        return aplicacion_transformaciones

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

    def transformar(self, transformaciones: dict) -> None:
        """Aplica todas las transformaciones a todos los elementos de la figura utilizando operaciones matriciales.

        Args:
            transformaciones (dict): Diccionario con las transformaciones a aplicar.
        """
        for elemento in self._elementos:
            if isinstance(
                elemento, Poligono
            ):  # Asegúrate de que el elemento es un Polígono
                elemento.transformar(transformaciones)
            # Aquí puedes añadir otras condiciones si tienes más tipos de elementos que necesiten transformaciones.

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
