"""
Archivo: fractal_julia.py

Descripción:
Este archivo contiene la implementación de la clase `FractalJulia`, que representa
una ventana interactiva diseñada para la visualización de fractales de Julia.

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
from constantes import Default, Texts, Fractales  # Constantes y textos predeterminados.
from concurrent.futures import ProcessPoolExecutor


def calcular_fila_julia(row, width, height, x_min, x_max, y_min, y_max, max_iter, c):
    x, y = np.linspace(x_min, x_max, width), np.linspace(y_min, y_max, height)
    Z = x + 1j * y[row]
    img_row = np.zeros(width)
    for col in range(width):
        z = Z[col]
        iterations = 0
        while abs(z) <= 2 and iterations < max_iter:
            z = z * z + c
            iterations += 1
        img_row[col] = iterations
    return img_row


def generar_fractal_julia(width, height, x_min, x_max, y_min, y_max, max_iter, c):
    img = np.zeros((height, width))
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(
                calcular_fila_julia,
                row,
                width,
                height,
                x_min,
                x_max,
                y_min,
                y_max,
                max_iter,
                c,
            )
            for row in range(height)
        ]
        for row, future in enumerate(futures):
            img[row, :] = future.result()
    return img


class FractalJulia(VentanaFractal):
    """
    Clase que representa una ventana interactiva para la visualización de fractales de Julia.

    Esta clase hereda de `VentanaFractal` y permite la configuración de parámetros esenciales
    para la generación del fractal, incluyendo el plano complejo, los colores y el conjunto
    específico de Julia.
    """

    def __init__(
        self,
        width: int = Default.WINDOW_WIDTH,
        height: int = Default.WINDOW_HEIGHT,
        title: str = Default.WINDOW_TITLE,
        julia_real: float = -0.7,
        julia_imaginario: float = 0.27015,
        julia_xmin: float = -1.5,
        julia_xmax: float = 1.5,
        julia_ymin: float = -1.5,
        julia_ymax: float = 1.5,
        julia_color_seleccionado: str = Texts.JULIA_COLORES_DEFAULT,
    ) -> None:
        """
        Inicializa una nueva instancia de la clase `FractalJulia`.

        Args:
            width (int): Ancho de la ventana en píxeles. Por defecto, Default.WINDOW_WIDTH.
            height (int): Alto de la ventana en píxeles. Por defecto, Default.WINDOW_HEIGHT.
            title (str): Título de la ventana. Por defecto, Default.WINDOW_TITLE.
            julia_real (float): Parte real del número complejo c para el conjunto de Julia.
            julia_imaginario (float): Parte imaginaria del número complejo c para el conjunto de Julia.
            julia_xmin (float): Límite mínimo del eje X en el plano complejo.
            julia_xmax (float): Límite máximo del eje X en el plano complejo.
            julia_ymin (float): Límite mínimo del eje Y en el plano complejo.
            julia_ymax (float): Límite máximo del eje Y en el plano complejo.
            julia_color_seleccionado (str): Color seleccionado para el fractal.
        """
        super().__init__(width, height, title)
        self.julia_real = julia_real
        self.julia_imaginario = julia_imaginario
        self.julia_xmin = julia_xmin
        self.julia_xmax = julia_xmax
        self.julia_ymin = julia_ymin
        self.julia_ymax = julia_ymax
        self.julia_color_seleccionado = julia_color_seleccionado

        self.max_iter = 300  # Número máximo de iteraciones para el cálculo

    def _generar_fractal(self) -> None:
        """
        Genera el fractal del conjunto de Julia y lo muestra en el canvas.
        """
        # Definir el número complejo c para el fractal de Julia
        c = complex(self.julia_real, self.julia_imaginario)

        # Inicializar el área de visualización del fractal
        self.x_min, self.x_max = self.julia_xmin, self.julia_xmax
        self.y_min, self.y_max = self.julia_ymin, self.julia_ymax

        # Llamar a la función que dibuja el fractal en el canvas
        self._dibujar_julia(c)

        # Depuración: Mostrar el color seleccionado en la consola
        print("Color seleccionado:", self.julia_color_seleccionado)
        # Actualizar el canvas con el nuevo fractal
        self.canvas.draw()

    ###################################################################################

    def _dibujar_julia(self, c):
        width, height = 2000, 2000
        img = generar_fractal_julia(
            width,
            height,
            self.x_min,
            self.x_max,
            self.y_min,
            self.y_max,
            self.max_iter,
            c,
        )
        plt.imshow(
            img,
            cmap=self.julia_color_seleccionado,
            extent=(self.x_min, self.x_max, self.y_min, self.y_max),
        )
