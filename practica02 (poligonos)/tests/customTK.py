import customtkinter as ctk
import tkinter as tk

class VentanaColor(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuraciones de la ventana
        self.title("Seleccionar Color")
        self.geometry("300x200")

        # Variable para el OptionMenu
        self.color_seleccionado = tk.StringVar(value="Rojo")  # Valor inicial

        # Crear el OptionMenu
        self.option_menu = ctk.CTkOptionMenu(
            self,
            variable=self.color_seleccionado,
            values=["Rojo", "Verde", "Azul", "Amarillo", "Negro", "Blanco"],
            command=self.actualizar_color  # Llama a la función cuando se selecciona un nuevo color
        )
        self.option_menu.pack(pady=20)  # Añadir el OptionMenu al centro de la ventana

        # Label para mostrar el color seleccionado
        self.label_color = ctk.CTkLabel(self, text=f"Color seleccionado: {self.color_seleccionado.get()}")
        self.label_color.pack(pady=10)

    def actualizar_color(self, color):
        # Actualiza el texto del label cuando se selecciona un nuevo color
        self.label_color.configure(text=f"Color seleccionado: {color}")

if __name__ == "__main__":
    app = VentanaColor()
    app.mainloop()
