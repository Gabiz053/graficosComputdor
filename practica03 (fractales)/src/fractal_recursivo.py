"""
Archivo: fractal_recursivo.py

Descripción:
Este archivo contiene la implementación de la clase `FractalRecursivo`, que representa
una ventana interactiva destinada a la generación y visualización de fractales
utilizando algoritmos recursivos.

Características principales:
- Configuración personalizada de parámetros del fractal (algoritmo, color, nivel).
- Uso de CustomTkinter para una interfaz gráfica moderna.
- Integración con Matplotlib para la visualización del fractal generado.

Autor: Gabriel Gómez García
Fecha: 27 de Noviembre de 2024
"""

# Imports estándar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Imports locales
from ventana_fractal import VentanaFractal  # Clase base para la ventana interactiva.
from constantes import (
    Default,
    Texts,
)  # Constantes y textos predeterminados para la configuración.


class FractalRecursivo(VentanaFractal):
    """
    Clase que representa una ventana interactiva para la generación de fractales recursivos.

    Hereda de la clase `Ventana` y permite la personalización de diversos parámetros
    del fractal, como el algoritmo a usar, el color del dibujo y el nivel de recursión.

    Atributos:
        algoritmo_seleccionado (str): Algoritmo de fractal elegido.
        color_seleccionado (str): Color seleccionado para el fractal.
        nivel_seleccionado (int): Nivel de recursión o detalle del fractal.
    """

    def __init__(
        self,
        width: int = Default.WINDOW_WIDTH,
        height: int = Default.WINDOW_HEIGHT,
        title: str = Default.WINDOW_TITLE,
        algoritmo_seleccionado: str = Texts.RECURSIVO_ALGORITMOS_DEFAULT,
        color_seleccionado: str = Texts.RECURSIVO_COLOR_DEFAULT,
        nivel_seleccionado: int = Texts.RECURSIVO_NIVEL_DEFAULT,
    ) -> None:
        """
        Inicializa una nueva instancia de la clase FractalRecursivo.

        Args:
            width (int): Ancho de la ventana en píxeles. Valor por defecto definido en Default.WINDOW_WIDTH.
            height (int): Alto de la ventana en píxeles. Valor por defecto definido en Default.WINDOW_HEIGHT.
            title (str): Título de la ventana. Valor por defecto definido en Default.WINDOW_TITLE.
            algoritmo_seleccionado (str): Algoritmo seleccionado para generar el fractal.
                Valor por defecto definido en Texts.RECURSIVO_ALGORITMOS_DEFAULT.
            color_seleccionado (str): Color seleccionado para el fractal.
                Valor por defecto definido en Texts.RECURSIVO_COLOR_DEFAULT.
            nivel_seleccionado (int): Nivel de recursión del fractal.
                Valor por defecto definido en Texts.RECURSIVO_NIVEL_DEFAULT.
        """
        super().__init__(width, height, title)
        self.algoritmo_seleccionado = algoritmo_seleccionado
        self.color_seleccionado = color_seleccionado
        self.nivel_seleccionado = nivel_seleccionado

    def _generar_fractal(self) -> None:
        """
        Llama al método correspondiente para generar el fractal basado en el algoritmo seleccionado.
        """

        # Depuración: Mostrar los parámetros seleccionados en la consola
        print("Algoritmo:", self.algoritmo_seleccionado)
        print("Color:", self.color_seleccionado)
        print("Nivel:", self.nivel_seleccionado)

        # Limpiar el plot antes de redibujar el fractal
        self.ax.clear()
        self.ax.axis("off")  # Re-desactivar los ejes

        if self.algoritmo_seleccionado == Texts.RECURSIVO_ALGORITMOS[0]:
            self._generar_triangulo_sierpinsky()
        elif self.algoritmo_seleccionado == Texts.RECURSIVO_ALGORITMOS[1]:
            self._generar_alfombra_sierpinsky()
        elif self.algoritmo_seleccionado == Texts.RECURSIVO_ALGORITMOS[2]:
            self._generar_curva_koch()
        elif self.algoritmo_seleccionado == Texts.RECURSIVO_ALGORITMOS[3]:
            self._generar_curva_hilbert()
        elif self.algoritmo_seleccionado == Texts.RECURSIVO_ALGORITMOS[4]:
            self._generar_arbol()
        else:
            print("Algoritmo no reconocido.")

        # Actualizar el canvas con el nuevo fractal
        self.canvas.draw()

    ###################################################################################
    def _generar_triangulo_sierpinsky(self) -> None:
        """
        Método para generar el Triángulo de Sierpinsky de manera recursiva.
        """
        print("Generando Triángulo de Sierpinsky...")

        # Parámetros para el triángulo inicial (triángulo equilátero)
        punto_a = np.array([0, 0])
        punto_b = np.array([1, 0])
        punto_c = np.array([0.5, np.sqrt(3) / 2])

        # Llamada recursiva para generar el triángulo
        self._dibujar_triangulo_sierpinsky(
            self.ax, punto_a, punto_b, punto_c, self.nivel_seleccionado
        )

        # Actualizar el canvas después de la generación
        self.canvas.draw()

    def _dibujar_triangulo_sierpinsky(self, ax, punto_a, punto_b, punto_c, nivel):
        """
        Función recursiva que dibuja el Triángulo de Sierpinsky.

        Args:
            ax (matplotlib.axes.Axes): El objeto del eje donde se dibuja.
            punto_a, punto_b, punto_c (np.array): Los tres puntos del triángulo.
            nivel (int): Nivel de recursión.
        """
        if nivel == 0:
            # Dibujar el triángulo base cuando se alcanza el nivel 0
            triangle = Polygon(
                [punto_a, punto_b, punto_c], closed=True, color=self.color_seleccionado
            )
            ax.add_patch(triangle)
        else:
            # Calcular los puntos medios de los lados del triángulo
            punto_ab = (punto_a + punto_b) / 2
            punto_bc = (punto_b + punto_c) / 2
            punto_ca = (punto_c + punto_a) / 2

            # Llamar recursivamente para los tres sub-triángulos
            self._dibujar_triangulo_sierpinsky(
                ax, punto_a, punto_ab, punto_ca, nivel - 1
            )
            self._dibujar_triangulo_sierpinsky(
                ax, punto_ab, punto_b, punto_bc, nivel - 1
            )
            self._dibujar_triangulo_sierpinsky(
                ax, punto_ca, punto_bc, punto_c, nivel - 1
            )

    ###################################################################################
    def _generar_alfombra_sierpinsky(self) -> None:
        """
        Método para generar la Alfombra de Sierpinsky de manera recursiva.
        """
        print("Generando Alfombra de Sierpinsky...")
        # Parámetros para el cuadrado inicial
        punto_inicial = np.array([0, 0])
        tamaño_inicial = 1  # El tamaño del cuadrado principal

        # Llamada recursiva para generar la alfombra
        self._dibujar_alfombra_sierpinsky(
            self.ax, punto_inicial, tamaño_inicial, self.nivel_seleccionado
        )

        # Actualizar el canvas después de la generación
        self.canvas.draw()

    def _dibujar_alfombra_sierpinsky(self, ax, punto_inicial, tamaño, nivel):
        """
        Función recursiva que dibuja la Alfombra de Sierpinsky.

        Args:
            ax (matplotlib.axes.Axes): El objeto del eje donde se dibuja.
            punto_inicial (np.array): El punto (x, y) donde empieza el cuadrado.
            tamaño (float): El tamaño del cuadrado.
            nivel (int): Nivel de recursión.
        """
        if nivel == 0:
            # Dibujar un cuadrado cuando se alcanza el nivel 0
            square = Polygon(
                [
                    punto_inicial,
                    punto_inicial + np.array([tamaño, 0]),
                    punto_inicial + np.array([tamaño, tamaño]),
                    punto_inicial + np.array([0, tamaño]),
                ],
                closed=True,
                color=self.color_seleccionado,
            )
            ax.add_patch(square)
        else:
            # Dividir el cuadrado en una malla 3x3
            nuevo_tamaño = tamaño / 3
            for i in range(3):
                for j in range(3):
                    if i == 1 and j == 1:  # Eliminar el cuadrado central
                        continue
                    # Calcular la posición del nuevo cuadrado
                    nuevo_punto = punto_inicial + np.array(
                        [i * nuevo_tamaño, j * nuevo_tamaño]
                    )
                    # Llamar recursivamente para los sub-cuadrados
                    self._dibujar_alfombra_sierpinsky(
                        ax, nuevo_punto, nuevo_tamaño, nivel - 1
                    )

    ###################################################################################
    def _generar_curva_koch(self) -> None:
        """
        Método para generar la Curva de Koch de manera recursiva.
        """
        print("Generando Curva de Koch...")

        # Definir los puntos iniciales de la curva
        punto_a = np.array([0, 0])
        punto_b = np.array([1, 0])

        # Llamada recursiva para generar la curva de Koch
        self._dibujar_curva_koch(self.ax, punto_a, punto_b, self.nivel_seleccionado)

        # Actualizar el canvas después de la generación
        self.canvas.draw()

    def _dibujar_curva_koch(self, ax, punto_a, punto_b, nivel):
        """
        Función recursiva que dibuja la Curva de Koch.

        Args:
            ax (matplotlib.axes.Axes): El objeto del eje donde se dibuja.
            punto_a, punto_b (np.array): Los dos puntos iniciales de la curva.
            nivel (int): Nivel de recursión.
        """
        if nivel == 0:
            # Dibujar una línea entre los puntos cuando se alcanza el nivel 0
            ax.plot(
                [punto_a[0], punto_b[0]],
                [punto_a[1], punto_b[1]],
                color=self.color_seleccionado,
                lw=2,
            )

        else:
            # Calcular los puntos que forman la curva de Koch
            punto_c = (2 * punto_a + punto_b) / 3  # Primer punto
            punto_d = (punto_a + 2 * punto_b) / 3  # Segundo punto

            # Calcular el punto pico
            punto_medio = (punto_a + punto_b) / 2
            altura = (
                np.sqrt(3) / 6 * np.linalg.norm(punto_b - punto_a)
            )  # Altura del triángulo equilátero
            vector = punto_b - punto_a
            rotacion = np.array(
                [[0, -1], [1, 0]]
            )  # Rotación 60 grados en sentido antihorario
            punto_pico = punto_medio + np.dot(rotacion, vector) * (
                altura / np.linalg.norm(vector)
            )

            # Llamada recursiva para los cuatro segmentos
            self._dibujar_curva_koch(ax, punto_a, punto_c, nivel - 1)
            self._dibujar_curva_koch(ax, punto_c, punto_pico, nivel - 1)
            self._dibujar_curva_koch(ax, punto_pico, punto_d, nivel - 1)
            self._dibujar_curva_koch(ax, punto_d, punto_b, nivel - 1)

    ###################################################################################
    def _generar_curva_hilbert(self) -> None:
        """
        Método para generar la Curva de Hilbert.
        """
        print("Generando Curva de Hilbert...")

        # Tamaño y centro de la curva
        cx, cy = 0.5, 0.5  # Centro del canvas normalizado a 0-1
        size = 1  # Tamaño total de la curva
        nivel = self.nivel_seleccionado  # Nivel de recursión

        # Generar la curva de Hilbert
        self._dibujar_curva_hilbert(self.ax, cx, cy, size, nivel, 0)

        self.canvas.draw()  # Dibujar la figura

    def _dibujar_curva_hilbert(self, ax, cx, cy, size, nivel, angulo):
        """
        Dibuja la curva de Hilbert recursivamente.

        Args:
            ax (matplotlib.axes.Axes): El eje donde se dibuja.
            cx, cy (float): Coordenadas del centro actual de la curva.
            size (float): Tamaño del lado actual de la curva.
            nivel (int): Nivel de recursión.
            angulo (int): Rotación actual en grados (0, 90, -90).
        """
        if nivel == 0:
            return

        # Coordenadas del tamaño reducido
        mitad = size / 2
        cuarto = size / 4

        # Definir los puntos de cada sección (sin rotar aún)
        puntos = [
            (cuarto, -cuarto),  # Arriba derecha
            (cuarto, cuarto),  # Abajo derecha
            (-cuarto, cuarto),  # Abajo izquierda
            (-cuarto, -cuarto),  # Arriba izquierda
        ]

        # Llamadas recursivas para subdivisiones
        # Aplicamos rotación a las líneas de conexión, no a las posiciones
        self._dibujar_curva_hilbert(
            ax, cx + puntos[0][0], cy + puntos[0][1], mitad, nivel - 1, 0
        )
        self._dibujar_curva_hilbert(
            ax, cx + puntos[1][0], cy + puntos[1][1], mitad, nivel - 1, 0
        )
        self._dibujar_curva_hilbert(
            ax, cx + puntos[2][0], cy + puntos[2][1], mitad, nivel - 1, 90
        )
        self._dibujar_curva_hilbert(
            ax, cx + puntos[3][0], cy + puntos[3][1], mitad, nivel - 1, -90
        )

        # Dibujar las líneas conectando los puntos, pero solo después de la recursión
        # Aquí calculamos las líneas entre los puntos, pero sin rotarlos
        for i in range(len(puntos) - 1):
            x0, y0 = cx + puntos[i][0], cy + puntos[i][1]
            x1, y1 = cx + puntos[i + 1][0], cy + puntos[i + 1][1]
            ax.plot([x0, x1], [y0, y1], color=self.color_seleccionado, lw=2)

        # Comentar o descomentar si se quieren cuadraditos
        # x0, y0 = cx + puntos[-1][0], cy + puntos[-1][1]
        # x1, y1 = cx + puntos[0][0], cy + puntos[0][1]
        # ax.plot([x0, x1], [y0, y1], color=self.color_seleccionado, lw=2)

    def _rotar_punto(self, x, y, angulo):
        """
        Rota un punto en 2D alrededor del origen por un ángulo dado.

        Args:
            x, y (float): Coordenadas iniciales del punto.
            angulo (float): Ángulo de rotación en grados.

        Returns:
            tuple: Coordenadas del punto rotado.
        """
        rad = np.radians(angulo)
        x_rot = x * np.cos(rad) - y * np.sin(rad)
        y_rot = x * np.sin(rad) + y * np.cos(rad)
        return x_rot, y_rot

    def _rotar_punto(self, x, y, angulo):
        """
        Rota un punto en 2D alrededor del origen por un ángulo dado.

        Args:
            x, y (float): Coordenadas iniciales del punto.
            angulo (float): Ángulo de rotación en grados.

        Returns:
            tuple: Coordenadas del punto rotado.
        """
        rad = np.radians(angulo)
        x_rot = x * np.cos(rad) - y * np.sin(rad)
        y_rot = x * np.sin(rad) + y * np.cos(rad)
        return x_rot, y_rot

    ###################################################################################

    def _generar_arbol(self) -> None:
        """
        Método para generar el árbol recursivo en el canvas de Tkinter.
        """
        print("Generando árbol recursivo...")

        # Definir el punto inicial (origen) y la longitud inicial de la rama
        punto_a = np.array([0, 0])  # Punto base (origen)
        longitud_inicial = 10.0  # Longitud de la primera rama
        angulo_inicial = np.pi / 2  # Ángulo inicial (vertical)

        # Llamada recursiva para generar el árbol
        self._dibujar_arbol(
            self.ax, punto_a, longitud_inicial, angulo_inicial, self.nivel_seleccionado
        )

        # Mostrar el árbol en el canvas de Tkinter
        self.canvas.draw()

    def _dibujar_arbol(self, ax, punto_a, longitud, angulo, nivel):
        """
        Función recursiva que dibuja el árbol recursivo en el eje de Matplotlib.

        Args:
            ax (matplotlib.axes.Axes): El objeto del eje donde se dibuja.
            punto_a (np.array): El punto inicial de la rama.
            longitud (float): La longitud de la rama.
            angulo (float): El ángulo de inclinación de la rama.
            nivel (int): Nivel de recursión.
        """
        if nivel == 0:
            return  # Si hemos llegado al nivel base, terminamos la recursión

        # Calcular el punto final de la rama
        punto_b = punto_a + longitud * np.array([np.cos(angulo), np.sin(angulo)])

        # Dibujar la rama (línea entre punto_a y punto_b)
        ax.plot(
            [punto_a[0], punto_b[0]],
            [punto_a[1], punto_b[1]],
            color=self.color_seleccionado,
            lw=2,
        )

        # Calcular la nueva longitud de las ramas hijas
        nueva_longitud = longitud * 0.7  # Reducir la longitud de las ramas

        # Calcular los ángulos para las ramas hijas (en este caso, inclinación hacia la izquierda y derecha)
        angulo_izquierda = angulo + np.pi / 6  # Ángulo para la rama izquierda
        angulo_derecha = angulo - np.pi / 6  # Ángulo para la rama derecha

        # Llamadas recursivas para las ramas hijas
        self._dibujar_arbol(
            ax, punto_b, nueva_longitud, angulo_izquierda, nivel - 1
        )  # Rama izquierda
        self._dibujar_arbol(
            ax, punto_b, nueva_longitud, angulo_derecha, nivel - 1
        )  # Rama derecha
