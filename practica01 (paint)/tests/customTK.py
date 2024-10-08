import customtkinter as ctk

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing App with CustomTkinter")
        
        # Configurar el tamaño de la ventana
        self.master.geometry("800x600")

        # Crear un lienzo para dibujar
        self.canvas = ctk.CTkCanvas(master, bg="white")
        self.canvas.pack(fill=ctk.BOTH, expand=True)

        # Configurar la variable de estado de dibujo
        self.drawing = False

        # Enlazar eventos del mouse
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        # Crear un marco para los botones
        self.button_frame = ctk.CTkFrame(master)
        self.button_frame.pack(fill=ctk.X, padx=10, pady=10)

        # Botón para limpiar el lienzo
        self.clear_button = ctk.CTkButton(self.button_frame, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.pack(side=ctk.LEFT, padx=5)

    def start_draw(self, event):
        # Comienza a dibujar
        self.drawing = True
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        if self.drawing:
            # Dibuja una línea entre el último punto y el nuevo punto
            self.canvas.create_line((self.last_x, self.last_y, event.x, event.y), fill="black", width=2)
            self.last_x, self.last_y = event.x, event.y

    def stop_draw(self, event):
        # Detiene el dibujo
        self.drawing = False

    def clear_canvas(self):
        # Limpia el lienzo
        self.canvas.delete("all")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # O "dark" para modo oscuro
    ctk.set_default_color_theme("green")  # Puedes cambiar el tema a "blue", "green", "dark-blue", etc.

    root = ctk.CTk()  # Crear la ventana principal
    app = DrawingApp(root)
    root.mainloop()
