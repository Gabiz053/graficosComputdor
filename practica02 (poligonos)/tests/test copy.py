import tkinter as tk
from tkinter import Canvas

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Relleno por Inundación")
        self.geometry("400x400")

        # Crear un lienzo
        self.lienzo = Canvas(self, width=400, height=400, bg="white")
        self.lienzo.pack()

        # Crear un polígono
        self.polygon_id = self.lienzo.create_polygon(100, 100, 300, 100, 300, 300, 100, 300, outline="black", fill="", width=2)

        # Vincular el evento de clic en el lienzo
        self.lienzo.bind("<Button-1>", self.rellenar)

    def rellenar(self, event):
        """
        Rellena el área del polígono utilizando el algoritmo de flood fill al hacer clic en el lienzo.
        """
        x0, y0 = event.x, event.y  # Coordenadas del clic
        color_relleno = "lightblue"
        color_fondo = self.lienzo.cget("bg")  # Color de fondo (blanco)

        # Verifica si se hizo clic dentro del polígono
        if self.lienzo.find_withtag(tk.CURRENT):
            # Inicia el algoritmo de flood fill
            self.flood_fill(x0, y0, color_fondo, color_relleno)

    def flood_fill(self, x, y, color_fondo, color_relleno):
        """
        Algoritmo de flood fill para rellenar un área.
        """
        # Comprueba si las coordenadas están dentro del lienzo
        if x < 0 or x >= 400 or y < 0 or y >= 400:
            return

        # Obtiene el color del pixel actual
        pixel_color = self.lienzo.find_closest(x, y)
        color_actual = self.lienzo.itemcget(pixel_color, "fill")

        # Si el color es el de fondo, lo cambiamos al color de relleno
        if color_actual == color_fondo or color_actual == "":
            self.lienzo.create_rectangle(x, y, x + 1, y + 1, fill=color_relleno, outline=color_relleno)

            # Llama recursivamente a flood_fill en las posiciones adyacentes
            self.flood_fill(x + 1, y, color_fondo, color_relleno)  # Derecha
            self.flood_fill(x - 1, y, color_fondo, color_relleno)  # Izquierda
            self.flood_fill(x, y + 1, color_fondo, color_relleno)  # Abajo
            self.flood_fill(x, y - 1, color_fondo, color_relleno)  # Arriba

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
