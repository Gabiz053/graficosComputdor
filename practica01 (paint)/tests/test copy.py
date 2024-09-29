from tkinter import Tk, Canvas, Button, Frame, BOTH

class MiAplicacion:
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(root, bg="white", width=1280, height=720)
        self.canvas.pack(fill=BOTH, expand=True)

        # Almacenar líneas
        self.lineas = []
        self.selected_line = None  # Línea seleccionada
        self.offset_x = 0  # Desplazamiento en x
        self.offset_y = 0  # Desplazamiento en y

        # Añadir contenido para demostrar líneas
        self.dibujar_lineas()

        # Vínculos de eventos
        self.canvas.bind("<Button-3>", self.seleccionar_linea)  # Click derecho para seleccionar
        self.canvas.bind("<B3-Motion>", self.mover_linea)  # Mover línea mientras arrastra el clic derecho
        self.canvas.bind("<ButtonRelease-3>", self.finalizar_mover_linea)  # Finalizar movimiento

    def dibujar_lineas(self):
        """Dibuja algunas líneas en el lienzo y las almacena."""
        for i in range(100, 1200, 100):
            linea = self.canvas.create_line(i, 100, i, 600, fill="blue", width=3)
            self.lineas.append(linea)  # Almacena la línea

    def seleccionar_linea(self, event):
        """Selecciona una línea si el cursor está cerca de ella."""
        self.selected_line = None
        for linea in self.lineas:
            coords = self.canvas.coords(linea)
            # Verifica si el cursor está cerca de la línea (en un rango de 10 píxeles)
            if self.es_cercano_a_linea(event.x, event.y, coords):
                self.selected_line = linea
                # Calcular el desplazamiento inicial
                self.offset_x = event.x - coords[0]  # Desplazamiento desde el primer punto de la línea
                self.offset_y = event.y - coords[1]  # Desplazamiento desde el segundo punto de la línea
                break

    def es_cercano_a_linea(self, x, y, coords):
        """Verifica si el punto (x, y) está cerca de la línea definida por coords."""
        x1, y1, x2, y2 = coords
        # Distancia mínima al segmento
        distancia_minima = 10  
        return (min(abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) /
                       ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5, 
                       abs(y - y1) + abs(y - y2) + abs(x - x1) + abs(x - x2)) < distancia_minima)

    def mover_linea(self, event):
        """Mueve la línea seleccionada con el ratón."""
        if self.selected_line:
            # Obtener coordenadas actuales de la línea
            coords = self.canvas.coords(self.selected_line)

            # Calcular el nuevo punto de inicio y final usando el desplazamiento
            new_x1 = event.x - self.offset_x
            new_y1 = event.y - self.offset_y
            new_x2 = new_x1 + (coords[2] - coords[0])
            new_y2 = new_y1 + (coords[3] - coords[1])

            # Mover la línea a las nuevas coordenadas
            self.canvas.coords(self.selected_line, new_x1, new_y1, new_x2, new_y2)

    def finalizar_mover_linea(self, event):
        """Finaliza el movimiento de la línea."""
        self.selected_line = None

if __name__ == "__main__":
    root = Tk()
    app = MiAplicacion(root)
    root.mainloop()
