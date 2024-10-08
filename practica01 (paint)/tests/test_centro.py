import tkinter as tk

# Función para mostrar las coordenadas al hacer clic, invirtiendo el eje Y
def mostrar_coordenadas(event):
    x_canvas = canvas.canvasx(event.x)  # Obtener la coordenada X relativa al canvas
    y_canvas = canvas.canvasy(event.y)  # Obtener la coordenada Y relativa al canvas
    # Invertir el eje Y
    print(f"Coordenadas: ({x_canvas}, {y_canvas})")

# Función para mover el canvas, donde la cantidad de desplazamiento se puede ajustar
def mover_canvas(dx, dy):
    # Desplazar horizontalmente
    canvas.xview_scroll(dx, "units")  
    # Desplazar verticalmente
    canvas.yview_scroll(dy, "units")

# Crear la ventana principal
root = tk.Tk()
root.geometry("1300x700")

# Crear un frame para contener el canvas y las barras de scroll
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

# Crear el canvas
canvas = tk.Canvas(frame, background="white", width=700, height=700)
canvas.pack(side="left")

# Crear las barras de desplazamiento
scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
scrollbar_x.pack(side="bottom", fill="x")

scrollbar_y = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar_y.pack(side="right", fill="y")

# Configurar el canvas para usar las barras de desplazamiento
canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

# Configurar el área desplazable (scrollregion) más amplia para que el origen esté en el centro
canvas.configure(scrollregion=(-1000, -1000, 1000, 1000))

# Mover la vista del canvas al centro (donde está el origen)

# Invertir el eje Y al crear las líneas de los ejes
canvas.create_line(-1000, 0, 1000, 0, fill="black", width=2)  # Eje X
canvas.create_line(0, 1000, 0, -1000, fill="black", width=2)  # Eje Y

canvas.create_line(344, 1555, 625, -56, fill="black", width=4)
canvas.create_line(-1334, 200, -0, -344, fill="black", width=4)


# Vincular el evento de clic con la función mostrar_coordenadas
canvas.bind("<Button-1>", mostrar_coordenadas)

# Teclado para mover el canvas
# Para aumentar el desplazamiento, puedes aumentar el número (por ejemplo, 10)
dx_units = 1  # Cambia este valor para ajustar el desplazamiento horizontal
dy_units = 1  # Cambia este valor para ajustar el desplazamiento vertical

root.bind("<Up>", lambda event: mover_canvas(0, -dy_units))    # Mover arriba
root.bind("<Down>", lambda event: mover_canvas(0, dy_units))    # Mover abajo
root.bind("<Left>", lambda event: mover_canvas(-dx_units, 0))   # Mover izquierda
root.bind("<Right>", lambda event: mover_canvas(dx_units, 0))    # Mover derecha

root.mainloop()
