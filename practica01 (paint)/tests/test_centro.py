import customtkinter as ctk

class VentanaCanvas(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Canvas con líneas movibles")
        self.geometry("800x600")

        self.canvas = ctk.CTkCanvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Lista para almacenar las líneas y su ID
        self.lineas = []
        self.selected_line = None
        self.start_x = None
        self.start_y = None

        # Dibujar líneas iniciales
        self.dibujar_lineas()

        # Eventos de ratón
        self.canvas.bind("<Button-1>", self.seleccionar_linea)
        self.canvas.bind("<B1-Motion>", self.mover_linea)
        self.canvas.bind("<ButtonRelease-1>", self.liberar_linea)

    def dibujar_lineas(self):
        # Crear líneas en el canvas
        self.lineas.append(self.canvas.create_line(100, 100, 200, 200, fill="blue", width=2))
        self.lineas.append(self.canvas.create_line(300, 150, 400, 250, fill="red", width=2))
        self.lineas.append(self.canvas.create_line(500, 100, 600, 200, fill="green", width=2))

    def seleccionar_linea(self, event):
        # Comprobar si se hace clic en una línea
        for linea_id in self.lineas:
            x1, y1, x2, y2 = self.canvas.coords(linea_id)
            if self.punto_en_linea(event.x, event.y, x1, y1, x2, y2):
                self.selected_line = linea_id
                self.start_x = event.x
                self.start_y = event.y
                break

    def mover_linea(self, event):
        if self.selected_line:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            # Mover la línea seleccionada
            self.canvas.move(self.selected_line, dx, dy)
            # Actualizar las coordenadas de inicio
            self.start_x = event.x
            self.start_y = event.y

    def liberar_linea(self, event):
        # Restablecer la línea seleccionada
        self.selected_line = None

    def punto_en_linea(self, x, y, x1, y1, x2, y2, tolerancia=5):
        # Comprobar si el punto (x, y) está cerca de la línea (x1, y1) a (x2, y2)
        dist = abs((y2 - y1) * x - (x2 - x1) * y1 + x2 * y1 - y2 * x1) / ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
        return dist <= tolerancia

if __name__ == "__main__":
    app = VentanaCanvas()
    app.mainloop()
