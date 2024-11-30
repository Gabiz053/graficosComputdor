import customtkinter as ctk
from lsystem import (
    LSystem,
)  # Asegúrate de tener el archivo lsystem.py con la clase LSystem
from ejemplos import Ejemplos


class Ventana(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.geometry("400x500")
        self.title("Ejemplos de L-Systems")
        self._crear_estilo()

        # Crear un Frame para organizar los widgets
        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Crear el desplegable (ComboBox) para ejemplos de L-systems
        self.opciones_ls = Ejemplos.OPCIONES
        self.desplegable = ctk.CTkOptionMenu(
            frame, values=self.opciones_ls, command=self.seleccionar_ejemplo
        )
        self.desplegable.pack(pady=10)

        # Crear un campo de entrada (Entry) para el número de iteraciones con un label
        self.label_iteraciones = ctk.CTkLabel(frame, text="Iteraciones:")
        self.label_iteraciones.pack(pady=5)
        self.entry_iteraciones = ctk.CTkEntry(
            frame, placeholder_text="Ej. 5", width=200
        )
        self.entry_iteraciones.insert(0, "5")  # Valor por defecto 5
        self.entry_iteraciones.pack(pady=10)

        # Crear un campo de entrada (Entry) para la velocidad con un label
        self.label_velocidad = ctk.CTkLabel(frame, text="Velocidad:")
        self.label_velocidad.pack(pady=5)
        self.entry_velocidad = ctk.CTkEntry(frame, placeholder_text="Ej. 5", width=200)
        self.entry_velocidad.insert(0, "0")  # Valor por defecto 5
        self.entry_velocidad.pack(pady=10)

        # Crear un campo de entrada (Entry) para la longitud de los segmentos con un label
        self.label_longitud = ctk.CTkLabel(frame, text="Longitud:")
        self.label_longitud.pack(pady=5)
        self.entry_longitud = ctk.CTkEntry(frame, placeholder_text="Ej. 10", width=200)
        self.entry_longitud.insert(0, "10")  # Valor por defecto 10
        self.entry_longitud.pack(pady=10)

        # Crear un checkbox para habilitar o deshabilitar el dibujo instantáneo
        self.checkbox_instantaneo = ctk.CTkCheckBox(
            frame, text="Dibujo Instantáneo", onvalue=True, offvalue=False
        )
        self.checkbox_instantaneo.pack(pady=10)

        # Crear un botón "Generar" que llama al método de dibujo
        self.boton_generar = ctk.CTkButton(frame, text="Generar", command=self.generar)
        self.boton_generar.pack(pady=10)

        # Diccionario de ejemplos con axioma y reglas
        self.ejemplos = Ejemplos.EJEMPLOS_LSYSTEM

        # Inicializamos con el primer ejemplo
        self.axioma = self.ejemplos[self.opciones_ls[0]]["axioma"]
        self.reglas = self.ejemplos[self.opciones_ls[0]]["reglas"]
        self.angulo = self.ejemplos[self.opciones_ls[0]]["angulo"]
        self.punto_inicial = self.ejemplos[self.opciones_ls[0]]["punto_inicial"]
        self.rotation_offset = self.ejemplos[self.opciones_ls[0]]["rotacion"]
        self.color_map = self.ejemplos[self.opciones_ls[0]]["colormap"]

    def seleccionar_ejemplo(self, seleccion):
        """Actualiza el axioma y las reglas cuando el usuario selecciona una opción."""
        self.axioma = self.ejemplos[seleccion]["axioma"]
        self.reglas = self.ejemplos[seleccion]["reglas"]
        self.angulo = self.ejemplos[seleccion]["angulo"]
        self.punto_inicial = self.ejemplos[seleccion]["punto_inicial"]
        self.rotation_offset = self.ejemplos[seleccion]["rotacion"]
        self.color_map = self.ejemplos[seleccion]["colormap"]

    def generar(self):
        try:
            # Obtener los valores de la interfaz
            iteraciones = int(self.entry_iteraciones.get())  # Obtener las iteraciones
            velocidad = int(self.entry_velocidad.get())  # Obtener la velocidad
            longitud = int(
                self.entry_longitud.get()
            )  # Obtener la longitud de los segmentos
            instantaneo = (
                self.checkbox_instantaneo.get()
            )  # Obtener si el dibujo debe ser instantáneo

            # Crear el L-System con los valores seleccionados
            lsystem = LSystem(
                self.axioma,
                self.reglas,
                angle=self.angulo,
                length=longitud,
                iterations=iteraciones,
                start_point=self.punto_inicial,
                rotation_offset=self.rotation_offset,
                color_map=self.color_map,
            )
            lsystem.draw(velocidad, instantaneo)
            self.generar()
        except Exception:
            # Si ocurre una excepción, vuelve a llamar a generar sin mostrar nada
            # self.generar()
            pass

    def _crear_estilo(self):
        """
        Aplica el tema y crea la fuente de la ventana.
        """
        ctk.set_default_color_theme("green")
        fuente = ctk.CTkFont(family="Segoe UI", size=12)
        self.option_add("*Font", fuente)


if __name__ == "__main__":
    app = Ventana()
    app.mainloop()
