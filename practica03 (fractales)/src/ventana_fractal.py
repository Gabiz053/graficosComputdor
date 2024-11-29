"""
Archivo: ventana_fractal.py

Descripción:
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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importación de Tkinter y CustomTkinter para la interfaz gráfica
import customtkinter as ctk  # Extensión para interfaces modernas y personalizables.

# Imports locales
from ventana import Ventana  # Clase base para la ventana interactiva.
from constantes import (
    Default,
    UserEvents,
)  # Constantes y textos predeterminados para la configuración.


class VentanaFractal(Ventana):
    """
    Clase que representa una ventana interactiva para la generación de fractales.

    Hereda de la clase `Ventana` y permite la personalización de diversos parámetros
    del fractal, como el algoritmo a usar, el color del dibujo y el nivel de recursión.

    Atributos:

    """

    def __init__(
        self,
        width: int = Default.WINDOW_WIDTH,
        height: int = Default.WINDOW_HEIGHT,
        title: str = Default.WINDOW_TITLE,
    ) -> None:
        """
        Inicializa una nueva instancia de la clase FractalRecursivo.

        Args:
            width (int): Ancho de la ventana en píxeles. Valor por defecto definido en Default.WINDOW_WIDTH.
            height (int): Alto de la ventana en píxeles. Valor por defecto definido en Default.WINDOW_HEIGHT.
            title (str): Título de la ventana. Valor por defecto definido en Default.WINDOW_TITLE.
        """
        super().__init__(width, height, title)

        # Velocidades de zoom
        self.zoom_speed = 0.0
        self.max_zoom_speed = 0.02
        self.acceleration_rate = 0.001
        self.deceleration_rate = 0.002
        self.zooming = False
        self.mouse_x, self.mouse_y = 0, 0

    def _crear_contenido_ventana(self) -> None:
        """
        Crea y configura los elementos de la ventana para la visualización del fractal.
        """
        # Crear un frame para el área de visualización
        self.frame_visualizacion = ctk.CTkFrame(self.ventana, corner_radius=10)
        self.frame_visualizacion.pack(fill="both", expand=True)

        # Añadir un texto inicial o una etiqueta para indicar el propósito del área
        label_info = ctk.CTkLabel(self.frame_visualizacion, text="Fractal generado.")
        label_info.pack(pady=20, padx=20)

        # Crear el canvas y el plot solo una vez
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.ax.set_aspect("equal")
        self.ax.axis("off")  # Desactivar los ejes
        self.fig.patch.set_facecolor("#121212")  # Cambiar el color de fondo de la figura
        self.ax.set_facecolor("#121212")        # Cambiar el color de fondo del área de los ejes


        # Configurar la figura para que ocupe todo el espacio
        self.fig.subplots_adjust(
            left=0, right=1, top=1, bottom=0
        )  # Ajusta los márgenes de la figura

        # Crear el canvas para integrarlo con Tkinter
        self.canvas = FigureCanvasTkAgg(
            self.fig, master=self.frame_visualizacion
        )  # 'self.frame_visualizacion' es el contenedor de Tkinter
        self.canvas.draw()

        # Ajustar el canvas para que ocupe todo el espacio disponible
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Detectar el clic en el canvas para aplicar el zoom
        self.canvas.get_tk_widget().bind(UserEvents.MOUSE_MOVE, self.on_mouse_move)
        self.canvas.get_tk_widget().bind(UserEvents.LEFT_CLICK, self.on_left_click)
        self.canvas.get_tk_widget().bind(UserEvents.RIGHT_CLICK, self.on_right_click)
        self.canvas.get_tk_widget().bind(UserEvents.LEFT_RELEASE, self.on_release)
        self.canvas.get_tk_widget().bind(UserEvents.RIGHT_RELEASE, self.on_release)

        # Llamar al método para generar el fractal según el algoritmo seleccionado
        self._generar_fractal()

    def on_mouse_move(self, evento):
        """Actualiza la posición actual del ratón en el canvas."""
        self.mouse_x, self.mouse_y = evento.x, evento.y

    def on_left_click(self, evento):
        """Inicia el zoom hacia afuera y la aceleración."""
        self.zoom_direction = -1  # Alejar
        self.zooming = True
        self._apply_zoom()

    def on_right_click(self, evento):
        """Inicia el zoom hacia adentro y la aceleración."""
        self.zoom_direction = 1  # Acercar
        self.zooming = True
        self._apply_zoom()

    def on_release(self, evento):
        """Activa la desaceleración al soltar el botón del ratón."""
        self.zooming = False

    def _apply_zoom(self):
        """Gestiona el zoom continuo con aceleración y desaceleración."""
        if self.zooming:
            # Acelerar hasta alcanzar la velocidad máxima
            if self.zoom_speed < self.max_zoom_speed:
                self.zoom_speed += self.acceleration_rate
        else:
            # Desacelerar hasta detenerse
            if self.zoom_speed > 0:
                self.zoom_speed -= self.deceleration_rate
            else:
                self.zoom_speed = 0  # Detener el zoom
                return  # Salir del bucle

        # Realizar el zoom
        self._zoom()

        # Continuar aplicando zoom
        self.canvas.get_tk_widget().after(10, self._apply_zoom)

    def _zoom(self):
        """Actualiza los límites del gráfico según el factor de zoom y la dirección."""
        # Obtener los límites actuales del gráfico
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # Factor de escala (zoom in o zoom out)
        scale_factor = 1 + self.zoom_speed * self.zoom_direction

        # Usar la posición actual del ratón para calcular el punto de zoom
        canvas_x, canvas_y = self.mouse_x, self.mouse_y

        # Invertir la coordenada Y del canvas para que coincida con el sistema de matplotlib
        canvas_height = self.canvas.get_tk_widget().winfo_height()
        inverted_canvas_y = canvas_height - canvas_y

        # Transformar las coordenadas del canvas en coordenadas del gráfico
        graph_x, graph_y = self.ax.transData.inverted().transform(
            (canvas_x, inverted_canvas_y)
        )

        # Calcular el cambio proporcional en los límites
        rel_x = (graph_x - xlim[0]) / (xlim[1] - xlim[0])
        rel_y = (graph_y - ylim[0]) / (ylim[1] - ylim[0])

        # Calcular el nuevo tamaño de los límites
        new_width = (xlim[1] - xlim[0]) * scale_factor
        new_height = (ylim[1] - ylim[0]) * scale_factor

        # Ajustar los nuevos límites manteniendo la posición del ratón
        new_xlim = [
            graph_x - rel_x * new_width,
            graph_x + (1 - rel_x) * new_width,
        ]
        new_ylim = [
            graph_y - rel_y * new_height,
            graph_y + (1 - rel_y) * new_height,
        ]

        # Actualizar los límites de los ejes
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)

        # Redibujar el canvas con los nuevos límites
        self.canvas.draw()

    # @abstracmethod
    def _generar_fractal(self) -> None:
        """
        Llama al método correspondiente para generar el fractal basado en el algoritmo seleccionado.
        Debe implementarlo la clase que herede
        """
        pass
