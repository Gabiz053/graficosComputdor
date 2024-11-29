"""
Archivo: fractal_mandelbrot.py

Descripción:
Este archivo contiene la implementación de la clase `FractalMandelbrot`, que representa
una ventana interactiva diseñada para la visualización de fractales de Mandelbrot.

Características principales:
- Configuración personalizada del color del fractal.
- Uso de CustomTkinter para la interfaz gráfica.
- Integración con Matplotlib para futuras visualizaciones del fractal.

Autor: Gabriel Gómez García
Fecha: 27 de Noviembre de 2024
"""

# Imports estándar
import numpy as np  # Para cálculos numéricos avanzados.
import matplotlib.pyplot as plt  # Para gráficos y visualizaciones.

# Imports locales
from ventana_fractal import VentanaFractal  # Clase base para ventanas.
from constantes import Default, Texts  # Constantes y textos predeterminados.
from concurrent.futures import ProcessPoolExecutor


def calcular_fila_mandelbrot(
    row, width, height, x_min, x_max, y_min, y_max, max_iter, complejidad
):
    x, y = np.linspace(x_min, x_max, width), np.linspace(y_min, y_max, height)
    C = x + 1j * y[row]
    Z = np.zeros_like(C)
    img_row = np.zeros(width)
    for col in range(width):
        z = 0
        c = C[col]
        iterations = 0
        while abs(z) <= 2 and iterations < max_iter:
            z = (z**complejidad) + c
            iterations += 1
        img_row[col] = iterations
    # processor_id = os.getpid()
    # print(f"Procesador {processor_id} está procesando la fila {row}")
    return img_row


def generar_fractal(width, height, x_min, x_max, y_min, y_max, max_iter, complejidad):
    img = np.zeros((height, width))
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(
                calcular_fila_mandelbrot,
                row,
                width,
                height,
                x_min,
                x_max,
                y_min,
                y_max,
                max_iter,
                complejidad,
            )
            for row in range(height)
        ]
        for row, future in enumerate(futures):
            img[row, :] = future.result()
    return img


class FractalMandelbrot(VentanaFractal):
    """
    Clase que representa una ventana interactiva para la visualización de fractales de Mandelbrot.

    Esta clase hereda de `Ventana` y permite la personalización del color del fractal,
    mostrando una representación gráfica basada en los parámetros seleccionados.

    Atributos:
        color_seleccionado (str): Color seleccionado para renderizar el fractal.
    """

    def __init__(
        self,
        width: int = Default.WINDOW_WIDTH,
        height: int = Default.WINDOW_HEIGHT,
        title: str = Default.WINDOW_TITLE,
        color_seleccionado: str = Texts.MANDELBROT_COLORES_DEFAULT,
        complejidad: int = 2,
    ) -> None:
        """
        Inicializa una nueva instancia de la clase FractalMandelbrot.

        Args:
            width (int): Ancho de la ventana en píxeles. Valor por defecto definido en Default.WINDOW_WIDTH.
            height (int): Alto de la ventana en píxeles. Valor por defecto definido en Default.WINDOW_HEIGHT.
            title (str): Título de la ventana. Valor por defecto definido en Default.WINDOW_TITLE.
            color_seleccionado (str): Color seleccionado para el fractal.
                Valor por defecto definido en Texts.MANDELBROT_COLORES_DEFAULT.
        """
        super().__init__(width, height, title)
        self.color_seleccionado = color_seleccionado
        self.complejidad = complejidad

    def _generar_fractal(self) -> None:
        """
        Genera el fractal del conjunto de Mandelbrot y lo muestra en el canvas.
        """
        # Parámetros del fractal
        self.max_iter = 100  # Número máximo de iteraciones para determinar si un punto pertenece al conjunto

        # Inicializar el área de visualización del fractal
        self.x_min, self.x_max = -2.0, 1.0
        self.y_min, self.y_max = -1.5, 1.5

        # Llamar a la función que dibuja el fractal en el canvas
        self._dibujar_mandelbrot()

        # Depuración: Mostrar el color seleccionado en la consola
        # print("Color seleccionado:", self.color_seleccionado)
        # Actualizar el canvas con el nuevo fractal
        self.canvas.draw()

    ###################################################################################

    def _generar_fractal(self) -> None:
        self.max_iter = 100  # Número máximo de iteraciones
        self.x_min, self.x_max = -2.0, 1.0
        self.y_min, self.y_max = -1.5, 1.5
        self._dibujar_mandelbrot()
        print("Color seleccionado:", self.color_seleccionado)
        print("Complejidad seleccionada: ", self.complejidad)
        self.canvas.draw()

    def _dibujar_mandelbrot(self):
        width, height = 2000, 2000
        img = generar_fractal(
            width,
            height,
            self.x_min,
            self.x_max,
            self.y_min,
            self.y_max,
            self.max_iter,
            self.complejidad,
        )
        plt.imshow(
            img,
            cmap=self.color_seleccionado,
            extent=(self.x_min, self.x_max, self.y_min, self.y_max),
        )
