"""
Archivo: ventana_menu.py

Este archivo define la clase VentanaMenu que extiende la funcionalidad
de la clase abstracta Ventana. Crea una ventana con un menu para la
aplicacion grafica.

Autor: Gabriel Gomez Garcia
Fecha: 21 de septiembre de 2024
"""

import tkinter as tk
import customtkinter as ctk

from CTkColorPicker import *

from ventana import Ventana
from algoritmos_dibujo import *
from constantes import MenuVen, Texto, Default, Pinceles, Color


class VentanaMenu(Ventana):
    """
    Clase que representa una ventana con un menu desplegable interactivo.

    Hereda de la clase abstracta Ventana, anadiendo un menu superior y
    una seccion de herramientas para interactuar con el lienzo.

    Atributos heredados:
        _width (int): El ancho de la ventana en pixeles.
        _height (int): La altura de la ventana en pixeles.
        _title (str): El titulo de la ventana.
        _ventana (ctk.CTk): La instancia de la ventana principal de customtkinter.

    Atributos de instancia:
        _color_seleccionado (str): color seleccionado para dibujar.
        _herramienta_seleccionada (str): herramienta seleccionada para dibujar.
        _tamanho_pincel (int): grosor de las figuras dibujadas.
    """

    def __init__(
        self,
        width: int = Default.VENTANA_WIDTH,
        height: int = Default.VENTANA_HEIGHT,
        title: str = Default.VENTANA_TITLE,
        color_seleccionado: str = Default.COLOR,
        herramienta_seleccionada: AlgoritmoDibujo = Default.HERRAMIENTA,
        tamanho_pincel: int = Default.TAMANHO_DIBUJAR,
    ) -> None:
        """
        Inicializa la ventana con las dimensiones y el titulo proporcionados.

        Args:
            width (int): Ancho de la ventana en pixeles.
            height (int): Alto de la ventana en pixeles.
            title (str): Titulo de la ventana.
            color_seleccionado (str): Color seleccionado para dibujar.
            herramienta_seleccionada (AlgoritmoDibujo): Herramienta seleccionada para dibujar.
            tamanho_pincel (int): grosor de las figuras dibujadas.
        """
        super().__init__(width, height, title)
        self._color_seleccionado = color_seleccionado
        self._herramienta_seleccionada = herramienta_seleccionada
        self._tamanho_pincel = tamanho_pincel

    def _crear_contenido_ventana(self) -> None:
        """
        Configura el contenido de la ventana anadiendo un menu de opciones.

        Este metodo sobrescribe la funcion abstracta heredada para implementar
        un menu superior y una barra de herramientas
        """
        self._crear_menu_superior()
        self._crear_menu_herramientas()

    def _crear_menu_superior(self) -> None:
        print("a")

    def _crear_menu_herramientas(self) -> None:
        """
        Crea la estructura de la ventana con un área de trabajo a la izquierda
        y una columna de botones a la derecha usando un diseño de cuadrícula.
        """
        ######### Crear el frame izquierdo para el área de contenido (donde va el canvas)
        self.frame_izquierdo = ctk.CTkFrame(self._ventana, corner_radius=10)

        # se pone para que ocupe todo el espacio disponible
        self.frame_izquierdo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Título para el frame izquierdo
        titulo_izquierdo = ctk.CTkLabel(
            self.frame_izquierdo, text=Texto.FRAME_IZQUIERDO, font=self.fuente
        )
        titulo_izquierdo.pack(pady=10)

        ########## Crear el frame derecho para los botones (se desliza)
        self.frame_derecho = ctk.CTkScrollableFrame(self._ventana, corner_radius=10)
        self.frame_derecho.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Título para el frame derecho
        titulo_derecho = ctk.CTkLabel(
            self.frame_derecho, text=Texto.FRAME_DERECHO, font=self.fuente
        )
        titulo_derecho.pack(pady=10)

        # Configurar la proporción de la cuadrícula
        # se expanden hasta el final de y
        # tienen el mismo peso x por lo que se expanden a la mitad los dos
        self._ventana.grid_rowconfigure(0, weight=1)  # La fila 0 se expande hasta abajo
        self._ventana.grid_columnconfigure(0, weight=1)  # El frame izquierdo
        self._ventana.grid_columnconfigure(1, weight=1)  # El frame derecho

        ####### Ahora lo de dentro de cada frame

        #### izquierdo
        # Aqui va el canvas
        self._lienzo = ctk.CTkCanvas(
            self.frame_izquierdo, highlightthickness=0, bg=Default.CANVAS_COLOR
        )
        self._lienzo.pack(
            fill=tk.BOTH, expand=True, padx=10, pady=5
        )  # El canvas ocupa todo el espacio del frame

        #### derecho

        # Creamos un frame para cada region de opciones
        self.frame_opciones_1 = ctk.CTkFrame(
            self.frame_derecho, corner_radius=10, fg_color=Color.GRIS_CLARO
        )
        self.frame_opciones_1.pack(
            pady=10, padx=10, fill="x"
        )  # Cambiar fill a "x" para ocupar solo ancho

        self.frame_opciones_2 = ctk.CTkFrame(
            self.frame_derecho, corner_radius=10, fg_color=Color.GRIS_CLARO
        )
        self.frame_opciones_2.pack(
            pady=10, padx=10, fill="x"
        )  # Cambiar fill a "x" para ocupar solo ancho

        self.frame_opciones_3 = ctk.CTkFrame(
            self.frame_derecho, corner_radius=10, fg_color=Color.GRIS_CLARO
        )
        self.frame_opciones_3.pack(
            pady=10, padx=10, fill="x"
        )  # Cambiar fill a "x" para ocupar solo ancho

        self.frame_opciones_4 = ctk.CTkFrame(
            self.frame_derecho, corner_radius=10, fg_color=Color.GRIS_CLARO
        )
        self.frame_opciones_4.pack(
            pady=10, padx=10, fill="x"
        )  # Cambiar fill a "x" para ocupar solo ancho

        self.frame_opciones_5 = ctk.CTkFrame(
            self.frame_derecho, corner_radius=10, fg_color=Color.GRIS_CLARO
        )
        self.frame_opciones_5.pack(
            pady=10, padx=10, fill="x"
        )  # Cambiar fill a "x" para ocupar solo ancho

        self.frame_opciones_6 = ctk.CTkFrame(
            self.frame_derecho, corner_radius=10, fg_color=Color.GRIS_CLARO
        )
        self.frame_opciones_6.pack(
            pady=10, padx=10, fill="x"
        )  # Cambiar fill a "x" para ocupar solo ancho

        # Crear una etiqueta de título para el frame de opciones
        titulo_opciones = ctk.CTkLabel(
            self.frame_opciones_1,
            text="Opciones de Pincel",
            font=self.fuente,
        )
        titulo_opciones.grid(row=0, column=0, pady=(10, 0), sticky="nsew", columnspan=3)

        # Crear una línea separadora
        self.separator = ctk.CTkFrame(
            self.frame_opciones_1, height=2, corner_radius=10, fg_color=Color.GRIS
        )
        self.separator.grid(
            row=1, column=0, columnspan=3, pady=(10, 0), padx=20, sticky="ew"
        )

        # Crear el OptionMenu
        seleccion_pincel = tk.StringVar(value=Default.PINCEL)  # Valor inicial
        option_menu = ctk.CTkOptionMenu(
            self.frame_opciones_1,
            variable=seleccion_pincel,
            values=list(Pinceles.PINCELES.keys()),
            width=200,  # Argumentos de diseño
            height=30,
            anchor="center",
            command=self._seleccionar_pincel,
        )
        option_menu.grid(
            row=2, column=0, padx=20, pady=10, sticky="nsew"
        )  # Coloca el OptionMenu en la columna 0

        # Crear el Slider para seleccionar el tamaño de la línea
        self.slider_tamano = ctk.CTkSlider(
            self.frame_opciones_1,
            from_=1,  # Tamaño mínimo
            to=100,  # Tamaño máximo
            number_of_steps=50,  # Para tener pasos discretos
            width=200,  # Argumentos de diseño
            height=20,
            command=self._actualizar_tamano,
        )
        self.slider_tamano.set(
            Default.TAMANHO_DIBUJAR
        )  # Establecer el valor inicial en 1
        self.slider_tamano.grid(
            row=2, column=1, padx=(30, 0), pady=10, sticky="ew"
        )  # Coloca el Slider en la columna 1

        # Crear una etiqueta para mostrar el tamaño seleccionado
        self.label_tamano = ctk.CTkLabel(
            self.frame_opciones_1,
            text=f"Tamaño de línea: {self.slider_tamano.get()}",
            font=self.fuente,
            width=150,  # Argumentos de diseño
            height=20,
        )
        self.label_tamano.grid(
            row=2, column=2, pady=5, padx=(0, 10), sticky="nsew"
        )  # Coloca la etiqueta en la columna 2

        # Configurar el peso de las columnas
        for i in range(3):
            self.frame_opciones_1.grid_columnconfigure(
                i, weight=1
            )  # Distribuir el peso igualmente

        ### opciones 2
        # Configurar la cuadrícula dentro de frame_opciones_2
        # Título de Borradores
        titulo_borradores = ctk.CTkLabel(
            self.frame_opciones_2, text="Borradores", font=self.fuente
        )
        titulo_borradores.grid(
            row=0, column=0, pady=(10, 0), sticky="nsew", columnspan=3
        )

        # Crear una línea separadora
        self.separator2 = ctk.CTkFrame(
            self.frame_opciones_2, height=2, corner_radius=10, fg_color=Color.GRIS
        )
        self.separator2.grid(
            row=1, column=0, columnspan=3, pady=(10, 0), padx=20, sticky="ew"
        )

        # Botones en la tercera fila
        btn_borrar = ctk.CTkButton(
            self.frame_opciones_2,
            text="Borrar",
            width=200,  # Argumentos de diseño
            height=30,
            command=self.borrar,
        )
        btn_borrar.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        btn_borrar_todo = ctk.CTkButton(
            self.frame_opciones_2,
            text="Borrar Todo",
            width=200,  # Argumentos de diseño
            height=30,
            command=self.borrar_todo,
        )
        btn_borrar_todo.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        btn_deshacer = ctk.CTkButton(
            self.frame_opciones_2,
            text="Deshacer",
            width=200,  # Argumentos de diseño
            height=30,
            command=self.deshacer,
        )
        btn_deshacer.grid(row=2, column=2, pady=5, padx=10, sticky="ew")

        # Configurar el peso de las columnas
        for i in range(3):
            self.frame_opciones_2.grid_columnconfigure(
                i, weight=1
            )  # Distribuir el peso igualmente

        #### opcones 3
        titulo_colores = ctk.CTkLabel(
            self.frame_opciones_3, text="Colores", font=self.fuente
        )
        titulo_colores.grid(row=0, column=0, pady=(10, 0), sticky="nsew", columnspan=3)

        # Crear una línea separadora
        self.separator3 = ctk.CTkFrame(
            self.frame_opciones_3, height=2, corner_radius=10, fg_color=Color.GRIS
        )
        self.separator3.grid(
            row=1, column=0, columnspan=3, pady=(10, 0), padx=20, sticky="ew"
        )

        # Botones en la tercera fila
        self.btn_color = ctk.CTkButton(
            self.frame_opciones_3,
            text="Seleccion Colores",
            width=200,  # Argumentos de diseño
            height=30,
            command=self.seleccionar_color,
        )
        self.btn_color.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Configurar el peso de las columnas
        for i in range(3):
            self.frame_opciones_3.grid_columnconfigure(
                i, weight=1
            )  # Distribuir el peso igualmente

            # Título de Agrupamiento
        titulo_agrupamiento = ctk.CTkLabel(
            self.frame_opciones_4, text="Agrupar y Desagrupar", font=self.fuente
        )
        titulo_agrupamiento.grid(
            row=0, column=0, pady=(10, 0), sticky="nsew", columnspan=3
        )

        # Crear una línea separadora
        self.separator4 = ctk.CTkFrame(
            self.frame_opciones_4, height=2, corner_radius=10, fg_color=Color.GRIS
        )
        self.separator4.grid(
            row=1, column=0, columnspan=3, pady=(10, 0), padx=20, sticky="ew"
        )

        # Botón para Agrupar
        btn_agrupar = ctk.CTkButton(
            self.frame_opciones_4,
            text="Agrupar",
            command=self.agrupar_figuras,  # Implementa esta función según tus necesidades
        )
        btn_agrupar.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Botón para Desagrupar
        btn_desagrupar = ctk.CTkButton(
            self.frame_opciones_4,
            text="Desagrupar",
            command=self.desagrupar_figuras,  # Implementa esta función según tus necesidades
        )
        btn_desagrupar.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Configurar el peso de las columnas
        for i in range(3):
            self.frame_opciones_4.grid_columnconfigure(
                i, weight=1
            )  # Distribuir el peso igualmente

        # Título de Salida de Texto
        titulo_salida_texto = ctk.CTkLabel(
            self.frame_opciones_5, text="Salida de Puntos de la Línea", font=self.fuente
        )
        titulo_salida_texto.grid(
            row=0, column=0, pady=(10, 0), sticky="nsew", columnspan=3
        )

        # Crear una línea separadora
        self.separator5 = ctk.CTkFrame(
            self.frame_opciones_5, height=2, corner_radius=10, fg_color=Color.GRIS
        )
        self.separator5.grid(
            row=1, column=0, columnspan=3, pady=(10, 0), padx=20, sticky="ew"
        )

        # Crear un CTkTextbox (solo lectura)
        self.textbox_salida = ctk.CTkTextbox(
            self.frame_opciones_5,
            width=380,
            height=200,
            state="disabled",  # Deshabilitado para que no se pueda escribir
        )
        self.textbox_salida.grid(
            row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        # Configurar el peso de las columnas
        for i in range(3):
            self.frame_opciones_5.grid_columnconfigure(
                i, weight=1
            )  # Distribuir el peso igualmente

    def agrupar_figuras(self):
        # Verifica si hay figuras para agrupar
        print("Figuras agrupadas:")

    def desagrupar_figuras(self):
        # Verifica si hay un grupo para desagrupar
        print("desagrupando")

    def seleccionar_color(self):
        pick_color = AskColor()  # open the color picker
        self.color_seleccionado = pick_color.get()  # get the color string
        print(f"color seleccionado {self.color_seleccionado}")

    def _seleccionar_pincel(self, pincel):
        print(f"Pincel seleccionado: {pincel}")

    def _actualizar_tamano(self, tamano):
        self.label_tamano.configure(text=f"Tamaño de línea: {tamano}")

    def borrar(self):
        print("Borrar al click sobre figura")

    def borrar_todo(self):
        print("Borrar todo")

    def deshacer(self):
        print("Deshacer última acción")

    def _actualizar_tamano(self, valor):
        """Actualiza el tamaño del pincel según el valor del slider."""
        self.tamanho_pincel = int(float(valor))  # Actualiza el tamaño del pincel
        self.label_tamano.configure(
            text=f"Tamaño de línea: {self.tamanho_pincel}"
        )  # Actualiza la etiqueta

    def _seleccionar_pincel(self, seleccion):
        """Actualiza la descripción según el pincel seleccionado."""
        self.herramienta_seleccionada = Pinceles.PINCELES[seleccion]
        print(f"herramienta {self.herramienta_seleccionada}")

    ########### getters y setters ##############
    @property
    def herramienta_seleccionada(self) -> AlgoritmoDibujo:
        """Obtiene la herramienta seleccionada."""
        return self._herramienta_seleccionada

    @herramienta_seleccionada.setter
    def herramienta_seleccionada(self, valor: AlgoritmoDibujo) -> None:
        """Establece la herramienta seleccionada."""
        self._herramienta_seleccionada = valor

    @property
    def color_seleccionado(self) -> str:
        """Obtiene el color seleccionado."""
        return self._color_seleccionado

    @color_seleccionado.setter
    def color_seleccionado(self, valor: str) -> None:
        """Establece el color seleccionado."""
        self._color_seleccionado = valor

    @property
    def tamanho_pincel(self) -> int:
        """Obtiene el tamanho del pincel."""
        return self._tamanho_pincel

    @tamanho_pincel.setter
    def tamanho_pincel(self, valor: int) -> None:
        """Establece el tamanho del pincel."""
        self._tamanho_pincel = valor

    @property
    def lienzo(self):
        """Obtiene el lienzo."""
        return self._lienzo

    # Setter para _lienzo
    @lienzo.setter
    def lienzo(self, valor):
        """Establece el lienzo."""
        if isinstance(
            valor, ctk.CTkCanvas
        ):  # Verificamos que el valor sea un CTkCanvas
            self._lienzo = valor
        else:
            raise ValueError("El valor debe ser un CTkCanvas.")
