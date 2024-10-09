import tkinter as tk
from tkinter import ttk  # Para algunos widgets como ProgressBar o Treeview

# Crear la ventana principal
root = tk.Tk()
root.geometry("400x600")
root.title("Ejemplo de todos los widgets de Tkinter")

# Función de callback para el botón
def boton_callback():
    print("Botón presionado")

# Función de callback para el checkbox
def checkbox_callback():
    print("Checkbox:", checkbox_var.get())

# Función de callback para el radio button
def radio_callback():
    print("Radio button seleccionado:", radio_var.get())

# Función de callback para el scale
def scale_callback(valor):
    print("Scale:", valor)

# Label (Etiqueta)
label = tk.Label(root, text="Este es un Label")
label.pack(pady=10)

# Button (Botón)
button = tk.Button(root, text="Presiona", command=boton_callback)
button.pack(pady=10)

# Entry (Campo de entrada)
entry = tk.Entry(root)
entry.insert(0, "Escribe algo aquí")
entry.pack(pady=10)

# OptionMenu (Menú de opciones)
opciones = ["Opción 1", "Opción 2", "Opción 3"]
opcion_var = tk.StringVar(value="Opción 1")
option_menu = tk.OptionMenu(root, opcion_var, *opciones)
option_menu.pack(pady=10)

# Checkbutton (Checkbox)
checkbox_var = tk.BooleanVar()
checkbox = tk.Checkbutton(root, text="Checkbutton", variable=checkbox_var, command=checkbox_callback)
checkbox.pack(pady=10)

# Radiobutton (Botón de opción)
radio_var = tk.StringVar(value="Opción 1")
radio1 = tk.Radiobutton(root, text="Opción 1", variable=radio_var, value="Opción 1", command=radio_callback)
radio1.pack(pady=5)
radio2 = tk.Radiobutton(root, text="Opción 2", variable=radio_var, value="Opción 2", command=radio_callback)
radio2.pack(pady=5)

# Scale (Deslizador)
scale = tk.Scale(root, from_=0, to=100, orient="horizontal", command=scale_callback)
scale.pack(pady=10)

# ProgressBar (Barra de progreso) - Usando ttk
progress_bar = ttk.Progressbar(root, length=200, mode='determinate')
progress_bar.pack(pady=10)
progress_bar['value'] = 50  # Valor inicial (50%)

# Text (Área de texto)
text = tk.Text(root, height=5, width=30)
text.pack(pady=10)
text.insert(tk.END, "Este es un Text. Puedes escribir aquí...")

# Combobox (Caja de selección) - Usando ttk
combobox = ttk.Combobox(root, values=["Item 1", "Item 2", "Item 3"])
combobox.set("Item 1")  # Valor predeterminado
combobox.pack(pady=10)

# Treeview (Vista en árbol) - Usando ttk
treeview = ttk.Treeview(root, columns=("col1", "col2"), show="headings")
treeview.heading("col1", text="Columna 1")
treeview.heading("col2", text="Columna 2")
treeview.insert("", tk.END, values=("Fila 1", "Dato 1"))
treeview.insert("", tk.END, values=("Fila 2", "Dato 2"))
treeview.pack(pady=10)

# Iniciar el bucle de la aplicación
root.mainloop()
