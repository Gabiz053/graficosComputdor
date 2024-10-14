import customtkinter as ctk

class Aplicacion(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ejemplo de Textbox")
        self.geometry("300x200")

        # Frame para el área de texto
        frame_salida_texto = ctk.CTkFrame(self)
        frame_salida_texto.pack(pady=20)

        # Crear el Textbox
        self.area_texto = ctk.CTkTextbox(frame_salida_texto, width=200, height=100)
        self.area_texto.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Botón para limpiar el texto
        boton_limpiar = ctk.CTkButton(self, text="Limpiar Texto", command=self.limpiar_texto)
        boton_limpiar.pack(pady=10)

    def limpiar_texto(self):
        """Limpia el texto del textbox."""
        self.area_texto.delete("1.0", ctk.END)  # Elimina todo el texto

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
