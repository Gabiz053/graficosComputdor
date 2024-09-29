
import tkinter as tk
from typing import Tuple


class Aplicacion:
    ESCALA = 10  # 1 unidad = 10 píxeles

    def __init__(self):
        self.ventana = tk.Tk()
        self.canvas = tk.Canvas(self.ventana, width=400, height=400)
        self.canvas.pack()

        # Dibujar un cuadrado en el centro
        self.dibujar_cuadrado(self.canvas, 0, 0, 5, 'blue')  # x=0, y=0, lado=5 unidades

        self.ventana.mainloop()

    def convertir_a_pixeles(self, x: int, y: int) -> Tuple[int, int]:
        """Convierte las coordenadas en unidades a píxeles."""
        return x * self.ESCALA, y * self.ESCALA

    def dibujar_cuadrado(self, lienzo: tk.Canvas, x_centrado: int, y_centrado: int, lado: int, color: str) -> None:
        """Dibuja un cuadrado usando coordenadas centradas en el lienzo."""
        width = lienzo.winfo_width()
        height = lienzo.winfo_height()

        # Obtener las coordenadas en píxeles
        x1, y1 = self.convertir_a_pixeles(x_centrado - lado / 2, y_centrado - lado / 2)
        x2, y2 = self.convertir_a_pixeles(x_centrado + lado / 2, y_centrado + lado / 2)

        # Ajustar para centrar
        x1 += width // 2
        y1 = height // 2 - y1
        x2 += width // 2
        y2 = height // 2 - y2

        # Dibujar el cuadrado
        lienzo.create_rectangle(x1, y1, x2, y2, outline=color, fill=color)

if __name__ == '__main__':
    Aplicacion()