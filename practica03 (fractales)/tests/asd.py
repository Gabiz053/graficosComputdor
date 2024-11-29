import tkinter as tk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

# Constantes predeterminadas para la ventana y eventos
class Default:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    WINDOW_TITLE = "Generador de Fractales"

class UserEvents:
    LEFT_CLICK = "<Button-1>"
    RIGHT_CLICK = "<Button-3>"
    LEFT_RELEASE = "<ButtonRelease-1>"
    RIGHT_RELEASE = "<ButtonRelease-3>"
    MOUSE_MOVE = "<Motion>"

class Ventana:
    """Ventana base con funcionalidad general."""
    def __init__(self, width, height, title):
        self.ventana = ctk.CTk()
        self.ventana.geometry(f"{width}x{height}")
        self.ventana.title(title)

    def ejecutar(self):
        self.ventana.mainloop()

class VentanaFractal(Ventana):
    """Ventana específica para la visualización de fractales."""
    def __init__(self, width=Default.WINDOW_WIDTH, height=Default.WINDOW_HEIGHT, title=Default.WINDOW_TITLE):
        super().__init__(width, height, title)
        self.zoom_speed = 0.0
        self.max_zoom_speed = 0.02
        self.acceleration_rate = 0.001
        self.deceleration_rate = 0.002
        self.zooming = False
        self.mouse_x, self.mouse_y = 0, 0
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.ventana)
        self.canvas.draw()

    def _crear_contenido_ventana(self):
        """Configura los componentes visuales."""
        frame_visualizacion = ctk.CTkFrame(self.ventana)
        frame_visualizacion.pack(fill="both", expand=True)
        label_info = ctk.CTkLabel(frame_visualizacion, text="Fractal generado")
        label_info.pack(pady=20, padx=20)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas.get_tk_widget().bind(UserEvents.MOUSE_MOVE, self.on_mouse_move)
        self.canvas.get_tk_widget().bind(UserEvents.LEFT_CLICK, self.on_left_click)
        self.canvas.get_tk_widget().bind(UserEvents.RIGHT_CLICK, self.on_right_click)
        self.canvas.get_tk_widget().bind(UserEvents.LEFT_RELEASE, self.on_release)
        self.canvas.get_tk_widget().bind(UserEvents.RIGHT_RELEASE, self.on_release)

    def on_mouse_move(self, evento):
        self.mouse_x, self.mouse_y = evento.x, evento.y

    def on_left_click(self, evento):
        self.zoom_direction = -1
        self.zooming = True
        self._apply_zoom()

    def on_right_click(self, evento):
        self.zoom_direction = 1
        self.zooming = True
        self._apply_zoom()

    def on_release(self, evento):
        self.zooming = False

    def _apply_zoom(self):
        if self.zooming:
            if self.zoom_speed < self.max_zoom_speed:
                self.zoom_speed += self.acceleration_rate
        else:
            if self.zoom_speed > 0:
                self.zoom_speed -= self.deceleration_rate
            else:
                self.zoom_speed = 0
                return
        self._zoom()
        self.canvas.get_tk_widget().after(10, self._apply_zoom)

    def _zoom(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        scale_factor = 1 + self.zoom_speed * self.zoom_direction
        canvas_x, canvas_y = self.mouse_x, self.mouse_y
        canvas_height = self.canvas.get_tk_widget().winfo_height()
        inverted_canvas_y = canvas_height - canvas_y
        graph_x, graph_y = self.ax.transData.inverted().transform((canvas_x, inverted_canvas_y))
        rel_x = (graph_x - xlim[0]) / (xlim[1] - xlim[0])
        rel_y = (graph_y - ylim[0]) / (ylim[1] - ylim[0])
        new_width = (xlim[1] - xlim[0]) * scale_factor
        new_height = (ylim[1] - ylim[0]) * scale_factor
        new_xlim = [graph_x - rel_x * new_width, graph_x + (1 - rel_x) * new_width]
        new_ylim = [graph_y - rel_y * new_height, graph_y + (1 - rel_y) * new_height]
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.canvas.draw()

    def _generar_fractal(self):
        pass


class FractalIFS(VentanaFractal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iterations = 10000  # Número de iteraciones
        self.lista_funciones = [
            ({"a": 0.5, "b": 0, "c": 0, "d": 0.5, "e": 0, "f": 0}, 0.33, "red"),
            ({"a": 0.5, "b": 0, "c": 0, "d": 0.5, "e": 0.5, "f": 0.5}, 0.33, "green"),
            ({"a": 0.5, "b": 0, "c": 0, "d": 0.5, "e": 0.5, "f": -0.5}, 0.34, "blue")
        ]
        self.checkbox_default_pro = True

    def dibujar_ifs(self):
        """Genera y dibuja el fractal IFS"""
        if not self.lista_funciones:
            print("Error: No se ha definido ninguna función en lista_funciones.")
            return

        # Inicializar el punto inicial
        x, y = 0, 0  # El punto inicial

        puntos_fractal = []

        for _ in range(self.iterations):
            funcion_seleccionada = self._seleccionar_funcion()
            valores, prob, color = funcion_seleccionada
            a, b, c, d, e, f = valores["a"], valores["b"], valores["c"], valores["d"], valores["e"], valores["f"]

            # Calcular el nuevo punto transformado
            x_nuevo = a * x + c * y + e
            y_nuevo = b * x + d * y + f

            # Almacenar el punto
            puntos_fractal.append((x_nuevo, y_nuevo))

            # Actualizar el punto para la siguiente iteración
            x, y = x_nuevo, y_nuevo

        # Convertir los puntos a formato adecuado para graficar
        puntos_x = [p[0] for p in puntos_fractal]
        puntos_y = [p[1] for p in puntos_fractal]

        # Limpiar el gráfico antes de dibujar el nuevo fractal
        self.ax.clear()

        # Ajustar los límites del gráfico
        self.ax.set_xlim(min(puntos_x) - 1, max(puntos_x) + 1)
        self.ax.set_ylim(min(puntos_y) - 1, max(puntos_y) + 1)

        # Dibujar los puntos generados en el gráfico
        self.ax.scatter(puntos_x, puntos_y, s=0.1, c="black")

        # Redibujar el canvas con los puntos
        self.canvas.draw()

    def _seleccionar_funcion(self):
        """Selecciona una función aleatoria de lista_funciones"""
        if self.checkbox_default_pro:
            probabilidades = [1 / len(self.lista_funciones)] * len(self.lista_funciones)
        else:
            probabilidades = [prob for _, prob, _ in self.lista_funciones]
        probabilidades_acumuladas = self._calcular_probabilidades_acumuladas(probabilidades)
        num_aleatorio = random.random()
        for i, prob_acumulada in enumerate(probabilidades_acumuladas):
            if num_aleatorio < prob_acumulada:
                return self.lista_funciones[i]

    def _calcular_probabilidades_acumuladas(self, probabilidades):
        """Calcula las probabilidades acumuladas a partir de las probabilidades individuales."""
        acumuladas = []
        acumulado = 0.0
        for prob in probabilidades:
            acumulado += prob
            acumuladas.append(acumulado)
        return acumuladas


# Crear la ventana y ejecutar
ventana_fractal = FractalIFS()
ventana_fractal._crear_contenido_ventana()
ventana_fractal.dibujar_ifs()
ventana_fractal.ejecutar()
