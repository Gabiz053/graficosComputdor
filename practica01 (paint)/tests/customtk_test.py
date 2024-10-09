import customtkinter as ctk

# Inicializar CustomTkinter
ctk.set_appearance_mode("System")  # Opciones: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Tema de color

# Crear la ventana principal
root = ctk.CTk()
root.geometry("400x600")
root.title("Ejemplo de todos los widgets de CustomTkinter")

# Función de callback para el botón
def boton_callback():
    print("Botón presionado")

# Función de callback para el checkbox
def checkbox_callback():
    print("Checkbox:", checkbox.get())

# Función de callback para el switch
def switch_callback():
    print("Switch:", switch.get())

# Función de callback para el slider
def slider_callback(valor):
    print("Slider:", valor)

# Función de callback para el radio button
def radio_callback():
    print("Radio button seleccionado:", radio_var.get())

# Label (Etiqueta)
label = ctk.CTkLabel(root, text="Este es un CTkLabel")
label.pack(pady=10)

# Button (Botón)
button = ctk.CTkButton(root, text="Presiona", command=boton_callback)
button.pack(pady=10)

# Entry (Campo de entrada)
entry = ctk.CTkEntry(root, placeholder_text="Escribe algo aquí")
entry.pack(pady=10)

# CTkOptionMenu (Menú de opciones)
opciones = ["Opción 1", "Opción 2", "Opción 3"]
option_menu = ctk.CTkOptionMenu(root, values=opciones)
option_menu.pack(pady=10)
option_menu.set("Opción 1")

# Checkbox
checkbox = ctk.CTkCheckBox(root, text="CTkCheckBox", command=checkbox_callback)
checkbox.pack(pady=10)

# Switch (Interruptor)
switch = ctk.CTkSwitch(root, text="CTkSwitch", command=switch_callback)
switch.pack(pady=10)

# Slider (Deslizador)
slider = ctk.CTkSlider(root, from_=0, to=100, command=slider_callback)
slider.pack(pady=10)

# Radio Button (Botón de opción)
radio_var = ctk.StringVar(value="Opción 1")
radio1 = ctk.CTkRadioButton(root, text="Opción 1", variable=radio_var, value="Opción 1", command=radio_callback)
radio1.pack(pady=5)
radio2 = ctk.CTkRadioButton(root, text="Opción 2", variable=radio_var, value="Opción 2", command=radio_callback)
radio2.pack(pady=5)

# ProgressBar (Barra de progreso)
progress_bar = ctk.CTkProgressBar(root)
progress_bar.pack(pady=10)
progress_bar.set(0.5)  # Valor inicial (50%)

# CTkTextbox (Cuadro de texto)
textbox = ctk.CTkTextbox(root, width=300, height=100)
textbox.pack(pady=10)
textbox.insert("0.0", "Este es un CTkTextbox. Puedes escribir aquí...")

# Iniciar el bucle de la aplicación
root.mainloop()
