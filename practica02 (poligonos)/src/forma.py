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


class Poligono(ObjetoDibujo):
    """Clase que representa un polígono definido por varios puntos."""

    def __init__(
        self,
        puntos: np.ndarray,
        lienzo: Canvas,
        color: str = Default.DRAWING_COLOR,
        herramienta: AlgoritmoDibujo = Default.DRAWING_TOOL,
        tamanho: int = Default.DRAWING_SIZE,
        rellenar: bool = True,
    ) -> None:
        """
        Inicializa el polígono con un array de puntos.

        Args:
            puntos (np.ndarray): Array de puntos (3 x n) que definen el polígono.
            lienzo (Canvas): La instancia de lienzo principal de tkinter.
            color (str): Color del polígono.
            herramienta (AlgoritmoDibujo): Herramienta utilizada para dibujar.
            tamanho (int): Tamaño del polígono.
        """
        super().__init__(lienzo, color, herramienta, tamanho)
        self._puntos: np.ndarray = puntos  # Asigna el array de puntos directamente
        self._puntos_contorno: list[int] = []
        self._puntos_relleno: list[int] = []
        self._rellenar = rellenar

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
        if nueva_matriz.shape[0] != 3:
            raise ValueError("La matriz debe tener exactamente 3 filas (x , y y todo 1).")
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
        """Dibuja el polígono en el lienzo y lo rellena en tiempo real.

        Returns:
            list: Lista de IDs de los elementos dibujados.
        """
        # Dibuja el contorno del polígono
        contorno_ids = self._dibujar_contorno()
        relleno_ids = []

        if self._rellenar:
            # Rellena el interior del polígono
            relleno_ids = self._rellenar_interior()

        # Combina ambos conjuntos de IDs para poder borrarlos después
        self._puntos_contorno = contorno_ids
        self._puntos_relleno = relleno_ids
        return self._puntos_contorno, self._puntos_relleno

    def _dibujar_contorno(self) -> list:
        """Dibuja el contorno del polígono en el lienzo.

        Returns:
            list: Lista de IDs de los elementos de contorno dibujados.
        """
        contorno_ids = []
        num_puntos = self._puntos.shape[1]

        for i in range(num_puntos):
            x1 = self._puntos[0, i]
            y1 = self._puntos[1, i]
            x2 = self._puntos[0, (i + 1) % num_puntos]
            y2 = self._puntos[1, (i + 1) % num_puntos]

            _, lista_dibujados = self.herramienta.dibujar_linea(
                self.lienzo, self.color, self.tamanho, x1, y1, x2, y2
            )
            contorno_ids.extend(lista_dibujados)

        return contorno_ids

    def _rellenar_interior(self) -> list:
        """Rellena el interior del polígono usando el método de escaneo de líneas.

        Returns:
            list: Lista de IDs de los elementos de relleno dibujados.
        """
        relleno_ids = []
        y_min = int(min(-self._puntos[1]))  # Cambia el signo de Y
        y_max = int(max(-self._puntos[1]))  # Cambia el signo de Y

        for y_scan in range(y_min, y_max + 1):
            intersecciones = self._calcular_intersecciones(-y_scan)  # Invertir y_scan

            for j in range(0, len(intersecciones) - 1, 2):
                x_start, x_end = intersecciones[j], intersecciones[j + 1]
                linea_id = self.lienzo.create_line(
                    x_start, y_scan, x_end, y_scan, fill=self.color
                )
                relleno_ids.append(linea_id)

        return relleno_ids
        # _, linea_dibujada = self.herramienta.dibujar_linea(
        #     self.lienzo, self.color, self.tamanho, x_start, y_scan, x_end, y_scan
        # )

        # Si quisiera usar mi metodo de pintar lineas para esto. pero va muy lento
        # asi que hago un pcoo de trampa y uso el del canvas

    def _calcular_intersecciones(self, y_scan: int) -> list:
        """Calcula las intersecciones de una línea horizontal con los lados del polígono.

        Args:
            y_scan (int): Coordenada Y de la línea de escaneo.

        Returns:
            list: Lista de coordenadas X donde se producen intersecciones.
        """
        intersecciones = []
        num_puntos = self._puntos.shape[1]

        for i in range(num_puntos):
            x1, y1 = self._puntos[0, i], self._puntos[1, i]
            x2, y2 = (
                self._puntos[0, (i + 1) % num_puntos],
                self._puntos[1, (i + 1) % num_puntos],
            )

            if (y1 <= y_scan < y2) or (y2 <= y_scan < y1):
                x_inter = x1 + (y_scan - y1) * (x2 - x1) / (y2 - y1)
                intersecciones.append(int(x_inter))

        intersecciones.sort()
        return intersecciones

    def borrar(self) -> bool:
        """Borra los puntos dibujados del lienzo.

        Returns:
            bool: True si se borró con éxito, False si no había puntos que borrar.
        """
        if len(self._puntos_contorno) == 0:
            return False
        for punto_id in self._puntos_contorno + self._puntos_relleno:
            self.lienzo.delete(punto_id)
        self._puntos_contorno.clear()  # Limpia la lista después de borrar
        self._puntos_relleno.clear()
        return True

    def cambiar_color(self, color: str) -> None:
        """Cambia el color del polígono."""
        self.color = color
        for punto_id in self._puntos_contorno + self._puntos_relleno:
            # Cambiar solo el color de relleno (para líneas y polígonos rellenos)
            try:
                self.lienzo.itemconfig(punto_id, fill=color)
            except Exception as e:
                # pass
                print(f"Error cambiando el color del elemento con ID {punto_id}: {e}")

    def cambiar_outline(self, color: str) -> None:
        """Cambia el contorno del polígono."""
        for punto_id in self._puntos_contorno:
            try:
                # Cambiar solo el color del contorno (para polígonos)
                self.lienzo.itemconfig(punto_id, outline=color)
            except Exception as e:
                # pass
                print(f"Error cambiando el outline del elemento con ID {punto_id}: {e}")

    def transformar(self, transformaciones: dict) -> list:
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
        # print(transformaciones)
        aplicacion_transformaciones = Transformacion(transformaciones, self._puntos)

        # Borrar el polígono actual antes de redibujarlo
        self.borrar()
        # print(self._puntos)

        # Aplicar las transformaciones
        self._puntos = aplicacion_transformaciones.transformar(self._puntos)
        # print(self._puntos)

        # Dibujar el polígono actualizado
        self.dibujar()

        # Retornar el objeto de transformaciones
        return aplicacion_transformaciones, self._puntos


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
        self._elementos.remove(elemento)
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
