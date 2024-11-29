"""
Archivo: ventana_menu.py

Este archivo define la clase VentanaMenu, que extiende la funcionalidad
de la clase abstracta Ventana. Proporciona una interfaz gráfica con un
menú interactivo para gestionar diferentes secciones de la aplicación.

Autor: Gabriel Gomez Garcia
Fecha: 21 de septiembre de 2024
"""

# Imports estándar
import tkinter as tk

# Imports de terceros
import customtkinter as ctk
from CTkColorPicker import AskColor

# Imports locales
from ventana import Ventana
from constantes import Default, Color, Texts, Fractales

from fractal_recursivo import FractalRecursivo
from fractal_mandelbrot import FractalMandelbrot
from fractal_julia import FractalJulia
from fractal_ifs import FractalIFS


class VentanaMenu(Ventana):
    """
    Clase que representa una ventana con un menú interactivo.

    Extiende la clase abstracta Ventana para añadir funcionalidades específicas,
    como un menú superior y secciones interactivas para trabajar con fractales.

    Atributos heredados:
        _width (int): Ancho de la ventana en píxeles.
        _height (int): Alto de la ventana en píxeles.
        _title (str): Título de la ventana.
        _ventana (ctk.CTk): Instancia de la ventana principal de customtkinter.

    Atributos de instancia:
        _menu_fractales (ctk.CTkFrame): Frame que contiene el menú de fractales.
    """

    def __init__(
        self,
        width: int = Default.WINDOW_WIDTH,
        height: int = Default.WINDOW_HEIGHT,
        title: str = Default.WINDOW_TITLE,
    ) -> None:
        """
        Inicializa la ventana configurando dimensiones, título y elementos base.

        Args:
            width (int): Ancho de la ventana en píxeles. Por defecto, Default.WINDOW_WIDTH.
            height (int): Alto de la ventana en píxeles. Por defecto, Default.WINDOW_HEIGHT.
            title (str): Título de la ventana. Por defecto, Default.WINDOW_TITLE.
        """
        super().__init__(width, height, title)
        self._menu_fractales: ctk.CTkFrame = None

    def _crear_contenido_ventana(self) -> None:
        """
        Configura el contenido principal de la ventana.

        Añade un menú de fractales y ajusta la proporción de la cuadrícula
        para permitir un diseño adaptativo. Sobrescribe el método heredado.
        """
        self._menu_fractales = self._crear_menu_fractales(self._ventana)
        self._configurar_grid(self._ventana)

    def _crear_menu_fractales(self, ventana: ctk.CTk) -> ctk.CTkFrame:
        """
        Crea el menú lateral para gestionar las opciones de fractales.

        Args:
            ventana (ctk.CTk): La ventana principal de la aplicación.

        Returns:
            ctk.CTkFrame: Frame que contiene las opciones del menú de fractales.
        """
        menu_fractales = ctk.CTkScrollableFrame(ventana, corner_radius=10)
        menu_fractales.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self._configurar_grid(menu_fractales)

        # Añadir título al menú
        titulo_menu_fractales = ctk.CTkLabel(
            menu_fractales, text=Texts.SECCION_FRACTALES, font=(self.fuente, 16)
        )
        titulo_menu_fractales.grid(row=0, column=0, pady=10, padx=10, sticky="n")

        # Crear secciones del menú
        self._crear_seccion_recursivo(Texts.RECURSIVO, menu_fractales)
        self._crear_seccion_julia(Texts.JULIA, menu_fractales)
        self._crear_seccion_mandelbrot(Texts.MANDELBROT, menu_fractales)
        self._crear_seccion_ifs(Texts.IFS, menu_fractales)

        return menu_fractales

    ################### FRACTAL RECURSIVO ###################
    def _crear_seccion_recursivo(
        self, titulo: str, parent_frame: ctk.CTkScrollableFrame
    ) -> None:
        """
        Crea la sección específica para fractales recursivos dentro del menú.

        Args:
            titulo (str): Título de la sección.
            parent_frame (ctk.CTkScrollableFrame): Frame contenedor del menú.
        """

        # todas las variables que se usan en fractal recursivo:
        self.recursivo_algoritmo_seleccionado = Texts.RECURSIVO_ALGORITMOS_DEFAULT
        self.recursivo_color_seleccionado = Texts.RECURSIVO_COLOR_DEFAULT
        self.recursivo_nivel_seleccionado = Texts.RECURSIVO_NIVEL_DEFAULT

        frame_recursivo = self._crear_frame_seccion(parent_frame, titulo)
        frame_recursivo.grid(row=1, column=0, pady=(10, 0), padx=10, sticky=ctk.NSEW)

        # Menú desplegable para elegir algoritmos
        label_algoritmo = ctk.CTkLabel(frame_recursivo, text=Texts.RECURSIVO_EJEMPLO)
        label_algoritmo.grid(row=2, column=0, pady=(10, 5), padx=10, sticky=ctk.W)

        self.dropdown_algoritmo = ctk.CTkOptionMenu(
            frame_recursivo,
            values=Texts.RECURSIVO_ALGORITMOS,
            command=self.recursivo_actualizar_algoritmo,  # Llamamos a un método para guardar el valor seleccionado
        )
        self.dropdown_algoritmo.grid(
            row=2, column=1, pady=(10, 5), padx=(5, 10), sticky=ctk.EW
        )

        # Botón para elegir el color
        label_color = ctk.CTkLabel(frame_recursivo, text=Texts.RECURSIVO_COLOR)
        label_color.grid(row=2, column=2, pady=(10, 5), padx=10, sticky=ctk.W)

        self.recursivo_boton_color = ctk.CTkButton(
            frame_recursivo,
            text=Texts.RECURSIVO_COLOR_BOTON,
            command=self.recursivo_elegir_color,  # Método para elegir el color
            fg_color=Texts.RECURSIVO_COLOR_DEFAULT,
        )
        self.recursivo_boton_color.grid(
            row=2, column=3, pady=(10, 5), padx=(5, 10), sticky=ctk.EW
        )

        # Barra horizontal para elegir nivel (1-10)
        label_nivel = ctk.CTkLabel(frame_recursivo, text=Texts.RECURSIVO_NIVEL)
        label_nivel.grid(row=2, column=4, pady=(10, 5), padx=10, sticky=ctk.W)

        self.slider_nivel = ctk.CTkSlider(
            frame_recursivo,
            from_=Texts.RECURSIVO_NIVEL_MIN,
            to=Texts.RECURSIVO_NIVEL_MAX,
            orientation=ctk.HORIZONTAL,
            command=self.recursivo_actualizar_nivel,
        )
        self.slider_nivel.set(5)
        self.slider_nivel.grid(
            row=2, column=6, pady=(10, 5), padx=(5, 10), sticky=ctk.EW
        )

        # Etiqueta para mostrar el valor del nivel
        self.label_nivel_valor = ctk.CTkLabel(
            frame_recursivo,
            text=str(Texts.RECURSIVO_NIVEL_DEFAULT),
            font=(self.fuente, 12),
        )
        self.label_nivel_valor.grid(
            row=2, column=5, pady=(10, 5), padx=(5, 10), sticky=ctk.EW
        )

        # Botón para generar fractales recursivos
        boton = ctk.CTkButton(
            frame_recursivo,
            text=Texts.RECURSIVO_GENERAR,
            command=self.recursivo_generar_fractal,  # Método para manejar la generación del fractal
        )
        boton.grid(row=4, column=0, columnspan=8, pady=(10, 10), padx=10, sticky=ctk.EW)

        # Configurar columnas para un diseño adaptable
        for i in range(8):
            frame_recursivo.grid_columnconfigure(i, weight=1)

    def recursivo_actualizar_nivel(self, nivel):
        """
        Actualiza el texto de la etiqueta que muestra el valor del nivel del fractal.

        Args:
            nivel (float): El nivel seleccionado en el slider.
        """
        self.recursivo_nivel_seleccionado = int(
            nivel
        )  # Convertir el valor a entero si es necesario
        self.label_nivel_valor.configure(text=str(int(nivel)))

    def recursivo_actualizar_algoritmo(self, algoritmo: str) -> None:
        """
        Guarda el algoritmo seleccionado.

        Args:
            algoritmo (str): El algoritmo elegido por el usuario en el menú desplegable.
        """
        self.recursivo_algoritmo_seleccionado = algoritmo

    def recursivo_elegir_color(self) -> None:
        """Abre un selector de color y actualiza el color seleccionado."""
        self.recursivo_color_seleccionado = self._abrir_seleccion_color()
        self.recursivo_boton_color.configure(fg_color=self.recursivo_color_seleccionado)

    def recursivo_generar_fractal(self) -> None:
        """
        Genera el fractal recursivo basado en los parámetros seleccionados.
        """
        # Lógica para generar el fractal utilizando los valores almacenados
        print(
            f"Generando fractal con: Algoritmo: {self.recursivo_algoritmo_seleccionado}, "
            f"Color: {self.recursivo_color_seleccionado}, Nivel: {self.recursivo_nivel_seleccionado}"
        )

        # Configuración inicial de la ventana y creación de la instancia
        width: int = Fractales.WINDOW_WIDTH
        height: int = Fractales.WINDOW_HEIGHT
        title: str = Fractales.TITLE_RECURSIVO

        algoritmo_seleccionado: str = self.recursivo_algoritmo_seleccionado
        color_seleccionado: str = self.recursivo_color_seleccionado
        nivel_seleccionado: int = self.recursivo_nivel_seleccionado

        # Crear y mostrar la ventana de fractales
        self.fractal = FractalRecursivo(
            width,
            height,
            title,
            algoritmo_seleccionado,
            color_seleccionado,
            nivel_seleccionado,
        )
        
        self.fractal.mostrar_ventana()
        
    ################### FRACTAL JULIA ###################
    def _crear_seccion_julia(
        self, titulo: str, parent_frame: ctk.CTkScrollableFrame
    ) -> None:
        """
        Crea la sección específica para fractales de Julia dentro del menú.

        Args:
            titulo (str): Título de la sección.
            parent_frame (ctk.CTkScrollableFrame): Frame contenedor del menú.
        """

        # variables para obtener los valores de los campos de texto
        self.julia_real = None
        self.julia_imaginario = None
        self.julia_xmin = None
        self.julia_xmax = None
        self.julia_ymin = None
        self.julia_ymax = None
        self.julia_color = None
        self.julia_color_seleccionado = Texts.JULIA_COLORES_DEFAULT

        frame_julia = self._crear_frame_seccion(parent_frame, titulo)
        frame_julia.grid(row=2, column=0, pady=(10, 0), padx=10, sticky="nsew")

        # Etiquetas y entradas para número real e imaginario
        ctk.CTkLabel(frame_julia, text=Texts.JULIA_REAL, font=(self.fuente, 12)).grid(
            row=2, column=0, pady=(10, 5), padx=10, sticky="w"
        )
        self.julia_input_real = ctk.CTkEntry(frame_julia, placeholder_text="Ej: 0.355")
        self.julia_input_real.grid(
            row=2, column=1, pady=(10, 5), padx=(5, 10), sticky="ew"
        )

        ctk.CTkLabel(
            frame_julia, text=Texts.JULIA_IMAGINARIO, font=(self.fuente, 12)
        ).grid(row=2, column=2, pady=(10, 5), padx=10, sticky="w")
        self.julia_input_imaginario = ctk.CTkEntry(
            frame_julia, placeholder_text="Ej: 0.355"
        )
        self.julia_input_imaginario.grid(
            row=2, column=3, pady=(10, 5), padx=(5, 10), sticky="ew"
        )

        # Etiquetas y entradas para xmin, xmax, ymin, ymax
        ctk.CTkLabel(frame_julia, text=Texts.JULIA_XMIN, font=(self.fuente, 12)).grid(
            row=3, column=0, pady=(10, 5), padx=10, sticky="w"
        )
        self.julia_input_xmin = ctk.CTkEntry(frame_julia, placeholder_text="Ej: -2.0")
        self.julia_input_xmin.grid(
            row=3, column=1, pady=(10, 5), padx=(5, 10), sticky="ew"
        )

        ctk.CTkLabel(frame_julia, text=Texts.JULIA_XMAX, font=(self.fuente, 12)).grid(
            row=4, column=0, pady=(10, 5), padx=10, sticky="w"
        )
        self.julia_input_xmax = ctk.CTkEntry(frame_julia, placeholder_text="Ej: 2.0")
        self.julia_input_xmax.grid(
            row=4, column=1, pady=(10, 5), padx=(5, 10), sticky="ew"
        )

        ctk.CTkLabel(frame_julia, text=Texts.JULIA_YMIN, font=(self.fuente, 12)).grid(
            row=3, column=2, pady=(10, 5), padx=10, sticky="w"
        )
        self.julia_input_ymin = ctk.CTkEntry(frame_julia, placeholder_text="Ej: -2.0")
        self.julia_input_ymin.grid(
            row=3, column=3, pady=(10, 5), padx=(5, 10), sticky="ew"
        )

        ctk.CTkLabel(frame_julia, text=Texts.JULIA_YMAX, font=(self.fuente, 12)).grid(
            row=4, column=2, pady=(10, 5), padx=10, sticky="w"
        )
        self.julia_input_ymax = ctk.CTkEntry(frame_julia, placeholder_text="Ej: 2.0")
        self.julia_input_ymax.grid(
            row=4, column=3, pady=(10, 5), padx=(5, 10), sticky="ew"
        )

        # Menú desplegable para elegir algoritmos
        ctk.CTkLabel(
            frame_julia, text=Texts.JULIA_EJEMPLO, font=(self.fuente, 12)
        ).grid(row=6, column=0, pady=(10, 5), padx=10, sticky="w")
        dropdown_algoritmo = ctk.CTkOptionMenu(
            frame_julia,
            values=Texts.JULIA_ALGORITMOS,
            command=self.julia_actualizar_algoritmo,
        )
        dropdown_algoritmo.set(Texts.JULIA_ALGORITMOS[0])
        dropdown_algoritmo.grid(
            row=6, column=1, pady=(10, 5), padx=(5, 10), sticky="ew", columnspan=1
        )

        # Menú desplegable para elegir colores
        ctk.CTkLabel(frame_julia, text=Texts.JULIA_COLOR, font=(self.fuente, 12)).grid(
            row=6, column=2, pady=(10, 5), padx=10, sticky="w"
        )
        dropdown_color = ctk.CTkOptionMenu(
            frame_julia,
            values=Texts.JULIA_COLORES,
            command=self.julia_elegir_color,
        )
        dropdown_color.grid(row=6, column=3, pady=(10, 5), padx=(5, 10), sticky="ew")

        # Botón para generar fractales de Julia
        boton = ctk.CTkButton(
            frame_julia,
            text=Texts.JULIA_GENERAR,
            command=self.julia_generar_fractal,
        )
        boton.grid(row=7, column=0, columnspan=4, pady=(10, 10), padx=10, sticky="ew")

        # Configurar columnas para un diseño adaptable
        for i in range(4):  # Ahora hay 4 columnas principales (etiqueta y control)
            frame_julia.grid_columnconfigure(i, weight=1)

    def julia_actualizar_algoritmo(self, algoritmo: str) -> None:
        """
        Actualiza los valores de los inputs según el algoritmo seleccionado.

        Args:
            algoritmo (str): El nombre del algoritmo elegido por el usuario en el menú desplegable.
        """
        # Según el algoritmo seleccionado, asignar los valores predefinidos
        if algoritmo == Texts.JULIA_ALGORITMOS[1]:
            real = 0.355
            imaginario = 0.355
            xmin = -1.5
            xmax = 1.5
            ymin = -1.5
            ymax = 1.5
        elif algoritmo == Texts.JULIA_ALGORITMOS[2]:
            real = -0.70176
            imaginario = -0.3842
            xmin = -2.0
            xmax = 2.0
            ymin = -2.0
            ymax = 2.0
        elif algoritmo == Texts.JULIA_ALGORITMOS[3]:
            real = 0.285
            imaginario = 0.01
            xmin = -1.5
            xmax = 1.5
            ymin = -1.5
            ymax = 1.5
        else:
            # Si no se encuentra el algoritmo, no hace nada
            print(f"Algoritmo '{algoritmo}' borrando.")
            self.julia_input_real.delete(0, "end")

            self.julia_input_imaginario.delete(0, "end")

            self.julia_input_xmin.delete(0, "end")

            self.julia_input_xmax.delete(0, "end")

            self.julia_input_ymin.delete(0, "end")

            self.julia_input_ymax.delete(0, "end")

            return

        # Actualizar los campos con los valores correspondientes
        self.julia_input_real.delete(0, "end")
        self.julia_input_real.insert(0, real)

        self.julia_input_imaginario.delete(0, "end")
        self.julia_input_imaginario.insert(0, imaginario)

        self.julia_input_xmin.delete(0, "end")
        self.julia_input_xmin.insert(0, xmin)

        self.julia_input_xmax.delete(0, "end")
        self.julia_input_xmax.insert(0, xmax)

        self.julia_input_ymin.delete(0, "end")
        self.julia_input_ymin.insert(0, ymin)

        self.julia_input_ymax.delete(0, "end")
        self.julia_input_ymax.insert(0, ymax)

    def julia_elegir_color(self, color) -> None:
        """ """
        self.julia_color_seleccionado = color

    def julia_generar_fractal(self):
        """
        Función que maneja el evento de generar el fractal de Julia y guarda los valores introducidos.
        """
        # Guardar los valores introducidos en las variables
        self.julia_real = (
            float(self.julia_input_real.get()) if self.julia_input_real.get() else None
        )
        self.julia_imaginario = (
            float(self.julia_input_imaginario.get())
            if self.julia_input_imaginario.get()
            else None
        )
        self.julia_xmin = (
            float(self.julia_input_xmin.get()) if self.julia_input_xmin.get() else None
        )
        self.julia_xmax = (
            float(self.julia_input_xmax.get()) if self.julia_input_xmax.get() else None
        )
        self.julia_ymin = (
            float(self.julia_input_ymin.get()) if self.julia_input_ymin.get() else None
        )
        self.julia_ymax = (
            float(self.julia_input_ymax.get()) if self.julia_input_ymax.get() else None
        )

        # Aquí puedes añadir la lógica para generar el fractal utilizando estos valores
        # Por ejemplo, llamar a un método que use estos valores para calcular el fractal de Julia
        print(f"Generando fractal Julia con los parámetros:")
        print(f"Real: {self.julia_real}, Imaginario: {self.julia_imaginario}")
        print(f"Xmin: {self.julia_xmin}, Xmax: {self.julia_xmax}")
        print(f"Ymin: {self.julia_ymin}, Ymax: {self.julia_ymax}")
        print(f"Color: {self.julia_color_seleccionado}")

        # Configuración inicial de la ventana y creación de la instancia
        width: int = Fractales.WINDOW_WIDTH
        height: int = Fractales.WINDOW_HEIGHT
        title: str = Fractales.TITLE_JULIA

        julia_real = self.julia_real
        julia_imaginario = self.julia_imaginario
        julia_xmin = self.julia_xmin
        julia_xmax = self.julia_xmax
        julia_ymin = self.julia_ymin
        julia_ymax = self.julia_ymax
        julia_color_seleccionado = self.julia_color_seleccionado

        # Crear y mostrar la ventana del fractal de Julia
        fractal = FractalJulia(
            width,
            height,
            title,
            julia_real,
            julia_imaginario,
            julia_xmin,
            julia_xmax,
            julia_ymin,
            julia_ymax,
            julia_color_seleccionado,
        )
        fractal.mostrar_ventana()

################### FRACTAL MANDELBROT ###################
    def _crear_seccion_mandelbrot(
        self, titulo: str, parent_frame: ctk.CTkScrollableFrame
    ) -> None:
        """
        Crea la sección específica para fractales de Mandelbrot dentro del menú.

        Args:
            titulo (str): Título de la sección.
            parent_frame (ctk.CTkScrollableFrame): Frame contenedor del menú.
        """
        # variables que vamos a usar
        self.mandelbrot_color_seleccionado = Texts.MANDELBROT_COLORES_DEFAULT
        self.mandelbrot_complejidad = 2  # Valor por defecto de la complejidad

        frame_mandelbrot = self._crear_frame_seccion(parent_frame, titulo)
        frame_mandelbrot.grid(row=3, column=0, pady=(10, 0), padx=10, sticky="nsew")

        # Botón para generar fractales de Mandelbrot
        boton_generar = ctk.CTkButton(
            frame_mandelbrot,
            text=Texts.MANDELBROT_GENERAR,
            command=self.mandelbrot_generar_fractal,
        )
        boton_generar.grid(
            row=3, column=0, pady=(10, 10), padx=10, sticky="ew", columnspan=8
        )

        # Etiqueta para el color
        etiqueta_color = ctk.CTkLabel(
            frame_mandelbrot,
            text=Texts.MANDELBROT_COLOR,
            anchor="w",
        )
        etiqueta_color.grid(row=2, column=0, pady=(10, 5), padx=10, sticky="w")

        # Desplegable para cambiar el color
        opciones_colores = Texts.MANDELBROT_COLORES
        desplegable_color = ctk.CTkOptionMenu(
            frame_mandelbrot,
            values=opciones_colores,
            command=self.mandelbrot_elegir_color,
        )
        desplegable_color.grid(
            row=2, column=1, pady=(10, 5), padx=10, sticky="nsew",
        )

        # Etiqueta para complejidad
        etiqueta_complejidad = ctk.CTkLabel(
            frame_mandelbrot,
            text="Complejidad",
            anchor="w",
        )
        etiqueta_complejidad.grid(row=2, column=2, pady=(10, 5), padx=(10, 5), sticky="e")

        # Entrada para complejidad
        self.entrada_complejidad = ctk.CTkEntry(
            frame_mandelbrot,
            width=50,
            justify="center",
        )
        self.entrada_complejidad.insert(0, str(self.mandelbrot_complejidad))  # Valor por defecto
        self.entrada_complejidad.grid(row=2, column=3, pady=(10, 5), padx=(5, 10), sticky="w")

        # Configurar columnas para un diseño adaptable
        for i in range(5):
            frame_mandelbrot.grid_columnconfigure(i, weight=1)


    def mandelbrot_elegir_color(self, color) -> None:
        """ """
        self.mandelbrot_color_seleccionado = color

    def mandelbrot_generar_fractal(self) -> None:
        """
        Genera el fractal mandelbrot basado en los parámetros seleccionados.
        """
        # Lógica para generar el fractal utilizando los valores almacenados
        print(f"Generando fractal con: Color: {self.mandelbrot_color_seleccionado}.")

        # Configuración inicial de la ventana y creación de la instancia
        width: int = Fractales.WINDOW_WIDTH
        height: int = Fractales.WINDOW_HEIGHT
        title: str = Fractales.TITLE_MANDELBROT

        color_seleccionado: str = self.mandelbrot_color_seleccionado
        complejidad = int(self.entrada_complejidad.get())

        # Crear y mostrar la ventana del fractal Mandelbrot
        fractal = FractalMandelbrot(width, height, title, color_seleccionado, complejidad)
        fractal.mostrar_ventana()

    ################### FRACTAL IFS ###################
    def _crear_seccion_ifs(
        self, titulo: str, parent_frame: ctk.CTkScrollableFrame
    ) -> None:
        """
        Crea la sección específica para fractales IFS dentro del menú.

        Args:
            titulo (str): Título de la sección.
            parent_frame (ctk.CTkScrollableFrame): Frame contenedor del menú.
        """

        # La lista que va a contener todas las funciones
        self.lista_funciones = []
        self.ifs_color_seleccionado = Texts.IFS_COLOR_DEFAULT
        self.ifs_default_prob = ctk.BooleanVar(value=True)

        frame_ifs = self._crear_frame_seccion(parent_frame, titulo)
        frame_ifs.grid(row=4, column=0, pady=(10, 0), padx=10, sticky="nsew")

        # Inputs para las variables a, c, e (fila 1) y b, d, f (fila 2)
        labels_inputs = [
            ("a", 0, 0),
            ("c", 0, 2),
            ("e", 0, 4),  # Fila 1
            ("b", 1, 0),
            ("d", 1, 2),
            ("f", 1, 4),
        ]  # Fila 2
        self.inputs_ifs = {}
        for label, row, col in labels_inputs:
            etiqueta = ctk.CTkLabel(frame_ifs, text=f"{label}:", anchor="e")
            etiqueta.grid(row=2 + row, column=col, padx=5, pady=5, sticky="e")
            input_field = ctk.CTkEntry(frame_ifs)
            input_field.grid(row=2 + row, column=col + 1, padx=5, pady=5, sticky="ew")
            self.inputs_ifs[label] = input_field

        # Checkbox para defaultPro
        self.checkbox_default_pro = ctk.CTkCheckBox(
            frame_ifs,
            text="defaultProbabilidad",
            variable=self.ifs_default_prob,  # Asociar la variable
        )
        self.checkbox_default_pro.grid(
            row=2, column=7, padx=5, pady=5, sticky="w", columnspan=1
        )

        # Input para prob
        etiqueta_prob = ctk.CTkLabel(frame_ifs, text="prob:", anchor="e")
        etiqueta_prob.grid(row=3, column=6, padx=5, pady=5, sticky="e")
        self.input_prob = ctk.CTkEntry(frame_ifs)
        self.input_prob.grid(row=3, column=7, padx=5, pady=5, sticky="ew")

        # Botón para añadir funciones
        boton_add_function = ctk.CTkButton(
            frame_ifs,
            text="Añadir Función",
            command=self.ifs_add_function,
        )
        boton_add_function.grid(
            row=5, column=0, columnspan=4, pady=(10, 10), padx=10, sticky="ew"
        )

        self.ifs_boton_color = ctk.CTkButton(
            frame_ifs,
            text=Texts.IFS_COLOR_BOTON,
            command=self.ifs_elegir_color,
            fg_color=Texts.IFS_COLOR_DEFAULT,
        )
        self.ifs_boton_color.grid(
            row=5, column=4, columnspan=4, pady=(10, 10), padx=10, sticky="ew"
        )

        # Lista editable para las funciones creadas
        self.text_lista_funciones = ctk.CTkTextbox(frame_ifs, height=100)
        self.text_lista_funciones.grid(
            row=6, column=0, columnspan=8, pady=(10, 10), padx=10, sticky="nsew"
        )

        # Configurar la fila de la lista para que sea expandible
        frame_ifs.grid_rowconfigure(
            6, weight=1
        )  # Hacer que la fila 6 se expanda verticalmente

        # Botones debajo de la lista editable
        boton_modificar_funcion = ctk.CTkButton(
            frame_ifs,
            text="Modificar Función",
            command=self.ifs_modificar_funcion,
        )
        boton_modificar_funcion.grid(
            row=7, column=0, columnspan=2, pady=(10, 10), padx=10, sticky="ew"
        )
        
        # Menú desplegable para elegir algoritmos
        dropdown_algoritmo = ctk.CTkOptionMenu(
            frame_ifs,
            values=Texts.IFS_ALGORITMOS,
            command=self.ifs_actualizar_algoritmo,
        )
        dropdown_algoritmo.set(Texts.IFS_ALGORITMOS[0])
        dropdown_algoritmo.grid(
            row=7, column=3,  pady=(10, 10), padx=10, sticky="ew"
        )

        boton_borrar_ultima = ctk.CTkButton(
            frame_ifs,
            text="Borrar Última",
            command=self.ifs_borrar_ultima,
        )
        boton_borrar_ultima.grid(
            row=7, column=4, columnspan=2, pady=(10, 10), padx=10, sticky="ew"
        )

        boton_borrar_todo = ctk.CTkButton(
            frame_ifs,
            text="Borrar Todo",
            command=self.ifs_borrar_todo,
        )
        boton_borrar_todo.grid(
            row=7, column=6, columnspan=2, pady=(10, 10), padx=10, sticky="ew"
        )

        # Nuevos campos debajo de los botones
        etiqueta_num_funciones = ctk.CTkLabel(frame_ifs, text="N:", anchor="e")
        etiqueta_num_funciones.grid(row=8, column=0, padx=5, pady=5, sticky="e")

        self.input_num_funciones = ctk.CTkEntry(frame_ifs)
        self.input_num_funciones.grid(row=8, column=1, padx=5, pady=5, sticky="ew")

        etiqueta_iterations = ctk.CTkLabel(frame_ifs, text="Iterations:", anchor="e")
        etiqueta_iterations.grid(row=8, column=4, padx=5, pady=5, sticky="e")

        self.input_iterations = ctk.CTkEntry(frame_ifs)
        self.input_iterations.grid(row=8, column=5, padx=5, pady=5, sticky="ew")

        etiqueta_threshold = ctk.CTkLabel(frame_ifs, text="Threshold:", anchor="e")
        etiqueta_threshold.grid(row=8, column=6, padx=5, pady=5, sticky="e")

        self.input_threshold = ctk.CTkEntry(frame_ifs)
        self.input_threshold.grid(row=8, column=7, padx=5, pady=5, sticky="ew")

        # Botón para generar fractal
        boton_generar_fractal = ctk.CTkButton(
            frame_ifs,
            text="Generar Fractal IFS",
            command=self.ifs_generar_fractal,
        )
        boton_generar_fractal.grid(
            row=9, column=0, columnspan=8, pady=(10, 10), padx=10, sticky="ew"
        )

        # Configurar columnas para diseño adaptable
        for i in range(8):  # Ajustamos a las 8 columnas
            frame_ifs.grid_columnconfigure(i, weight=1)
            frame_ifs.grid_rowconfigure(i, weight=1)


    def ifs_actualizar_algoritmo(self, eleccion: str) -> None:
        """
        Actualiza la lista de funciones IFS según el algoritmo seleccionado.

        Args:
            eleccion (str): Algoritmo elegido, debe estar en IFS_ALGORITMOS.
        """
        if eleccion not in Texts.IFS_PREDEFINIDOS.keys():
            print(f"Error: '{eleccion}' no es un algoritmo válido.")
            return

        # Eliminar funciones actuales
        self.lista_funciones.clear()

        # Recuperar funciones predefinidas para el algoritmo seleccionado
        funciones = Texts.IFS_PREDEFINIDOS.get(eleccion, [])
        for valores, prob, color in funciones:
            
            self.lista_funciones.append((valores, prob, color))

        # Actualizar visualización
        self.input_iterations.delete(0, "end")
        self.input_threshold.delete(0, "end")
        
        self.input_iterations.insert(0, 100000)
        self.input_threshold.insert(0, 50)
        
        self.ifs_pintar_funciones()
    
    def ifs_elegir_color(self) -> None:
        """Abre un selector de color y actualiza el color seleccionado."""
        self.ifs_color_seleccionado = self._abrir_seleccion_color()
        self.ifs_boton_color.configure(fg_color=self.ifs_color_seleccionado)

    def ifs_add_function(self) -> None:
        """
        Lógica para añadir una función a la lista editable en la sección IFS.
        """
        # Recuperar valores de los inputs
        valores = {
            var: input_field.get() for var, input_field in self.inputs_ifs.items()
        }
        prob = self.input_prob.get()
        self.ifs_default_prob = self.checkbox_default_pro.get()
        color = self.ifs_color_seleccionado

        self.lista_funciones.append((valores, prob, color))

        # Crear texto representativo de la función
        self.ifs_pintar_funciones()

    def ifs_pintar_funciones(self):
        # borramos interfaz y redibujamos
        self.text_lista_funciones.delete("1.0", "end")

        # pintamos cada una de ellas
        iteracion = 0
        for valores, prob, color in self.lista_funciones:
            iteracion += 1
            funcion = f"Funcion {iteracion}. a: {valores['a']}, b: {valores['b']}, c: {valores['c']}, d: {valores['d']}, e: {valores['e']}, f: {valores['f']}, prob: {prob}, color: {color}\n"

            # Añadir a la lista editable
            self.text_lista_funciones.insert("end", f"{funcion}")

    def ifs_borrar_ultima(self) -> None:
        """
        Lógica para borrar la última función de la lista.
        """
        if len(self.lista_funciones) > 0:
            self.lista_funciones.pop()
            self.ifs_pintar_funciones()

    def ifs_borrar_todo(self) -> None:
        """
        Lógica para borrar todas las funciones de la lista.
        """
        self.text_lista_funciones.delete("1.0", "end")
        self.lista_funciones.clear()

    def ifs_modificar_funcion(self) -> None:
        """
        Lógica para modificar la función seleccionada en la lista.
        """
        # Obtener la función con el indice seleccionado
        numero_funcion = (
            int(self.input_num_funciones.get()) if self.input_num_funciones.get() else 1
        )

        if len(self.lista_funciones) < numero_funcion:
            print("Escoge un numero de funcion valido")

        else:
            funcion_seleccionada = self.lista_funciones.pop(numero_funcion - 1)
            valores, prob, color = funcion_seleccionada
            print(valores, prob, color)

            self.inputs_ifs["a"].delete(0, "end")
            self.inputs_ifs["a"].insert(0, valores["a"])
            self.inputs_ifs["c"].delete(0, "end")
            self.inputs_ifs["c"].insert(0, valores["c"])
            self.inputs_ifs["e"].delete(0, "end")
            self.inputs_ifs["e"].insert(0, valores["e"])
            self.inputs_ifs["b"].delete(0, "end")
            self.inputs_ifs["b"].insert(0, valores["b"])
            self.inputs_ifs["d"].delete(0, "end")
            self.inputs_ifs["d"].insert(0, valores["d"])
            self.inputs_ifs["f"].delete(0, "end")
            self.inputs_ifs["f"].insert(0, valores["f"])
            self.input_prob.delete(0, "end")
            self.input_prob.insert(0, prob)
            self.ifs_color_seleccionado = color
            self.ifs_boton_color.configure(fg_color=self.ifs_color_seleccionado)

            self.ifs_pintar_funciones()

    def ifs_generar_fractal(self) -> None:
        """
        Genera el fractal ifs basado en los parámetros seleccionados.
        """
        # Lógica para generar el fractal utilizando los valores almacenados
        print(f"Generando fractal ifs con {len(self.lista_funciones)} funciones")

        # Configuración inicial de la ventana y creación de la instancia
        width: int = Fractales.WINDOW_WIDTH
        height: int = Fractales.WINDOW_HEIGHT
        title: str = Fractales.TITLE_IFS
        lista_funciones: list = self.lista_funciones
        ifs_default_prob = bool(self.checkbox_default_pro.get())
        iterations: int = int(self.input_iterations.get())
        threshold: int = int(self.input_threshold.get())

        # Crear y mostrar la ventana del fractal IFS
        fractal = FractalIFS(width, height, title, lista_funciones, ifs_default_prob, iterations, threshold)
        fractal.mostrar_ventana()

    ################### Métodos auxiliares para crear cada frame y modularizarlo ###################

    def _crear_frame_seccion(
        self, parent_frame: ctk.CTkFrame, titulo: str
    ) -> ctk.CTkFrame:
        """
        Crea un frame para organizar los elementos de una sección del menú.

        Este método crea un contenedor (frame) para una sección del menú, añadiendo un título y un separador
        para mejorar la organización visual del contenido.

        Args:
            parent_frame (ctk.CTkFrame): Frame contenedor principal donde se agregará este frame.
            titulo (str): Título de la sección que aparecerá en la parte superior del frame.

        Returns:
            ctk.CTkFrame: El frame configurado con el título y el separador.
        """
        # Crear el frame principal de la sección
        frame_seccion = ctk.CTkFrame(
            parent_frame, corner_radius=10, fg_color=Color.LIGHT_GRAY
        )
        frame_seccion.grid(row=0, column=0, pady=(10, 0), sticky="nsew", columnspan=8)

        # Añadir el título a la sección
        titulo_seccion = ctk.CTkLabel(
            frame_seccion, text=titulo, font=(self.fuente, 14)
        )
        titulo_seccion.grid(row=0, column=0, pady=(10, 0), sticky="nsew", columnspan=8)

        # Crear una línea separadora debajo del título
        separator = ctk.CTkFrame(
            frame_seccion, height=2, corner_radius=10, fg_color=Color.GRAY
        )
        separator.grid(
            row=1, column=0, columnspan=8, pady=(10, 0), padx=20, sticky="ew"
        )

        return frame_seccion

    def _configurar_grid(self, ventana: ctk.CTkFrame) -> None:
        """
        Configura las proporciones de la cuadrícula en el contenedor dado.

        Este método ajusta la cuadrícula del contenedor para que los elementos se ajusten adecuadamente
        a las proporciones del contenedor. Es útil para garantizar que los elementos dentro de la ventana
        o frame se distribuyan correctamente.

        Args:
            ventana (ctk.CTkFrame): El contenedor al que se aplicará la configuración de cuadrícula.
        """
        # Configurar el peso de la fila y columna para que se expandan
        ventana.grid_rowconfigure(0, weight=1)
        ventana.grid_columnconfigure(0, weight=1)

    def _abrir_seleccion_color(self) -> str:
        """
        Abre un selector de color y devuelve el color seleccionado.

        Este método abre un cuadro de diálogo para seleccionar un color y devuelve el valor del color
        seleccionado en formato de cadena (como un código hexadecimal).

        Returns:
            str: El código del color seleccionado en formato hexadecimal.
        """
        pick_color = AskColor()  # Abre el selector de color
        return (
            pick_color.get()
        )  # Obtiene el color seleccionado y lo devuelve como cadena
