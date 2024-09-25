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

# Implementación del algoritmo DDA con bloques de 5x5 píxeles
class DDALineStrategy(AlgoritmoDibujo):
    def dibujar_linea(self, lienzo, color, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        x_increment = dx / steps
        y_increment = dy / steps
        x, y = x1, y1

        for _ in range(steps + 1):
            # Saltar cada 5 píxeles para dibujar bloques de 5x5
            if int(abs(x - x1)) % 5 == 0 and int(abs(y - y1)) % 5 == 0:
                self.dibujar_pack(lienzo, color, round(x), round(y))

            x += x_increment
            y += y_increment

    def dibujar_pack(self, lienzo, color, x, y):
        # Dibuja un bloque de 5x5 en la posición (x, y)
        lienzo.create_rectangle(x, y, x + 5, y + 5, outline=color, fill=color)

# Implementación del algoritmo de Bresenham con bloques de 5x5 píxeles
class BresenhamLineStrategy(AlgoritmoDibujo):
    def dibujar_linea(self, lienzo, color, x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            # Dibuja un bloque de 5x5 en la posición actual
            if abs(x1 - x2) % 5 == 0 and abs(y1 - y2) % 5 == 0:
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
        # Dibuja un bloque de 5x5 en lugar de un píxel individual
        lienzo.create_rectangle(x, y, x + 5, y + 5, outline=color, fill=color)

# Clase para la aplicación Paint
class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint - Algoritmos de Dibujo")
        self.color = "black"
        self.lienzo = tk.Canvas(root, bg="white", width=800, height=600)
        self.lienzo.pack(fill=tk.BOTH, expand=True)

        self.x_inicial = None
        self.y_inicial = None

        self.lineas = []  # Guardar las líneas dibujadas como vectores

        # Estrategia de dibujo
        self.estrategia = DDALineStrategy()  # Cambia a BresenhamLineStrategy si lo prefieres

        # Eventos de mouse para dibujar
        self.lienzo.bind("<Button-1>", self.iniciar_dibujo)
        self.lienzo.bind("<B1-Motion>", self.dibujar_en_movimiento)
        self.lienzo.bind("<ButtonRelease-1>", self.terminar_dibujo)

        # Evento para hacer zoom con la rueda del ratón
        self.lienzo.bind("<MouseWheel>", self.hacer_zoom)

        # Botón para elegir color
        self.boton_color = tk.Button(root, text="Elegir Color", command=self.elegir_color)
        self.boton_color.pack()

        self.factor_zoom = 1.0  # Factor de zoom inicial

    def iniciar_dibujo(self, event):
        self.x_inicial = event.x
        self.y_inicial = event.y

    def dibujar_en_movimiento(self, event):
        # Se redibuja en tiempo real mientras se mueve el ratón
        self.lienzo.delete("linea_temp")
        self.estrategia.dibujar_linea(self.lienzo, self.color, self.x_inicial, self.y_inicial, event.x, event.y)

    def terminar_dibujo(self, event):
        # Se guarda la línea final al soltar el clic
        self.lineas.append(Vector(self.x_inicial, self.y_inicial, event.x, event.y))
        self.estrategia.dibujar_linea(self.lienzo, self.color, self.x_inicial, self.y_inicial, event.x, event.y)
        self.x_inicial, self.y_inicial = None, None

    def elegir_color(self):
        # Cambiar el color de dibujo
        self.color = colorchooser.askcolor()[1]

    def hacer_zoom(self, event):
        # Ajustar el factor de zoom
        if event.delta > 0:  # Zoom in
            self.factor_zoom *= 1.1
        else:  # Zoom out
            self.factor_zoom /= 1.1

        # Aplicar el zoom al lienzo
        self.lienzo.scale("all", 0, 0, self.factor_zoom, self.factor_zoom)

# Configuración de la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
