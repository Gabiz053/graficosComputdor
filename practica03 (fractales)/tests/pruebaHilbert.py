import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

class FractalApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.zooming = False
        self.zoom_direction = 0
        self.zoom_factor = 1.1  # Factor de zoom
        self._crear_contenido_ventana()

    def _crear_contenido_ventana(self) -> None:
        """
        Crea y configura los elementos de la ventana para la visualización del fractal.
        """
        # Crear un frame para el área de visualización
        self.frame_visualizacion = ctk.CTkFrame(self.ventana, corner_radius=10)
        self.frame_visualizacion.pack(fill="both", expand=True)

        # Añadir un texto inicial o una etiqueta para indicar el propósito del área
        label_info = ctk.CTkLabel(self.frame_visualizacion, text="Fractal generado recursivamente.")
        label_info.pack(pady=20, padx=20)

        # Crear el canvas y el plot solo una vez
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.ax.set_aspect("equal")
        self.ax.axis("off")  # Desactivar los ejes

        # Configurar la figura para que ocupe todo el espacio
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Ajusta los márgenes de la figura

        # Crear el canvas para integrarlo con Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_visualizacion)  # 'self.frame_visualizacion' es el contenedor de Tkinter
        self.canvas.draw()

        # Ajustar el canvas para que ocupe todo el espacio disponible
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Detectar el clic en el canvas para aplicar el zoom
        self.canvas.get_tk_widget().bind("<Button-1>", self.on_left_click)  # Izquierda: zoom hacia fuera
        self.canvas.get_tk_widget().bind("<Button-3>", self.on_right_click)  # Derecha: zoom hacia dentro
        self.canvas.get_tk_widget().bind("<ButtonRelease-1>", self.on_release)  # Detener zoom
        self.canvas.get_tk_widget().bind("<ButtonRelease-3>", self.on_release)  # Detener zoom

        # Llamar al método para generar el fractal según el algoritmo seleccionado
        self._generar_fractal()

    def _generar_fractal(self):
        # Aquí va la lógica para generar el fractal que deseas visualizar
        pass

    def on_left_click(self, evento):
        # Iniciar el zoom hacia afuera
        self.zooming = True
        self.zoom_direction = -1  # Dirección del zoom (-1 = alejar)
        self._start_zoom()

    def on_right_click(self, evento):
        # Iniciar el zoom hacia adentro
        self.zooming = True
        self.zoom_direction = 1  # Dirección del zoom (1 = acercar)
        self._start_zoom()

    def on_release(self, evento):
        # Detener el zoom cuando se suelta el botón
        self.zooming = False

    def _start_zoom(self):
        """Comienza a hacer zoom suavemente de manera continua."""
        if self.zooming:
            self._zoom()
            self.canvas.get_tk_widget().after(50, self._start_zoom)  # Llamar a _start_zoom cada 50 ms

    def _zoom(self):
        """Actualiza los límites del gráfico según el factor de zoom y la dirección."""
        # Obtener los límites actuales del gráfico
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # Calcular el nuevo tamaño de los límites en función de la dirección del zoom
        width = (xlim[1] - xlim[0]) * self.zoom_factor ** self.zoom_direction
        height = (ylim[1] - ylim[0]) * self.zoom_factor ** self.zoom_direction

        # Actualizar los límites de los ejes
        self.ax.set_xlim([xlim[0] - (width - (xlim[1] - xlim[0])) / 2, xlim[1] + (width - (xlim[1] - xlim[0])) / 2])
        self.ax.set_ylim([ylim[0] - (height - (ylim[1] - ylim[0])) / 2, ylim[1] + (height - (ylim[1] - ylim[0])) / 2])

        # Redibujar el canvas con los nuevos límites
        self.canvas.draw()

# Aquí se crea la ventana principal
root = ctk.CTk()
app = FractalApp(root)
root.mainloop()
