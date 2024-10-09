import customtkinter as ctk
import tkinter as tk

class MiAplicacion(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurar la ventana principal
        self.title("Opciones de Pincel")
        self.geometry("400x500")

        # Inicializar el color seleccionado
        self.color_seleccionado = "#000000"  # Color por defecto (negro)

        # Crear un frame para opciones
        self.frame_opciones_1 = ctk.CTkFrame(self)
        self.frame_opciones_1.pack(pady=10, padx=10, fill="both", expand=True)

        # Configurar el peso de las columnas
        for i in range(3):
            self.frame_opciones_1.grid_columnconfigure(i, weight=1)

        # Título de la sección de opciones
        self.fuente = ("Arial", 14)
        titulo_opciones = ctk.CTkLabel(
            self.frame_opciones_1,
            text="Opciones de Pincel",
            font=self.fuente,
        )
        titulo_opciones.grid(row=0, column=0, pady=(10, 0), sticky="nsew", columnspan=3)

        # Frame para la paleta de colores
        self.frame_colores = ctk.CTkFrame(self.frame_opciones_1)
        self.frame_colores.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky="nsew")

        # Crear botones para colores
        colores = ["#FF5733", "#33FF57", "#3357FF", "#FFFF33", "#FF33FF", "#33FFFF", "#FFFFFF", "#000000"]
        for i, color in enumerate(colores):
            btn_color = ctk.CTkButton(
                self.frame_colores,
                bg_color=color,
                command=lambda c=color: self.cambiar_color(c),
                text="",  # Dejar vacío para que el botón solo muestre el color
                width=20,  # Ajustar el ancho del botón
                height=20  # Ajustar la altura del botón
            )
            btn_color.grid(row=0, column=i, padx=5, pady=5)

        # Label para mostrar el color seleccionado
        self.label_color = ctk.CTkLabel(
            self.frame_opciones_1,
            text=f"Color Seleccionado: {self.color_seleccionado}",
            font=self.fuente
        )
        self.label_color.grid(row=2, column=0, columnspan=3, pady=10, sticky="nsew")

    def cambiar_color(self, color):
        self.color_seleccionado = color
        self.label_color.configure(text=f"Color Seleccionado: {self.color_seleccionado}")

if __name__ == "__main__":
    app = MiAplicacion()
    app.mainloop()
