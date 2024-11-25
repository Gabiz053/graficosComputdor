import customtkinter as ctk

class CustomSpinbox(ctk.CTkFrame):
    def __init__(self, parent, min_value=0, max_value=100, initial_value=0, step=1, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Limites y paso del Spinbox
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = ctk.IntVar(value=initial_value)

        # Botón para disminuir el valor
        self.decrement_button = ctk.CTkButton(self, text="◀", width=20, command=self.decrement)
        self.decrement_button.grid(row=0, column=0, padx=5, pady=5)

        # Campo de entrada para mostrar el valor actual
        self.entry = ctk.CTkEntry(self, width=50, textvariable=self.value, justify="center")
        self.entry.grid(row=0, column=1, padx=5, pady=5)

        # Botón para incrementar el valor
        self.increment_button = ctk.CTkButton(self, text="▶", width=20, command=self.increment)
        self.increment_button.grid(row=0, column=2, padx=5, pady=5)

    def increment(self):
        if self.value.get() + self.step <= self.max_value:
            self.value.set(self.value.get() + self.step)

    def decrement(self):
        if self.value.get() - self.step >= self.min_value:
            self.value.set(self.value.get() - self.step)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("300x200")
        
        # Crear una instancia de CustomSpinbox
        spinbox = CustomSpinbox(self, min_value=0, max_value=10, initial_value=5, step=1)
        spinbox.pack(pady=20)

app = App()
app.mainloop()
