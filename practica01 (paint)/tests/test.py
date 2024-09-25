import tkinter as tk
from tkinter import colorchooser

# Clase para representar un vector (línea)
class Vector:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

# Algoritmo base para dibujar líneas
class AlgoritmoDibujo:
    def dibujar_linea(self, lienzo, color, x1, y1, x2, y2):
        raise NotImplementedError("Este método debe ser implementado por una subclase")

# Implementación del algoritmo DDA
class DDALineStrategy(AlgoritmoDibujo):
    def dibujar_linea(self, lienzo, color, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        x_increment = dx / steps
        y_increment = dy / steps
        x, y = x1, y1

        # Dibuja el primer "pack" de 5x5 píxeles
        self.dibujar_pack(lienzo, color, x, y)

        for _ in range(steps):
            x += x_increment
            y += y_increment
            # Dibuja un pack de 5x5 en lugar de un solo píxel
            self.dibujar_pack(lienzo, color, round(x), round(y))

    def dibujar_pack(self, lienzo, color, x, y):
        # Dibuja un rectángulo de 5x5 en lugar de un píxel individual
        lienzo.create_rectangle(x, y, x + 5, y + 5, outline=color, fill=color)

# Implementación del algoritmo de Bresenham
class BresenhamLineStrategy(AlgoritmoDibujo):
    def dibujar_linea(self, lienzo, color, x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            # Dibuja un pack de 5x5 en lugar de un solo píxel
            self.dibujar_pack(lienzo, color, x1, y1)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def dibujar_pack(self, lienzo, color, x, y):
        # Dibuja un rectángulo de 5x5 en lugar de un píxel individual
        lienzo.create_rectangle(x, y, x + 5, y + 5, outline=color, fill=color)

# Clase para la aplicación Paint
class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint - Algoritmos de Dibujo")
        self.color = "black"
        self.lienzo = tk.Canvas(root, bg="white", width=800, height=600)
        self.lienzo.pack(fill=tk.BOTH, expand=True)

        # Variables para almacenar el punto inicial
        self.x_inicial = None
        self.y_inicial = None

        # Lista de vectores (líneas)
        self.lineas = []

        # Estrategia de dibujo (algoritmo)
        self.estrategia = DDALineStrategy()  # Puedes cambiar a BresenhamLineStrategy

        # Configuración de eventos
        self.lienzo.bind("<Button-1>", self.iniciar_dibujo)
        self.lienzo.bind("<B1-Motion>", self.dibujar_en_movimiento)
        self.lienzo.bind("<ButtonRelease-1>", self.terminar_dibujo)

        # Botón para elegir color
        self.boton_color = tk.Button(root, text="Elegir Color", command=self.elegir_color)
        self.boton_color.pack(side=tk.LEFT)

        # Botón para cambiar algoritmo
        self.boton_algoritmo = tk.Button(root, text="Cambiar a Bresenham", command=self.cambiar_algoritmo)
        self.boton_algoritmo.pack(side=tk.LEFT)

    def iniciar_dibujo(self, evento):
        self.x_inicial = evento.x
        self.y_inicial = evento.y

    def dibujar_en_movimiento(self, evento):
        x_final = evento.x
        y_final = evento.y
        self.lienzo.delete("linea_temporal")  # Borra la línea temporal previa
        self.lienzo.create_line(self.x_inicial, self.y_inicial, x_final, y_final, fill=self.color, tags="linea_temporal")

    def terminar_dibujo(self, evento):
        x_final = evento.x
        y_final = evento.y
        self.lienzo.delete("linea_temporal")
        # Almacenar la línea como un vector
        vector = Vector(self.x_inicial, self.y_inicial, x_final, y_final)
        self.lineas.append(vector)

        # Dibujar la línea usando la estrategia actual
        self.estrategia.dibujar_linea(self.lienzo, self.color, self.x_inicial, self.y_inicial, x_final, y_final)

    def elegir_color(self):
        # Abre un diálogo para elegir un color
        color_seleccionado = colorchooser.askcolor(color=self.color)[1]
        if color_seleccionado:
            self.color = color_seleccionado

    def cambiar_algoritmo(self):
        # Cambia entre el algoritmo DDA y Bresenham
        if isinstance(self.estrategia, DDALineStrategy):
            self.estrategia = BresenhamLineStrategy()
            self.boton_algoritmo.config(text="Cambiar a DDA")
        else:
            self.estrategia = DDALineStrategy()
            self.boton_algoritmo.config(text="Cambiar a Bresenham")

# Crear la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
